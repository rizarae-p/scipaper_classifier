import rispy
from bs4 import BeautifulSoup
import spacy
from spacy.matcher import PhraseMatcher
from collections import Counter

def clean_html(raw_html):
    """
    Clean HTML content and extract plain text.

    Args:
        raw_html (str): The raw HTML content to be cleaned.

    Returns:
        str: The plain text extracted from the HTML content.
    """
    soup = BeautifulSoup(raw_html, "html.parser")
    cleantext = soup.get_text()
    return cleantext

def tokenize_and_match(text):
    """
    Tokenize and match specific phrases in the input text using spaCy.

    Args:
        text (str): The text in which phrases will be matched.

    Returns:
        list of str: A list of matched phrases found in the input text.
    """    
    nlp = spacy.load('en_core_web_sm')
    matcher = PhraseMatcher(nlp.vocab)

    with open("classes", "r") as file:
        animals = [line.strip() for line in file]

    patterns = [nlp(animal) for animal in animals]
    matcher.add("ANIMAL", patterns)
    doc = nlp(text)
    matches = matcher(doc)

    matched_texts = []
    for match_id, start, end in matches:
        span = doc[start:end]
        matched_texts.append(span.text)
    
    return matched_texts


def count_keywords(file_name='madlc_citations.ris', exclude_others=True, include_titles=False):
    """
    Count occurrences of keywords in the titles and abstracts of RIS entries.

    Args:
        file_name (str, optional): The name of the RIS file to process.
        exclude_others (bool, optional): If True, exclude the "others" category from the results. Default False. 
            Some papers cite deeplabcut in discussion but don't use it as methods, then classified as "others". 
        include_titles (bool, optional): If True, include titles in the output, otherwise only include counts.
            Default False. This option is interesting if you want to check specifically which items are counted in which 
            in each category.

    Returns:
        dict: A dictionary where keys are keywords, and values are dictionaries with counts and lists of titles.
    """
    entries = []
    with open(file_name, 'r', encoding='utf-8') as file:
        entries = list(rispy.load(file))

    entries = [dict(i) for i in entries]
    keys = {}

    for entry in entries:
        title = clean_html(entry['title'])
        abstract = clean_html(entry['abstract'])
        keywords = Counter(set(tokenize_and_match(title)))

        if len(keywords) < 1:
            keywords = Counter(tokenize_and_match(abstract))
            if len(keywords) < 1:
                top_keyword = 'others'
            else:
                top_keyword = sorted(keywords, key=lambda x: (-keywords[x], x))[0]
        else:
            top_keyword = sorted(keywords, key=lambda x: (-keywords[x], x))[0]

        if top_keyword != 'others' or not exclude_others:
            if top_keyword not in keys:
                if include_titles:
                    keys[top_keyword] = {'count': 1, 'titles': [entry['title']]}
                else:
                    keys[top_keyword] = {'count': 1}  # Initialize as a dictionary
            else:
                keys[top_keyword]['count'] += 1
                if include_titles:
                    if 'titles' not in keys[top_keyword]:
                        keys[top_keyword]['titles'] = []
                    keys[top_keyword]['titles'].append(entry['title'])

    total_entries = len(entries) 
    print(f"Total number of entries in the RIS file: {total_entries}")

    return keys