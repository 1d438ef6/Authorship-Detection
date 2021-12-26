from tm import tm
import traceback,json

fehlend = [48, 6083, 6088, 2090, 2132, 6379, 6424, 6471, 6620, 6678, 4781, 6764, 4849, 6784, 4867, 6831, 6834, 4939, 6897, 6901, 5011, 6946, 6949, 5052, 6984, 5067, 5074, 7006, 5088, 7022, 5135, 5137, 7101, 5196, 7165, 1369, 1418, 5402, 5403, 7388, 7432, 7443, 1559, 1563, 7475, 5533, 7482, 7499, 1618, 3196, 3197, 3204, 7527, 3238, 7581, 3246, 3248, 5639, 7588, 7616, 7619, 3285, 7633, 3306, 7670, 7678, 3331, 5741, 7689, 5748, 3338, 7737, 3392, 7758, 7761, 7775, 7787, 5854, 7794, 7806, 5876, 5880, 7827, 7838, 1951, 7884, 7887, 5948, 7897, 7899, 7904, 7905, 7915, 7917, 7963, 7981, 7985, 7998, 8019, 8021, 8031, 8047, 8060, 8063, 8064, 8074, 8077, 8116]

def combine_text():
    global fehlend
    with open('all_docs.txt','w',encoding="utf8") as f:
        f.write(' ')
    for e in range(1,8138):
        if e in fehlend: continue
        print(e)
    
        try:
            p2 = "D:/Studium/Softwareprojekt/train/train/dataset-wide/problem-"+str(e)+".txt"
            with open(p2,'r',encoding="utf8") as f:
                text = f.read()

            with open('all_docs.txt','a',encoding="utf8") as f:
                f.write(text)
                f.write('\n')
        except Exception:
            traceback.print_exc()
    print('done')

def save_word_freq():
    print('aaaaaaaaaaa')
    f = open('dictionary.txt','r',encoding="utf8")
    d = f.read().split('\n')
    f.close()
    #with open('freq_of_all_words.txt','w',encoding="utf8") as f:
    #    f.write('')
    ret = {}
    for e in range(1,8138):
        if e in fehlend: continue
        print(e)
    
        try:
            p2 = "D:/Studium/Softwareprojekt/train/train/dataset-wide/problem-"+str(e)+".txt"
            with open(p2,'r',encoding="utf8") as f:
                text = f.read()
            w = tm.split_in_words(text)
            for i in w:
                if i in d:
                    if i in ret.keys():
                        ret[i]+=1
                    else:
                        ret[i]=1
            
        except Exception:
            traceback.print_exc()
    with open('freq_of_all_words.txt','w',encoding="utf8") as f:
        json.dump(ret, f)

save_word_freq()
