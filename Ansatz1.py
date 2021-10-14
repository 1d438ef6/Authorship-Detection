class tm:
    def remove_special_characters(text = None):                             #ersetzt Umlaute im Text
        if text == None:
            return -1
        special_character = {"ä", "Ä", "ö", "Ö", "ü", "Ü", "ß"}             #zu ersetzende Umlaute
        replace_with = {"ae", "Ae", "oe", "Oe", "ue", "Ue", "ss"}           #womit die Umlaute ersetzt werden sollen
        if len(special_character) == len(replace_with):                     
            for i in range(len(special_character)):
                text = text.replace(special_character[i],replace_with[i])
        else:
            return -1
        return text
    def split_in_paragraphes(text = None):                                  #teilt den gegebenen Text in Paragraphen
        if text == None:                                                    #wenn kein Text übergeben wurde -> Error 
            return -1
        return text.split('\n\n')
    def split_in_sentences(text = None):                                    #teilt den gegebenen Text in Sätze
        if text == None:                                                    #wenn kein Text übergeben wurde -> Error
            return -1
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
    def get_word_frequency(text = None, dictionary = None):                 #errechnet die Worthäufigkeit eines Textes
        if text == None:
            return -1
        if dictionary == None:
            dictionary = tm.generate_dictionary(text)
        frequency = [0 for i in range(len(dictionary))]
        text.lower()
        words = tm.split_in_words(text)
        for e in words:
            pos = dictionary.index(e)
            frequency[pos] = frequency[pos] + 1
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
    def get_number_of_symbols_in_row(text = None, symbol = ",", symbols = [".","!","?",",","-"]):
        if text == None:
            return -1
        print(text)
        symbol_marker = tm.get_symbols(text, symbols)
        print(symbol_marker)
        nosir = []
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

        
    
text = "test! Words in row. A question? Word and another word and question."
text2 = "more text. more knorke. have to! write some. stupid? words."
print(tm.get_number_of_symbols_in_row(text=text+text2, symbol="."))
#print(tm.generate_dictionary(text))
#print(tm.get_word_frequency(text))
#print(tm.get_relative_word_frequency(text))
#print(tm.get_relevant_syntagmas(text))

