from Reader_2 import Reader
from config import PATH_SAMPLE_SUBMISSION
from utils import submission_to_file
from BM25_2 import BM25

import pandas as pd
from tqdm import tqdm
import numpy as np

def fit_on_submission_docs():
    sub_dict = dict()
    bm25 = BM25(metric="bm25", qf=1, r=0, k1=1.2, k2=100, b=1/350, R=0.0, fixed_corpus=False)
    reader = Reader(model = bm25, fit_online = True, fit_corpus="title")
    reader.read_docs(iscorpus=False, isothers = True, others_list=["title"])

    queries_list = reader.read_queries()
    sample_submission = pd.read_csv(PATH_SAMPLE_SUBMISSION)


    for i, query in tqdm(enumerate(queries_list)):

        temp_docidxes = list(sample_submission[sample_submission.QueryId == i + 1].DocumentId)

        temp_title_dict = {docid: reader.title_dict[docid] for docid in temp_docidxes}

        query_dict = reader.model.get_score_single(query, temp_docidxes, temp_title_dict, title_weight = 0.8)
        top_docidex = bm25.get_top(query_dict = query_dict, top_k = 10)
        sub_dict[i + 1] = top_docidex

    submission_to_file(sub_dict = sub_dict, sample_sub = sample_submission)



def fit_on_submission_docs_bigrams():
    #lb 0.55002 0.27769

    sub_dict = dict()
    bm25 = BM25(metric="bm25", qf=1, r=0, k1=1.2, k2=100, b=1/350, R=0.0, fixed_corpus=False, bigram=True)
    reader = Reader(model = bm25, fit_online = True, fit_corpus="title")
    reader.read_docs(iscorpus=False, isothers = True, others_list=["title"])

    queries_list = reader.read_queries()
    sample_submission = pd.read_csv(PATH_SAMPLE_SUBMISSION)


    for i, query in tqdm(enumerate(queries_list)):

        temp_docidxes = list(sample_submission[sample_submission.QueryId == i + 1].DocumentId)

        temp_title_dict = {docid: reader.title_dict[docid] for docid in temp_docidxes}

        query_dict_single = reader.model.get_score_single(query, temp_docidxes, temp_title_dict, title_weight = 0.8)
        query_dict_bigram = reader.model.get_score_bigram(query, temp_docidxes, temp_title_dict, title_weight = 1.6)

        query_dict = dict()

        for docid in temp_docidxes:
            query_dict[docid] = query_dict_single[docid] + query_dict_bigram[docid]


        top_docidex = bm25.get_top(query_dict = query_dict, top_k = 10)
        sub_dict[i + 1] = top_docidex

    submission_to_file(sub_dict = sub_dict, sample_sub = sample_submission)


def fit_on_submission_docs_bigrams_description():
    # lb 0.49011 0.24796
    sub_dict = dict()
    bm25 = BM25(metric="bm25", qf=1, r=0, k1=1.2, k2=100, b=1/350, R=0.0, fixed_corpus=False, bigram=True)
    reader = Reader(model = bm25, fit_online = True, fit_corpus="description")
    reader.read_docs(iscorpus=False, isothers = True, others_list=["title"])

    queries_list = reader.read_queries()
    sample_submission = pd.read_csv(PATH_SAMPLE_SUBMISSION)


    for i, query in tqdm(enumerate(queries_list)):

        temp_docidxes = list(sample_submission[sample_submission.QueryId == i + 1].DocumentId)

        temp_title_dict = {docid: reader.title_dict[docid] for docid in temp_docidxes}

        query_dict_single = reader.model.get_score_single(query, temp_docidxes, temp_title_dict, title_weight = 0.8)
        query_dict_bigram = reader.model.get_score_bigram(query, temp_docidxes, temp_title_dict, title_weight = 1.6)

        query_dict = dict()

        for docid in temp_docidxes:
            query_dict[docid] = query_dict_single[docid] + query_dict_bigram[docid]


        top_docidex = bm25.get_top(query_dict = query_dict, top_k = 10)
        sub_dict[i + 1] = top_docidex

    submission_to_file(sub_dict = sub_dict, sample_sub = sample_submission)


def fit_on_submission_docs_bigrams_keywords():
    # lb 0.49011 0.24796
    sub_dict = dict()
    bm25 = BM25(metric="bm25", qf=1, r=0, k1=1.2, k2=100, b=1/350, R=0.0, fixed_corpus=False, bigram=True)
    reader = Reader(model = bm25, fit_online = True, fit_corpus="keywords")
    reader.read_docs(iscorpus=False, isothers = True, others_list=["title"])

    queries_list = reader.read_queries()
    sample_submission = pd.read_csv(PATH_SAMPLE_SUBMISSION)


    for i, query in tqdm(enumerate(queries_list)):

        temp_docidxes = list(sample_submission[sample_submission.QueryId == i + 1].DocumentId)

        temp_title_dict = {docid: reader.title_dict[docid] for docid in temp_docidxes}

        query_dict_single = reader.model.get_score_single(query, temp_docidxes, temp_title_dict, title_weight = 0.8)
        query_dict_bigram = reader.model.get_score_bigram(query, temp_docidxes, temp_title_dict, title_weight = 1.6)

        query_dict = dict()

        scaler = np.max(query_dict_single) / np.max(query_dict_bigram)

        for docid in temp_docidxes:
            query_dict[docid] = query_dict_single[docid] + scaler * query_dict_bigram[docid]


        top_docidex = bm25.get_top(query_dict = query_dict, top_k = 10)
        sub_dict[i + 1] = top_docidex

    submission_to_file(sub_dict = sub_dict, sample_sub = sample_submission)