from multiprocessing import Process, Queue
import time


from utils import trace_worker, get_all_dat_files, DocItem, check_existance
from config import PATH_URLS, PATH_DUMP, WORKER_NUM, PATH_CONTENT
from Parser import Parser



class runParser:
    def __init__(self, worker_num):
        self.worker_num = worker_num
        self.parser = Parser()

    def load_csv_worker(self, files, worker_id, res_queue):
        for i, file in enumerate(files):
            if i % self.worker_num != worker_id: continue
            with open(file, encoding='utf-8', errors='ignore') as input_file:
                trace_worker(i, worker_id)
                try:
                    url = input_file.readline().rstrip()
                    html = input_file.read()
                except:
                    continue
                res_queue.put(DocItem(url, *self.parser.get_marks(html)))
            trace_worker(i, worker_id, 1)
        res_queue.put(None)

    def load_files_multiprocess(self, input_file_name):
        processes = []
        res_queue = Queue()
        for i in range(self.worker_num):
            process = Process(target=self.load_csv_worker, args=(input_file_name, i, res_queue))
            processes.append(process)
            process.start()

        complete_workers = 0
        while complete_workers != self.worker_num:
            item = res_queue.get()
            if item is None:
                complete_workers += 1
            else:
                yield item
        for process in processes: process.join()

    def read_urls(self, f_name):
        urls = {}
        with open(f_name) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        for url in content:
            split = url.split('\t')
            urls[split[1]] = int(split[0])
        return urls

    def go_parse(self):
        urls = self.read_urls(PATH_URLS)
        assert check_existance(PATH_DUMP), "FILE {} ALREADY EXIST".format(PATH_DUMP)

        f = open(PATH_DUMP, "w", encoding='utf-8')
        start = time.time()
        files = get_all_dat_files(PATH_CONTENT)
        print("Start parsing {} docs".format(len(files)))
        s_parser = self.load_files_multiprocess(files)
        for doc in s_parser:
            f.write(
                "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(urls[doc.doc_url],
                                                                  doc.doc_url,
                                                                  doc.links,
                                                                  doc.title,
                                                                  doc.body,
                                                                  doc.h1,
                                                                  doc.h2,
                                                                  doc.h3,
                                                                  doc.keywords,
                                                                  doc.description)
            )
        f.close()
        print("Congratulations, your docs dump in {}, total time {} sec".format(PATH_DUMP, time.time() - start))


if __name__ == "__main__":
    run_parser = runParser(worker_num = WORKER_NUM)
    run_parser.go_parse()