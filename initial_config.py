import nltk

def run_config():
    nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger_eng')
    nltk.download('words')
    nltk.download('maxent_ne_chunker_tab')
    nltk.download('vader_lexicon')

    with open("initial.txt", "w") as file:
        file.write("Done!")
