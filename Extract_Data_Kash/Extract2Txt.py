#! /usr/bin/env python3

import os
import pytesseract
from pdf2image import convert_from_path 
import fitz
#import subprocess


## PDF Miner pass
def pdfminer_pass():
    ''' PDF Miner.Six first pass; Calls bash script; requires it be executable (chmod +x pdfmine.sh)'''
    os.system('./pdfmine.sh')
    #subprocess.call(['sh',path+'pdfmine.sh'])
    return

## PyMuPdf Pass
def pymupdf_pass(path,out_path):
    '''PyMyPdf first pass'''
    for file in os.listdir(path):
        #print(file)
        pymupdf_one(path+file,out_path)
    print(len(os.listdir(path)))
    return

def pymupdf_one(filename,out_path):
    doc = fitz.open(filename)
    text = ''
    for page in doc:
        text += page.get_text('text')
    file1 = open(out_path+os.path.splitext(os.path.basename(filename))[0]+".txt","w")	
    file1.writelines(text)
    file1.close()
    return


## Tesseract OCR pass
def tesseract_pass(path,out_path,out_path1):
    ''' Runs Tesseract OCR on list of pdfs '''
    list_of_img_pdfs = check(out_path,500)
    for file in list_of_img_pdfs:
        tesseract_one(path+os.path.splitext(file)[0]+".pdf",out_path1)
        print(file)
    return

def tesseract_one(file,out_path):
    out = convert_from_path(file,500)
    raw_text = ''
    for o in out:
        raw_text += str(pytesseract.image_to_string(o))
    file1= open(out_path+os.path.splitext(os.path.basename(file))[0]+".txt","w")
    file1.writelines(raw_text)
    file1.close()
    return

def check(path,thresh=500):
    ''' Determine which files are did not get extracted with previous pass; Checks
    file size'''
    list_of_img_pdfs = []
    for file in os.listdir(path):
        if os.path.getsize(path+file) < thresh:
            list_of_img_pdfs.append(file)
    return list_of_img_pdfs

#file = '2019_july_2_922281564166445297_official-documents-amendment-to-the-loan-agreement-for-loan-8564-ga.pdf'
#out_path = '/home/kbari/git_repo/FinanceErdosProj/Extract_Data_Kash/'
#tesseract_one(file,out_path)

path = '/home/kbari/git_repo/FinanceErdosProj/Original_Data/'
    ## Set path to output PyMuPdf text files
out_path = '/home/kbari/git_repo/FinanceErdosProj/PyMuPdf_Text/'
    ## Run PyMuPdf
    #pymupdf_pass(path,out_path)
    ## Output for Tesseract Files
out_path1 = '/home/kbari/git_repo/FinanceErdosProj/Tesseract_Text/'
    ## Run Tesseract on remaining Files
list_of_img_pdfs = check(out_path)
#tesseract_pass(out_path,out_path1)


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
    tesseract_pass(out_path,out_path1)
    return

if __name__ == "__main__":
    main()
