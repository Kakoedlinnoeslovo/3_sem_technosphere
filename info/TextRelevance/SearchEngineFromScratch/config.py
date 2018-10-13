import time

PATH_DUMP = '../temp/new_documents_save_with_stop.dump'
PATH_URLS = '../data/urls.numerate.txt'
PATH_CONTENT = '../content/'
PATH_QUERY = "../data/queries.numerate_review.txt"
PATH_SAMPLE_SUBMISSION = "../data/sample.submission.text.relevance.spring.2018.csv"
PATH_RESULT = "../subs/"
PATH_PICKLE = "../temp/"
WORKER_NUM = 3


#structure of content is content/20170702/doc.0000.dat, ...., content/20170702/doc.4532.dat,
#                       content/20170704/doc.0000.dat, ....., content/20170704/doc.4532.dat, ...
# where *.dat is saved html file
#
#structure of queries.corrected2.txt is
#1	мультивиза в Израиль какие страны можно посетить Какие страны можно посетить с шенгенской визой? Шенген:
#2	надо ли носить компресс гольфы после операции на голеностопе антиэмболические чулки, и ответим на вопрос,
#3	жировики на спине можно ли применять пиявки идеале воду с пиявками можно сливать в дуршлаг или сито
#4	как прописать просто админку Как прописать себе админку на сервере cs1.6 Как прописать админку на своем сервере
#5	хто буде судити суперкубок 2017 між шахтар динамо який відбудеться в одесі Шахтар - Динамо:
#6	как доехать от метро мякинино до крокус сити холл Контакты - Crocus City Hall -
#7	как заменить подшипник ступицы ваз 2121 Снятие и установка подшипников
#8	как установить мод сумеречный лес на майнкрафт 1 12 The Twilight Forest - тёмный, сумеречный лес
#