import sys
import string
import re

#Einlesen
def read_file(path):
    inputfile= open(path ,'r')
    content = inputfile.read()
    inputfile.close()
    print(content)
    return content

print("\nOriginaltext: ")
text = read_file("texte/autor1.txt")

# Vorverarbeitung
def preprocessing(text):

    text_clean = text.replace('--', '')
    
    text_clean = text_clean.replace('\n', ' ')
    
    text_clean = " ".join(text_clean.split())
    
    return text_clean

filtered_text = preprocessing(text)

# Zählen der Wörter insgesamt
def count_words(text):
    words_list = text.split()
    counts = len(words_list)
    return counts

number_of_words = count_words(filtered_text)
print(f"\nAnzahl der Wörter insgesamt: {number_of_words}")

# Zählen der Wörter die nur einmal im Text vorkommen
def count_unique_words(filtered_text):
    text_lower = filtered_text.lower() # in kleine Buchstaben umwandeln
    filtered_text = text_lower.translate(str.maketrans('', '', string.punctuation)) # Satzzeichen aus Betrachtung ausschließen
    words_list = filtered_text.split()
    
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

number_unique_words = count_unique_words(text)
print(f"Anzahl der einzigartigen Wörter: {number_unique_words}")


# Zählen der Wörter innerhalb eines Satzes
def words_per_sentence(filtered_text):
    text_without_break = filtered_text.replace('\n', ' ')
    
    sentences = re.split(r'[.!?]', text_without_break)
    print(f"Anzahl der Sätze: {len(sentences)}") # Sätze ausgeben lassen

    sentence_lengths = []

    for sentence in sentences:
        filtered_sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        filtered_sentence = sentence.strip()
        if not filtered_sentence:
            continue

        words = filtered_sentence.split()
        number_of_words = len(words)


        valid_words = []
        
        for word in words:
            if word.isalpha():
                valid_words.append(word)

        sentence_lengths.append(len(valid_words))

    return sentence_lengths

number_of_words_in_sentence = words_per_sentence(filtered_text)
print(f"Anzahl der Wörter in Sätzen: {number_of_words_in_sentence}")


# Einzelne Wortlängen bestimmen
def get_word_lengths(filtered_text):
    text_lower = filtered_text.lower()
    filtered_text = text_lower.translate(str.maketrans('', '', string.punctuation))
    
    words_list = filtered_text.split()
    
    word_lengths = []
    for word in words_list:
        word_lengths.append(len(word))
        
    return word_lengths

list_word_lengths = get_word_lengths(filtered_text)
print(f"Wortlängen: {list_word_lengths}")