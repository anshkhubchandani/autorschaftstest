import string
import re


# Zählen der Wörter insgesamt
def count_words(text):
    words_list = text.split()
    counts = len(words_list)
    return counts

# Zählen der Wörter die nur einmal im Text vorkommen
def count_unique_words(text):
    text_lower = text.lower() # in kleine Buchstaben umwandeln
    #text = text_lower.translate(str.maketrans('', '', string.punctuation)) # Satzzeichen aus Betrachtung ausschließen
    words_list = text_lower.split()
    
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


# Zählen der Wörter innerhalb eines Satzes
def words_per_sentence(text):
    text_without_break = text.replace('\n', ' ')
    
    sentences = re.split(r'[.!?]', text_without_break)

    # Korrekte Sätze herausfiltern
    valid_sentences = []

    for sentence in sentences:
        if sentence.strip() != "":
            valid_sentences.append(sentence)

    print(f"Anzahl der Sätze: {len(valid_sentences)}")
    
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


# Einzelne Wortlängen bestimmen
def get_word_lengths(text):
    text_lower = text.lower()
    #text = text_lower.translate(str.maketrans('', '', string.punctuation))
    
    words_list = text.split()
    
    word_lengths = []
    for word in words_list:
        word_lengths.append(len(word))
        
    return word_lengths
