from vorverarbeitung import read_file, preprocessing
from autoren import (similarity, get_author_signature, find_best_author)
from textanalyse import ( count_words, count_different_words, count_unique_words, average_word_length, ttr, hlr, words_per_sentence, parts_per_sentence, get_signature)

def main():
    """
    Hauptprogramm des Autorschaftstests.
    Liest einen unbekannten Text ein, berechnet seine Signatur,
    vergleicht ihn mit bekannten Referenztexten und gibt die
    wahrscheinlichste Zuordnung aus.
    """

    test_filename = input("Dateiname im Ordner texte: ")
    test_path = "texte/" + test_filename

    text = read_file(test_path)
    filtered_text = preprocessing(text)
    text_signature = get_signature(filtered_text)

    #Eingabe_text
    print(f"Textanalyse für: {test_filename}")
    print("-----------------------------------")


    print(f"Anzahl Wörter: {count_words(filtered_text)}")#
    print(f"Anzahl verschiedene Wörter: {count_different_words(filtered_text)}")
    print(f"Einmalvorkommende Wörter: {count_unique_words(filtered_text)}")

    print()
    print(f"DWL: {average_word_length(filtered_text):.2f}")
    print(f"TTR: {ttr(filtered_text):.2f}")
    print(f"HLR: {hlr(filtered_text):.2f}")
    print(f"DSL: {words_per_sentence(filtered_text):.2f}")
    print(f"DSS: {parts_per_sentence(filtered_text):.2f}")
    print(f"Signatur: {text_signature}")


    author_signatures = {}

    author_signatures["Goethe (Italienische Reise)"] = get_author_signature("texte/Goethe-ItalienischeReise1-referenz.txt")
    author_signatures["Goethe (Faust)"] = get_author_signature("texte/faust-referenz.txt")
    author_signatures["Schiller"] = get_author_signature("texte/SchillerBriefe-referenz.txt")
    author_signatures["Eichendorff"] = get_author_signature("texte/Eichendorff-Taugenichts.txt")
    author_signatures["Thomas Mann"] = get_author_signature("texte/Mann-Tonio-Kroeger.txt")
    author_signatures["Wittgenstein"] = get_author_signature("texte/Wittgenstein-Tractatus.txt")
    author_signatures["Busoni"] = get_author_signature("texte/Busoni-Tonkunst.txt")
    

    print()
    print("Signaturen der Autoren")
    print("----------------------")

    for author in author_signatures:
        signature = author_signatures[author]

        print(
            f"{author}: "
            f"DWL={signature[0]:.2f}, "
            f"TTR={signature[1]:.2f}, "
            f"HLR={signature[2]:.2f}, "
            f"DSL={signature[3]:.2f}, "
            f"DSS={signature[4]:.2f}"
        )

    print()
    print("Ähnlichkeitswerte")
    print("------------------")

    for author in author_signatures:
        value = similarity(
            text_signature,
            author_signatures[author]
        )

        print(f"{author}: {value:.2f}")

    best_author, smallest_value = find_best_author(
        text_signature,
        author_signatures
    )

    print()
    print(f"Wahrscheinlichster Autor: {best_author}")
    print(f"Ähnlichkeitswert: {smallest_value:.2f}")

main()