import os
import fitz  
from parse import tokenize_and_match

def check_deeplabcut_citation(pdf_path):
    """
    Check if the Methodology, Materials and Methods, or Results section of a PDF document contains the term "DeepLabCut".

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        bool: True if "DeepLabCut" is mentioned in the Methodology, Materials and Methods, or Results, False otherwise.
    """
    if "Supplementary" in pdf_path:
        return False
    print(f"Reading {pdf_path}...")
    full_text = ""
    sections_for_checking = ["Methodology","Materials and Methods","Results","Methods"]

    with fitz.open(pdf_path) as pdf_document:
        toc = pdf_document.get_toc()
        if len(toc) == 0 or all(entry[2] == 0 for entry in toc):
            print("No table of contents found, reading full document.")
            full_text = pdf_document.load_page(0).get_text("text")  
            for page_num in range(len(pdf_document)): 
                page_text = pdf_document.load_page(page_num).get_text("text")
                full_text += "\n" + page_text
        else:
            print("Table of contents found.")
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

    deeplabcut_cited = "DeepLabCut" in full_text
    return deeplabcut_cited, full_text

def analyze_papers(directory):
    """
    Analyze the PDF files in a directory to count the number of papers that cite DeepLabCut
    and the number of papers that do not cite DeepLabCut.

    Args:
        directory (str): The path to the directory containing the PDF files.

    Returns:
        tuple: A tuple containing four elements:
            - int: Number of papers citing DeepLabCut.
            - int: Number of papers not mentioning DeepLabCut.
            - dict: A dictionary containing filenames of papers with citations to DeepLabCut.
            - dict: A dictionary containing filenames of papers without citations to DeepLabCut.
    """    
    papers_with_deeplabcut = 0
    papers_without_deeplabcut = 0

    papers_with_deeplabcut_dict = {}
    papers_without_deeplabcut_dict = {}

    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            deeplabcut_cited = check_deeplabcut_citation(file_path)
            if deeplabcut_cited:
                papers_with_deeplabcut += 1
                papers_with_deeplabcut_dict[filename] = file_path
            else:
                papers_without_deeplabcut += 1
                papers_without_deeplabcut_dict[filename] = file_path

    return papers_with_deeplabcut, papers_without_deeplabcut, papers_with_deeplabcut_dict, papers_without_deeplabcut_dict

def extract_text_from_pdf(pdf_path):
    """
    Extract full text from a PDF document.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The full text extracted from the PDF.
    """
    full_text = ""
    print(f"Reading {pdf_path}...")

    with fitz.open(pdf_path) as pdf_document:
        for page_num in range(len(pdf_document)): 
            page_text = pdf_document.load_page(page_num).get_text("text")
            full_text += "\n" + page_text

    return full_text

def get_animals_from_papers(paper_paths):
    """
    Extract a list of animals used in each paper that cites DeepLabCut.

    Args:
        paper_paths (dict): A dictionary where keys are paper titles and values are paths to the papers.

    Returns:
        dict: A dictionary where keys are paper titles and values are lists of animals used in each paper.
    """
    animals_in_papers = {}

    for title, pdf_path in paper_paths.items():
        print(f"Processing {pdf_path}...")
        full_text = extract_text_from_pdf(pdf_path)
        animals = tokenize_and_match(full_text)
        animals_in_papers[title] = animals
    
    return animals_in_papers


# start = False 
    # for page_num in range(1,len(pdf_document)):
    #     page = pdf_document[page_num]
    #     page_text = page.get_text("blocks")
    #     for idx,m in enumerate(page_text):
    #         print(idx,m)
    #     break
        # for col in page_text:
        #     print(col[0])
        #     if not(issubclass(type(col), str)):
        #         continue
        #     else:
        #         print(col)
        #         for section in sections_for_checking:
        #             if f"{section}\n" in col:
        #                 full_text+=col
    #             text_after = page_text.split(f"\n{section}\n")
    #             start = True
    #             full_text += text_after[1]
    #         if start:
    #             full_text += page_text
    #         if "Conclusion" in page_text:
    #             start = False
    # print(full_text)



import os
import fitz
from parse import tokenize_and_match

def extract_section_text(pdf_path, section_name):
    """
    Extract text from a specified section of a PDF document.

    Args:
        pdf_path (str): The path to the PDF file.
        section_name (str): The name of the section to extract.

    Returns:
        str: The extracted text from the specified section.
    """
    full_text = ""
    with fitz.open(pdf_path) as pdf_document:
        toc = pdf_document.get_toc()
        if len(toc) == 0 or all(entry[2] == 0 for entry in toc):
            print("No table of contents found, reading full document.")
            for page_num in range(len(pdf_document)): 
                page_text = pdf_document.load_page(page_num).get_text("text")
                full_text += "\n" + page_text
        else:
            print("Table of contents found.")
            sections = {}
            current_section = None
            for toc_entry in toc:
                level, title, page_num = toc_entry
                page_num -= 1
                if page_num < 0: 
                    continue
                if section_name in title:
                    if current_section is not None:
                        sections[current_section]['end'] = page_num
                    current_section = section_name
                    sections[current_section] = {'start': page_num, 'end': None}
                elif current_section is not None:
                    sections[current_section]['end'] = page_num
                    current_section = None
            if current_section is not None:
                sections[current_section]['end'] = len(pdf_document)
            
            if section_name in sections:
                start, end = sections[section_name]['start'], sections[section_name]['end']
                for page_num in range(start, end):
                    page_text = pdf_document.load_page(page_num).get_text("text")
                    full_text += "\n" + page_text

    return full_text

def get_animals_from_abstract(pdf_path):
    """
    Extract a list of animals mentioned in the Abstract section of a PDF document.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        list: A list of animals mentioned in the Abstract section.
    """
    abstract_text = extract_section_text(pdf_path, "Abstract")
    animals = tokenize_and_match(abstract_text)
    return animals

def analyze_papers_from_abstracts(papers_with_deeplabcut_dict):
    """
    Analyze the PDF files that cite DeepLabCut to extract and count mentions of animals in the Abstract section.

    Args:
        papers_with_deeplabcut_dict (dict): A dictionary containing filenames of papers with citations to DeepLabCut.

    Returns:
        dict: A dictionary where keys are paper titles and values are lists of animals mentioned in each paper.
    """
    animals_in_papers = {}

    for filename, file_path in papers_with_deeplabcut_dict.items():
        print(f"Processing {file_path}...")
        animals = get_animals_from_abstract(file_path)
        animals_in_papers[filename] = animals

    return animals_in_papers
