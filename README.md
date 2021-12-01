## Table of Contents
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Contents](#contents)
4. [Collaboration](#collaboration)
5. [FAQs](#faqs)
## General Info
***
Qarik Corporate Project for the Erdos Institute
## Technologies
***
A list of technologies used within the project:
* [Python](https://www.python.org/): Version -- 
  * [PyMuPDF](https://pdfminersix.readthedocs.io/en/latest/)
  * [Tesseract OCR](https://pypi.org/project/pytesseract/)
  * [NLTK](https://www.nltk.org/)
  * [Gensim](https://radimrehurek.com/gensim/)
  * [scikit-learn](https://scikit-learn.org/stable/)
  * [GLoVe](https://pypi.org/project/glove_python/)
* [Tableau](https://www.tableau.com/): Version --
## Contents
***
#### Presentation Folder
* Technical_Summary.ipynb provides technical overview as well as some visualizations 
of important results. Refer to this notebook to also have links to specific
folders.
* Executive_Summary.pdf provides summarized insights for stakeholders and
  addresses important KPIs.
* Team_Bear_Slides has slides for our 5 minute presentation for the Erdos
  Institute 
#### Extract_Data Folder
* Folder Contains script to extract text from pdf files. Has code to try and
  extract text from all pdfs. Can use packages PyMuPDF and pyTesseract. 
Additionally has code to use PDFMiner.six, but is commented out as it did not
perform as well as other packages. PyMuPDF and PDFMiner.six work on native
PDFs. For scanned PDFs, we use pyTesseract, which is OCR software (longer run
time to extract using OCR).
#### PyMuPdf_Text Folder
* Output of PyMuPDF conversion from pdf to txt.
#### Tesseract_Text Folder
* Output of pyTesseract conversion from pdf to txt.
#### Clean_Data Folder
* Folder contains scripts and notebooks to extract loan amount, country, date,
  project description, project name and some preprocessing.
#### Cluster_Data
* Folder contains two folders for two different models for
  clustering the loan agreements by the project description and project name. 
  *  Latent Dirchlet Allocation model
  *  k-means clustering model with the GLoVe model
#### gdp_analysis
*  Folder contains notebooks describing analysis of GDP in relation to whether
   countries obtained loans
#### Regression_Classifier
*  Folder containing cleaned data as well as regression model used to predict
   loan amount from extracted features.
#### ProjectStory.twbx
* Tableau Storybook providing visualizations of loan data and external data
  from world bank.
## Collaboration
***
This project was worked on by Group Bear for the Erdos Institute during Fall 2021. The members include Kashif Bari, Kevin Bombardier, Attilio Castano, Bingjin Liu. Our mentor was James Bramante.
