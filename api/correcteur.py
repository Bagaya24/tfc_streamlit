from symspellpy.symspellpy import SymSpell, Verbosity
import pkg_resources
import os

# Initialiser SymSpell avec une distance d'édition max de 2
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

# Charger un dictionnaire préexistant (ici en anglais, mais tu peux en créer un en français)
# Format du fichier : "mot fréquence"
dictionary_path = os.path.join("frequency_dictionary_en_82_765.txt")
if not sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1):
    print("Échec du chargement du dictionnaire.")
    exit()

# Texte à corriger
input_text = "Ths is a smple txt with sme speling erors."

# Séparer les mots et les corriger un à un
corrected_words = []
for word in input_text.split():
    suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
    if suggestions:
        corrected_words.append(suggestions[0].term)
    else:
        corrected_words.append(word)

corrected_text = " ".join(corrected_words)
print("Texte corrigé :", corrected_text)
