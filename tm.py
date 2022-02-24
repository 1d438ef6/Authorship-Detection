"""
    This Code provide some simple functions for feature extraction from text.

    Leon D. Wutke, Dec. 2021.
"""

# -*- coding: utf-8 -*-

import string

#R Zeugs
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector
from rpy2.robjects.packages import importr

from langdetect import detect, DetectorFactory

from hyphenate import hyphenator

class tm:

    #R-Zeugs was vermutlich irrelevant ist, da meine Textmining Funktionen besser sind
    packageNames = ('dplyr','tidytext','corpus','topicmodels')
    utils = rpackages.importr('utils')
    if not all(rpackages.isinstalled(x) for x in packageNames):
        utils = rpackages.importr('utils')
        utils.chooseCRANmirror(ind=1)
        packnames_to_install = [x for x in packageNames if not rpackages.isinstalled(x)]
        if len(packnames_to_install) > 0:
            utils.install_packages(StrVector(packnames_to_install))

    DetectorFactory.seed = 0
    languages = ['af', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et', 'fa', 'fi', 'fr', 'gu', 'he',
                 'hi', 'hr', 'hu', 'id', 'it', 'ja', 'kn', 'ko', 'lt', 'lv', 'mk', 'ml', 'mr', 'ne', 'nl', 'no', 'pa', 'pl',
                 'pt', 'ro', 'ru', 'sk', 'sl', 'so', 'sq', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'uk', 'ur', 'vi', 'zh-cn', 'zh-tw']
    
    def remove_special_characters(text = None):                             #ersetzt Umlaute im Text
        if text == None: return -1
        special_character = ["ä", "Ä", "ö", "Ö", "ü", "Ü", "ß"]             #zu ersetzende Umlaute
        replace_with = ["ae", "Ae", "oe", "Oe", "ue", "Ue", "ss"]           #womit die Umlaute ersetzt werden sollen
        if len(special_character) == len(replace_with):                     
            for i in range(len(special_character)):
                text = text.replace(special_character[i],replace_with[i])
            return text
        else:
            return -1
    def replace_characters(text = None, to_replace = {''}, replace_with = {''}):        #ersetzt Zeichen
        if text == None: return -1
        i = 0
        while len(replace_with)<len(to_replace):
            replace_with.append(replace_with[i%len(replace_with)])
            i+=1
        for i in range(len(to_replace)):
            text = text.replace(to_replace[i],replace_with[i])
        return text
    def split_in_paragraphes(text = None, sep='\n\n'):                                  #teilt den gegebenen Text in Paragraphen
        if text == None: return -1
        return text.split(sep)
    def split_in_sentences(text = None, replace = False):                   #teilt den gegebenen Text in Sätze
        if text == None: return -1
        to_replace_with_nothing = {chr(8220), chr(8222)}
        to_replace_with_space = {"\n",'  '}
        if replace:
            for e in to_replace_with_nothing:
                text = text.replace(e,'')
            for e in to_replace_with_space:
                text = text.replace(e,' ')
        for i in range(len(text)-3):                                        #ersetzt das Ende jedes Satzes mit '#-#'
            if text[i]=='.' or text[i]=='!' or text[i]=='?':
                if not text[i-1].isdigit():
                    if text[i+2].isupper():
                        text=text[:i+1] + '#-#' + text[i+2:]
        return text.split('#-#')                                              #trennt text an '#-#'
    def split_in_words(text = None, make_lowercase = False):                                        #teilt den gegebenen Text in Wörter
        if text == None: return -1
        things_to_replace = {"-\n", ".", "!", "?", "\"", "\'", "-", ",",";","(",")",":"}#Sonderzeichen die entfernt werden
        for i in things_to_replace:
            text = text.replace(i, "")
        text = text.replace("\n"," ")
        if make_lowercase:
            text = text.lower()
        return text.split(" ")
    def generate_dictionary(text = None, words = None):                     #erzeugt eine Liste mit allen möglichen Wörtern im Text
        if text == None and words == None: return -1
        if words == None:                                                   #wenn eine Liste mit Wörtern übergeben wird, wird das nicht mehr gebraucht
            text = text.lower()
            words = tm.split_in_words(text)
        words = list(set(words))                                            #doppelte Umwandlung, um alle doppelten Wörter zu entfernen
        words.sort()
        return words
    def combine_dictionaries(*dictionaries):                                #kombiniert eine beliebige Anzahl an dictionaries
        if dictionaries == None: return -1
        #if len(dictionaries)<2:                                             #ab diesem Punkt war ich zu faul ausführlich zu kommentieren
        #    return -1
        dictionary = []
        for d in dictionaries:
            dictionary += d
        dictionary = list(set(dictionary))
        dictionary.sort()
        return dictionary
    def combine_dictionary_with_frequencies(dictionary = None, frequencies = None):     #kombiniert ein dictionary mit Worthäufigkeiten
        if dictionary == None or frequencies == None: return -1
       
        if len(dictionary) == len(frequencies):
            combination = [(dictionary[i],frequencies[i]) for i in range(len(dictionary))]
            return combination
        else:
            return -1
    def get_number_of_sentences(text = None, replace = False):                               #gibt die Anzahl von Sätzen in einem Text zurück
        if text == None: return -1
        return len(tm.split_in_sentences(text=text,replace=replace))
    def get_word_frequency(text = None, dictionary = None):                 #errechnet die Worthäufigkeit eines Textes
        if text == None: return -1
        if dictionary == None:
            dictionary = tm.generate_dictionary(text)
        text=text.lower()
        words = tm.split_in_words(text)
        frequency = [words.count(i) for i in dictionary]
        return frequency
    def get_relative_word_frequency(text = None, dictionary = None):        #errechnet die relative Worthäufigkeit
        if text == None: return -1
        frequency = tm.get_word_frequency(text, dictionary)
        now1 = len(frequency)                   #number of words that are counted in frequency
        now2 = len(tm.split_in_words(text))     #number of all words in the text
        rel_frequency = [frequency[i] / now2 for i in range(now1)]
        return rel_frequency
    def get_average_word_length(text = None):                               #gibt die durchschnittliche Wortlänge zurück
        if text == None: return -1
        words = tm.split_in_words(text)
        return sum([len(i) for i in words])/len(words)
    def get_number_of_words(text = None):                                   #gibt die Anzahl der Wörter in einem Text zurück
        if text == None: return -1
        return len(tm.split_in_words(text))
    def get_average_words_per_sentence(text = None,replace=False):                        #gibt die durchschnittliche Anzahl an Wörtern pro Satz zurück
        if text == None: return -1
        sentences = tm.split_in_sentences(text=text,replace=replace)
        return sum([len(tm.split_in_words(s)) for s in sentences]) / len(sentences)
    def get_letter_frequency(text = None):                                  #gibt die Buchstaben Häufigkeit zurück
        if text == None: return -1
        alphabet = string.ascii_letters[:26]
        text = text.lower()
        return [text.count(i) for i in alphabet]
    def get_rel_letter_frequency(text = None):                              #gibt die relative Buchstabenhäufigkeit zurück
        if text == None: return -1
        frequency = tm.get_letter_frequency(text)
        l = sum(frequency)
        return [frequency[i] / l for i in range(26)]
    def get_symbols(text = None, symbols = [".","!","?",",","-"]):          #gibt alle Sonderzeichen im Text zurück
        if text == None: return -1
        return [z for z in text if z in symbols]
    def get_symbol_frequency(text = None, symbols = [".","!","?",",","-"]): #gibt die Häufigkeit der Sonderzeichen zurück
        if text == None: return -1
        symbol_marker = tm.get_symbols(text, symbols)
        return [symbol_marker.count(i) for i in symbols]
    def get_relative_symbol_frequency(text = None, symbols = [".","!","?",",","-"]):#gibt die relative Häufigkeit der Sonderzeichen zurück
        if text == None: return -1
        frequency = tm.get_symbol_frequency(text, symbols);
        nos1 = len(frequency)                       #number of symbols that are counted in frequency
        if nos1>0:
            nos2 = sum(frequency)                       #number of all symbols in the text
            return [f/nos2 for f in frequency]
        else:
            return [0 for i in frequency]
    def get_number_of_symbol_in_row(text = None, symbol = ",", symbols = [".","!","?",",","-"]):   #gibt eine Liste mit Häufigkeiten wieder in denen ein bestimmtes Zeichen in Reihe auftritt
        if text == None: return -1
        if not symbol in symbols:       #das gesuchte symbol kann nicht gefunden werden
            return -1
        if not symbol in text:          #des gesuchte symbol ist nicht im Text vorhanden
            return 0
        symbol_marker = tm.get_symbols(text, symbols)
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
        if text == None: return -1
        nosir = tm.get_number_of_symbol_in_row(text, symbol, symbols)
        if not (nosir == 0 or nosir == -1):         #get_number_of_symbol_in_row() liefert keinen Fehler zurück
            return sum(nosir)/len(nosir)
        else:
            return -1
    def get_syntagmas(text = None, position = -1, dictionary = None):       #gibt alle Syntagmas (position) eines Textes zurück
        if text == None: return -1
        text = text.lower()
        if dictionary == None:
            dictionary = tm.generate_dictionary(text)
        local_context = tm.split_in_sentences(text)
        syntagma = []
        for s in local_context:
            words = tm.split_in_words(s)
            for w in words:
                p = words.index(w)
                if 0 <= p+position < len(words):
                    t = (dictionary.index(w), dictionary.index(words[p+position]))
                    syntagma.append(t)
        return syntagma
    def get_sentence_complexity(text = None, symbol = ",", replace = False):            #gibt die Satzkomplexität zurück
        if text == None: return -1
        h = tm.get_symbol_frequency(text = text, symbols = symbol)[0]
        return h/tm.get_number_of_sentences(text)
    def get_sentence_complexity2(text = None, symbol = ",", replace = False):            #gibt die Satzkomplexität zurück
        if text == None: return -1
        return tm.get_sentence_complexity(text=text,symbol=symbol,replace=replace) * (sum(tm.get_symbol_frequency(text=text))/tm.get_number_of_sentences(text=text,replace=replace))
    def get_number_of_filler_words(text = None, filler_words = ["von","der","die","das","aber"]):     #gibt die Anzahl der gegebenen Füllwörter zurück 
        if text == None or len(filler_words)<1: return -1
        return tm.get_word_frequency(text=text,dictionary=filler_words)
    def get_relative_number_of_filler_words(text = None, filler_words = ["von","der","die","das","aber"]):          #gibt die relative Anzahl der gegebenen Füllwörter zurück
        if text == None or len(filler_words)<1: return -1
        return tm.get_relative_word_frequency(text=text,dictionary=filler_words)
    def get_sentence_length(text = None, replace = False):                          #gibt array mit allen satzlängen zurück
        if text == None: return -1
        return [len(i) for i in tm.split_in_sentences(text=text,replace=replace)]
    def get_relative_sentence_length(text=None,replace=False):                      #gibt satzlänge relativ zur satzanzahl zurück
        if text == None: return -1
        return sum(tm.get_sentence_length(text=text,replace=replace))/tm.get_number_of_sentences(text=text,replace=replace)
    def get_average_number_of_syllables_per_word(text=None):                                    #gibt durchschnittliche silbenanzahl pro wort zurück
        if text == None: return -1
        words = tm.split_in_words(text=text)
        return sum([len(hyphenator.hyphenate_word(w)) for w in words])/len(words)
    def get_word_varianz(text = None):                                              #gibt die anzahl verwendeter wörter zurück (Wortvarianz)
        if text == None: return -1
        return len(tm.generate_dictionary(text=text))
    def get_word_varianz2(text = None):                                             #gibt die Wortvarianz gewichtet auf die textlänge zurück
        if text == None: return -1
        return 1/((1/tm.get_word_varianz(text=text))*len(tm.split_in_words(text=text)))
    def get_flesch_reading_ease(text=None):                                         #gibt den Flesch reading ease zurück
        if text == None: return -1
        return 206.835-(84.6*tm.get_average_number_of_syllables_per_word(text=text))-(1.015*tm.get_average_words_per_sentence(text=text,replace=True))
    def get_number_of_short_words(text = None):                                     #gibt die anzahl kurzer wörter zurück                         
        if text == None: return -1
        return sum([1 for i in tm.split_in_words(text=text) if len(i)<4])
    def get_number_of_short_words2(text=None):                                      #gibt die anzahl kurzer wörter gewichtet auf textlänge zurück
        if text==None: return -1
        return tm.get_number_of_short_words(text=text)/len(tm.split_in_words(text=text))
    def contain_number(text = None):                                                #gibt zurück ob ein text zahlen beinhaltet
        if text == None: return -1
        return any(i.isdigit() for i in text)
    def get_language(text=None):                                                    #gibt die sprache eines textes zurück
        if text == None: return -1
        languages = ['af', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et', 'fa', 'fi', 'fr', 'gu', 'he',
                     'hi', 'hr', 'hu', 'id', 'it', 'ja', 'kn', 'ko', 'lt', 'lv', 'mk', 'ml', 'mr', 'ne', 'nl', 'no', 'pa', 'pl',
                     'pt', 'ro', 'ru', 'sk', 'sl', 'so', 'sq', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'uk', 'ur', 'vi', 'zh-cn', 'zh-tw']
        return languages.index(detect(text))
    def get_language2(text=None,lang=10):                                           #gibt wahrscheinlichkeit wieder dass wort bestimmter sprache angehörig ist
        t = tm.split_in_sentences(text=text,replace=True)
        l = [[tm.get_language(w) for w in t].count(i) for i in range(55)]
        return l[lang]/len(t)
    def get_topic(text = None):                                                     #gibt das topic eines textes zurück (zukünftig)
        if text == None: return -1
        #robjects.r('''
        #library(topicmodels)
        #ap_lda = 
        #''')
    def lemmatize(text = None):
        pass
        


if __name__ == "__main__":
    pass
