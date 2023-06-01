"""
    This Code provide some simple functions for feature extraction from text.

    Leon D. Wutke, Dec. 2021.
"""

# -*- coding: utf-8 -*-

import string
from langdetect import detect, DetectorFactory
from typing import List

from hyphenate import hyphenator


class tm:

    DetectorFactory.seed = 0
    languages = ['af', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et', 'fa', 'fi', 'fr', 'gu',
                 'he',
                 'hi', 'hr', 'hu', 'id', 'it', 'ja', 'kn', 'ko', 'lt', 'lv', 'mk', 'ml', 'mr', 'ne', 'nl', 'no', 'pa',
                 'pl',
                 'pt', 'ro', 'ru', 'sk', 'sl', 'so', 'sq', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'uk', 'ur', 'vi',
                 'zh-cn', 'zh-tw']

    def remove_special_characters(text: str = None):
        assert text is not None
        special_character = ["ä", "Ä", "ö", "Ö", "ü", "Ü", "ß"]  # zu ersetzende Umlaute
        replace_with = ["ae", "Ae", "oe", "Oe", "ue", "Ue", "ss"]  # womit die Umlaute ersetzt werden sollen
        assert len(special_character) == len(replace_with)
        for i in range(len(special_character)):
            text = text.replace(special_character[i], replace_with[i])
        return text

    def replace_characters(text: str = None, to_replace: List[str] = None, replace_with: List[str] = None):
        assert text is not None and to_replace is not None and replace_with is not None
        i = 0
        while len(replace_with) < len(to_replace):
            replace_with.append(replace_with[i % len(replace_with)])
            i += 1
        for i in range(len(to_replace)):
            text = text.replace(to_replace[i], replace_with[i])
        return text

    def split_in_paragraphes(text: str = None, sep: str = '\n\n'):  # teilt den gegebenen Text in Paragraphen
        assert text is not None
        return text.split(sep)

    def split_in_sentences(text: str = None, replace: bool = False):  # teilt den gegebenen Text in Sätze
        assert text is not None
        to_replace_with_nothing = {chr(8220), chr(8222)}
        to_replace_with_space = {"\n", '  '}
        if replace:
            for e in to_replace_with_nothing:
                text = text.replace(e, '')
            for e in to_replace_with_space:
                text = text.replace(e, ' ')
        for i in range(len(text) - 3):  # ersetzt das Ende jedes Satzes mit '#-#'
            if text[i] == '.' or text[i] == '!' or text[i] == '?':
                if not text[i - 1].isdigit():
                    if text[i + 2].isupper():
                        text = text[:i + 1] + '#-#' + text[i + 2:]
        return text.split('#-#')  # trennt text an '#-#'

    def split_in_words(text: str = None, make_lowercase: bool = False):  # teilt den gegebenen Text in Wörter
        assert text is not None
        things_to_replace = {"-\n", ".", "!", "?", "\"", "\'", "-", ",", ";", "(", ")",
                             ":"}  # Sonderzeichen die entfernt werden
        for i in things_to_replace:
            text = text.replace(i, "")
        text = text.replace("\n", " ")
        if make_lowercase:
            text = text.lower()
        return text.split(" ")

    def generate_dictionary(text: str = None, words: List[str] = None):  # erzeugt eine Liste mit allen möglichen Wörtern im Text
        assert text is not None or words is not None
        if words is None:  # wenn eine Liste mit Wörtern übergeben wird, wird das nicht mehr gebraucht
            text = text.lower()
            words = tm.split_in_words(text)
        words = list(set(words))  # doppelte Umwandlung, um alle doppelten Wörter zu entfernen
        words.sort()
        return words

    def combine_dictionaries(*dictionaries: List[str]):  # kombiniert eine beliebige Anzahl an dictionaries
        assert dictionaries is not None
        assert len(dictionaries) > 1
        dictionary = []
        for d in dictionaries:
            dictionary += d
        dictionary = list(set(dictionary))
        dictionary.sort()
        return dictionary

    def combine_dictionary_with_frequencies(dictionary: List[str] = None,
                                            frequencies: List = None):  # kombiniert ein dictionary mit Worthäufigkeiten
        assert dictionary is not None and frequencies is not None
        assert len(dictionary) == len(frequencies)
        combination = [(dictionary[i], frequencies[i]) for i in range(len(dictionary))]
        return combination

    def get_number_of_sentences(text: str = None, replace: bool = False):  # gibt die Anzahl von Sätzen in einem Text zurück
        assert text is not None
        return len(tm.split_in_sentences(text=text, replace=replace))

    def get_word_frequency(text: str = None, dictionary: List[str] = None):  # errechnet die Worthäufigkeit eines Textes
        assert text is not None
        words = tm.split_in_words(text=text, make_lowercase=True)
        if dictionary is None:
            dictionary = tm.generate_dictionary(text)
        return [words.count(i) for i in dictionary]

    def get_relative_word_frequency(text: str = None, dictionary: List[str] = None):  # errechnet die relative Worthäufigkeit
        assert text is not None
        frequency = tm.get_word_frequency(text=text, dictionary=dictionary)
        now = len(frequency)  # number of words that are counted in frequency
        return [frequency[i] / now for i in range(now)]

    def get_average_word_length(text: str = None):  # gibt die durchschnittliche Wortlänge zurück
        assert text is not None
        words = tm.split_in_words(text)
        return sum([len(i) for i in words]) / len(words)

    def get_number_of_words(text: str = None):  # gibt die Anzahl der Wörter in einem Text zurück
        assert text is not None
        return len(tm.split_in_words(text))

    def get_average_words_per_sentence(text: str =None,
                                       replace: bool = False):  # gibt die durchschnittliche Anzahl an Wörtern pro Satz zurück
        assert text is not None
        sentences = tm.split_in_sentences(text=text, replace=replace)
        return sum([len(tm.split_in_words(s)) for s in sentences]) / len(sentences)

    def get_letter_frequency(text: str = None):  # gibt die Buchstaben Häufigkeit zurück
        assert text is not None
        alphabet = string.ascii_letters[:26]
        text = text.lower()
        return [text.count(i) for i in alphabet]

    def get_rel_letter_frequency(text: str = None):  # gibt die relative Buchstabenhäufigkeit zurück
        assert text is not None
        frequency = tm.get_letter_frequency(text)
        l = sum(frequency)
        return [frequency[i] / l for i in range(26)]

    def get_symbols(text: str = None, symbols: List[str] = [".", "!", "?", ",", "-"]):  # gibt alle Sonderzeichen im Text zurück
        assert text is not None
        return [z for z in text if z in symbols]

    def get_symbol_frequency(text: str = None,
                             symbols: List[str] = [".", "!", "?", ",", "-"]):  # gibt die Häufigkeit der Sonderzeichen zurück
        assert text is not None
        symbol_marker = tm.get_symbols(text, symbols)
        return [symbol_marker.count(i) for i in symbols]

    def get_relative_symbol_frequency(text: str = None, symbols: List[str] = [".", "!", "?", ",","-"]):  # gibt die relative Häufigkeit der Sonderzeichen zurück
        assert text is not None
        frequency = tm.get_symbol_frequency(text, symbols);
        nos1 = len(frequency)  # number of symbols that are counted in frequency
        if nos1 > 0:
            nos2 = sum(frequency)  # number of all symbols in the text
            return [f / nos2 for f in frequency]
        else:
            return [0 for i in frequency]

    def get_number_of_symbol_in_row(text: str = None, symbol: str = ",", symbols: List[str] = [".", "!", "?", ",","-"]):  # gibt eine Liste mit Häufigkeiten wieder in denen ein bestimmtes Zeichen in Reihe auftritt
        assert text is not None
        assert symbol in symbols   # das gesuchte symbol kann nicht gefunden werden
        if symbol not in text:     # des gesuchte symbol ist nicht im Text vorhanden
            return 0
        symbol_marker = tm.get_symbols(text, symbols)
        nosir = []  # number of symbols in row
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

    def get_average_number_of_symbol_in_row(text: str = None, symbol: str = ",", symbols: List[str] = [".", "!", "?", ",","-"]):  # gibt die durschnittlich Häufigkeit eines bestimmten Zeichens in Reihe zurück
        assert text is not None
        nosir = tm.get_number_of_symbol_in_row(text=text, symbol=symbol, symbols=symbols)
        if not (nosir == 0):  # get_number_of_symbol_in_row() liefert keinen Fehler zurück
            return sum(nosir) / len(nosir)
        else:
            return 0

    def get_syntagmas(text: str = None, position: int = -1, dictionary: List[str] = None):  # gibt alle Syntagmas (position) eines Textes zurück
        assert text is not None
        text = text.lower()
        if dictionary is None:
            dictionary = tm.generate_dictionary(text)
        local_context = tm.split_in_sentences(text)
        syntagma = []
        for s in local_context:
            words = tm.split_in_words(s)
            for w in words:
                p = words.index(w)
                if 0 <= p + position < len(words):
                    t = (dictionary.index(w), dictionary.index(words[p + position]))
                    syntagma.append(t)
        return syntagma

    def get_sentence_complexity(text: str = None, symbol: str = ",", replace: bool = False):  # gibt die Satzkomplexität zurück
        assert text is not None
        h = tm.get_symbol_frequency(text=text, symbols=symbol)[0]
        return h / tm.get_number_of_sentences(text=text, replace=replace)

    def get_sentence_complexity2(text: str = None, symbol: str = ",", replace: bool = False):  # gibt die gewichtete Satzkomplexität zurück
        assert text is not None
        return tm.get_sentence_complexity(text=text, symbol=symbol, replace=replace) * (
                    sum(tm.get_symbol_frequency(text=text)) / tm.get_number_of_sentences(text=text, replace=replace))

    def get_number_of_filler_words(text: str = None, filler_words: List[str] = ["von", "der", "die", "das", "aber"]):  # gibt die Anzahl der gegebenen Füllwörter zurück
        assert text is not None
        assert len(filler_words) > 0
        return tm.get_word_frequency(text=text, dictionary=filler_words)

    def get_relative_number_of_filler_words(text: str = None, filler_words: List[str] = ["von", "der", "die", "das", "aber"]):  # gibt die relative Anzahl der gegebenen Füllwörter zurück
        assert text is not None
        assert len(filler_words) > 0
        return tm.get_relative_word_frequency(text=text, dictionary=filler_words)

    def get_sentence_length(text: str = None, replace: bool = False):  # gibt array mit allen satzlängen zurück
        assert text is not None
        return [len(i) for i in tm.split_in_sentences(text=text, replace=replace)]

    def get_relative_sentence_length(text: str = None, replace: bool = False):  # gibt satzlänge relativ zur satzanzahl zurück
        assert text is not None
        return sum(tm.get_sentence_length(text=text, replace=replace)) / tm.get_number_of_sentences(text=text,
                                                                                                    replace=replace)

    def get_average_number_of_syllables_per_word(text: str = None):  # gibt durchschnittliche silbenanzahl pro wort zurück
        assert text is not None
        words = tm.split_in_words(text=text)
        return sum([len(hyphenator.hyphenate_word(w)) for w in words]) / len(words)

    def get_word_varianz(text: str = None):  # gibt die anzahl verwendeter wörter zurück (Wortvarianz)
        assert text is not None
        return len(tm.generate_dictionary(text=text))

    def get_word_varianz2(text: str = None):  # gibt die Wortvarianz gewichtet auf die textlänge zurück
        assert text is not None
        return 1 / ((1 / tm.get_word_varianz(text=text)) * len(tm.split_in_words(text=text)))

    def get_flesch_reading_ease(text: str = None):  # gibt den Flesch reading ease zurück
        assert text is not None
        return 206.835 - (84.6 * tm.get_average_number_of_syllables_per_word(text=text)) - (
                    1.015 * tm.get_average_words_per_sentence(text=text, replace=True))

    def get_number_of_short_words(text: str = None):  # gibt die anzahl kurzer wörter zurück
        assert text is not None
        return sum([1 for i in tm.split_in_words(text=text) if len(i) < 4])

    def get_number_of_short_words2(text: str = None):  # gibt die anzahl kurzer wörter gewichtet auf textlänge zurück
        assert text is not None
        return tm.get_number_of_short_words(text=text) / len(tm.split_in_words(text=text))

    def contain_number(text: str = None):  # gibt zurück ob ein text zahlen beinhaltet
        assert text is not None
        return any(i.isdigit() for i in text)

    def get_language(text: str = None):  # gibt die sprache eines textes zurück
        assert text is not None
        languages = ['af', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et', 'fa', 'fi', 'fr',
                     'gu', 'he',
                     'hi', 'hr', 'hu', 'id', 'it', 'ja', 'kn', 'ko', 'lt', 'lv', 'mk', 'ml', 'mr', 'ne', 'nl', 'no',
                     'pa', 'pl',
                     'pt', 'ro', 'ru', 'sk', 'sl', 'so', 'sq', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'uk', 'ur',
                     'vi', 'zh-cn', 'zh-tw']
        return languages.index(detect(text))

    def get_language2(text: str = None, lang: int = 10):  # gibt wahrscheinlichkeit wieder dass wort bestimmter sprache angehörig ist
        t = tm.split_in_sentences(text=text, replace=True)
        l = [[tm.get_language(w) for w in t].count(i) for i in range(55)]
        return l[lang] / len(t)

    def get_topic(text: str = None):  # gibt das topic eines textes zurück (zukünftig)
        assert text is not None
        # robjects.r('''
        # library(topicmodels)
        # ap_lda =
        # ''')

    def lemmatize(text: str = None):
        pass


if __name__ == "__main__":
    pass
