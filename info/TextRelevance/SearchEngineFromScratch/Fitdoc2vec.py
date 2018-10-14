from Reader_2 import Reader


import gensim.models as gsm
from gensim.models.doc2vec import TaggedDocument



reader = Reader(fit_online = False, fit_corpus = None)

whole_dict = reader.read_docs(iscorpus=True, isothers=False, others_list=[])

#tagging the text files
class DocIterator(object):
    def __init__(self, doc_list, labels_list):
        self.labels_list = labels_list
        self.doc_list = doc_list

    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            yield TaggedDocument(words=doc, tags=[self.labels_list[idx]])

queries = reader.read_queries()

queries_labels = ["QRY_{}".format(i) for i in range(len(queries))]


tot_corpus = list(whole_dict.values()) + queries
tot_labels = list(whole_dict.keys()) + queries_labels

it = DocIterator( tot_corpus, tot_labels)

#train doc2vec model

model = gsm.Doc2Vec(size=300, window=10, min_count=5, workers=11,alpha=0.025, min_alpha=0.025) # use fixed learning rate

model.build_vocab(it)


for epoch in range(10):
    model.train(it, total_examples= len(tot_labels), epochs=1)
    model.alpha -= 0.002 # decrease the learning rate
    model.min_alpha = model.alpha # fix the learning rate, no deca


model.save("../temp/doc2vec_title_dict.model")

print("model is saved")


#loading the model
model="../temp/doc2vec_title_dict.model"
m=gsm.Doc2Vec.load(model)
print("model is loaded")


#path to test files
#new_test = ["мультивиза", "в", "израиль", "какие", "страны", "можно", "посетить", "виза", "многократная"]
#new_test = "жировики на спине можно ли применить пиявки".split()
#print(new_test)
inferred_docvec = m.infer_vector(queries[0])
print(m.docvecs.most_similar([inferred_docvec], topn=10))
