import os
import fitz  

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
        if len(toc) == 0:
            print("No table of contents found, reading full document.")
            full_text = pdf_document.load_page(0).get_text("text")  # Read first page for initial check
            for page_num in range(1, len(pdf_document)):  # Loop through remaining pages
                page_text = pdf_document.load_page(page_num).get_text("text")
                full_text += "\n" + page_text
        else:
            print("Table of contents found.")
            for section in sections_for_checking:
                for toc_entry in toc:
                    if section in toc_entry:
                        page_num = toc_entry[2]+1
                        page_text = pdf_document.load_page(page_num).get_text("text")
                        full_text += "\n" + page_text

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