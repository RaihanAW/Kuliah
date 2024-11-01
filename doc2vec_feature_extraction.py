from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import nltk
import pandas as pd
nltk.download('punkt')

file_path = 'Dataset\Dataset Teks.xlsx'
sheet = 'Sheet1'
column_name = 'data'

df = pd.read_excel(file_path, sheet_name=sheet)
data = df[column_name].tolist()
tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]

max_epochs = 100
vec_size = 200
alpha = 0.025

model = Doc2Vec(vector_size=vec_size, alpha=alpha, min_alpha=0.00025, min_count=1, dm=1)
model.build_vocab(tagged_data)

for epoch in range(max_epochs):
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
    model.alpha -= 0.0002  # decrease the learning rate alpha
    model.min_alpha = model.alpha  # fix the learning rate, no decay

test_data = word_tokenize("Love the channel.....but using an MOT this way is unsafe...and encourages possibly fatal behavior.")
v1 = model.infer_vector(test_data)
print("Inferred document vector:", v1)