

def read_file(path):
    inputfile= open(path ,'r')
    content = inputfile.read()
    inputfile.close()
    return content

""""
1. Entfernt --
2. Entfernt Zeilenumbrüche -> macht aus zeilenumbrüchen leerzeichen
3. entfernt überflüssige Leerzeichen
"""
def preprocessing(text):
    text = text.replace("--", " ")
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text

# Satzzeichen noch nicht entfernen!! wir brauchen sie später für DSS