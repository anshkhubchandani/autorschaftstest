from vorverarbeitung import read_file, preprocessing

""" Functionen 
* DWL = durchschnittliche Wortlänge
* TTR = Anzahl verschiedener Wörter / Anzahl aller Wörter
* HLR = Anzahl Wörter, die genau einmal vorkommen / Anzahl aller Wörter
* DSL = durchschnittliche Wörter pro Satz
* DSS = durchschnittliche Satzteile pro Satz
"""

def get_words(text):
    text = text.lower() 

    text = text.replace(".", " ")
    text = text.replace(",", " ")
    text = text.replace("!", " ")
    text = text.replace("?", " ")
    text = text.replace(":", " ")
    text = text.replace(";", " ")
    text = text.replace("-", " ")
    text = text.replace("(", " ")
    text = text.replace(")", " ")
    text = text.replace("[", " ")
    text = text.replace("]", " ")
    text = text.replace("{", " ")
    text = text.replace("}", " ")
    text = text.replace('"', " ")

    words_list = text.split()
    return words_list


def count_words(text):
    """ Anzahl der Wörter im Text """
    words_list = get_words(text)
    return len(words_list)

def count_different_words(text):
    """ Anzahl der verschiedenen Wörter im Text """
    words_list = get_words(text)
    different_words = []

    for word in words_list:
        if word not in different_words:
            different_words.append(word)
    return len(different_words)


def count_unique_words(text):
    """ Anzahl der Wörter, die genau einmal im Text vorkommen 
        wichtig für HLR (Hapax Legomena Ratio) """
    words_list = get_words(text)
    word_counts = {}

    for word in words_list:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    unique_count = 0
    for word in word_counts:
        if word_counts[word] == 1:
            unique_count += 1

    return unique_count

def average_word_length(text):
    """ Durchschnittliche Wortlänge """
    words_list = get_words(text)
    total_length = 0 

    for word in words_list:
        total_length += len(word)

    return total_length / len(words_list)

def ttr(text):
    """ Type-Token-Ratio (TTR) = Anzahl verschiedener Wörter / Anzahl aller Wörter """
    all_words = count_words(text)
    different_words = count_different_words(text)
    return different_words / all_words

def hlr(text):
    """ Hapax Legomena Ratio (HLR) = Anzahl Wörter, die genau einmal vorkommen / Anzahl aller Wörter """
    all_words = count_words(text)
    unique_words = count_unique_words(text)
    return unique_words / all_words

def get_sentences(text):
    """ Texte in Sätze aufteilen """
    text = text.replace("!", " ")
    text = text.replace("?", " ")
    sentences = text.split(".")
    valid_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()
        if sentence != "":
            valid_sentences.append(sentence)

    return valid_sentences


def words_per_sentence(text):
    """ DSL = durchschnittliche Wörter pro Satz """
    sentences = get_sentences(text)
    total_words = 0 

    for sentence in sentences:
        total_words += count_words(sentence)
    return total_words / len(sentences)


def parts_per_sentence(text):
    """ DSS = durchschnittliche Satzteile pro Satz
        Komma, Doppelpunkt und Semikolon trennen Satzteile """
    sentences = get_sentences(text)
    total_parts = 0

    for sentence in sentences:
        parts = 1
        parts += sentence.count(",")
        parts += sentence.count(";")
        parts += sentence.count(":")
        total_parts += parts

    return total_parts / len(sentences)

