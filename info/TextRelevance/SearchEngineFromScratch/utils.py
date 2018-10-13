from config import PATH_RESULT, PATH_PICKLE

import logging
from os import listdir
from collections import namedtuple
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pymystem3 import Mystem
import re
import os.path
import datetime
import pickle
from functools import lru_cache

TRACE_NUM = 1000
DOCITEM_FIELDS  = ['doc_url', 'links', 'title', 'body', 'h1', 'h2', 'h3', 'keywords', 'description']
DocItem = namedtuple('DocItem', DOCITEM_FIELDS)

STEM = Mystem(entire_input=True)
stop_words_en = stopwords.words('english')
stop_words_ru = stopwords.words('russian')
patt = re.compile(r'[\w]+', flags=re.UNICODE)

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO, datefmt='%H:%M:%S')

HASH_TABLE = dict()


def trace(items_num, trace_num=TRACE_NUM):
    if items_num % trace_num == 0: logging.info("Complete items %05d" % items_num)


def trace_worker(items_num, worker_id, trace_num=TRACE_NUM):
    if items_num % trace_num == 0: logging.info("Complete items %05d in worker_id %d" % (items_num, worker_id))


def get_all_dat_files(folder):
    f_folders = [folder + f for f in listdir(folder) if f != '.DS_Store']
    files = []
    for fold in f_folders:
        files.extend([fold + '/' + f for f in listdir(fold)])
    return files


def clear_text_old(text):
    assert isinstance(text, str) or isinstance(text, list)

    chunks = list()

    if isinstance(text, str):
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    if isinstance(text, list):
        chunks = text

    text = '\n'.join(chunk for chunk in chunks if chunk)

    words_list = list()
    lemm_list = STEM.lemmatize(text)

    for word in lemm_list:
            if (patt.search(word) and word.isalpha()):
                clear_word = word_tokenize(word.lower())[0]
                words_list.append(clear_word)
    return words_list


#@lru_cache(maxsize=256)
def clear_text(text):
    global HASH_TABLE
    words_list = list()
    lemm_list = STEM.lemmatize(text)
    for word in lemm_list:
        if word in HASH_TABLE:
            words_list.append(HASH_TABLE[word])
        else:
            if (patt.search(word) and word.isalpha()):
                clear_word = word_tokenize(word.lower())[0]
                words_list.append(clear_word)
                HASH_TABLE[word] = clear_word
    return words_list




def check_existance(fname):
    return not os.path.isfile(fname)


def submission_to_file(sub_dict, sample_sub):
    assert isinstance(sub_dict, dict)
    print("Start submitting")


    file_name = PATH_RESULT + 'sub_{}.csv'.format(datetime.datetime.now().strftime("%y-%m-%d-%H-%M"))
    with open(file_name, "w") as f:
        f.write('{},{}\n'.format(list(sample_sub.columns)[0], list(sample_sub.columns)[1]))

        for q, doc in sub_dict.items():
            for d in doc:
                f.write('{},{}\n'.format(q, d))

    print("Submit {} is ready".format(file_name))


def pickle_data(corpus_dict, corpus_type):
    print("Start pickling {}".format(corpus_type))

    assert corpus_type in DOCITEM_FIELDS[1:] or corpus_type == "whole", \
    "VARIABLE corpus_type MUST BE IN DOCITEM_FIELDS or whole"

    with open(PATH_PICKLE + "{}.pickled".format(corpus_type), "wb") as outfile:
        pickle.dump(corpus_dict, outfile)

    print("End pickling {}".format(corpus_type))