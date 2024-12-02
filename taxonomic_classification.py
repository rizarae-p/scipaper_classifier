import parse
import pandas as pd
from Bio import Entrez
from Bio.Entrez import HTTPError

Entrez.email = 'teruel.anna@gmail.com'

def common_to_scientific_names(common_names):
    scientific_names = []
    
    for common_name in common_names:
        try:
            handle = Entrez.esearch(db="taxonomy", term=f"{common_name}[Common Name]")
            record = Entrez.read(handle)
            handle.close()

            if record["Count"] == "0":
                scientific_names.append(None)
            else:
                taxid = record["IdList"][0]
                handle = Entrez.efetch(db="taxonomy", id=taxid, retmode="xml")
                records = Entrez.read(handle)
                handle.close()
                scientific_name = records[0]["ScientificName"]
                scientific_names.append(scientific_name)
        except Exception as e:
            print(f"An error occurred for '{common_name}': {str(e)}")
            scientific_names.append(None)
    
    return scientific_names

def classify_animal(animal_list, api_key):
    Entrez.api_key = api_key
    results = []
    for animal in animal_list:
        try:
            handle = Entrez.esearch(db="taxonomy", term=animal)
            record = Entrez.read(handle)
            taxid = record["IdList"][0]
            handle = Entrez.efetch(db="taxonomy", id=taxid, retmode="xml")
            records = Entrez.read(handle)
            taxonomy_data = records[0]
            results.append(taxonomy_data)
        except HTTPError as e:
            print(f"HTTPError for '{animal}': {e}")
            results.append(None) 
    
    df = pd.DataFrame(results)
    return df

if __name__ == "__main__":
    animal_counts = {'mouse': 651, 'rat': 148, 'fly': 50, 'ant': 24, 'macaque': 18, 'dolphin': 2, 'bird': 29, 'fish': 72, 
                     'rabbit': 10, 'pig': 17, 'dog': 19, 'cobra': 1, 'monkey': 37, 'insect': 23, 'bug': 3, 'beetle': 4, 'rodent': 30, 
                     'primate': 30, 'snake': 2, 'elephant': 3, 'turkey': 1, 'cricket': 6, 'spider': 5, 'worm': 11, 'zebra': 8, 
                     'salamander': 1, 'larva': 13, 'frog': 1, 'jellyfish': 1, 'cat': 17, 'bat': 8, 'cheetah': 4, 'octopus': 4, 
                     'chimpanzee': 5, 'bee': 11, 'cow': 6, 'mosquito': 3, 'hamster': 1, 'squirrel': 2, 'gecko': 6, 'lizard': 4, 
                     'zooplankton': 1, 'chicken': 8, 'eel': 1, 'goat': 3, 'tiger': 2, 'moth': 2, 'hedgehog': 1, 'wolf': 1, 'shrimp': 2, 
                     'otter': 1, 'pupa': 1, 'cockroach': 2, 'sheep': 2, 'horse': 11, 'caterpillar': 1, 'bear': 7, 'baboon': 1, 'mite': 1, 
                     'duck': 1, 'crab': 2, 'cuttlefish': 1, 'sloth': 1, 'goose': 1, 'butterfly': 1, 'camel': 1, 'sea urchin': 1, 'caribou': 1, 
                     'flea': 1, 'snail': 1, 'alligator': 1, 'crocodile': 1, 'termite': 1, 'wasp': 1}

    common_names = list(animal_counts.keys())
    scientific_names = common_to_scientific_names(common_names)

    api_key = 'YOUR_NCBI_API_KEY'  # Replace with your NCBI API key
    classification_df = classify_animal(scientific_names, api_key)

    # Now you can group and sort the results by taxonomic group
    if not classification_df.empty:
        classification_df['CommonName'] = common_names  # Add the common names for reference
        classification_df['Count'] = classification_df['CommonName'].map(animal_counts)  # Add counts

        # Group by taxonomic class, family, order, etc.
        grouped = classification_df.groupby('Class')
        sorted_results = grouped.apply(lambda x: x.sort_values(by='Count', ascending=False))

        print(sorted_results)