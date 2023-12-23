# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 15:42:01 2023

@author: Fazuximy
"""

from bs4 import BeautifulSoup
import requests
import re
import os


def extract_speech(url:str, file_name:str, export_dir:str):
    # Function for extracting text from the Danish Queen's New Year speeches and saving them to a text file
    """
    url: The URL which the speech should be extracted from
    filename: The name of the file which the output text file should be called
    export_dir: The folder where the text file should be saved
    """
    
    result = requests.request("GET", url)

    website_soup = BeautifulSoup(result.text,'html.parser')

    # For the Queen's speeches the speech text is within this div
    speech_content = website_soup.find('div', {"class": "speech-article-content"})

    try:
    
        text_paragraphs = []
        for paragraph in speech_content:
            if not paragraph.text.isspace():
                # Removing multiple spaces
                paragraph_text = re.sub("\s{2,}","",paragraph.text)
                text_paragraphs.append(paragraph_text)
                
    except:
        print(f"{url} did not work.")
        return

    # Getting the year of the speech
    speech_date = website_soup.find('time')
    date_text = speech_date.text
    year_text = re.findall("\d{4}",date_text)[0]

    # The paragraphs are joined together with two newlines to allow for proper spacing in the text file
    speech_text = "\n\n".join(text_paragraphs)
    file_text_name = f"{file_name}_{year_text}.txt"
    file_path = os.path.join(export_dir,file_text_name)

    with open(file_path, 'w') as text_file:
        text_file.write(speech_text)


def main():

    # Used to extract speeches to text files
        # Since the URLs are very inconsistent, you have to look the URL up of the missing speeches
    FILE_NAME = "dronningens_nytårstale"
    EXPORT_FOLDER = "data"
    working_dir = os.getcwd()
    export_dir = os.path.join(working_dir,EXPORT_FOLDER)
    
    # The most consistent URL for the speeches
    standard_url = "https://www.dansketaler.dk/tale/dronningens-nytaarstale-"
    
    # From earliest to latest speech in years
    year_range = list(range(1972,2023))
    
    for year in year_range:
        extract_speech(standard_url+str(year), FILE_NAME, export_dir)
        
        
if __name__ == '__main__':
    main()
