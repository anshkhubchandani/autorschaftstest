from vorverarbeitung import read_file, preprocessing
from textanalyse import (
    count_words,
    count_unique_words,
    words_per_sentence,
    get_word_lengths
)

text = read_file("texte/autor1.txt")
filtered_text = preprocessing(text)

print(f"Originaler Text:\n{text}\n")

print(f"Anzahl Wörter: {count_words(filtered_text)}")
print(f"Einzigartige Wörter: {count_unique_words(filtered_text)}")
print(f"Wörter pro Satz: {words_per_sentence(filtered_text)}")
print(f"Wortlängen: {get_word_lengths(filtered_text)}")