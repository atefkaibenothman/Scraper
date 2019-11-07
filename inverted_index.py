# inverted_index.py
# Atef Kai Benothman

import os
import json
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from bs4.element import Comment

# Stems the block of text into a list
def stem_text(text):
    stemmer = PorterStemmer()
    text = text.split()
    # Uses a porter stemmer to stem words
    stemmed_text = [stemmer.stem(i) for i in text]

    for i in range(len(text)):
        print(i, text[i], "->", stemmed_text[i])



# Returns the validatity of an element. If it is valid, return True. Else, return False.
def get_text(element):
    black_list = ["[document]","noscript", "header", "html", "meta", "head", "input", "script", "style"]
    if element.parent.name in black_list:
        return False
    if isinstance(element, Comment):
        return False
    return True

# Retuns all valid text from HTML
def extract_text(file_path):
    print("FILE PATH: ", file_path)
    with open(file_path) as json_file:
        data = json.load(json_file)
        content = data["content"]
        print("URL: ", data["url"])

        soup = BeautifulSoup(content, features="html.parser")
        all_text = soup.findAll(text=True)
        visible_texts = filter(get_text, all_text)
        text = u" ".join(t.strip() for t in visible_texts)
        
        stem_text(text)


# Iterates through all json files in directory
def iterate_all_files(root_dir):
    for dirName, subdirList, fileList in os.walk(root_dir):
        if dirName == "DEV 2/today_uci_edu": # CHANGE THIS
            print()
            print("dirName: ", dirName)
            print("fileList: ", len(fileList))
            print("=====================================")
            for i in range(len(fileList)):
                file_path = dirName + "/" + fileList[i]
                print(i, file_path)
                extract_text(file_path)
                print()
            print()


if __name__ == "__main__":
    root_directory = "DEV 2"
    iterate_all_files(root_directory)