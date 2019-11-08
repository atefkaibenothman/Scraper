# inverted_index.py
# Atef Kai Benothman

import re
import os
import ast
import json
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from bs4.element import Comment

# TODO:  Words in bold, in headings (h1, h2, h3), and in titles should be 
#        treated as more important than the other words.

# Globals
total_docs = 0
doc_id = 1
index = dict()
doc_list = dict()


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

# Returns the STEMMED text
def get_valid_text(content):
    soup = BeautifulSoup(content, features="html.parser")
    all_text = soup.findAll(text=True)
    visible_texts = filter(get_text, all_text)
    text = u" ".join(t.strip() for t in visible_texts)
    stemmed_text = stem_text(text)
    return stemmed_text

# write to index
def write_to_index_file():
    global index
    with open("index_raw.txt", "a") as f:
        for k,v in index.items():
            f.write(str(k)+" -> "+str(v)+"\n")
        #f.write(str(index)+"\n\n")

def add_to_index_with_text(stemmed_text):
    # For each term, if it is not in the index add it to the index with value 1
    # It it is in the index, add 1 to the value
    global index
    for term in stemmed_text:
        if term not in index:
            index[term] = {doc_id:1}
        else:
            if doc_id not in index[term].keys():
                index[term][doc_id] = 1
            else:
                index[term][doc_id] += 1

    # Check if the length of the index exceeds 1500
    # If it does, write the index to file and clear it
    if len(index.keys()) >= 10000:
        print("writing")
        write_to_index_file()
        # print("merging")
        # merge_index()
        index = dict()

def merge_index():
    with open("index.txt", "r") as f:
        x = f.read().splitlines()
        res = ast.literal_eval(x)
        
        # for k,v in sorted(res.items(),key=lambda x: x[0]):
        #     print(k,"->",v)

        test_dict = dict()
        for k,v in res.items():
            if k not in test_dict:
                test_dict[k] = v
            else:
                test_dict[k].update(v)

    print("MERGED")
    with open("index_raw.txt", "a") as f:
        for k,v in test_dict.items():
            f.write(str(k)+" -> "+str(v)+"\n")

    test_dict = dict()

# Writes the mapping in doc_list to file and clears the mapping
def write_to_doc_file():
    global doc_list
    with open("docs.txt", "a") as f:
        for k,v in doc_list.items():
            f.write(str(k) + " -> " + str(v) + "\n")
    doc_list = dict()

# Retuns all valid text from HTML
def extract_text(file_path):
    global doc_id
    global doc_list
    global index

    with open(file_path) as json_file:
        data = json.load(json_file)
        content = data["content"]
        url = data["url"]

        print("URL: ", url)
        print("-------------------------------------")

        # When the size of doc_list equals 100, write to file
        if len(doc_list) >= 1000:
            write_to_doc_file()
        # Add to doc list
        doc_list[doc_id] = url

        # Get all text from document and stem it
        stemmed_text = get_valid_text(content)
        
        # Add stemmed text to index
        add_to_index_with_text(stemmed_text)

        # Add 1 to the total doc count
        doc_id += 1


# Iterates through all json files in directory
def iterate_all_files(root_dir):
    global total_docs
    global index
    global doc_list
    test_files = ["DEV 2/cyberclub_ics_uci_edu", "DEV 2/cloudberry_ics_uci_edu"]
    for dirName, subdirList, fileList in os.walk(root_dir):
        # if dirName in test_files: # COMMENT THIS WHEN DOING REAL TEST
            print("DIRECTORY NAME: ", dirName)
            print("NUM FILES IN DIRECTORY: ", len(fileList))
            print("=====================================")

            # Iterate through all files in directory
            for i in range(len(fileList)):
                total_docs += 1
                file_path = dirName + "/" + fileList[i]
                print("-------------------------------------")
                print(i, file_path)
                print("TOTAL NUM FILES: ", total_docs)
                print("LEN OF DOC LIST: ", len(doc_list))
                print("LEN OF INDEX: ", len(index))
                
                extract_text(file_path)

                print()


# Checks to see if the report files are already included
def check_for_text_files():
    try:
        os.remove("docs.txt")
        os.remove("index_raw.txt")
        print("successfully removed 'docs.txt' and 'index.txt")
    except:
        pass

if __name__ == "__main__":
    check_for_text_files()

    root_directory = "DEV 2"
    iterate_all_files(root_directory)

    # Add data to documents
    write_to_index_file()
    # merge_index()
    write_to_doc_file()
    
    