import parse
import pandas as pd
from Bio import Entrez
from Bio.Entrez import HTTPError

Entrez.email = 'teruel.anna@gmail.com'

def common_to_scientific_names(common_names:list):
    """
    Convert a list of common animal names to their corresponding scientific names.

    Args:
        common_names (list): A list of common animal names.

    Returns:
        list: A list of scientific names corresponding to the input common names.
              If a common name cannot be found, the corresponding entry in the list is set to None.
    """
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

def classify_animal(animal_list:list, api_key:str):
    """
    Classify a list of animals based on their scientific names using the NCBI Taxonomy Database.

    Args:
        animal_list (list): A list of scientific names of animals to be classified.
        api_key (str): A valid API key for access to NCBI services. You need a user in the NCBI server and
                find the API keys in user settings. 

    Returns:
        pd.DataFrame: A DataFrame containing taxonomic data for the given animals retrieved from the NCBI Taxonomy Database.
                     The DataFrame includes information about the animals' classification at various taxonomic levels.
                     If a classification fails for an animal, the corresponding row in the DataFrame will contain None.
    """
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
