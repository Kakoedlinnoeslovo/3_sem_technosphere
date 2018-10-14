from utils import DocItem, clear_text, DOCITEM_FIELDS, pickle_data, clear_text_old
from config import PATH_DUMP, PATH_QUERY, PATH_PICKLE

from tqdm import tqdm
import time

class Reader:
    def __init__(self, fit_online, fit_corpus, model = None):
        self.model = model
        self.fit_online = fit_online
        self.fit_corpus = fit_corpus
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
                temp_text_list_new = list()

                for word in temp_text_list:
                    if len(word) == 1:
                        continue
                    else:
                        temp_text_list_new.append(word)

                words_list += temp_text_list_new

            if iscorpus:
                corpus_dict[temp_docitem.doc_url] = words_list

            if self.fit_online:
                if self.fit_corpus == "whole":
                    self.model.add_doc(doc = words_list, docid = temp_docitem.doc_url)
                else:
                    temp_list = getattr(temp_docitem, self.fit_corpus)
                    temp_short_body = getattr(temp_docitem, "body")[:200]
                    #temp_short_links = getattr(temp_docitem, "links")[:10]
                    temp_short_description = getattr(temp_docitem, "description")
                    temp_list += temp_short_body + temp_short_description
                    self.model.add_doc(doc = temp_list, docid = temp_docitem.doc_url)

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
        return corpus_dict



    def read_queries(self):
        queries_list = list()
        print("Start reading queries")
        with open(PATH_QUERY, "r") as f:
            for line in tqdm(f.readlines()):
                words_list = line.split()[1:]
                words_list = clear_text_old(words_list)
                queries_list.append(words_list)
        print("End reading queries")
        return queries_list





