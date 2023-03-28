from nltk.corpus import stopwords

import numpy as np
import numpy.linalg as lg
import spacy

nlp = spacy.load("en_core_web_sm")
english_stopwords = stopwords.words("english")

FILES_COUNTER = 480

lemmas_tf_idf = []
query_tf = {}
query = list()

uniq_lemmas = {}
total_lemmas = 0

results = {}
sorted_results = {}


def create_tf_idf_matrix():
    for j in range(0, FILES_COUNTER):
        with open('lemmas_tf_idf/' + str(j) + ".txt", 'r', encoding="utf-8") as f:
            lemmas_tf_idf.append({})
            lines = f.readlines()
            for line in lines:
                arr = line.split(' ')
                for lemma in arr[:len(arr) - 2]:
                    lemmas_tf_idf[j][lemma] = [float(arr[-2]), float(arr[-1])]


def vector_search():
    for i in range(0, FILES_COUNTER):
        curr_file_lemmas = lemmas_tf_idf[i]
        list1 = []
        list2 = []
        for key in curr_file_lemmas.keys():
            list1.append(curr_file_lemmas[key][0])
            list2.append(query_tf[key] if key in query_tf.keys() else 0.0)
        if lg.norm(list2) == 0:
            continue
        result = np.dot(list1, list2) / (lg.norm(list1) * lg.norm(list2))
        if result == 0:
            continue
        results[i] = result


if __name__ == "__main__":
    query = 'humbled'

    create_tf_idf_matrix()

    doc = nlp(query)
    for i in doc:
        if i.text in ('\n', '', ' '):
            continue
        if i.is_alpha and not i.like_num and not i.is_punct and i.text.lower() not in english_stopwords:
            if i.lemma_ not in uniq_lemmas.keys():
                uniq_lemmas[i.lemma_] = 0
            uniq_lemmas[i.lemma_] += 1
            total_lemmas += 1

    for key in uniq_lemmas.keys():
        query_tf[key] = uniq_lemmas[key] / total_lemmas

    vector_search()

    print(results)
    # {33: 0.0021152713841205754, 189: 0.004338813340628896, 288: 0.004497574212891799, 289: 0.009102325501284396}
    sorted_results = sorted(results, reverse=True)
    print(sorted_results)
    # [289, 288, 189, 33]

