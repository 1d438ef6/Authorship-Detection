import pandas as pd
import traceback,json
from tm import tm
from os.path import isdir
import joblib
import os

#Features über ganze Docs in CSV
def run_through_docs():
    path = "C:/Users/johan/Desktop/Softwareprojekt/validation/dataset-narrow"            
    start = 1
    stop = 1722
    path_to_dataset = path
    features = []
    for file_num in range(start, stop):
        path_1 = f"{path_to_dataset}/truth-problem-{file_num}.json"
        path_2 = f"{path_to_dataset}/problem-{file_num}.txt"

        if not os.path.isfile(path_1.encode()) or not os.path.isfile(path_2):
            continue
        
        with open(path_1, "r", encoding="utf-8") as file_1:
            data = json.load(file_1)
            authors = data.get("authors", None)

        with open(path_2, "r", encoding="utf-8") as file_2:
            text = file_2.read()
                   
        if text is None: 
            continue
        else: 
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
        v.append(authors)
        v.append(file_num)
        features.append(v)
    return features
    

df = run_through_docs()
c = ['aNWP','aNSW','rSL','avWLiC','avWpS','aSN','SC','avNSyl','WV2','FRE','aNShort','language','.','!','?',',','-','of','is','the','class', 'doc']
dataf = pd.DataFrame(df, columns=c)
dataf.to_csv('feature_save_val_narrow_ganz.csv')


def get_features(text=None,generate_feature=False,model=None):                                             #gibt die features für einen text zurück
    if text is None: return -1
    if model is None and generate_feature: rfc=joblib.load('rfc_model_test.pkl')
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

#gibt die differenz zwischen 2 feature-listen zurück
def get_diff(a1,a2,b=[]):                                                   
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

#feature_save über Absätze mit allen Features, Autor Und Dokument
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

