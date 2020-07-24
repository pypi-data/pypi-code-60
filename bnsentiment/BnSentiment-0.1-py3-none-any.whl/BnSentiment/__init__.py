"""
Author = Kowsher Ahmed, Avishek Das,
Email = ahmedshuvo969@gmail.com, avishek.das.ayan@gmail.com
"""

from pathlib import Path
script_location = Path(__file__).absolute().parent

vec_loc = script_location / "vectorizer"
model_loc = script_location / "classifier"

with open(sw_loc,'r',encoding = 'utf-8') as f:
    stop_words = f.read()

import pickle

def tokenizer(text):
  return text.split()

with open(vec_loc, 'rb') as p:
    vect = pickle.load(p)
with open(model_loc, 'rb') as p:
    clas = pickle.load(p)

def predict(text):
	t = vect.transform([s])
	cl = clas.predict(t)
	if cl==0: return "Negative"
	else: return "Positive"
