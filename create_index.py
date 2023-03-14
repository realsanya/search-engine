import spacy
import re
import glob
from bs4 import BeautifulSoup
from nltk.corpus import stopwords


nlp = spacy.load("en_core_web_sm")
english_stopwords = stopwords.words("english")


def extract_tokens(text: str):
    tokens = set()
    doc = nlp(text.strip())

    for i in doc:
        if i.text in ('\n', '', ' '):
            continue
        if i.is_alpha and not i.like_num and not i.is_punct and i.text.lower() not in english_stopwords:
            tokens.add(i.text)
    return tokens


def get_words():
    lemmas = []
    with open('lemmas.txt', 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')

    for line in lines:
        line_lemmas = line.split(' ')
        for lemma in line_lemmas:
            lemmas.append(lemma)
    return lemmas


if __name__ == '__main__':

    words = get_words()
    index = {}
    directory = 'pumping'
    for file in glob.iglob(f'{directory}/*.txt'):
        with open(file, 'rb') as f:
            file_idx = re.search('pumping/(.+?).txt', file).group(1)
            soup = BeautifulSoup(f.read(), "html.parser")
            doc_tokens = extract_tokens(soup.text.lower())
            for word in words:
                if word in doc_tokens:
                    if word in index.keys():
                        if file_idx in index[word]:
                            continue
                        else:
                            index[word].append(file_idx)
                    else:
                        index[word] = [file_idx]

    text = [f'{k} ' + ' '.join(map(str, list(v))) for k, v in index.items()]

    with open('index_lemmas.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(text))


