
import json
from pathlib import Path
import math, random
import pickle


def files_to_indexed_list(data_size = -1):
    BOS = 'xbos'  # beginning-of-sentence tag
    FLD = 'xfld'  # data field tag
    EOJ = 'xeoj'  # end of joke tag

    #get jokes:
    PATH=Path('data')

    files = list(PATH.iterdir())

    for fname in files:
        if "eddit" in str(fname):
            reddit_dataset = str(fname)
        if "upid" in str(fname):
            stupid_dataset = str(fname)
    reddit_jokes = json.load(open(reddit_dataset))
    stupid_jokes = json.load(open(stupid_dataset))

    #discard reddit jokes with 0 score:
    rated_jokes = [joke for joke in reddit_jokes if joke['score'] > 0]

    #regularize to match stupid_jokes:
    title_body = [joke['title']+' '+joke['body'] for joke in rated_jokes]

    all_jokes = []
    for i in range(len(reddit_jokes)):
        r_joke = reddit_jokes[i]
        #|print(r_joke)
        r_joke['rating']=round(math.log(r_joke['score']+random.randrange(1,10))/math.log(10)*5/2, 2)
        if r_joke['rating']>5:
            r_joke['rating']=5
        del r_joke['score'] 
        r_joke['body'] = r_joke['title']+" "+r_joke['body']
        del r_joke['title']
    for s_joke in stupid_jokes:
        del s_joke['category']

    #combine joke sets:
    combined_jokes = reddit_jokes + stupid_jokes

    title_body = [joke['body']+' ' for joke in combined_jokes]

    
    #make into a very long string:
    text = ''
    if data_size == -1: #either combine them all
        text = " " + EOJ + " "
        text = text.join(title_body)
    else: #or just consider the first many characters
        for joke in title_body:
            text = text + ' ' + joke + ' ' + EOJ + ' '
            if len(text) > data_size: 
                break

    #get a set of all characters in the text:
    chars = sorted(list(set(text)))
    vocab_size = len(chars)+1

    chars.insert(0, "\0")

    #index characters in text:
    char_indices = {c: i for i, c in enumerate(chars)}
    indices_char = {i: c for i, c in enumerate(chars)}

    idx = [char_indices[c] for c in text]

    return (idx, char_indices, indices_char, chars, vocab_size)

def format():
    PATH='data/'

    TRN_PATH = 'trn/'
    VAL_PATH = 'val/'
    TRN = f'{PATH}{TRN_PATH}'
    VAL = f'{PATH}{VAL_PATH}'

    idx = files_to_indexed_list()

    trn = open(TRN+"trn.txt","w")
    trn.write("test")
    trn.write(str(idx[0:int(len(idx)*2/3)]))
    trn.close()
    val = open(VAL+"val.txt","w")
    val.write("test")
    val.write(str(idx[int(len(idx)*2/3):len(idx)-1]))
    val.close()
    
def save_data_to_pickle(pickle_name, data_size = -1):
    data = files_to_indexed_list(data_size)
    pickle_file = open(pickle_name,'wb')
    pickle.dump(data, pickle_file)
    pickle_file.close()
    return data
    
def load_data(pickle_name):
    pickle_file = open(pickle_name,'rb')
    data = pickle.load(pickle_file)
    pickle_file.close()
    return data