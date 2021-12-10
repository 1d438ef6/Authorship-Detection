#import matplotlib.pyplot as plt
#from mpl_toolkits import mplot3d
from tm import tm, point
import json
import random
import traceback
import threading, time


def getNextUsableNeighbbours(p=None, Netz=None, n=1):
    temp_arr = [i for i in Netz]# if i.usable]
    temp_arr.remove(p)
    #for i in Netz:
    #    if p.dist(i)>500:
    #        temp_arr.remove(i)
    temp_arr.sort(reverse=False,key=p.dist)
    #a = [p.dist(temp_arr[i]) for i in range(n)]
    #print(a)
    return temp_arr[:n]
def isClassified(Netz=None):
    for i in Netz:
        if i.PointClass==0: return False
    return True
        
        
NUMBER_OF_NEIGHBOURS = 7
DST = 5000
NUMBER_OF_RANDOM_POINTS = 5

#falsch, mehr als ein author richtig erkannt, richtig
#ergebnis=[0,0,0]
fehlend = [48, 6083, 6088, 2090, 2132, 6379, 6424, 6471, 6620, 6678, 4781, 6764, 4849, 6784, 4867, 6831, 6834, 4939, 6897, 6901, 5011, 6946, 6949, 5052, 6984, 5067, 5074, 7006, 5088, 7022, 5135, 5137, 7101, 5196, 7165, 1369, 1418, 5402, 5403, 7388, 7432, 7443, 1559, 1563, 7475, 5533, 7482, 7499, 1618, 3196, 3197, 3204, 7527, 3238, 7581, 3246, 3248, 5639, 7588, 7616, 7619, 3285, 7633, 3306, 7670, 7678, 3331, 5741, 7689, 5748, 3338, 7737, 3392, 7758, 7761, 7775, 7787, 5854, 7794, 7806, 5876, 5880, 7827, 7838, 1951, 7884, 7887, 5948, 7897, 7899, 7904, 7905, 7915, 7917, 7963, 7981, 7985, 7998, 8019, 8021, 8031, 8047, 8060, 8063, 8064, 8074, 8077, 8116]
g_points = []

def knn(start=1, end=1, gpercentage=80,repeat=10):
    if start == end:
        end+=1
    elif start>end:
        start,end = end,start
    global fehlend,g_points

    p3 = "D:/Studium/Softwareprojekt/Programmierung/Authorship-Detection--Style-Change-Detection/ergebnis.json"
    with open(p3) as jsonFile:
        initdata = json.load(jsonFile)
    m1 = initdata["min"]
    m2 = initdata["max"]

    for abcdef in range(repeat):
        print("itteration: ", abcdef)
        ergebnis = [0,0,0]
        #temp_punkte = []
        #temp_punkte.clear()
        
        random.seed(random.shuffle("abduw56783hdc jrur7f893uhJAIHDUG/83q9".split()))
        #c = [1,2,3]
        #temp_punkte.append(point(values=[random.uniform(m1[j],m2[j]) for j in range(len(m1))],usable=False,PointClass=random.choices(c,k=1)[0]))
        #c.remove(temp_punkte[0].PointClass)
        #for i in range(NUMBER_OF_RANDOM_POINTS-1):
        #    p = point(values=[random.uniform(m1[j],m2[j]) for j in range(len(m1))],usable=False,PointClass=temp_punkte[0].PointClass)
        #    while temp_punkte[0].dist(p) < DST:
        #        p.changeValues(values=[random.uniform(m1[j],m2[j]) for j in range(len(m1))])
        #    temp_punkte.append(p)
        #temp_punkte.append(point(values=[random.uniform(m1[j],m2[j]) for j in range(len(m1))],usable=False,PointClass=random.choices(c,k=1)[0]))
        #c.remove(temp_punkte[NUMBER_OF_RANDOM_POINTS].PointClass)
        #while temp_punkte[0].dist(temp_punkte[NUMBER_OF_RANDOM_POINTS]) < DST: temp_punkte[NUMBER_OF_RANDOM_POINTS].changeValues(values=[random.uniform(m1[j],m2[j]) for j in range(len(m1))])
        #for i in range(NUMBER_OF_RANDOM_POINTS-1):
        #    p = point(values=[random.uniform(m1[j],m2[j]) for j in range(len(m1))],usable=False,PointClass=temp_punkte[0].PointClass)
        #    while temp_punkte[NUMBER_OF_RANDOM_POINTS].dist(p) < DST:
        #        p.changeValues(values=[random.uniform(m1[j],m2[j]) for j in range(len(m1))])
        #    temp_punkte.append(p)
        #temp_punkte.append(point(values=[random.uniform(m1[j],m2[j]) for j in range(len(m1))],usable=False,PointClass=random.choices(c,k=1)[0]))
        #c.remove(temp_punkte[NUMBER_OF_RANDOM_POINTS*2].PointClass)
        #while temp_punkte[0].dist(temp_punkte[NUMBER_OF_RANDOM_POINTS*2]) < DST and temp_punkte[NUMBER_OF_RANDOM_POINTS].dist(temp_punkte[NUMBER_OF_RANDOM_POINTS*2]) < DST: temp_punkte[NUMBER_OF_RANDOM_POINTS].changeValues(values=[random.uniform(m1[j],m2[j]) for j in range(len(m1))])
        #for i in range(NUMBER_OF_RANDOM_POINTS-1):
        #    p = point(values=[random.uniform(m1[j],m2[j]) for j in range(len(m1))],usable=False,PointClass=temp_punkte[0].PointClass)
        #    while temp_punkte[NUMBER_OF_RANDOM_POINTS*2].dist(p) < DST:
        #        p.changeValues(values=[random.uniform(m1[j],m2[j]) for j in range(len(m1))])
        #    temp_punkte.append(p)
            
        
        print ("punkte: ", temp_punkte)#[a.values for a in temp_punkte])
        
        for e in range(start,end):
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
                h = []
                for i in changes:
                    if i == 1:
                        pos+=1
                        h.append(structure[pos])
                    else:
                        h.append(structure[pos])
                #print(h)
                with open(p2,'r',encoding="utf8") as f:
                    text = f.read()
                paragraphs = tm.split_in_paragraphes(text=text)
                #c = []
                #for i in range(int(len(paragraphs)/3)+1):
                #    c.append(1)
                #for i in range(int(len(paragraphs)/3)+1):
                #    c.append(2)
                #for i in range(int(len(paragraphs)/3)+1):
                #    c.append(3)

            
                Netz = []
                for i in temp_punkte:
                    Netz.append(point(values=i.values,usable=i.usable,PointClass=i.PointClass))
                v=[]

            
            
                for p in paragraphs(text):
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
                #if e == 1:
                #    m1 = v
                #    m2 = v
                #for i in range(len(v)):
                #    try:
                #        if v[i] < m1[i]:
                #            m1[i] = v[i]
                #    except IndexError:
                #        m1.append(v[i])
                #    try:
                #        if v[i] > m2[i]:
                #            m2[i] = v[i]
                #    except IndexError:
                #        m2.append(v[i])
                    p1 = point(values=v,usable=True,PointClass=(1 if h[paragraphs.index(p).equals('A1') else 2 if h[paragraphs.index(p).equals('A2')] else 3))#random.choices(c,k=1)[0])
                    #c.remove(p1.PointClass)
                    Netz.append(p1)
                while not isClassified(Netz):
                    for j in Netz:
                        dist = [j.dist(k) for k in Netz if not j.equals(k)]
                        hh = [i.PointClass for i in getNextUsableNeighbbours(j, Netz, NUMBER_OF_NEIGHBOURS)]
                        h1 = [hh.count(1),hh.count(2),hh.count(3)]
                        h2 = h1.index(max(h1))+1
                        if h2 != j.PointClass and j.usable:
                            Netz[Netz.index(j)].PointClass = h2  
                #print("------------------------------------")
                #a = [i.PointClass for i in Netz]
                #print(a)
                if len(set([i.PointClass for i in Netz if i.usable])) == authors:
                    ergebnis[2] += 1
                elif len(set([i.PointClass for i in Netz if i.usable])) >= authors and authors!=1:
                    ergebnis[1] += 1
                elif (len(set([i.PointClass for i in Netz if i.usable])) > 1 and authors==1) or (len(set([i.PointClass for i in Netz if i.usable])) ==1 and authors>1):
                    ergebnis[0] += 1
                print("Ergebnis: ", ergebnis)
            #except FileNotFoundError:
            #    fehlend.append(e)
            #    traceback.print_exc()
            except Exception:
                traceback.print_exc()
        ph = (100*ergebnis[2])/(end-start)
        print("aaaaaaaa:", ph)
        if gpercentage <= ph:
            g_points.append([temp_punkte])


try:
    starttime = time.time()
    t1 = threading.Thread( target = knn, args = (1, 8138, 60,15) )
    t2 = threading.Thread( target = knn, args = (1, 8138, 60,15) )
    #t3 = threading.Thread( target = knn, args = (4001, 6000, ) )
    #t4 = threading.Thread( target = knn, args = (6001, 8138, ) )
    t1.start()
    t2.start()
    #t3.start()
    #t4.start()
    t1.join()
    t2.join()
    #t3.join()
    #t4.join
    endtime = time.time()
    print("executiontime: ", endtime-starttime)
except Exception:
    traceback.print_exc()

#print("falsch, mehr als ein author richtig erkannt, richtig:")
#print(ergebnis)
print("--------------------------------------------------------------------------")
#print("fehlende Dateien:")
#print(fehlend)
#print("--------------------------------------------------------------------------")
#print("min:")
#print(m1)
#print("max:")
#print(m2)
print("gute Punkte:")
print(g_points)

mydict = {
    "g_punkte": g_points
}

with open("gpunkte.json", "w") as outfile:
    json.dump(mydict, outfile, default = lambda x:x.__dict__())
