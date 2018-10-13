from utils import DocItem, clear_text, DOCITEM_FIELDS, pickle_data, clear_text_old
from config import PATH_DUMP, PATH_QUERY, PATH_PICKLE

from tqdm import tqdm
import gc
import time
import pickle

class Reader:
    def __init__(self, model = None, fit_online = False):
        self.model = model
        self.fit_online = fit_online
        self.links_dict = dict()
        self.title_dict =  dict()
        self.body_dict = dict()
        self.h1_dict = dict()
        self.h2_dict = dict()
        self.h3_dict = dict()
        self.keywords_dict = dict()
        self.description_dict = dict()


    @staticmethod
    def _parse_second(b):
        return [[x.strip()[1:-1] for x in b.split('\t')[2:][i][1:-1].split(',')] for i in range(len(b.split('\t')[2:]))]


    def _get_corpus(self, corpus_type):
        assert corpus_type in DOCITEM_FIELDS[1:] or corpus_type == "whole", \
            "VARIABLE corpus_type MUST BE IN DOCITEM_FIELDS or whole"

        if corpus_type == "whole":
            with open(PATH_PICKLE + "corpus_dict.pickled", "rb") as infile:
                dict = pickle.load(infile)
            return dict

        if corpus_type == "links":
            with open(PATH_PICKLE + "links_dict.pickled", "rb") as infile:
                dict = pickle.load(infile)
            return dict

        if corpus_type == "title":
            with open(PATH_PICKLE + "title_dict.pickled", "rb") as infile:
                dict = pickle.load(infile)
            return dict

        if corpus_type == "body":
            with open(PATH_PICKLE + "body_dict.pickled", "rb") as infile:
                dict = pickle.load(infile)
            return dict

        if corpus_type == "h1":
            with open(PATH_PICKLE + "h1_dict.pickled", "rb") as infile:
                dict = pickle.load(infile)
            return dict

        if corpus_type == "h2":
            with open(PATH_PICKLE + "h2_dict.pickled", "rb") as infile:
                dict = pickle.load(infile)
            return dict

        if corpus_type == "h3":
            with open(PATH_PICKLE + "h3_dict.pickled", "rb") as infile:
                dict = pickle.load(infile)
            return dict

        if corpus_type == "keywords":
            with open(PATH_PICKLE + "keywords_dict.pickled", "rb") as infile:
                dict = pickle.load(infile)
            return dict

        if corpus_type == "description":
            with open(PATH_PICKLE + "description_dict.pickled", "rb") as infile:
                dict = pickle.load(infile)
            return dict



    def read_docs(self, iscorpus, isothers, others_list):
        """
        :param iscorpus: True, False,
        :param isothers: True, False
        :return: doc_text: {doc_number, [word1, word2, ..., wordN]},

        doc = DocItem[doc_number]: doc.links, doc.title,
        doc.body, doc.h1,doc.h2, doc.h3,doc.keywords, doc.description
        """


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
            #'links', 'title', 'body', 'h1', 'h2', 'h3', 'keywords', 'description'
            for field in DOCITEM_FIELDS[1:]:
                temp_text_list = getattr(temp_docitem, field)
                words_list += temp_text_list

            if iscorpus:
                corpus_dict[temp_docitem.doc_url] = words_list

            if self.fit_online:
                self.model.add_doc(doc = words_list, docid = temp_docitem.doc_url)

            if isothers:
                if "links" in others_list:
                    self.links_dict[temp_docitem.doc_url] = getattr(temp_docitem, "links")
                if "title" in others_list:
                    self.title_dict[temp_docitem.doc_url] = getattr(temp_docitem, "title")
                if "body" in others_list:
                    self.body_dict[temp_docitem.doc_url] = getattr(temp_docitem, "body")
                if "h1" in others_list:
                    self.h1_dict[temp_docitem.doc_url] = getattr(temp_docitem, "h1")
                if "h2" in others_list:
                    self.h2_dict[temp_docitem.doc_url] = getattr(temp_docitem, "h2")
                if "h3" in others_list:
                    self.h3_dict[temp_docitem.doc_url] = getattr(temp_docitem, "h3")
                if "keywords" in others_list:
                    self.keywords_dict[temp_docitem.doc_url] = getattr(temp_docitem, "keywords")
                if "description" in others_list:
                    self.description_dict[temp_docitem.doc_url] = getattr(temp_docitem, "description")

        print("End reading docs")
        #pickle_data(corpus_dict = corpus_dict, corpus_type = corpus_type)
        del all_data
        gc.collect()

        return corpus_dict


    def get_online(self, docidxes, all_data, fields_list):
        result = list()
        for i in range(len(fields_list)):
            temp_dict = dict()
            result.append(temp_dict)

        for b in all_data:
            docid = int(b.split('\t')[0])
            if docid in docidxes:
                temp_docitem = DocItem(docid, *self._parse_second(b))
                for i, field in enumerate(fields_list):
                    result[i][docid] = getattr(temp_docitem, field)
            else:
                continue
        return result



    def read_queries(self):
        queries_list = list()
        print("Start reading queries")
        with open(PATH_QUERY, "r") as f:
            for line in tqdm(f.readlines()):
                words_list = line.split()[1:]
                words_list = clear_text_old(words_list)
                #words_str = ' '.join(x for x in words_list)
                queries_list.append(words_list)
        print("End reading queries")
        return queries_list

if __name__ == "__main__":
    reader = Reader()
    docitem_list = reader.read_docs(corpus_type = "whole")
    queries_list = reader.read_queries()




