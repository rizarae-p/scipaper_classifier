import rispy
from bs4 import BeautifulSoup

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    cleantext = soup.get_text()
    return cleantext

entries = []
with open('madlc_citations.ris', 'r', encoding='utf-8') as file:
    entries = list(rispy.load(file))

entries = [dict(i) for i in entries]

for entry in entries:
	title = clean_html(entry['title'])
	abstract = clean_html(entry['abstract'])
	print(title,abstract)