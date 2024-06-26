import os
import fitz  
import pickle
import spacy
from spacy.matcher import PhraseMatcher
from collections import Counter


WATCHLIST = ["rodent","pupa"]

def tokenize_and_match(text,matcher,nlp):
    """
    Tokenize and match specific phrases in the input text using spaCy.

    Args:
        text (str): The text in which phrases will be matched.

    Returns:
        list of str: A list of matched phrases found in the input text.
    """    

    doc = nlp(text)
    matches = matcher(doc)

    matched_texts = []
    for match_id, start, end in matches:
        span = doc[start:end]
        matched_texts.append(span.text)
    
    return matched_texts

def get_top_keyword(animals):
    """
      This function identifies the most frequent animal term 
      (excluding terms from a watchlist) from a list of animal mentions.

      Args:
          aanimals (list): A list containing animal mentions extracted from text.

      Returns:
          str: The most frequent animal term (excluding watchlist terms), 
              or False if no animal terms are found.
    """
    #watch_terms = ["egg","python","rodent","pupa","larva","primate","insect","bug"]
    # animals = [a for a in aanimals if a not in watch_terms]

    top_keyword = ""
    if len(animals) > 1:
        _animals = Counter(animals)
        top_keyword = sorted(_animals, key=lambda x: (-_animals[x], x))[0]
    elif len(animals) == 1:
        top_keyword = animals[0]
    else:
        return False
    return top_keyword

def isSupplementary(pdf_path):
    """
      This function checks if the name of a PDF file contains keywords 
      indicating it's a supplementary file.

      Args:
          pdf_path (str): The path to the PDF file.

      Returns:
          bool: True if the filename suggests it's a supplementary file, False otherwise.
    """
    keywords = ["_supplement"]
    for i in keywords:
        if i in pdf_path:
            return True
    return False

def get_top_keyword_from_pdf(pdf_path, matcher,nlp):
    """
      This function analyzes a PDF to find the most frequent animal term 
      (excluding terms from a watchlist) from the relevant sections 
      ("Methodology", "Materials and Methods", "Results", "Methods"). 
      It skips supplementary files.

      Args:
          pdf_path (str): The path to the PDF file.

      Returns:
          str: The most frequent animal term (excluding watchlist terms), 
              or False if no animal terms are found or the file is supplementary.
    """
    # if isSupplementary(pdf_path):
    #     print("Supplementary doc -- skip")
    #     return False
    full_text = ""
    sections_for_checking = ["Abstract", "Methodology","Materials and Methods","Results","Methods", "Materials and Equipment"]

    with fitz.open(pdf_path) as pdf_document:
        toc = pdf_document.get_toc()
        if len(toc) > 0:
            # print("Table of contents found.")
            sections = {}
            current_section = None
            for toc_entry in toc:
                level, title, page_num = toc_entry
                page_num -= 1
                if page_num < 0: 
                    continue
                for section in sections_for_checking:
                    if section in title:
                        if current_section is not None:
                            sections[current_section]['end'] = page_num
                        current_section = section
                        sections[current_section] = {'start': page_num, 'end': None}
                        break
            if current_section is not None:
                sections[current_section]['end'] = len(pdf_document)
            
            for sec_name, pages in sections.items():
                start, end = pages['start'], pages['end']
                for page_num in range(start, end):
                    page_text = pdf_document.load_page(page_num).get_text("text")
                    full_text += "\n" + page_text

        if len(full_text) == 0:
            pdf_length = len(pdf_document)
            if pdf_length > 6:
                mid_page = pdf_length//2
                # print("No table of contents found, reading selected pages 1",",".join([str(a) for a in range(mid_page-2,mid_page+2,1)]))
                full_text = pdf_document.load_page(0).get_text("text") + "\n" + pdf_document.load_page(1).get_text("text")
                for page_num in range(mid_page-2,mid_page+2,1): 
                    if page_num < pdf_length:
                        page_text = pdf_document.load_page(page_num).get_text("text")
                        full_text += "\n" + page_text
            elif pdf_length > 2:
                full_text = pdf_document.load_page(0).get_text("text")
                for page_num in range(1,pdf_length): 
                        page_text = pdf_document.load_page(page_num).get_text("text")
                        full_text += "\n" + page_text
            else:
                print("Skip",pdf_path)
                return False


    animals = tokenize_and_match(full_text, matcher,nlp)
    top_keyword = get_top_keyword(animals)
    # print(pdf_path, top_keyword, animals)

    return top_keyword

def analyze_papers(directory):
    """
      This function analyzes all PDF files in a given directory to identify 
      the most frequent animal term (excluding terms from a watchlist) 
      for each paper. It extracts text from relevant sections 
      ("Methodology", "Materials and Methods", "Results", "Methods") 
      and skips supplementary files.

      Args:
          directory (str): The path to the directory containing PDF files.

      Returns:
          tuple: A tuple containing three elements:
              - total_counter (dict): A dictionary where keys are animal terms 
                  (excluding watchlist terms) and values are their total counts across all papers.
              - tot (int): The total number of animal terms found (excluding watchlist terms).
              - skipped (int): The number of PDF files skipped (e.g., supplementary files).
    """
    tot = 0
    skipped = 0 
    total_counter = {}
    ctr = 1
    nlp = spacy.load('en_core_web_sm')
    # print("English dictionary loaded..")
    matcher = PhraseMatcher(nlp.vocab)

    with open("classes", "r") as file:
        animals = [line.strip() for line in file]

    patterns = [nlp(animal) for animal in animals]
    matcher.add("ANIMAL", patterns)

    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            # print("Reading",ctr,"of",len(os.listdir(directory)))
            file_path = os.path.join(directory, filename)
            _file_path = file_path.replace("papers_full/","").replace("-"," ").replace("_"," ").replace(".pdf","").lower()
            doc = nlp(_file_path)
            title_tokens = matcher(doc)
            matched_texts = []
            for match_id, start, end in title_tokens:
                span = doc[start:end]
                matched_texts.append(span.text)
            top_keyword = get_top_keyword(matched_texts)
            if not(top_keyword):
                top_keyword = get_top_keyword_from_pdf(file_path, matcher,nlp)
            
            if top_keyword not in total_counter.keys():
                total_counter[top_keyword] = 1
                tot+=1
            else:
                total_counter[top_keyword] += 1
                tot+=1
            if not(top_keyword):
                print("No topword",filename)
                skipped+=1
        ctr+=1
    return total_counter,tot,skipped

# def analyze_pickle(filename):
#     skipped = 0
#     total_counter = {}
#     tot = 0
    

#     with open(filename, "rb") as f:
#       loaded_object = pickle.load(f)

#     for paper_title in loaded_object.keys():
#       aanimals = loaded_object[paper_title]
#       top_keyword = get_top_keyword(aanimals)

#       if top_keyword:
#         if top_keyword not in total_counter.keys():
#             total_counter[top_keyword] = 1
#             tot+=1
#         else:
#             total_counter[top_keyword] += 1
#             tot+=1
#       else:
#         skipped+=1

#       if top_keyword in WATCHLIST:
#         print(top_keyword, animals, paper_title)

#     return total_counter,tot,skipped

