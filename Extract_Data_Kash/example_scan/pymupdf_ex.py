#! /usr/bin/env python3

import fitz
import os

filename='/home/kbari/git_repo/FinanceErdosProj/Extract_Data_Kash/example_scan/2019_july_2_922281564166445297_official-documents-amendment-to-the-loan-agreement-for-loan-8564-ga.pdf'
out_path='/home/kbari/git_repo/FinanceErdosProj/Extract_Data_Kash/example_scan/'
doc = fitz.open(filename)
file1= open(out_path+os.path.splitext(os.path.basename(filename))[0]+"_pymupdf.txt","w")
text = ''
for page in doc:
    text += page.get_text('text')
file1.writelines(text)
file1.close()
