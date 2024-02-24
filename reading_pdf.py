import os
import fitz  # PyMuPDF

def check_deeplabcut_citation(pdf_path):
    """
    Check if the text of a PDF document contains the term "DeepLabCut".

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        bool: True if "DeepLabCut" is mentioned in the text, False otherwise.
    """   
    pdf_document = fitz.open(pdf_path)

    full_text = "" 
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        full_text += page.get_text()
    
    pdf_document.close()

    deeplabcut_cited = "DeepLabCut" in full_text
    return deeplabcut_cited

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
