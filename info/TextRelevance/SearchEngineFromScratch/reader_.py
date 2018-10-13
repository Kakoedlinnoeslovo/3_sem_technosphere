from collections import namedtuple
import time
from tqdm import tqdm

PATH_DUMP = '../temp/new_documents_save_with_stop.dump'
DOCITEM_FIELDS  = ['doc_url', 'links', 'title', 'body', 'h1', 'h2', 'h3', 'keywords', 'description']
DocItem = namedtuple('DocItem', DOCITEM_FIELDS)


class Reader:
    def __init__(self):
        pass

    @staticmethod
    def _parse_second(b):
        return [[x.strip()[1:-1] for x in b.split('\t')[2:][i][1:-1].split(',')] for i in range(len(b.split('\t')[2:]))]

    def read_docs(self):
        print("Start reading lines from {}".format(PATH_DUMP))
        start_time = time.time()
        with open(PATH_DUMP, 'r') as f:
            all_data = f.readlines()
        print("End reading lines, tot time {}".format(time.time() - start_time))

        corpus_dict = dict()

        print("Start reading {} docs".format(len(all_data)))
        for b in tqdm(all_data):
            temp_docitem = DocItem(int(b.split('\t')[0]), *self._parse_second(b))

            words_list = []

            # 'links', 'title', 'body', 'h1', 'h2', 'h3', 'keywords', 'description'
            # temp_docitem.doc_url is a number
            # temp_docitem.links, temp_docitem.title, temp_docitem.body, ....

            for field in DOCITEM_FIELDS[1:]:
                temp_text_list = getattr(temp_docitem, field)
                words_list += temp_text_list

            corpus_dict[temp_docitem.doc_url] = words_list

        return corpus_dict