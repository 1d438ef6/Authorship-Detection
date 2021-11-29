import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from tm import tm, point
import json
import random


def getNextUsableNeighbbours(p=None, Netz=None, n=1):
    temp_arr = [i for i in Netz if i.usable]
    temp_arr.remove(p)
    temp_arr.sort(key=p.dist)
    return temp_arr[:n]
        
        
NUMBER_OF_NEIGHBOURS = 7

if True:
    i =255
    print(i)
    if True:
        p1 = "D:/Studium/Softwareprojekt/train/train/dataset-wide/truth-problem-"+str(i)+".json"
        p2 = "D:/Studium/Softwareprojekt/train/train/dataset-wide/problem-"+str(i)+".txt"
        with open(p1) as jsonFile:
            data = json.load(jsonFile)
        print(data["authors"])
        structure = data["structure"]
        changes = data["changes"]
        pos = 0
        h = []
        for i in changes:
            if i == 1:
                pos+=1
                h.append(structure[pos])
            else:
                h.append(structure[pos])
        with open(p2,'r',encoding="utf8") as f:
            text = f.read()
        paragraphs = tm.split_in_paragraphes(text=text)
        Netz = []
        v=[]
        for p in paragraphs:
            if len(tm.split_in_words(p))>0:
                v = [
                #Lexical
                    len(tm.split_in_words(p)),                                      #absolute number of words in paragraph
                    tm.get_number_of_short_words(text=p),                           #absolute number of short words
                    tm.get_relative_sentence_length(text=p,replace=True),           #relativ sentence length
                    tm.get_average_word_length(text=p),                             #average word length in charachters
                    tm.get_average_words_per_sentence(text=p),                      #average words per sentence
                    tm.get_number_of_sentences(text=p, replace=True),               #absolute sentence number
            
                    tm.get_sentence_complexity(text=p,symbol=',',replace=True),
                    tm.get_average_number_of_syllables_per_word(text=p),
                    tm.get_word_varianz2(text=p),
                    tm.get_flesch_reading_ease(text=p),
                    tm.get_symbol_frequency(text=p,symbols=['\''])[0]               #absolute number of shortings
                ]
            for i in tm.get_relative_symbol_frequency(text=p):
                v.append(i)
            for i in tm.get_relative_number_of_filler_words(text=p,filler_words=['of','is','the']):
                v.append(i)
            p1 = point(values=v,usable=True,PointClass=random.choices([1,2,3],[33,33,33],k=1)[0])
            Netz.append(p1)
            dist.append
        a = [i.PointClass for i in Netz]
        print(a)
        for i in range(5):
            for j in Netz:
                dist = [j.dist(k) for k in Netz if not j.equals(k)]
                h = [i.PointClass for i in getNextUsableNeighbbours(j, Netz, NUMBER_OF_NEIGHBOURS)]
                print(h)
                h1 = [h.count(1),h.count(2),h.count(3)]
                print(h1)
                h2 = h1.index(max(h1))+1
                print(h2)
                if h2 != j.PointClass:
                    Netz[Netz.index(j)].PointClass = h2
            a = [i.PointClass for i in Netz]
            print(a)        
            print("------------------------------------")
        a = [i.PointClass for i in Netz]
        print(a) 
                    
    #except:
        #print("Error")
