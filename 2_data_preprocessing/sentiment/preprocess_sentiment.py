import pandas as pd
import argparse
#sys.path.append('../utils')


import nltk
import contractions
import re


class TextNormalizer:

    def __init__(self):
        nltk.download('words')
        nltk.download('punkt')
        nltk.download('wordnet')
        self.corpus_words = set(nltk.corpus.words.words())
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        self.lemmatizer = nltk.stem.WordNetLemmatizer()

    def normalize(self, text):
        proc_text = " ".join(contractions.fix(w).lower() for w in text.split())
        proc_text = re.sub(r'[^a-zA-Z\s]', '', proc_text)
        proc_text = re.sub("\s\s+", " ", proc_text)
        proc_text = " ".join(self.lemmatizer.lemmatize(w) for w in nltk.word_tokenize(proc_text)
                             if w in self.corpus_words and w not in self.stop_words)
        return proc_text.strip()



parser = argparse.ArgumentParser(description='Preprocesses file with sentiment data given its path')

# arguments
parser.add_argument('file_path', type=str)


def main(file_path):
    df = pd.read_csv(file_path)
    text_normalizer = TextNormalizer()
    df["Text"] = df.Text.map(lambda x: text_normalizer.normalize(x))

    file_path_out = f'{file_path.split(".")[-2]}_processed.csv'
    df.to_csv(file_path_out, index=False)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args.file_path)
