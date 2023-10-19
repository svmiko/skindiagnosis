import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv
import time
from scrape_functions import *


websites = [#'Mayo Clinic', 
            #'Cleveland Clinic',
            # 'WebMD',
            #'Healthline.com',
            #'niams.nih.gov',
            # 'Harvard Health'
            # 'AAD',
            # 'cedars-sinai',
	         'Wikipedia',
	        # 'Skinsight',
            # 'Dermnetnz',
	        # 'NHS',
            # 'cdc',
            # 'rarediseases',
            # 'msdmanuals',
            # 'pennmedicine'
            ]

disease = {
    #'Pigmentation Disorders': ['Vitiligo', 'Albinism', 'Melasma', 'Freckles', 'Hypopigmentation', 'Hyperpigmentation'],
    'Connective Tissue Diseases': ['Lupus', 'Scleroderma', 'Dermatomyositis']}



def extract_first_url(soup):
    url_list =[]
    result_links = soup.find_all('a')
    for link in result_links:
        if link.get("href").startswith("/url"):
            link_url = link.get("href")[7:-86]
            if len(url_list) <1:
                url_list.append(link_url)
                break
    return link_url



def get_websites(disease_dict, websites_list):
    url_list = []
    for website in websites_list:
        for disease_name, keywords in disease_dict.items():
            d_cat = disease_name
            for keyword in keywords:
                query = f'{website} {keyword} symptoms'
                search_url = f'https://www.google.com/search?q={query}'
                # print(search_url)  
                response = requests.get(search_url)
                time.sleep(2) # a delay between requests
            #print(response.status_code)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    url_list.append([disease_name, keyword, website, extract_first_url(soup)])
    return url_list

def add_to_df(df, disease_name, keyword, website, symptoms):
    new_data = {
            'Disease': [disease_name],
            'Keyword': [keyword],
            'Website': [website],
            'Symptoms': [symptoms]
            }
    new_df = pd.DataFrame(new_data)
    df = pd.concat([df, new_df])
    return df


def scrape_data(url_list):
    data = {
            'Disease': [],
            'Keyword': [],
            'Website': [],
            'Symptoms':[]
        }
    df = pd.DataFrame(data)
    for disease_name, keyword, website, link_url in url_list:
    # visit page
        page_response = requests.get(link_url)
        # print(page_response.status_code)
        if page_response.status_code == 200:
            page_soup = BeautifulSoup(page_response.content, 'html.parser')

            if "mayoclinic.org" in link_url:
                df = add_to_df(df,disease_name, keyword, link_url, scrape_mayoclinic(page_soup))

            elif "clevelandclinic.org" in link_url:
                df = add_to_df(df,disease_name, keyword, link_url, scrape_cleveland(page_soup))

            elif "healthline.com" in link_url:
                df = add_to_df(df, disease_name, keyword, link_url, scrape_healthline(page_soup))
            
            elif "niams.nih.gov" in link_url:
                df = add_to_df(df, disease_name, keyword, link_url, scrape_niams(page_soup))
            elif "wikipedia" in link_url:
                df = add_to_df(df, disease_name, keyword, link_url, scrape_wikipedia(page_soup))
            elif "rarediseases" in link_url: 
                df = add_to_df(df, disease_name, keyword, link_url, scrape_rarediseases(page_soup))
            elif "aad.org" in link_url: 
                df = add_to_df(df, disease_name, keyword, link_url, scrape_aad(page_soup))
            elif "webmd.com" in link_url:
                df = add_to_df(df, disease_name, keyword, link_url, scrape_webmd(page_soup))
            elif "cedars-sinai.org" in link_url:
                df = add_to_df(df, disease_name, keyword, link_url, scrape_cedars_sinai(page_soup))
            elif "skinsight.com" in link_url:
                df = add_to_df(df, disease_name, keyword, link_url, scrape_skinsight(page_soup))
    return df


print(scrape_data(get_websites(disease,websites)))



# test code
# print(get_websites(disease,websites))
# query = 'Mayoclinic Lupus symptoms'
# search_url = f'https://www.google.com/search?q={query}'
# response = requests.get(search_url)
# print(extract_first_url(BeautifulSoup(response.content, 'html.parser')))