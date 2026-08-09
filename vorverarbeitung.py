

def read_file(path):
    """
    Liest den vollständigen Inhalt einer Textdatei ein.
    Parameter:
        path: Pfad zur Datei

    Rückgabe:
        Inhalt der Datei als String
    """

    inputfile= open(path ,"r")
    content = inputfile.read()
    inputfile.close()
    return content


def preprocessing(text):
    """
    Bereitet einen eingelesenen Text für die Analyse vor.
    Zeilenumbrüche und doppelte Bindestriche werden ersetzt
    und überflüssige Leerzeichen entfernt.

    Parameter:
        text: ursprünglicher Text

    Rückgabe:
        bereinigter Text
    """

    text = text.replace("--", " ")
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text

# Satzzeichen nicht entfernen, da sie später
# für die Satztrennung und DSS benötigt werden.