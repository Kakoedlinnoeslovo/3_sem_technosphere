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

it = DocIterator( list(whole_dict.values()), list(whole_dict.keys()))

#train doc2vec model
model = gsm.Doc2Vec(size=300,
                    window=10,
                    min_count=1,
                    workers=11,
                    alpha=0.025,
                    min_alpha=0.025) # use fixed learning rate
model.build_vocab(it)
model.train(it, total_examples= len(list(whole_dict.keys())), epochs=100)


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