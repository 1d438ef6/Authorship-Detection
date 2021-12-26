import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import traceback,json,time
from tm import tm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import joblib

fehlend = [48, 6083, 6088, 2090, 2132, 6379, 6424, 6471, 6620, 6678, 4781, 6764, 4849, 6784, 4867, 6831, 6834, 4939, 6897, 6901, 5011, 6946, 6949, 5052, 6984, 5067, 5074, 7006, 5088, 7022, 5135, 5137, 7101, 5196, 7165, 1369, 1418, 5402, 5403, 7388, 7432, 7443, 1559, 1563, 7475, 5533, 7482, 7499, 1618, 3196, 3197, 3204, 7527, 3238, 7581, 3246, 3248, 5639, 7588, 7616, 7619, 3285, 7633, 3306, 7670, 7678, 3331, 5741, 7689, 5748, 3338, 7737, 3392, 7758, 7761, 7775, 7787, 5854, 7794, 7806, 5876, 5880, 7827, 7838, 1951, 7884, 7887, 5948, 7897, 7899, 7904, 7905, 7915, 7917, 7963, 7981, 7985, 7998, 8019, 8021, 8031, 8047, 8060, 8063, 8064, 8074, 8077, 8116]

def get_features(text):
    v = [
        #Lexical
        len(tm.split_in_words(text=text)),                                      #absolute number of words in paragraph
        tm.get_number_of_short_words2(text=text),                           #relative number of short words
        tm.get_relative_sentence_length(text=text,replace=True),           #relativ sentence length
        tm.get_average_word_length(text=text),                             #average word length in charachters
        tm.get_average_words_per_sentence(text=text),                      #average words per sentence
        tm.get_number_of_sentences(text=text, replace=True),               #absolute sentence number
            
        tm.get_sentence_complexity2(text=text,symbol=',',replace=True),
        tm.get_average_number_of_syllables_per_word(text=text),
        tm.get_word_varianz2(text=text),
        tm.get_flesch_reading_ease(text=text),
        tm.get_symbol_frequency(text=text,symbols=['\''])[0]/len(tm.split_in_words(text=text)),               #relativ number of shortings
        tm.get_language(text=text)                                         #language of paragraph
                        
    ]
    for i in tm.get_relative_symbol_frequency(text=text):
        v.append(i)
    for i in tm.get_relative_number_of_filler_words(text=text,filler_words=['of','is','the']):
        v.append(i)
    aaa = pd.DataFrame([v],columns=['aNWP','aNSW','rSL','avWLiC','avWpS','aSN','SC','avNSyl','WV2','FRE','aNShort','language','.','!','?',',','-','of','is','the'])
    #print(aaa)
    rfc = joblib.load('rfc_model_test.pkl')
    temp_h=rfc.predict(aaa)
    #print(temp_h)
    v.append(1 if temp_h=='A1' else 2 if temp_h=='A2' else 3)
    return v

def get_diff(a1,a2,b=[]):
    if len(a1) != len(a2):
        while len(a1)<len(a2): a1.append(0)
        while len(a1)>len(a2): a2.append(0)
    ret=[]
    for i in range(len(a1)):
        if len(b)>i:
            if b[i]==1:
                if a1[i]==a2[i]: ret.append(1)
                else: ret.append(0)
            else: ret.append(abs(a1[i]-a2[i]))
        else: ret.append(abs(a1[i]-a2[i]))
    return ret
            

starttime1 = time.time()
x, y = [],[]
print('start')
if False:
    data2 = pd.read_csv('feature_save2.csv')
    X_train, X_test, y_train, y_test = train_test_split(
                                        data2[['aNWP','aNSW','rSL','avWLiC','avWpS','aSN','SC','avNSyl','WV2','FRE','aNShort','language','.','!','?',',','-','of','is','the']],
                                        data2['class'],
                                        test_size=0.1)
    print(type(X_test))
    rfc=RandomForestClassifier(n_estimators=50)
    rfc.fit(X_train,y_train)
    joblib.dump(rfc, 'rfc_model_test.pkl')

#if False:
for e in range(1,8138):
    if e in fehlend: continue
    print(e)
    
    try:
        p1 = "D:/Studium/Softwareprojekt/train/train/dataset-wide/truth-problem-"+str(e)+".json"
        p2 = "D:/Studium/Softwareprojekt/train/train/dataset-wide/problem-"+str(e)+".txt"
        with open(p1) as jsonFile:
            data = json.load(jsonFile)
        authors = data["authors"]
        structure = data["structure"]
        changes = data["changes"]
        pos = 0
        h = [structure[pos]]
        for i in changes:
            if i == 1:
                pos+=1
                h.append(structure[pos])
            else:
                h.append(structure[pos])
                        
        with open(p2,'r',encoding="utf8") as f:
            text = f.read()

        
        paragraphs = tm.split_in_paragraphes(text=text)

        for p in paragraphs:
            if paragraphs.index(p)<len(paragraphs)-1:
                p1 = p
                p2 = paragraphs[paragraphs.index(p)+1]
                v=get_diff(get_features(p1),get_features(p2),[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1])
                v.append(0 if h[paragraphs.index(p)]==h[paragraphs.index(p)+1] else 1)
                
                x.append(v)    

        #print(len(h))
        #print(h)
        #print('\n--------------\n'.join(paragraphs))
            
            
        #for p in range(len(paragraphs)):
        #    if len(tm.split_in_words(paragraphs[p]))>70:
        #        v = get_features(paragraphs[p])
        #        #print(v)
        #        v.append(h[p])
        #        x.append(v)
            #print(x)
    except Exception:
        traceback.print_exc()

data=pd.DataFrame(x,columns=['aNWP','aNSW','rSL','avWLiC','avWpS','aSN','SC','avNSyl','WV2','FRE','aNShort','language','.','!','?',',','-','of','is','the','pred_class','class'])
print(data)
data.to_csv('feature_save3.csv')
#with open('feature_save1.txt','w') as f:
#    f.write(x)
#print('start')
best_acc=0
n_acc = 0
best_f1 =0
n_f1 = 0
data = pd.read_csv('feature_save3.csv')
for i in range(50,1500,50):
    print(i)
    X_train, X_test, y_train, y_test = train_test_split(
                                        data[['aNWP','aNSW','rSL','avWLiC','avWpS','aSN','SC','avNSyl','WV2','FRE','aNShort','.','!','?',',','-','of','is','the','pred_class']],
                                        data['class'],
                                        test_size=0.3)
#starttime2 = time.time()
    clf=RandomForestClassifier(n_estimators=i)
    clf.fit(X_train,y_train)
    y_pred=clf.predict(X_test)
    acc=metrics.accuracy_score(y_test, y_pred)
    f1=metrics.f1_score(y_test,y_pred,average='macro')
    #print(f1)
    if acc>best_acc:
        best_acc=acc
        n_acc = i
    if f1>best_f1:
        best_f1=f1
        n_f1=i
    print("Accuracy:",acc)
    print("f1:",f1)
    endtime = time.time()
#print('total time: ',endtime-starttime1)
#print('classifier time: ', endtime-starttime2)
print('best acc result:',best_acc,'n of trees:',n_acc,sep=' ')
print('best f1 result:',best_f1,'n of trees:',n_f1,sep=' ')
