from bs4 import BeautifulSoup
from nltk.corpus import stopwords

import numpy as np
import re
import spacy
import glob

nlp = spacy.load("en_core_web_sm")
english_stopwords = stopwords.words("english")

total_tokens = {}
total = 0


def extract(text: str, idx: int):
    tokens = {}
    counter = 0

    doc = nlp(text.strip())

    for i in doc:
        if i.text in ('\n', '', ' '):
            continue
        if i.is_alpha and not i.like_num and not i.is_punct and i.text.lower() not in english_stopwords:
            counter += 1
            if i.text in tokens:
                tokens[i.text] += 1
            else:
                tokens[i.text] = 1

    with open(f'tokens_tf_idf/{idx}.txt', 'w') as tokens_f:
        for token in tokens:
            tf = tokens[token] / counter
            idf = np.log(total / total_tokens[token])
            tokens_f.write(token + ' ' + str(tf) + ' ' + str(tf * idf) + '\n')


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
                    if i.text in total_tokens:
                        total_tokens[i.text] += 1
                    else:
                        total_tokens[i.text] = 1

    for file in glob.iglob(f'pumping/*.txt'):
        with open(file, 'rb') as f:
            file_idx = re.search('pumping/(.+?).txt', file).group(1)
            soup = BeautifulSoup(f.read(), "html.parser")
            extract(soup.text.lower(), file_idx)



