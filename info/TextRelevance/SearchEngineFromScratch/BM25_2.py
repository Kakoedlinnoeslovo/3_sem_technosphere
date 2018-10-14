from InvertedIndex import build_inverted_index
from InvertedIndex import DocumentLength
from InvertedIndex import InvertedIndex

import numpy as np
import time

class BM25:
    def __init__(self, corpus = None, docidxs = None, metric = "bm25",
                 qf = 1, r = 0, k1 = 1.2, k2 = 100, b = 0.75, R = 0.0, fixed_corpus = False, bigram = False):
        self.bm25_table = None
        self.fixed_corpus = fixed_corpus
        if corpus is None:
            corpus = list()
        assert isinstance(corpus, list)
        self.tot_docs = len(corpus)
        self.bigram = bigram


        if len(corpus) != 0:
            start_time = time.time()
            self.invidx, self.doclen = build_inverted_index(corpus, docidxs)
        else:
            self.invidx = InvertedIndex()
            self.doclen = DocumentLength()

        if metric == "bm25":
            self.score_formula = self._bm25_score
        if metric == "tfidf":
            self.score_formula = self._tfidf_score
        else:
            #default
            self.score_formula = self._bm25_score

        self.qf = qf
        self.r = r
        self.k1 = k1
        self.k2 = k2
        self.b = b
        self.R = R


    def add_doc(self, doc, docid):
        assert isinstance(doc, list)
        assert isinstance(docid, int)
        assert not self.fixed_corpus, "The corpus is fixed and can not be changed"

        self.doclen.add(doc_len=len(doc), docid = docid)
        self.tot_docs +=1
        for position, term in enumerate(doc):
            if len(term) == 1:
                continue
            if self.bigram:
                self.invidx.add_extra(term, docid, position)
            else:
                self.invidx.add(term, docid)



    def _tfidf_score(self, term, docid):
        if self.bigram:
            term_occurances = self.invidx.get_term_occurancies_extra(term, docid)
        else:
            term_occurances = self.invidx.get_term_occurances(term, docid)
        doc_len = self.doclen.get_length(docid)
        number_docs_per_term = len(self.invidx.get_term_docs(term))
        tf = float(term_occurances)/doc_len
        idf = np.log(float(self.tot_docs)/number_docs_per_term + 1)
        return tf*idf


    def _idf_score(self, term):
        N = self.tot_docs
        n = len(self.invidx.get_term_docs(term))

        idf = np.log(((self.r + 0.5) * (N - n - self.R + self.r + 0.5)) /
                     ((self.R - self.r + 0.5) * (n - self.r + 0.5)))

        return idf


    def _residual_idf(self, term):
        #D = self.tot_docs
        #DF = len(self.invidx.get_term_docs(term))

        if self.bigram:
            CF = self.invidx.get_cf_extra(term)
            TotLemms = self.invidx.get_tot_lemms_extra()
            ICF = - np.log(CF / TotLemms)
        else:
            CF = self.invidx.get_cf(term)
            TotLemms = self.invidx.get_tot_lemms()
            ICF = - np.log(CF / TotLemms)

        #rIDF = - np.log(DF/D) #+ np.log(1 - np.exp(- CF/D)) + 10

        #rIDF = np.log( 1 - np.exp(-1.5 * CF/D) ) + 1
        return ICF


    def _bm25_score(self, term, docid):
        if self.bigram:
            f = self.invidx.get_term_occurancies_extra(term, docid)
        else:
            f = self.invidx.get_term_occurances(term, docid)

        dl = self.doclen.get_length(docid)
        avdl = self.doclen.get_average_length()

        def compute_K(dl, avdl):
            return self.k1 * ((1 - self.b) + self.b * (float(dl) / avdl))

        K = compute_K(dl, avdl)
        idf = self._idf_score(term)

        tf = (f * (self.k1 + 1)) / (K + f)

        third = self.qf * (self.k1 + 1) / (self.k2 + self.qf)
        return idf * tf * third


    def get_score(self, query, docs_list = None, docidxes = None):
        assert isinstance(query, list)
        if docs_list is None:
            docs_list = list()

        if docidxes is None:
            docidxes = list()

        assert isinstance(docs_list, list)
        assert isinstance(docidxes, list)
        assert len(docs_list) == len(docidxes)


        query_dict = dict()

        if len(docs_list) == 0:
            #count score on whole corpus
            for term in query:
                if term in self.invidx.index:
                    docs_list = self.invidx.get_term_docs(term)
                    for docid in docs_list:
                        score = self.score_formula(term, docid)
                        if docid in query_dict:
                            query_dict[docid] += score
                        else:
                            query_dict[docid] = score
        else:
            #count score only on docs_list corpus

            WALL_WORDS_ADDITION = dict()
            N_MISSED = dict()

            for docid in docidxes:
                query_dict[docid] = 0
                WALL_WORDS_ADDITION[docid] = 0
                N_MISSED[docid] = 0

            for term in query:
                for docid, doc in zip(docidxes, docs_list):
                    if term in doc:
                        score = self.score_formula(term, docid)
                        query_dict[docid] += score
                        WALL_WORDS_ADDITION[docid] += self._idf_score(term)
                    else:
                        N_MISSED[docid] += 1
            for docid in docidxes:
                query_dict[docid] += 0.2 * WALL_WORDS_ADDITION[docid] * 0.03 ** N_MISSED[docid]

        return query_dict



    def get_top(self, query_dict, top_k = 10):
        sorted_keys = sorted(query_dict, key = query_dict.get, reverse = True)

        if len(sorted_keys) >= top_k:
            top_docidex = sorted_keys[:top_k]
        else:
            top_docidex = sorted_keys

        return top_docidex


    def _bm25_score_extra(self, term, docid, title, title_weight):
        assert isinstance(title, list)

        if self.bigram:
            f = self.invidx.get_term_occurancies_extra(term, docid)
        else:
            f = self.invidx.get_term_occurances(term, docid)

        dl = self.doclen.get_length(docid)
        avdl = self.doclen.get_average_length()

        def compute_K(dl, avdl):
            return self.k1 * ((1 - self.b) + self.b * (float(dl) / avdl))

        K = compute_K(dl, avdl)
        idf = self._residual_idf(term)

        title_addition = 0

        if term in title:
            title_addition = 0.2 * title_weight

        tf = (f * (self.k1 + 1) / (K + f)) + title_addition

        third = self.qf * (self.k1 + 1) / (self.k2 + self.qf)
        return idf * tf * third


    def get_score_single(self, query, docidxes, title_dict, title_weight):
        assert isinstance(query, list)
        assert isinstance(docidxes, list)
        assert isinstance(title_dict, dict)

        query_dict = dict()
        WALL_WORDS_ADDITION = dict()
        N_MISSED = dict()

        for docid in docidxes:
            query_dict[docid] = 0
            WALL_WORDS_ADDITION[docid] = 0
            N_MISSED[docid] = 0

        for term in query:
            term_docs = self.invidx.get_term_docs(term)
            for docid in docidxes:
                if docid in term_docs:
                    score = self._bm25_score_extra(term, docid, title_dict[docid], title_weight)
                    query_dict[docid] += score
                    WALL_WORDS_ADDITION[docid] += self._residual_idf(term)
                else:
                    N_MISSED[docid] += 1
        for docid in docidxes:
            query_dict[docid] += 0.2 * WALL_WORDS_ADDITION[docid] * 0.03 ** N_MISSED[docid]
            if N_MISSED[docid] == 0:
                #Wphrase
                query_dict[docid] += 0.1 *  WALL_WORDS_ADDITION[docid] * 1/2

        return query_dict



    def _get_bigram_tf(self, term1, term2, positions1, positions2, title, title_weight):
        tf = 0
        assert isinstance(title, list)

        for i, pos1 in enumerate(positions1):
            temp_array = np.array(positions2) - pos1

            temp_tf_right_order = len(temp_array[temp_array == 1]) * 1 + 0.5 ** i
            temp_tf_wrong_order = len(temp_array[temp_array == - 1]) * 0.5 + 0.5 ** i

            temp_tf_right_order_next = len(temp_array[temp_array == 2]) * 0.5 + 0.5 ** i
            temp_tf_wrong_order_next = len(temp_array[temp_array == -2]) * 0.5 + 0.5 ** i

            temp_tf = temp_tf_right_order + temp_tf_wrong_order + temp_tf_right_order_next + temp_tf_wrong_order_next
            tf+=temp_tf


        tf = tf / (tf +1)
        title_str = " ".join(x for x in title)

        if term1 + " " + term2 in title_str:
            tf += 0.5 * title_weight

        return tf



    def get_score_bigram(self, query, docidxes, title_dict, title_weight):
        assert isinstance(query, list)
        assert isinstance(docidxes, list)
        assert isinstance(title_dict, dict)

        query_dict = dict()

        for docid in docidxes:
            query_dict[docid] = 0

        for i in range(len(query) - 1):
            term1 = query[i]
            term2 = query[i + 1]

            docids1 = self.invidx.get_term_docs(term1)
            docids2 = self.invidx.get_term_docs(term2)

            common_docids = set(docids1).intersection(docids2)

            for docid in common_docids:
                positions1 = self.invidx.get_term_positions(term1, docid)
                positions2 = self.invidx.get_term_positions(term2, docid)
                if docid in docidxes:
                    tf = self._get_bigram_tf(term1, term2, positions1, positions2, title_dict[docid], title_weight)
                    idf = self._residual_idf(term1) + self._residual_idf(term2)
                    query_dict[docid] += 0.3 * idf * tf


        return query_dict







