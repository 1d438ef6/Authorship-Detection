import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from tm import tm
import json

p1 = "D:/Studium/Softwareprojekt/train/train/dataset-wide/truth-problem-7813.json"
p2 = "D:/Studium/Softwareprojekt/train/train/dataset-wide/problem-7813.txt"
#p2="warofart.txt"

with open(p1) as jsonFile:
    data = json.load(jsonFile)
structure = data["structure"]
changes = data["changes"]
print(structure)
print(changes)
pos = 0
h = []
for i in changes:
    if i == 1:
        pos+=1
        h.append(structure[pos])
    else:
        h.append(structure[pos])
print(h)
with open(p2,'r',encoding="utf8") as f:
    text = f.read()

paragraphs = tm.split_in_paragraphes(text=text)
print(len(paragraphs))

fig = plt.figure()
ax = plt.axes(projection ='3d')

for p in paragraphs:
    if len(tm.split_in_words(p))>70:
        v = [
            tm.get_sentence_complexity(text=p,symbol=',',replace=True),
            tm.get_average_word_length(text=p),
            #tm.get_sentence_length(text=p,replace=True),
            tm.get_relative_sentence_length(text=p,replace=True),
            tm.get_average_words_per_sentence(text=p),
            tm.get_average_number_of_syllables_per_word(text=p),
            tm.get_word_varianz2(text=p)*25,
            tm.get_flesch_reading_ease(text=p)
            ]
        for i in tm.get_relative_symbol_frequency(text=p):
            v.append(i)
        for i in tm.get_relative_number_of_filler_words(text=p,filler_words=['of','is','the']):
            v.append(i*50)
        x = [i for i in range(len(v))]
        c = "green" if h[paragraphs.index(p)-1]=='A1' else "red" if h[paragraphs.index(p)-1]=='A2' else "blue"
        #SC - Sentence Complexity, AWL - Average Word Length, RSL - Relative Sentence Length, AWS - Average words per Sentence, ASN - average syllable number
        #plt.xticks(ticks=x,labels=['SC','AWL','RSL','AWS','ASN','WV','FRE','.','!','?',',','-','of','is','the'])

        
        ax.plot3D(v[:int(len(v)/3)-1],v[int(len(v)/3):int(2*len(v)/3)-1],v[int(2*len(v)/3)],color=c)

plt.title('Test')
 
# show a legend on the plot
plt.legend()
 
# function to show the plot
plt.show()
