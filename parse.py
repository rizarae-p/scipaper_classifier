import rispy
from bs4 import BeautifulSoup
import spacy
from spacy.matcher import PhraseMatcher


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

entries = []
with open('madlc_citations.ris', 'r', encoding='utf-8') as file:
    entries = list(rispy.load(file))

entries = [dict(i) for i in entries]

for entry in entries:
	title = clean_html(entry['title'])
	abstract = clean_html(entry['abstract'])
	print(tokenize_and_match(title))