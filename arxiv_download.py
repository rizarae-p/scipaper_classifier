import urllib.request
import feedparser

search_query = 'quantum computing' 
start = 0                          
max_results = 5                    
base_url = 'http://export.arxiv.org/api/query?'

query = f'search_query=all:{search_query}&start={start}&max_results={max_results}'
url = base_url + query

response = urllib.request.urlopen(url)
response_text = response.read()

feed = feedparser.parse(response_text)

for entry in feed.entries:
    pdf_link = [link.href for link in entry.links if link.type == 'application/pdf'][0]
    pdf_title = entry.title.replace(' ', '_')[:50] + '.pdf'  # Simplify title for filename
    print(f'Downloading: {pdf_title}')
    urllib.request.urlretrieve(pdf_link, pdf_title)
    print(f'Successfully downloaded {pdf_title}')

print('Download complete.')
