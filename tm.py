# -*- coding: utf-8 -*-

import string

#R Zeugs
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector
from rpy2.robjects.packages import importr


class tm:
    
    packageNames = ('dplyr','tidytext','corpus')
    utils = rpackages.importr('utils')
    if not all(rpackages.isinstalled(x) for x in packageNames):
        utils = rpackages.importr('utils')
        utils.chooseCRANmirror(ind=1)
        packnames_to_install = [x for x in packageNames if not rpackages.isinstalled(x)]
        if len(packnames_to_install) > 0:
            utils.install_packages(StrVector(packnames_to_install))
    
    def remove_special_characters(text = None):                             #ersetzt Umlaute im Text
        if text == None:
            return -1
        special_character = ["ä", "Ä", "ö", "Ö", "ü", "Ü", "ß"]             #zu ersetzende Umlaute
        replace_with = ["ae", "Ae", "oe", "Oe", "ue", "Ue", "ss"]           #womit die Umlaute ersetzt werden sollen
        if len(special_character) == len(replace_with):                     
            for i in range(len(special_character)):
                text = text.replace(special_character[i],replace_with[i])
        else:
            return -1
        return text
    def replace_characters(text = None, to_replace = {''}, replace_with = {''}):
        if text == None:
            return -1
        i = 0
        while len(replace_with)<len(to_replace):
            replace_with.append(replace_with[i%len(replace_with)])
            i+=1
        for i in range(len(to_replace)):
            text = text.replace(to_replace[i],replace_with[i])
        return text
    def split_in_paragraphes(text = None):                                  #teilt den gegebenen Text in Paragraphen
        if text == None:                                                    #wenn kein Text übergeben wurde -> Error 
            return -1
        return text.split('\n\n')
    def split_in_sentences(text = None, replace = False):                   #teilt den gegebenen Text in Sätze
        if text == None:                                                    #wenn kein Text übergeben wurde -> Error
            return -1
        to_replace_with_nothing = {chr(8220), chr(8222)}
        to_replace_with_space = {"\n",'  '}
        if replace:
            for e in to_replace_with_nothing:
                text = text.replace(e,'')
            for e in to_replace_with_space:
                text = text.replace(e,' ')
        for i in range(len(text)-3):                                        #ersetzt das Ende jedes Satzes mit '#'
            if text[i]=='.' or text[i]=='!' or text[i]=='?':
                if not text[i-1].isdigit():
                    if text[i+2].isupper():
                        text=text[:i+1] + '#' + text[i+2:]
        return text.split('#')                                              #trennt text an '#'
    def split_in_words(text = None):                                        #teilt den gegebenen Text in Wörter
        if text == None:                                                    #wenn kein Text übergeben wurde -> Error
            return -1
        things_to_replace = {"-\n", ".", "!", "?", "\"", "\'", "-", ",",";"}#Sonderzeichen die entfernt werden
        for i in things_to_replace:
            text = text.replace(i, "")
        text = text.replace("\n"," ")
        return text.split(" ")
    def generate_dictionary(text = None, words = None):                     #erzeugt eine Liste mit allen möglichen Wörtern im Text
        if text == None and words == None:                                  #wenn kein Text übergeben wurde -> Error
            return -1
        if words == None:                                                   #wenn eine Liste mit Wörtern übergeben wird, wird das nicht mehr gebraucht
            text = text.lower()
            words = tm.split_in_words(text)
        words = list(set(words))                                            #doppelte Umwandlung, um alle doppelten Wörter zu entfernen
        words.sort()
        return words
    def combine_dictionaries(*dictionaries):                                #kombiniert eine beliebige Anzahl an dictionaries
        if dictionaries == None:                                            #anscheinend unnötig, wird nix übergeben ist dictionaries != None und len(dictionaries)<2
            return -1
        if len(dictionaries)<2:                                             #ab diesem Punkt war ich zu faul ausführlich zu kommentieren
            return -1
        dictionary = []
        for d in dictionaries:
            dictionary += d
        dictionary = list(set(dictionary))
        dictionary.sort()
        return dictionary
    def combine_dictionary_with_frequencies(dictionary = None, frequencies = None):     #kombiniert ein dictionary mit Worthäufigkeiten
        if dictionary == None or frequencies == None:
            return -1
        combination = []
        if len(dictionary) == len(frequencies):
            for i in range(len(dictionary)):
                t = (dictionary[i],frequencies[i])
                combination.append(t)
            return combination
        else:
            return -1
    def get_number_of_sentences(text = None):                               #gibt die Anzahl von Sätzen in einem Text zurück
        if text == None:
            return -1
        return len(tm.split_in_sentences(text))
    def get_word_frequency(text = None, dictionary = None):                 #errechnet die Worthäufigkeit eines Textes
        if text == None:
            return -1
        if dictionary == None:
            dictionary = tm.generate_dictionary(text)
        frequency = [0 for i in range(len(dictionary))]
        text=text.lower()
        words = tm.split_in_words(text)
        for e in words:
            if e in dictionary:                                             #für den Fall das ein Wort des Textes nicht im dictionary enthalten ist, zB wenn man nur die Häufigkeit bestimmter Wörter sucht
                pos = dictionary.index(e)
                frequency[pos] = frequency[pos] + 1
            else:
                print(e + " ist nicht in dictionary vorhanden")
        return frequency
    def get_relative_word_frequency(text = None, dictionary = None):        #errechnet die relative Worthäufigkeit
        if text == None:
            return -1
        frequency = tm.get_word_frequency(text, dictionary)
        now1 = len(frequency)                   #number of words that are counted in frequency
        now2 = len(tm.split_in_words(text))     #number of all words in the text
        rel_frequency = [0 for i in range(now1)]
        for i in range(now1):
            rel_frequency[i] = frequency[i] / now2
        return rel_frequency
    def get_average_word_length(text = None):                               #gibt die durchschnittliche Wortlänge zurück
        if text == None:
            return -1
        words = tm.split_in_words(text)
        l = 0
        for w in words:
            l += len(w)
        return l/len(words)
    def get_number_of_words(text = None):                                   #gibt die Anzahl der Wörter in einem Text zurück
        if text == None:
            return -1
        return len(tm.split_in_words(text))
    def get_average_words_per_sentence(text = None):                        #gibt die durchschnittliche Anzahl an Wörtern pro Satz zurück
        if text == None:
            return -1
        sentences = tm.split_in_sentences(text)
        l_sentences = 0
        for s in sentences:
            w = tm.split_in_words(s)
            l_sentences += len(w)
        return l_sentences / len(sentences)
    def get_letter_frequency(text = None):                                  #gibt die Buchstaben Häufigkeit zurück
        if text == None:
            return -1
        alphabet = string.ascii_letters[:26]
        text = text.lower()
        frequency = [0 for i in range(26)]
        for l in text:
            if l in alphabet:
                pos = alphabet.index(l)
                frequency[pos] += 1
        return frequency
    def get_rel_letter_frequency(text = None):                              #gibt die relative Buchstabenhäufigkeit zurück
        if text == None:
            return -1
        frequency = tm.get_letter_frequency(text)
        rel_frequency = [0 for i in range(26)]
        l = 0
        for i in frequency:
            l += i
        for i in range(26):
            rel_frequency[i] = frequency[i] / l
        return rel_frequency
    def get_symbols(text = None, symbols = [".","!","?",",","-"]):          #gibt alle Sonderzeichen im Text zurück
        if text == None:
            return -1
        found_symbols = []
        for z in text:
            if z in symbols:
                found_symbols.append(z)
        return found_symbols
    def get_symbol_frequency(text = None, symbols = [".","!","?",",","-"]): #gibt die Häufigkeit der Sonderzeichen zurück
        if text == None:
            return -1
        symbol_marker = tm.get_symbols(text, symbols)     
        frequency = [0 for i in range(len(symbols))]
        for e in symbol_marker:
            pos = symbols.index(e)
            frequency[pos] = frequency[pos] + 1
        return frequency
    def get_relative_symbol_frequency(text = None, symbols = [".","!","?",",","-"]):#gibt die relative Häufigkeit der Sonderzeichen zurück
        if text == None:
            return -1
        frequency = tm.get_symbol_frequency(text, symbols);
        nos1 = len(frequency)                       #number of symbols that are counted in frequency
        nos2 = len(tm.get_symbols(text, symbols))   #number of all symbols in the text
        rel_frequency = [0 for i in range(nos1)]
        for i in range(nos1):
            rel_frequency[i] = frequency[i] / nos2
        return rel_frequency
    def get_number_of_symbol_in_row(text = None, symbol = ",", symbols = [".","!","?",",","-"]):   #gibt eine Liste mit Häufigkeiten wieder in denen ein bestimmtes Zeichen in Reihe auftritt
        if text == None:
            return -1
        if not symbol in symbols:       #das gesuchte symbol kann nicht gefunden werden
            return -1
        if not symbol in text:          #des gesuchte symbol ist nicht im Text vorhanden
            return 0
        print(text)
        symbol_marker = tm.get_symbols(text, symbols)
        print(symbol_marker)
        nosir = []          #number of symbols in row
        h = 0
        for i in range(len(symbol_marker)):
            if symbol_marker[i] == symbol:
                h += 1
            else:
                if not h == 0:
                    nosir.append(h)
                    h = 0  
        nosir.append(h)
        return nosir
    def get_average_number_of_symbol_in_row(text = None, symbol = ",", symbols = [".","!","?",",","-"]):        #gibt die durschnittlich Häufigkeit eines bestimmten Zeichens in Reihe zurück
        if text == None:
            return -1
        nosir = tm.get_number_of_symbol_in_row(text, symbol, symbols)
        if not (nosir == 0 or nosir == -1):         #get_number_of_symbol_in_row() liefert keinen Fehler zurück
            h = 0
            for e in nosir:
                h += e
            return h/len(nosir)
        else:
            return -1
    def get_syntagmas(text = None, position = -1, dictionary = None):       #gibt alle Syntagmas eines Textes zurück
        if text == None:
            return -1
        text = text.lower()
        if dictionary == None:
            dictionary = tm.generate_dictionary(text)
        local_context = tm.split_in_sentences(text)
        #print(local_context)
        syntagma = []
        for s in local_context:
            words = tm.split_in_words(s)
            #print(words)
            for w in words:
                p = words.index(w)
                if 0 <= p+position < len(words):
                    t = (dictionary.index(w), dictionary.index(words[p+position]))
                    syntagma.append(t)
        return syntagma

import json
class jsonConverter:                            #to use that damn jsons file
    def __init__(self, jsonFile):
        with open('data.json') as json_file:
            self.data = json.load(jsonFile)
    def get_number_of_authors(self):
        return self.data["authors"]
    def get_structure(self):
        return self.data["structure"]
    def if_multi_author(self):
        return self.data["multi-author"]
    def get_changes(self):
        return self.data["changes"]
    

if __name__ == "__main__":
    f = open("text.txt", "r", encoding="utf8")
    text3 = f.read()
    f.close()
    #print(text3)
    text3 = tm.remove_special_characters(text3)
    t = tm.split_in_sentences(text3, replace=True)
    print("a")

