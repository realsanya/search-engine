from collections import defaultdict
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

import numpy as np
import re
import spacy
import glob

nlp = spacy.load("en_core_web_sm")
english_stopwords = stopwords.words("english")

total_lemmas = {}
total = 0


def extract(text: str, idx: int):
    lemmas = {}
    lemmas_dct = defaultdict(set)
    counter = 0

    doc = nlp(text.strip())

    for i in doc:
        if i.text in ('\n', '', ' '):
            continue
        if i.is_alpha and not i.like_num and not i.is_punct and i.text.lower() not in english_stopwords:
            counter += 1
            lemmas_dct[i.lemma_].add(i.text)
            if i.lemma_ in lemmas:
                lemmas[i.lemma_] += 1
            else:
                lemmas[i.lemma_] = 1

    lemmas_lst = []
    for key, values in lemmas_dct.items():
        tf = lemmas[key] / counter
        idf = np.log(total / total_lemmas[key])
        line = f'{key} ' + ' '.join(list(values)) + ' ' + str(tf) + ' ' + str(tf * idf)
        lemmas_lst.append(line)

    with open(f'lemmas_tf_idf/{idx}.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lemmas_lst))


if __name__ == "__main__":
    for pumping in glob.iglob(f'pumping/*.txt'):
        with open(pumping, 'rb') as f_pump:
            pumping_soup = BeautifulSoup(f_pump.read(), "html.parser")
            doc = nlp(pumping_soup.text.lower().strip())
            total += 1

            for i in doc:
                if i.text in ('\n', '', ' '):
                    continue
                if i.is_alpha and not i.like_num and not i.is_punct and i.text.lower() not in english_stopwords:
                    if i.lemma_ in total_lemmas:
                        total_lemmas[i.lemma_] += 1
                    else:
                        total_lemmas[i.lemma_] = 1

    for file in glob.iglob(f'pumping/*.txt'):
        with open(file, 'rb') as f:
            file_idx = re.search('pumping/(.+?).txt', file).group(1)
            soup = BeautifulSoup(f.read(), "html.parser")
            extract(soup.text.lower(), file_idx)



