from collections import defaultdict
from bs4 import BeautifulSoup

import spacy
from nltk.corpus import stopwords
import glob

nlp = spacy.load("en_core_web_sm")
# nltk.download('stopwords')
english_stopwords = stopwords.words("english")

lemmas_dct = defaultdict(set)
tokens = set()


def extract(text: str):
    doc = nlp(text.strip())

    for i in doc:
        if i.text in ('\n', '', ' '):
            continue
        if i.is_alpha and not i.like_num and not i.is_punct and i.text.lower() not in english_stopwords:
            tokens.add(i.text)
            lemmas_dct[i.lemma_].add(i.text)


if __name__ == "__main__":

    directory = 'pumping'
    for file in glob.iglob(f'{directory}/*.txt'):
        with open(file, 'rb') as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            extract(soup.text.lower())

    print(tokens)
    print(lemmas_dct)

    with open('tokens.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(list(tokens)))

    lemmas_lst = []
    for key, values in lemmas_dct.items():
        line = f'{key} ' + ' '.join(list(values))
        lemmas_lst.append(line)

    with open('lemmas.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lemmas_lst))
