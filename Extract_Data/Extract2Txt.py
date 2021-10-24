#! /usr/bin/env python3

import os
import pytesseract
from pdf2image import convert_from_path 
import fitz


## PDF Miner runs on all files. Check shell script to modify directories
def pdfminer_pass():
    '''
    PDF Miner.Six first pass; Calls bash script; requires it be executable (chmod +x pdfmine.sh)
    '''
    os.system('./pdfmine.sh')
    return

## PyMuPdf to convert pdf files to txt files
def pymupdf_pass(path,out_path):
    '''
    Runs PyMuPdf to convert all pdfs to txt files
    '''
    for file in os.listdir(path):
        pymupdf_one(path+file,out_path)
    print(len(os.listdir(path)))
    return

def pymupdf_one(filename,out_path):
    '''
    Runs PyMuPdf to conver one pdf to a txt file
    '''
    doc = fitz.open(filename)
    text = ''
    for page in doc:
        text += page.get_text('text')
    file1 = open(out_path+os.path.splitext(os.path.basename(filename))[0]+".txt","w")	
    file1.writelines(text)
    file1.close()
    return


## Tesseract OCR to convert pdfs that are scanned images to txt files
def tesseract_pass(path,out_path,out_path1):
    ''' 
    Runs Tesseract OCR on all pdfs that did not get parsed by PyMuPdf.
    (Determined by check function))
    '''
    list_of_img_pdfs = check(out_path,500)
    for file in list_of_img_pdfs:
        tesseract_one(path+os.path.splitext(file)[0]+".pdf",out_path1)
        print(file)
        os.remove(out_path+file)
    return

def tesseract_one(file,out_path):
    '''
    Runs Tesseract OCR on one pdf img file
    '''
    out = convert_from_path(file,500)
    raw_text = ''
    for o in out:
        raw_text += str(pytesseract.image_to_string(o))
    file1= open(out_path+os.path.splitext(os.path.basename(file))[0]+".txt","w")
    file1.writelines(raw_text)
    file1.close()
    return

def check(path,thresh=500):
    '''
    Determine which files are did not get extracted by PyMuPdf; Checks
    file size
    '''
    list_of_img_pdfs = []
    for file in os.listdir(path):
        if os.path.getsize(path+file) < thresh:
            list_of_img_pdfs.append(file)
    return list_of_img_pdfs



### Main
def main():
    ## Set path where original Files are
    path = '/home/kbari/git_repo/FinanceErdosProj/Original_Data/' 
    ## Set path to output PyMuPdf text files
    out_path = '/home/kbari/git_repo/FinanceErdosProj/PyMuPdf_Text/'
    ## Run PyMuPdf; uncomment to run 
    #pymupdf_pass(path,out_path)
    ## Output for Tesseract Files
    out_path1 = '/home/kbari/git_repo/FinanceErdosProj/Tesseract_Text/'
    ## Run Tesseract on remaining Files; uncomment to run
    tesseract_pass(path,out_path,out_path1)
    return

if __name__ == "__main__":
    main()
