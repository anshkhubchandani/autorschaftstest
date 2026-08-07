def read_file(path):
    inputfile= open(path ,'r')
    content = inputfile.read()
    inputfile.close()
    return content


def preprocessing(text):
    text = text.replace("--", "")
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text