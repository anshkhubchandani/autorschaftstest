from vorverarbeitung import read_file, preprocessing
from textanalyse import get_signature

def get_author_signature(filename):
    """
    Berechnet die Signatur eines bekannten Referenztextes.
    Parameter:
        filename: Pfad zur Textdatei
    Rückgabe:
        Liste mit [DWL, TTR, HLR, DSL, DSS]
    """

    text = read_file(filename)
    filtered_text = preprocessing(text)
    signature = get_signature(filtered_text)
    return signature


def similarity(signature_text, signature_author):

    """ 
    Berechnet den gewichteten Ähnlichkeitswert zwischen
    zwei Signaturen.
    Je kleiner der Wert, desto ähnlicher sind die Texte.
    
    Parameter:
        signature_text: Signatur des unbekannten Textes
        signature_author: Signatur eines Referenztextes
    
    Rückgabe:
        Gewichteter Ähnlichkeitswert
    """

    weights = [11, 33, 50, 0.4, 4]
    total = 0
    for i in range(len(weights)):
        difference = abs(signature_text[i] - signature_author[i])
        total += difference * weights[i]

    return total


def find_best_author(text_signature, author_signatures):
    """
    Sucht den Referenztext mit dem kleinsten Ähnlichkeitswert.

    Parameter:
        text_signature:
            Signatur des unbekannten Textes
        author_signatures:
            Dictionary mit Namen und Signaturen
    
    Rückgabe:
        Name der besten Zuordnung und kleinster Ähnlichkeitswert
    """

    best_author = ""
    smallest_value = None

    for author in author_signatures:
        author_signature = author_signatures[author]

        value = similarity(text_signature, author_signature)

        if smallest_value is None or value < smallest_value:
            smallest_value = value
            best_author = author

    return best_author, smallest_value