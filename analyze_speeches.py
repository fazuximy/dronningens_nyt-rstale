# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 17:09:07 2023

@author: Fazuximy
"""

import os
from dataclasses import dataclass
import re

from nltk.stem.snowball import DanishStemmer
from nltk.tokenize import word_tokenize
import nltk
import lemmy

@dataclass
class SpeechData:
    speaker:str
    year:int
    text:str
    text_paragraphs:list[str]
    tokens:list[str]

FILE_NAME = "dronningens_nytårstale"
EXPORT_FOLDER = "data"
working_dir = os.getcwd()
export_dir = os.path.join(working_dir,EXPORT_FOLDER)

lemmatizer = lemmy.load("da")
stemmer = DanishStemmer()

year_range = list(range(1972,2023))
SPEAKER = "Hendes Majestæt Dronning Margrethe II"

speech_data_list = []
for year in year_range:
    
    file_name_year = f"{FILE_NAME}_{str(year)}.txt" 
    file_path = os.path.join(export_dir,file_name_year)
    
    with open(file_path, 'r') as text_file:
        speech_text = text_file.read()
        clean_speech_text = re.sub("\n+","\n",speech_text)
        speech_paragraphs = clean_speech_text.split("\n")
        tokens = word_tokenize(clean_speech_text.lower())
        Speech = SpeechData(SPEAKER,year,speech_text,speech_paragraphs, tokens)
        speech_data_list.append(Speech)
        
        
for speech in speech_data_list:

    danish_stop_words = nltk.corpus.stopwords.words('danish')
    
    removed_stop_words = [i for i in speech.tokens if i not in danish_stop_words]
    
    removed_punctuations = [i for i in removed_stop_words if re.match("^[\w\s]+$",i)]
    
    print(removed_punctuations.count("danmark"), speech.year)
    
    stemmed_words = [stemmer.stem(i) for i in removed_punctuations]
    