#! /usr/bin/env python3

import fitz
import os

filename='/home/kbari/git_repo/FinanceErdosProj/Extract_Data_Kash/example_normal/2019_november_28_859161577483616466_official-documents-loan-agreement-for-additional-financing-loan-9020-yf-closing-package.pdf'
out_path='/home/kbari/git_repo/FinanceErdosProj/Extract_Data_Kash/example_normal/'
doc = fitz.open(filename)
file1= open(out_path+os.path.splitext(os.path.basename(filename))[0]+"_pymupdf.txt","w")
text = ''
for page in doc:
    text += page.get_text('text')
file1.writelines(text)
file1.close()
