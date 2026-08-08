from vorverarbeitung import read_file, preprocessing
from textanalyse_mod import (
   count_words,
    count_different_words,
    count_unique_words,
    average_word_length,
    ttr,
    hlr,
    words_per_sentence,
    parts_per_sentence
)
filename = "texte/autor1.txt"
text = read_file(filename)
filtered_text = preprocessing(text)

print(f"Textanalyse für: {filename.split('/')[-1]}")
print("-----------------------------------")


print(f"Anzahl Wörter: {count_words(filtered_text)}")#
print(f"Anzahl verschiedene Wörter: {count_different_words(filtered_text)}")
print(f"Einmalvorkommende Wörter: {count_unique_words(filtered_text)}")

#print(f"Wörter pro Satz: {words_per_sentence(filtered_text)}")
#print(f"Wortlängen: {get_word_lengths(filtered_text)}")

print()

print(f"DWL: {average_word_length(filtered_text)}")
print(f"TTR: {ttr(filtered_text)}")
print(f"HLR: {hlr(filtered_text)}")
print(f"DSL: {words_per_sentence(filtered_text)}")
print(f"DSS: {parts_per_sentence(filtered_text)}")