import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import traceback,json,time
from tm import tm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import joblib
from os.path import exists, isdir

fehlend = [48, 6083, 6088, 2090, 2132, 6379, 6424, 6471, 6620, 6678, 4781, 6764, 4849, 6784, 4867, 6831, 6834, 4939, 6897, 6901, 5011, 6946, 6949, 5052, 6984, 5067, 5074, 7006, 5088, 7022, 5135, 5137, 7101, 5196, 7165, 1369, 1418, 5402, 5403, 7388, 7432, 7443, 1559, 1563, 7475, 5533, 7482, 7499, 1618, 3196, 3197, 3204, 7527, 3238, 7581, 3246, 3248, 5639, 7588, 7616, 7619, 3285, 7633, 3306, 7670, 7678, 3331, 5741, 7689, 5748, 3338, 7737, 3392, 7758, 7761, 7775, 7787, 5854, 7794, 7806, 5876, 5880, 7827, 7838, 1951, 7884, 7887, 5948, 7897, 7899, 7904, 7905, 7915, 7917, 7963, 7981, 7985, 7998, 8019, 8021, 8031, 8047, 8060, 8063, 8064, 8074, 8077, 8116]

def get_features(text=None,model=None):
    if text is None: return -1
    if model is None: rfc=joblib.load('rfc_model_test.pkl')
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
    temp_h=rfc.predict(pd.DataFrame([v],columns=['aNWP','aNSW','rSL','avWLiC','avWpS','aSN','SC','avNSyl','WV2','FRE','aNShort','language','.','!','?',',','-','of','is','the']))
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
            
def train_new_model(path_to_feature_save=None, n_of_trees=50):
    if path_to_feature_save is None or not exists(path_to_feature_save): return -1
    data2 = pd.read_csv(path_to_feature_save)
    X_train, X_test, y_train, y_test = train_test_split(
                                        data2[['aNWP','aNSW','rSL','avWLiC','avWpS','aSN','SC','avNSyl','WV2','FRE','aNShort','language','.','!','?',',','-','of','is','the']],
                                        data2['class'],
                                        test_size=0.1)
    rfc=RandomForestClassifier(n_estimators=n_of_trees)
    rfc.fit(X_train,y_train)
    return rfc

def generate_feature_save(path_to_dataset=None,start=None,stop=None,fehlend=None):
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
                        v=get_diff(get_features(p1),get_features(p2),[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1])
                        v.append(0 if h[paragraphs.index(p)]==h[paragraphs.index(p)+1] else 1)
                
                        x.append(v)    

            else:
                for p in range(len(paragraphs)):
                    if len(tm.split_in_words(paragraphs[p]))>70:
                        v = get_features(paragraphs[p])
                        v.append(h[p])
        except Exception:
            traceback.print_exc()
    
    return pd.DataFrame(x,columns=['aNWP','aNSW','rSL','avWLiC','avWpS','aSN','SC','avNSyl','WV2','FRE','aNShort','language','.','!','?',',','-','of','is','the','pred_class','class'])

def is_equal(feature1=None,feature2=None,model=None):
    if (feature1 is None and feature2 is not None) or (feature1 is not None and feature2 is None): return False
    elif feature1 is None and feature2 is None: return True
    rfc = model if model is not None else rfc=joblib.load('rfc_model_final.pkl')
    temp_h=rfc.predict(pd.DataFrame([get_diff(feature1,feature2,[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1])],columns=['aNWP','aNSW','rSL','avWLiC','avWpS','aSN','SC','avNSyl','WV2','FRE','aNShort','language','.','!','?',',','-','of','is','the','pred_class']))
    return temp_h==0
    

def generate_solution(text=None,model=None):
    if text is None: return -1
    rfc = model if model is not None else joblib.load('rfc_model_final.pkl')
    authors=[]
    changes=[]
    structure=[]
    
    paragraphs = tm.split_in_paragraphes(text)

    for p in paragraphs:
        if paragraphs.index(p) == 0:
            authors.append(get_features(text=p))
            structure.append('A1')
            changes.append(0)
        else:
            feature1=get_features(p)
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
                if ('A'+str(authors.index(h)))==structure[-1]:
                    changes.append(0)
                else:
                    structure.append('A'+str(authors.index(h)))
                    changes.append(1)
                authors[authors.index(h)]=[(authors.index(h)[i]+feature1[i])/2 for i in range(len(feature1))]
                
            
    myDict={
            "authors": len(set(structure)),
            "structure": structure,
            "site": "not implemented yet",
            "multi-author": 1 if len(set(structure))>1 else 0,
            "changes": changes
        }
    return myDict


from dataclasses import dataclass

@dataclass
class Model:
    models = list()

    author_id: int
    changes: bool = False

    def __post_init__(self):
        self.models.append(self)

    def get_all_changes(self):
        return self.models.changes

    @property
    def structure(self):
        _structure = list()

        for model in self.models:
            if len(_structure) != 0:
                _structure.append(model.author_id)
                continue
            if _structure[-1] != model.author_id:
                _structure.append(model.author_id)

        return [f"A{_s}" for _s in _structure]


@dataclass
class Author:
    author_counter = 0

    features: list
    author_id: int = 1

    def average_features(self, feature1):
        for num_feature in range(len(self.features)):
            self.features[num_feature] = self.features[num_feature] + feature1[num_feature] / 2

    def __post_init__(self):
        self.author_id = Author.author_counter
        Author.author_counter += 1

    def __str__(self):
        return f"Author: {self.author_id}"


def generate_solution2(text: str = "", model=None):
    if not text:
        return -1

    rfc = model if model is not None else joblib.load('rfc_model_final.pkl')



    authors = []
    changes = []
    structure = []

    ##############
    _authors = []
    # _models = []

    paragraphs = tm.split_in_paragraphes(text)

    for p in paragraphs:
        if paragraphs[0] == p:

            ###################
            _author = Author(features=get_features(text=p))
            _authors.append(_author)

            Model(author_id=_author.author_id)


        else:
            feature1: list = get_features(text=p)

            #############
            # if len(_h) > 1 then dont add author features PS: MysticBanana
            _h = [author for author in _authors if is_equal(feature1, author.features, rfc)]
            _h = _h[0]

            if len(_h.features) == 0:
                _author = Author(features=feature1)
                _authors.append(_author)
                Model(author_id=_author.author_id, changes=True)
            else:
                _author = _authors[-1]
                # if _author.author_id == _h.author_id:
                #     Model(author_id=_h.author_id)
                # else:
                #     Model(author_id=_h.author_id, changes=True)

                Model(author_id=_h.author_id, changes=(not _author.author_id == _h.author_id))
                _h.average_features(feature1=feature1)
    mystics_dict = {
        "authors": len(_authors),
        "structure": Model.structure,
        "site": "not implemented yet",
        "multi-author": int(not len(authors) == 1),
        "changes": Model.models[0].get_all_changes()
    }

    return mystics_dict # too

starttime1 = time.time()
print('start')

#p1 = "D:/Studium/Softwareprojekt/train/train/dataset-wide/truth-problem-"+str(data)+".json"
p2 = "D:/Studium/Softwareprojekt/train/train/dataset-wide/problem-"+str(5)+".txt"
#p2="warofart.txt"
with open(p2,'r',encoding="utf8") as f:
    text = f.read()
print(generate_solution2(text=text,model=2))

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
