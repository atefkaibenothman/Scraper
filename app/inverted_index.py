# inverted_index.py
# Atef Kai Benothman

import re
import os
import json
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from bs4.element import Comment

# TODO:  Words in bold, in headings (h1, h2, h3), and in titles should be 
#        treated as more important than the other words.

total_docs = 0
doc_id = 1
index = dict()
doc_list = dict()

# def add_to_index(stemmed_text, doc_id):
#     for term in set(stemmed_text):
#         if term not in index:
#             index[term] = [doc_id]
#         else:
#             index[term].append(doc_id)

# Stems the block of text into a list
def stem_text(text):
    stemmer = PorterStemmer()
    text = re.findall('[a-zA-Z0-9_]+', text.lower(), re.ASCII)
    # Uses a porter stemmer to stem words
    stemmed_text = [stemmer.stem(i) for i in text]
    return stemmed_text


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
    global doc_id
    with open(file_path) as json_file:
        data = json.load(json_file)
        content = data["content"]
        print("URL: ", data["url"])
        print("-------------------------------------")

        doc_list[doc_id] = data["url"]

        soup = BeautifulSoup(content, features="html.parser")
        all_text = soup.findAll(text=True)
        visible_texts = filter(get_text, all_text)
        text = u" ".join(t.strip() for t in visible_texts)
        
        # Step 1. Porter Stem
        stemmed_text = stem_text(text)
        # Step 2. Create Map
        # add_to_index(stemmed_text, doc_id)
        # doc_id += 1

        for term in stemmed_text:
            if term not in index:
                index[term] = [doc_id]
            else:
                index[term].append(doc_id)

        doc_id += 1


# Iterates through all json files in directory
def iterate_all_files(root_dir):
    for dirName, subdirList, fileList in os.walk(root_dir):
        # if dirName == "DEV 2/aiclub_ics_uci_edu": # CHANGE THIS
            print()
            print("dirName: ", dirName)
            print("fileList: ", len(fileList))
            print("=====================================")
            for i in range(len(fileList)):
                file_path = dirName + "/" + fileList[i]
                print("-------------------------------------")
                global total_docs
                total_docs += 1
                print("total docs:", total_docs)
                print(i, file_path)
                extract_text(file_path)
                print()
            print()

            print(doc_list)
            for k,v in sorted(index.items(),key=lambda x: x[0]):
                print(k,":",len(set(v)),"->",sorted(list(set(v))))

    # for k,v in index.items():
    #         print(k,v)

def sort_by_terms():
    
    for k,v in sorted(index.items(),key=lambda x: x[0]):
        print(k,":",len(set(v)),"->",list(set(v)))

if __name__ == "__main__":
    root_directory = "DEV 2"
    iterate_all_files(root_directory)
    sort_by_terms()