import nltk, pandas as pd, re
from nltk.corpus import stopwords

df = pd.read_csv('static/finencial_queries.csv')
ques = df['question'].values

data = map(nltk.sent_tokenize, ques)
cleaned = list(map(lambda file: re.sub(r'[^(a-zA-Z)\s]', '', file), ques))
data = list(map(nltk.word_tokenize, cleaned))
removed_stop = list(map(lambda sent: [str.lower(i) for i in sent if i not in stopwords.words('english')], data))


def preprocessing(sent):
    lower = sent.lower()
    cleaned = re.sub(r'[^(a-zA-Z)\s]', '', lower)
    tokens = nltk.word_tokenize(cleaned)
    return [i for i in tokens if i not in stopwords.words('english')]


def compare(sent1, sent2):
    vect = set(sent1 + sent2)
    l1, l2 = [], []
    for i in vect:
        if i in sent1:
            l1.append(1)
        else:
            l1.append(0)
        if i in sent2:
            l2.append(1)
        else:
            l2.append(0)
    c = 0
    for i in range(len(vect)):
        c += l1[i] * l2[i]
    sim = c / float((sum(l1) * sum(l2)) ** 0.5)
    return sim * 100


# compare(removed_stop[3], 'What ideal mutual fund portfolio look like'.split())


def getIndex(que):
    preprocessed_question = preprocessing(que)
    i, index, pct = 0, 0, 0.0
    for question in df.question:
        val = compare(preprocessed_question, preprocessing(question))
        if val > pct:
            pct, index = val, i
        i += 1
    return pct, index


def chat():
    que, res = '', 'Hello! How may i help you sir.....'
    while que.rstrip() != 'bye':
        print(res)
        que = input('> ')
        pct, ind = getIndex(que)
        res = df.iloc[ind].answer
        print(pct, end='  ')
    print('Bye...')


def correction(query):
    with open('media/chatbot/corrections', 'a') as file:
        print(query, end='\n', file=file, flush=True)


def get_answer(que):
    pct, index = getIndex(que)
    if pct >= 40.0:
        res = df.iloc[index].answer
    else:
        correction(que)
        res = "Sorry , unable to answer "
    return res
