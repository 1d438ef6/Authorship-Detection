import pandas as pd
from sklearn.neighbors import KNeighborsClassifier  #KNN
from sklearn import metrics #Accuracy Berechnung Precision, Recall, F1 usw
from sklearn.preprocessing import StandardScaler #Scaler standartizieren

    #Alle csv in eindeutige Variablen speichern
dfw_train = pd.read_csv('feature_save_train_wide_ganz.csv', usecols=['aNWP', 'aNSW', 'rSL', 'avWLiC', 'avWpS', 'aSN', 'SC', 'avNSyl', 'WV2', 'FRE', 'aNShort', 'language', '.', '!', '?', ',', '-', 'of', 'is', 'the', 'class', 'doc'])
dfw_val = pd.read_csv('feature_save_val_wide_ganz.csv', usecols=['aNWP', 'aNSW', 'rSL', 'avWLiC', 'avWpS', 'aSN', 'SC', 'avNSyl', 'WV2', 'FRE', 'aNShort', 'language', '.', '!', '?', ',', '-', 'of', 'is', 'the', 'class', 'doc'])
dfn_train = pd.read_csv('feature_save_train_narrow_ganz.csv', usecols=['aNWP', 'aNSW', 'rSL', 'avWLiC', 'avWpS', 'aSN', 'SC', 'avNSyl', 'WV2', 'FRE', 'aNShort', 'language', '.', '!', '?', ',', '-', 'of', 'is', 'the', 'class', 'doc'])
dfn_val = pd.read_csv('feature_save_val_narrow_ganz.csv', usecols=['aNWP', 'aNSW', 'rSL', 'avWLiC', 'avWpS', 'aSN', 'SC', 'avNSyl', 'WV2', 'FRE', 'aNShort', 'language', '.', '!', '?', ',', '-', 'of', 'is', 'the', 'class', 'doc'])


   ##kNN für Datensatz Wide


    #Tabelle auf die verschiednen Variablen hinsichtlich Auswertung aufteilen
X_train = dfw_train.drop(columns = ['class', 'doc'])
y_train = dfw_train['class']
X_test = dfw_val.drop(columns = ['class', 'doc'])
y_test = dfw_val['class']

    #Skalieren
scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

    #Knn trainieren
myKNN = KNeighborsClassifier(n_neighbors=200, weights='distance')
myKNN.fit(X_train, y_train)
y_predict = myKNN.predict(X_test)

    #Report
print('Wide: ', metrics.classification_report(y_test, y_predict))

    #Index abfragen von allen, die mit nur einem Autor predicted wurden
doc_num = dfw_val['doc']
index_mehrere_Autoren = []
for i in range(0, len(y_predict)) :
    if y_predict[i] != 3 :
        index_mehrere_Autoren.append(i)

with open('kNN_wide.txt', 'w') as f:
    for element in index_mehrere_Autoren:
        f.write(str(element) + '\n')
    f.close()






    ##kNN für Datensatz Narrow
    
    #Tabelle auf die verschiednen Variablen hinsichtlich Auswertung aufteilen
X_train = dfn_train.drop('class', axis=1)
y_train = dfn_train['class']
X_test = dfn_val.drop('class', axis=1)
y_test = dfn_val['class']

    #Skalieren
scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

    #Knn trainieren
myKNN = KNeighborsClassifier(n_neighbors=200, weights='distance')
myKNN.fit(X_train, y_train)
y_predict = myKNN.predict(X_test)

    #Report
print('Narrow: ', metrics.classification_report(y_test, y_predict))

    #Index abfragen von allen, die mit nur einem Autor predicted wurden
doc_num = dfn_val['doc']
index_mehrere_Autoren = []
for i in range(0, len(y_predict)) :
   if y_predict[i] != 3 :
        index_mehrere_Autoren.append(i)

with open('kNN_narrow.txt', 'w') as f:
    for element in index_mehrere_Autoren:
        f.write(str(element) + '\n')
    f.close()


