import spacy
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
from sklearn.model_selection import train_test_split
import numpy as np

tokn = spacy.load("en_core_web_sm")
with open('summarys.txt', 'r') as file:
    texts = file.read().splitlines()
tokens = []
lemmas = []
pos_tags = []
entities = []
syntax = []  # Added list for syntax analysis

for doc in tokn.pipe(texts, batch_size=50):
    tokens.append([token.text for token in doc])
    lemmas.append([token.lemma_ for token in doc])
    pos_tags.append([token.pos_ for token in doc])
    entities.append([(ent.text, ent.label_) for ent in doc.ents])
    syntax.append([(token.text, token.dep_, token.head.text) for token in doc])  # Added extraction of syntax information

all_lemmas = [lemma for sublist in lemmas for lemma in sublist]
lemma_freq = Counter(all_lemmas)


most_common_lemmas = lemma_freq.most_common(10)

train_texts, test_texts = train_test_split(lemmas, test_size=0.2, random_state=42)
model_w2v = Word2Vec(sentences=train_texts, vector_size=100, window=5, min_count=1, workers=4)

train_vectors_w2v = [np.mean([model_w2v.wv[word] for word in text], axis=0) for text in train_texts]
test_vectors_w2v = [np.mean([model_w2v.wv[word] for word in text], axis=0) for text in test_texts]

vectorizer_tfidf = TfidfVectorizer()
vectorizer_tfidf.fit([" ".join(text) for text in train_texts])

train_vectors_tfidf = vectorizer_tfidf.transform([" ".join(text) for text in train_texts]).toarray()
test_vectors_tfidf = vectorizer_tfidf.transform([" ".join(text) for text in test_texts]).toarray()

train_vectors = np.hstack((train_vectors_w2v, train_vectors_tfidf))
test_vectors = np.hstack((test_vectors_w2v, test_vectors_tfidf))
value = lemmas('sc', None)
