import rispy
from bs4 import BeautifulSoup
import spacy
from spacy.matcher import PhraseMatcher


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

entries = []
with open('madlc_citations.ris', 'r', encoding='utf-8') as file:
    entries = list(rispy.load(file))

entries = [dict(i) for i in entries]

for entry in entries:
	title = clean_html(entry['title'])
	abstract = clean_html(entry['abstract'])
	print(tokenize_and_match(title))