import rispy
from bs4 import BeautifulSoup
import spacy
from spacy.matcher import PhraseMatcher
from collections import Counter

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    cleantext = soup.get_text()
    return cleantext

def tokenize_and_match(text):
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

def count_keywords(file_name='madlc_citations.ris'):
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
				continue
		top_keyword = sorted(keywords, key=lambda x: (-keywords[x], x))[0]
		if top_keyword not in keys.keys():
			keys[top_keyword] = 1
		else:
			keys[top_keyword] +=1
	return keys



