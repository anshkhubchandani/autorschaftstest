""" Funktionen 
* DWL = durchschnittliche Wortlänge
* TTR = Anzahl verschiedener Wörter / Anzahl aller Wörter
* HLR = Anzahl Wörter, die genau einmal vorkommen / Anzahl aller Wörter
* DSL = durchschnittliche Wörter pro Satz
* DSS = durchschnittliche Satzteile pro Satz
"""

def get_words(text):
    """
    Bereitet den Text für die Wortanalyse vor
    und gibt alle Wörter als Liste zurück.
    """
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
    """ Gibt die Anzahl aller Wörter im Text zurück."""
    words_list = get_words(text)
    return len(words_list)

def count_different_words(text):
    """
    Gibt die Anzahl verschiedener Wörter im Text zurück.
    """
    words_list = get_words(text)
    different_words = []

    for word in words_list:
        if word not in different_words:
            different_words.append(word)
    return len(different_words)

def count_unique_words(text):
    """
    Gibt die Anzahl der Wörter zurück, die genau einmal
    im Text vorkommen.
    Dieser Wert wird für die HLR benötigt.
    """

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
    """
    Berechnet die durchschnittliche Wortlänge (DWL).
    """
    words_list = get_words(text)
    total_length = 0 

    for word in words_list:
        total_length += len(word)

    return total_length / len(words_list)

def ttr(text):
    """
    Berechnet die Type-Token-Ratio (TTR).
    TTR = verschiedene Wörter / alle Wörter
    """

    all_words = count_words(text)
    different_words = count_different_words(text)
    return different_words / all_words

def hlr(text):
    """
    Berechnet die Hapax-Legomena-Ratio (HLR).
    HLR = einmal vorkommende Wörter / alle Wörter
    """

    all_words = count_words(text)
    unique_words = count_unique_words(text)
    return unique_words / all_words

def get_sentences(text):
    """
    Teilt einen Text anhand von Punkt, Ausrufezeichen
    und Fragezeichen in Sätze auf.
    """
    text = text.replace("!", ".")
    text = text.replace("?", ".")
    sentences = text.split(".")
    valid_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()
        if sentence != "":
            valid_sentences.append(sentence)

    return valid_sentences


def words_per_sentence(text):
    """
    Berechnet die durchschnittliche Anzahl
    der Wörter pro Satz (DSL).
    Zuerst werden die Sätze bestimmt. 
    Dann werden die Wörter jedes Satzes gezählt.
    zB: Wenn ein Text zwei Sätze mit 5 und 7 Wörtern hat: 
    DSL = (5 + 7) / 2 = 6
    """

    sentences = get_sentences(text)
    total_words = 0 

    for sentence in sentences:
        total_words += count_words(sentence)
    return total_words / len(sentences)


def parts_per_sentence(text):
    """
    Berechnet die durchschnittliche Anzahl
    der Satzteile pro Satz (DSS).
    Komma, Doppelpunkt und Semikolon trennen Satzteile.
    """
    sentences = get_sentences(text)
    total_parts = 0

    for sentence in sentences:
        parts = 1
        parts += sentence.count(",")
        parts += sentence.count(";")
        parts += sentence.count(":")
        total_parts += parts

    return total_parts / len(sentences)


def get_signature(text):
    """
    Berechnet die Signatur eines Textes.
    Reihenfolge:
        0: DWL
        1: TTR
        2: HLR
        3: DSL
        4: DSS

    Parameter:
        text: vorverarbeiteter Text

    Rückgabe:
        Liste mit fünf Kennzahlen

    """

    signature = [
        average_word_length(text),
        ttr(text),
        hlr(text),
        words_per_sentence(text),
        parts_per_sentence(text)
    ]
    return signature