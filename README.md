## Table of Contents
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Contents](#contents)
4. [Collaboration](#collaboration)
5. [FAQs](#faqs)
### General Info
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
* Summary.ipynb and Executive_Summary.txt contain more specific information and
  summaries of the project goals/objectives along with specific information
* Extract_Data: Folder Contains script to extract text from pdf files. Output
  in PyMuPDF_Text and Tesseract_Text
* Clean_Data: Folder contains scripts and notebooks to extract loan amount, country, date,
  project description, project name and some preprocessing.
* Cluster_Data: Folder contains two folders for two different models for
  clustering the loan agreements by the project description. One uses LDA
(Latent Dirchlet Allocation) and the other uses k-means clustering after
vectorizing the text using the GLoVe model.
* gdp_analysis: Folder contains notebooks
* Finalized_Data: Folder containing cleaned data that was used in the models
* Presentation: Folder contains visualizations (generated by Tableau) as well
  as slides for our presentation for the Erdos Institute.
## Collaboration
***
This project was worked on by Group Bear for the Erdos Institute during Fall 2021. The members include Kashif Bari, Kevin Bombardier, Attilio Castano, Bingjin Liu. Our mentor was James Bramante.
## FAQs
***
A list of frequently asked questions:
