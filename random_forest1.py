import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import traceback,json,time
from tm import tm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import cross_validate
import joblib
from os.path import exists, isdir

#anpassen vor dem ausführen
pfad = f"D:/Studium/Softwareprojekt/"

fehlend = [48, 6083, 6088, 2090, 2132, 6379, 6424, 6471, 6620, 6678, 4781, 6764, 4849, 6784, 4867, 6831, 6834, 4939, 6897, 6901, 5011, 6946, 6949, 5052, 6984, 5067, 5074, 7006, 5088, 7022, 5135, 5137, 7101, 5196, 7165, 1369, 1418, 5402, 5403, 7388, 7432, 7443, 1559, 1563, 7475, 5533, 7482, 7499, 1618, 3196, 3197, 3204, 7527, 3238, 7581, 3246, 3248, 5639, 7588, 7616, 7619, 3285, 7633, 3306, 7670, 7678, 3331, 5741, 7689, 5748, 3338, 7737, 3392, 7758, 7761, 7775, 7787, 5854, 7794, 7806, 5876, 5880, 7827, 7838, 1951, 7884, 7887, 5948, 7897, 7899, 7904, 7905, 7915, 7917, 7963, 7981, 7985, 7998, 8019, 8021, 8031, 8047, 8060, 8063, 8064, 8074, 8077, 8116]

def get_features(text=None,generate_feature=False,model=None):                                             #gibt die features für einen text zurück
    if text is None: return -1
    if model is None and generate_feature: rfc=joblib.load('Models/rfc_model_test.pkl')
    else: rfc=model
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
    if generate_feature:
        temp_h=rfc.predict(pd.DataFrame([v],columns=['aNWP','aNSW','rSL','avWLiC','avWpS','aSN','SC','avNSyl','WV2','FRE','aNShort','language','.','!','?',',','-','of','is','the']))
        v.append(1 if temp_h=='A1' else 2 if temp_h=='A2' else 3)
    return v

def get_diff(a1,a2,b=[]):                                                   #gibt die differenz zwischen 2 feature-listen zurück
    if len(a1) != len(a2):
        while len(a1)<len(a2): a1.append(0)
        while len(a1)>len(a2): a2.append(0)
    ret=[]
    for i in range(len(a1)):
        if len(b)>i:
            if b[i]==1: ret.append(int(a1[i]==a2[i]))
            else: ret.append(abs(a1[i]-a2[i]))
        else: ret.append(abs(a1[i]-a2[i]))
    return ret
            
def train_new_model_for_feature_generation(path_to_feature_save=None, n_of_trees=50):           #trainiert ein model für die feature-generation
    if path_to_feature_save is None or not exists(path_to_feature_save): return -1
    data2 = pd.read_csv(path_to_feature_save)
    X_train, X_test, y_train, y_test = train_test_split(
                                        data2[['aNWP','aNSW','rSL','avWLiC','avWpS','aSN','SC','avNSyl','WV2','FRE','aNShort','language','.','!','?',',','-','of','is','the']],
                                        data2['class'],
                                        test_size=0.1)
    rfc=RandomForestClassifier(n_estimators=n_of_trees)
    rfc.fit(X_train,y_train)
    return rfc

def train_new_model(path_to_feature_save=None, n_of_trees=50):                                  #trainiert model für die lösungsgeneration
    if path_to_feature_save is None or not exists(path_to_feature_save): return -1
    data2 = pd.read_csv(path_to_feature_save)
    X_train, X_test, y_train, y_test = train_test_split(
                                        data2[['aNWP','aNSW','rSL','avWLiC','avWpS','aSN','SC','avNSyl','WV2','FRE','aNShort','language','.','!','?',',','-','of','is','the','pred_class']],
                                        data2['class'],
                                        test_size=0.1)
    rfc=RandomForestClassifier(n_estimators=n_of_trees)
    rfc.fit(X_train,y_train)
    y_pred=rfc.predict(X_test)
    print(f"micro average f1: {metrics.f1_score(y_test,y_pred,average='micro')}")
    print(f"macro average f1: {metrics.f1_score(y_test,y_pred,average='macro')}")
    return rfc

def generate_feature_save(path_to_dataset=None,start=None,stop=None,fehlend=None,diff=False,model=None,docNumber=False,generate_feature=False):       #generiert ein dataframe mit features für jeden paragraphen
    if path_to_dataset is None or not isdir(path_to_dataset): return -1
    if start is None or stop is None: return -1
    if fehlend is None: fehlend=[]
    x=[]
    for e in range(start,stop):
        if e in fehlend: continue
        print(e)
    
        try:
            p1 = path_to_dataset+"/truth-problem-"+str(e)+".json"
            p2 = path_to_dataset+"/problem-"+str(e)+".txt"
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

            if(diff):
                for p in paragraphs:
                    if paragraphs.index(p)<len(paragraphs)-1:
                        p1 = p
                        p2 = paragraphs[paragraphs.index(p)+1]
                        v=get_diff(get_features(text=p1,generate_feature=generate_feature,model=model),get_features(text=p2,generate_feature=generate_feature,model=model),[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1])
                        v.append(0 if h[paragraphs.index(p)]==h[paragraphs.index(p)+1] else 1)
                        if docNumber: v.append(e)
                        x.append(v)    

            else:
                for p in range(len(paragraphs)):
                    if len(tm.split_in_words(paragraphs[p]))>70:
                        v = get_features(text=paragraphs[p],generate_feature=generate_feature,model=model)
                        v.append(h[p])
                        if docNumber: v.append(e)
                        x.append(v)
        except Exception:
            traceback.print_exc()
            if e==start:
                return -1
            else: fehlend.append(e)
    c = ['aNWP','aNSW','rSL','avWLiC','avWpS','aSN','SC','avNSyl','WV2','FRE','aNShort','language','.','!','?',',','-','of','is','the']
    if generate_feature: c.append('pred_class')
    c.append('class')
    if docNumber: c.append('doc')
    return pd.DataFrame(x,columns=c), fehlend

def is_equal(feature1=None,feature2=None,model=None):                                       #überprüft ob 2 listen mit features vom gleichen autor kommen
    #if (feature1 is None and feature2 is not None) or (feature1 is not None and feature2 is None): return False
    #elif feature1 is None and feature2 is None: return True
    rfc = model if model is not None else joblib.load('Models/rfc_model_final.pkl')
    temp_h=rfc.predict(pd.DataFrame([get_diff(feature1,feature2,[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1])],columns=['aNWP','aNSW','rSL','avWLiC','avWpS','aSN','SC','avNSyl','WV2','FRE','aNShort','language','.','!','?',',','-','of','is','the','pred_class']))
    return temp_h==0
    

def generate_solution(text=None,model=None):                                                #generiert die lösung für eine textdatei
    if text is None: return -1
    rfc = model if model is not None else joblib.load('Models/rfc_model_final.pkl')
    authors=[]
    changes=[]
    structure=[]
    
    paragraphs = tm.split_in_paragraphes(text)

    for p in paragraphs:
        if paragraphs[0] == p:
            authors.append(get_features(text=p,generate_feature=True))
            structure.append('A1')
        else:
            feature1=get_features(p,generate_feature=True)
            h = []
            for a in authors:
                if is_equal(feature1,a,rfc):
                    h=a
                    break;
            if len(h)<2:
                authors.append(feature1)
                structure.append('A'+str(len(authors)))
                changes.append(1)
            else:
                if ('A'+str(authors.index(h)+1))==structure[-1]:
                    changes.append(0)
                else:
                    structure.append('A'+str(authors.index(h)+1))
                    changes.append(1)
                authors[authors.index(h)]=[(authors[authors.index(h)][i]+feature1[i])/2 for i in range(len(feature1))]
                
            
    myDict={
            "authors": len(set(structure)),
            "structure": structure,
            "site": "not implemented yet",
            "multi-author": 1 if len(set(structure))>1 else 0,
            "changes": changes
        }
    return myDict



print('start')

#zum erzeugen der Lösungsdateien
for i in range(1,8138): #train/dataset-wide
#for i in range(1,4078): #validation/dataset-wide
#for i in range(1,3442): #train/dataset-narrow
#for i in range(1,1772): #validation/dataset-narrow
    #auskommentieren zum ausführen
    #continue
    print(i)
    try:
        p2 = pfad + f"validation/validation/dataset-wide/problem-{i}.txt"
        with open(p2,'r',encoding="utf8") as f:
            text = f.read()
        d = generate_solution(text=text)
        with open(pfad + f"validation/validation/dataset-wide/truth-problem-{i}.json") as jsonFile:
            data = json.load(jsonFile)
        print('AAAAAA=',data)
        print("My Solution=",d)
        with open(pfad + f"validation/validation/solution-wide/solution-{i}.json",'w',encoding="utf8") as f:
            json.dump(d,f)
    except:
        #val_fehlend.append(i)
        print("error")
        traceback.print_exc()

#zum Überprüfen der Lösungsdateien
#authors, structure, multi-author, changes
richtig = [0,0,0,0]
docs = 0
for i in range(1,8138): #train/dataset-wide
#for i in range(1,4078): #validation/dataset-wide
#for i in range(1,3442): #train/dataset-narrow
#for i in range(1,1772): #validation/dataset-narrow
    #auskommentieren zum ausführen
    continue
    try:
        with open(pfad + f"validation/validation/dataset-wide/truth-problem-{i}.json") as jsonFile:
            data1 = json.load(jsonFile)
        with open(pfad + f"validation/validation/solution-wide/solution-{i}.json") as f:
            data2 = json.load(f)
        richtig[0] += 1 if data1['authors']==data2['authors'] else 0
        richtig[1] += 1 if data1['structure']==data2['structure'] else 0
        richtig[2] += 1 if data1['multi-author']==data2['multi-author'] else 0
        richtig[3] += 1 if data1['changes']==data2['changes'] else 0
        docs += 1 if data1['authors']==data2['authors'] and data1['structure']==data2['structure'] and data1['multi-author']==data2['multi-author'] and data1['changes']==data2['changes'] else 0
    except:
        print("ERROR")
print(richtig)
print(docs)


