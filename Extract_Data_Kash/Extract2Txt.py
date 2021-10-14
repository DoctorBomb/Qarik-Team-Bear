??? from here until ???END lines may have been inserted/deleted
#! /usr/bin/env python3

import os
import pytesseract
from pdf2image import convert_from_path 
import fitz
#import subprocess
#import pandas as pd

## Set path where pdf files are
#path = "/home/kbari/Documents/Erdos/pdfminer_texts/"

## Set output folder for text files
#out_path = "/home/kbari/Documents/Erdos/Text_Data/"

## PDF Miner pass
def pdfminer_pass():
    ''' PDF Miner.Six first pass; Calls bash script; requires it be executable (chmod +x pdfmine.sh)'''
    os.system('./pdfmine.sh')
    #subprocess.call(['sh',path+'pdfmine.sh'])
    return

## PyMuPdf Pass
def pymupdf_pass(path,out_path):
    '''PyMyPdf first pass'''
	for file in path:
		pdfmupdf_one(file,out_path)
	return

def pymupdf_one(file,out_path):
	doc = fitz.open(filename)
	file1= open(out_path+os.path.splitext(os.path.basename(filename))[0]+".txt","w")
	text = ''
	for page in doc:
		text += page.get_text('text')
	file1.writelines(text)
	file1.close()
	return


## Tesseract OCR pass
def tesseract_pass(path,out_path):
    ''' Runs Tesseract OCR on list of pdfs '''
    #tesseract_parse = []
    list_of_img_pdfs = check(path)
    for file in list_of_img_pdfs:
        tesseract_one(file,out_path)
    #df_tesser = pd.DataFrame(tesseract_parse,columns=[list_of_img_pdfs])
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

def check(path,thresh=1000):
    ''' Determine which files are did not get extracted with pdfminer; Checks
    file size'''
    list_of_img_pdfs = []
    for file in path:
        if os.path.getsize(file) < 1000:
            list_of_img_pdfs.append(file)
    return list_of_img_pdfs

file = '2019_july_2_922281564166445297_official-documents-amendment-to-the-loan-agreement-for-loan-8564-ga.pdf'
out_path = '/home/kbari/git_repo/FinanceErdosProj/Extract_Data_Kash/'
#tesseract_one(file,out_path)



### Main

def main():
    #path = '/home/kbari/git_repo/FinanceErdosProj/Original_Data/' 
    #out_path = '/home/kbari/git_repo/FinanceErdosProj/PyMuPdf_Text/'
    #pymupdf_pass(path,out_path)
    #out_path1 = '/home/kbari/git_repo/FinanceErdosProj/Tesseract_Text/'
    #tesseract_pass(out_path,out_path1)

if __name__ == "__main__":
    main()
