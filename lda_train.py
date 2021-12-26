import pandas
from gensim.parsing.preprocessing import STOPWORDS
from tm import tm
import json, traceback
import copy


fehlend = [48, 6083, 6088, 2090, 2132, 6379, 6424, 6471, 6620, 6678, 4781, 6764, 4849, 6784, 4867, 6831, 6834, 4939, 6897, 6901, 5011, 6946, 6949, 5052, 6984, 5067, 5074, 7006, 5088, 7022, 5135, 5137, 7101, 5196, 7165, 1369, 1418, 5402, 5403, 7388, 7432, 7443, 1559, 1563, 7475, 5533, 7482, 7499, 1618, 3196, 3197, 3204, 7527, 3238, 7581, 3246, 3248, 5639, 7588, 7616, 7619, 3285, 7633, 3306, 7670, 7678, 3331, 5741, 7689, 5748, 3338, 7737, 3392, 7758, 7761, 7775, 7787, 5854, 7794, 7806, 5876, 5880, 7827, 7838, 1951, 7884, 7887, 5948, 7897, 7899, 7904, 7905, 7915, 7917, 7963, 7981, 7985, 7998, 8019, 8021, 8031, 8047, 8060, 8063, 8064, 8074, 8077, 8116]

def create_dic():
    global fehlend
    d = []
    for e in range(1,8138):
        if e in fehlend: continue
        print(e)
    
        try:
            p1 = "D:/Studium/Softwareprojekt/train/train/dataset-wide/truth-problem-"+str(e)+".json"
            p2 = "D:/Studium/Softwareprojekt/train/train/dataset-wide/problem-"+str(e)+".txt"
            with open(p1) as jsonFile:
                data = json.load(jsonFile)
            topic = data["site"]
            with open(p2,'r',encoding="utf8") as f:
                text = f.read()

            tokenized_text = tm.split_in_words(text,True)

            ctt = copy.deepcopy(tokenized_text)
            
            for i in ctt:
                if (len(i)<4) or (i in STOPWORDS) or (tm.contain_number(i)) or ('\\' in i) or ('$' in i) or ('=' in i) or ('#' in i):
                    tokenized_text.remove(i)
            d = tm.combine_dictionaries(d, tokenized_text)
        except Exception:
            traceback.print_exc()
    return d
def get_freq_per_doc():
    f = open('dictionary.txt','r',encoding="utf8")
    d = f.read().split('\n')
    f.close()
    freq = [0 for i in range(len(d))]
    global fehlend
    ret = {}
    #with open('freq_per_doc.txt','w',encoding="utf8") as f:
    #    f.write(' ')
    for e in range(6774,8138):
        if e in fehlend: continue
        print(e)
    
        try:
            p1 = "D:/Studium/Softwareprojekt/train/train/dataset-wide/truth-problem-"+str(e)+".json"
            p2 = "D:/Studium/Softwareprojekt/train/train/dataset-wide/problem-"+str(e)+".txt"
            with open(p1) as jsonFile:
                data = json.load(jsonFile)
            topic = data["site"]
            with open(p2,'r',encoding="utf8") as f:
                text = f.read()
            h = {}
            tokenized_text = tm.split_in_words(text,True)
            for i in tokenized_text:
                if i in d:
                    if i in h.keys():
                        h[i]+=1
                    else:
                        h[i]=1
            #ret[e]=h
            with open('freq_per_doc.txt','a',encoding="utf8") as f:
                f.write(str(h))
                f.write('\n')
        except Exception:
            traceback.print_exc()
    return ret
def get_topics():
    global fehlend
    ret = []
    for e in range(1,4078):
        #if e in fehlend: continue
        #print(e)
    
        try:
            p1 = "D:/Studium/Softwareprojekt/validation/validation/dataset-wide/truth-problem-"+str(e)+".json"
            #p2 = "D:/Studium/Softwareprojekt/train/train/dataset-wide/problem-"+str(e)+".txt"
            with open(p1) as jsonFile:
                data = json.load(jsonFile)
            topic = data["site"]
            if not topic in ret:
                ret.append(topic)
        except Exception:
            traceback.print_exc()
    return ret

get_freq_per_doc()
