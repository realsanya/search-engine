def load_index():
    with open('index_lemmas.txt', 'r', encoding='utf-8') as f:
        data = f.read().split('\n')
    index = dict()
    all_indexes = set()
    for i in data:
        i, ids = i.split(' ', maxsplit=1)
        ids = set(list(map(int, ids.split(' '))))
        index[i] = ids
        all_indexes = all_indexes | ids
    return index, all_indexes


def get_indexes_by_word(indexes, word: str):
    if word in indexes:
        return indexes[word]
    return set()


def search(line):
    _and = '&'
    _or = '|'
    _not = '~'

    if str == '':
        return set()

    indexes, all_indexes = load_index()

    stack = []
    stack_operators = []

    for word in line.split(' '):
        if word.startswith(_not):
            word = word[1:]
            current_value = get_indexes_by_word(indexes, word)
            current_value = all_indexes - current_value
            stack.append(current_value)
            continue

        elif word == _and:
            stack_operators.append(_and)
            continue
        elif word == _or:
            stack_operators.append(_or)
            continue

        stack.append(get_indexes_by_word(indexes, word))

    result = stack.pop()

    for operator in stack_operators:
        obj2 = stack.pop()
        if operator == _and:
            result = result & obj2

        elif operator == _or:
            result = result | obj2
    return result


if __name__ == '__main__':
    answerAND = search('places & spotting')
    answerOR = search('places | spotting')
    answerNOT = search('places & ~spotting')

    with open('answers.txt', 'w', encoding='utf-8') as f:
        f.write(' '.join(map(str, answerAND)))
        f.write('\n' + 'Length (places & spotting) = ' + str(len(answerAND)) + '\n')
        f.write(' '.join(map(str, answerOR)))
        f.write('\n' + 'Length (places | spotting) = ' + str(len(answerOR)) + '\n')
        f.write(' '.join(map(str, answerNOT)))
        f.write('\n' + 'Length (places & ~spotting) = ' + str(len(answerNOT)) + '\n')