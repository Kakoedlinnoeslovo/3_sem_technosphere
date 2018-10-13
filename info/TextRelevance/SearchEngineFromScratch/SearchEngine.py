from BM25 import BM25
from Reader import Reader
from config import PATH_SAMPLE_SUBMISSION, PATH_DUMP
from utils import submission_to_file

import pandas as pd
from tqdm import tqdm




def fit_on_submission_docs():
    sub_dict = dict()
    reader = Reader()
    corpus_dict = reader.read_docs(iscorpus=True, isothers=False)

    queries_list = reader.read_queries()
    sample_submission = pd.read_csv(PATH_SAMPLE_SUBMISSION)


    for i, query in tqdm(enumerate(queries_list)):
        min_bound = min(sample_submission[sample_submission.QueryId == i + 1].DocumentId)
        max_bound = max(sample_submission[sample_submission.QueryId == i + 1].DocumentId)

        temp_corpus_dict = dict()

        for d in range(min_bound, max_bound):
           temp_corpus_dict[d] = corpus_dict[d]

        bm25 = BM25(corpus = list(temp_corpus_dict.values()),
                    docidxs = list(temp_corpus_dict.keys()),
                    metric = "bm25",
                    qf=1, r=0, k1=1.2, k2=100, b=0.75, R=0.0, fixed_corpus= True)

        query_dict = bm25.get_score(query)
        top_docidex = bm25.get_top(query_dict = query_dict, top_k = 10)
        sub_dict[i + 1] = top_docidex

    submission_to_file(sub_dict = sub_dict, sample_sub = sample_submission)



def fit_on_submission_docs_online():
    sub_dict = dict()
    bm25_model = BM25(metric="bm25", qf=1, r=0, k1=1.2, k2=100, b=0.75, R=0.0, fixed_corpus=False)
    reader = Reader(model=bm25_model, fit_online=True)
    reader.read_docs(iscorpus = False, isothers = True, others_list=["body"])

    queries_list = reader.read_queries()
    sample_submission = pd.read_csv(PATH_SAMPLE_SUBMISSION)


    for i, query in tqdm(enumerate(queries_list)):
        min_bound = min(sample_submission[sample_submission.QueryId == i + 1].DocumentId)
        max_bound = max(sample_submission[sample_submission.QueryId == i + 1].DocumentId)

        temp_docidxes = [d for d in range(min_bound, max_bound)]


        temp_corpus_dict = {docid: reader.body_dict[docid] for docid in temp_docidxes}


        query_dict = reader.model.get_score(query, list(temp_corpus_dict.values()), temp_docidxes)
        top_docidex = reader.model.get_top(query_dict = query_dict, top_k = 10)
        sub_dict[i + 1] = top_docidex

    submission_to_file(sub_dict = sub_dict, sample_sub = sample_submission)



def fit_on_submission_docs_online_title_occurancies():
    sub_dict = dict()
    bm25_model = BM25(metric="bm25", qf=1, r=0, k1=1.2, k2=100, b=0.75, R=0.0, fixed_corpus=False, bigram = False)
    reader = Reader(model=bm25_model, fit_online=True)
    reader.read_docs(iscorpus = False, isothers = True, others_list = ["title", "body"])

    queries_list = reader.read_queries()
    sample_submission = pd.read_csv(PATH_SAMPLE_SUBMISSION)


    for i, query in tqdm(enumerate(queries_list)):

        temp_docidxes = list(sample_submission[sample_submission.QueryId == i + 1].DocumentId)


        temp_title_dict = {docid: reader.title_dict[docid] for docid in temp_docidxes}
        temp_body_dict = {docid: reader.body_dict[docid] for docid in temp_docidxes}

        query_dict = reader.model.get_score_single(query, list(temp_body_dict.values()), temp_docidxes, temp_title_dict, title_weight = 0.2)
        top_docidex = reader.model.get_top(query_dict = query_dict, top_k = 10)
        sub_dict[i + 1] = top_docidex

    submission_to_file(sub_dict = sub_dict, sample_sub = sample_submission)



def fit_on_submission_docs_online_title_occurancies_bigram():
    sub_dict = dict()
    bm25_model = BM25(metric="bm25", qf=1, r=0, k1=1.2, k2=100, b=0.75, R=0.0,
                      fixed_corpus=False, bigram=True)

    reader = Reader(model=bm25_model, fit_online=True)
    reader.read_docs(iscorpus = False, isothers = True, others_list = ["title"])

    queries_list = reader.read_queries()
    sample_submission = pd.read_csv(PATH_SAMPLE_SUBMISSION)

    for i, query in tqdm(enumerate(queries_list)):

        temp_docidxes = list(sample_submission[sample_submission.QueryId == i + 1].DocumentId)

        temp_title_dict = {docid: reader.title_dict[docid] for docid in temp_docidxes}




        query_dict_single = bm25_model.get_score_single(query,
                                                        temp_docidxes,
                                                        temp_title_dict,
                                                        title_weight = 0.2)

        query_dict_bigram = bm25_model.get_score_bigram(query,
                                                        temp_docidxes,
                                                        temp_title_dict,
                                                        title_weight = 0.8)
        query_dict = dict()
        for docid in temp_docidxes:
            query_dict[docid] = query_dict_single[docid] + query_dict_bigram[docid]

        top_docidex = bm25_model.get_top(query_dict = query_dict, top_k = 10)
        sub_dict[i + 1] = top_docidex
        for docid in top_docidex:
            print(temp_title_dict[docid])


    submission_to_file(sub_dict = sub_dict, sample_sub = sample_submission)





def main_zones():
    #experiment2, LB: 0.54
    sub_dict = dict()
    bm25_model = BM25(metric="bm25", qf=1, r=0, k1=1.2, k2=100, b=0.75, R=0.0, fixed_corpus=False)
    reader = Reader(model = bm25_model, fit_online = True)
    reader.read_docs(iscorpus = False, isothers= True)


    queries_list = reader.read_queries()
    sample_submission = pd.read_csv(PATH_SAMPLE_SUBMISSION)


    for i, query in tqdm(enumerate(queries_list)):
        min_bound = min(sample_submission[sample_submission.QueryId == i + 1].DocumentId)
        max_bound = max(sample_submission[sample_submission.QueryId == i + 1].DocumentId)


        temp_docidxes  = [d for d in range(min_bound, max_bound)]

        temp_corpus_links = {docid: reader.links_dict[docid] for docid in temp_docidxes}
        temp_corpus_title = {docid: reader.title_dict[docid] for docid in temp_docidxes}
        temp_corpus_keywords = {docid: reader.keywords_dict[docid] for docid in temp_docidxes}
        temp_corpus_body = {docid: reader.body_dict[docid] for docid in temp_docidxes}
        temp_corpus_h1 = {docid: reader.h1_dict[docid] for docid in temp_docidxes}
        temp_corpus_h2 = {docid: reader.h2_dict[docid] for docid in temp_docidxes}
        temp_corpus_h3 = {docid: reader.h3_dict[docid] for docid in temp_docidxes}
        temp_corpus_description = {docid: reader.description_dict[docid] for docid in temp_docidxes}


        query_dict_links = reader.model.get_score(query, list(temp_corpus_links.values()), temp_docidxes)
        query_dict_title = reader.model.get_score(query, list(temp_corpus_title.values()), temp_docidxes)
        query_dict_body = reader.model.get_score(query, list(temp_corpus_body.values()), temp_docidxes)
        query_dict_keywords = reader.model.get_score(query, list(temp_corpus_keywords.values()), temp_docidxes)
        query_dict_description = reader.model.get_score(query, list(temp_corpus_description.values()), temp_docidxes)
        query_dict_h1 = reader.model.get_score(query, list(temp_corpus_h1.values()), temp_docidxes)
        query_dict_h2 = reader.model.get_score(query, list(temp_corpus_h2.values()), temp_docidxes)
        query_dict_h3 = reader.model.get_score(query, list(temp_corpus_h3.values()), temp_docidxes)

        query_dict = dict()

        for docid in temp_docidxes:
            query_dict[docid] = 5 * query_dict_title[docid] + \
                                query_dict_links[docid] + \
                                3 * query_dict_keywords[docid] + \
                                 2 * query_dict_description[docid] + \
                                 1/5 * query_dict_body[docid] + \
                                1/3 * query_dict_h1[docid] + \
                                1/3 * query_dict_h2[docid] + \
                                1/3 * query_dict_h3[docid]

        top_docidex = reader.model.get_top(query_dict, top_k = 10)

        sub_dict[i + 1] = top_docidex

    submission_to_file(sub_dict = sub_dict, sample_sub = sample_submission)






def fit_on_whole_k1_k2():
    #experiment3, without ngrams, with WALL_WORDS_ADDITION, witout occurrencies
    sub_dict = dict()
    bm25_model = BM25(metric="bm25", qf = 1, r = 0, k1 = 1.2, k2 = 100, b = 1/350, R = 0.0, fixed_corpus=False)
    reader = Reader(model = bm25_model, fit_online = True)
    corpus_dict = reader.read_docs(corpus_type = "whole")

    queries_list = reader.read_queries()
    sample_submission = pd.read_csv(PATH_SAMPLE_SUBMISSION)


    for i, query in tqdm(enumerate(queries_list)):
        min_bound = min(sample_submission[sample_submission.QueryId == i + 1].DocumentId)
        max_bound = max(sample_submission[sample_submission.QueryId == i + 1].DocumentId)


        temp_docidxes  = [d for d in range(min_bound, max_bound)]

        temp_corpus = {docid: corpus_dict[docid] for docid in temp_docidxes}


        query_dict = reader.model.get_score(query, list(temp_corpus.values()), temp_docidxes)


        top_docidex = reader.model.get_top(query_dict, top_k = 10)

        sub_dict[i + 1] = top_docidex

    submission_to_file(sub_dict = sub_dict, sample_sub = sample_submission)



