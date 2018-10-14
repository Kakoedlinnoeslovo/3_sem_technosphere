from tqdm import tqdm
import numpy as np

class InvertedIndex:
    def __init__(self):
        self.index = dict()
        self.tot_lemms  = None

    def add(self, term, docid):
        if term in self.index:
            if docid in self.index[term]:
                self.index[term][docid] += 1
            else:
                self.index[term][docid] = 1
        else:
            d = dict()
            d[docid] = 1
            self.index[term] = d

    def add_extra(self, term, docid, position):
        #invindex[term] =
        # {"docid1": (count1, [position1, position2, ..., positionN]), ...,
        #           "docidN": ([countN], [pos1,]}

        if term in self.index:
            if docid in self.index[term]:
                self.index[term][docid][0] += 1
                self.index[term][docid][1].append(position)
            else:
                self.index[term][docid] = [1, [position]]
        else:
            d = dict()
            d[docid] = [1, [position]]
            self.index[term] = d


    def get_term_occurances(self, term, docid):
        if term in self.index:
            if docid in self.index[term]:
                return self.index[term][docid]
            else:
                #print("docid {} does not exists".format(docid))
                return 0
        else:
            #print("term {} does not exists".format(term))
            return 0


    def get_term_occurancies_extra(self, term, docid):
        if term in self.index:
            if docid in self.index[term]:
                return self.index[term][docid][0]
            else:
                return 0
        else:
            return 0

    def get_cf_extra(self, term):
        if term in self.index:
            cf = np.sum([x[0] for x in self.index[term].values()])
        else:
            cf = 0
        return cf


    def get_tot_lemms(self):
        suma = 0
        if self.tot_lemms is None:
            for term in self.index.keys():
                suma += np.sum([x for x in self.index[term].values()])
            self.tot_lemms = suma
            return self.tot_lemms
        else:
            return self.tot_lemms


    def get_tot_lemms_extra(self):
        suma = 0
        if self.tot_lemms is None:
            for term in self.index.keys():
                suma += np.sum([x[0] for x in self.index[term].values()])
            self.tot_lemms = suma
            return self.tot_lemms
        else:
            return self.tot_lemms

    def get_cf(self, term):
        if term in self.index:
            cf = np.sum([x for x in self.index[term].values()])
        else:
            cf = 0
        return cf

    def get_term_positions(self, term, docid):
        if term in self.index:
            if docid in self.index[term]:
                return self.index[term][docid][1]
            else:
                return []
        else:
            return []


    def get_term_docs(self, term):
        if term in self.index:
            return list(self.index[term].keys())
        else:
            #print("term {} does not exists".format(term))
            return list()


    #BIGRAM MODEL:
    #term1, term2 is near, docids1 = get_term_docs(term1), docids2 = get_term_docs(term2),

    #for i in range(len(queries[0]) - 1):
        #term1 = queries[0][i]
        #term2 = queries[0][i+1]
        #if term1 and term2 in choosen_docs:
            #docs1 = get_term_docs(term1), docs2 = get_term_docs(term2)
            #common_docs = set(docs1).intersection(docs2)
            #for docs in common_docs:


    #term1, term2 is far


class DocumentLength:
    def __init__(self):
        self.doc_length = dict()

    def add(self, doc_len, docid):
        self.doc_length[docid] = doc_len

    def get_length(self, docid):
        if docid in self.doc_length:
            return self.doc_length[docid]
        else:
            print("docid {} does not exists".format(docid))
            return None

    def get_average_length(self):
        sum = 0
        for doc_len in self.doc_length.values():
            sum += doc_len
        average = float(sum) / len(self.doc_length)
        return average


def build_inverted_index(corpus, docidxs = None):

    assert isinstance(corpus[0], list)
    assert isinstance(corpus, list)

    if docidxs is None:
        docidxs = [x for x in range(len(corpus))]

    assert isinstance(docidxs, list)

    invidx = InvertedIndex()
    doclen = DocumentLength()
    for docid, doc in zip(docidxs, corpus):
        doclen.add(len(doc), docid)
        for term in doc:
            invidx.add(term, docid)

    return invidx, doclen




