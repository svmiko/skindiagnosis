import requests
import pandas as pd
from bs4 import BeautifulSoup
import os  
import csv
import time
from scrape_functions import *


websites = ['Mayo Clinic', 
            'Cleveland Clinic',
            'WebMD',
            'Healthline.com',
            'niams.nih.gov',
            'Harvard Health'
            'AAD',
            'cedars-sinai',
	        'Wikipedia',
	        'Skinsight',
            'Dermnetnz',
	        'NHS',
            'cdc',
            'rarediseases',
            'msdmanuals',
            'medline',
            'patientinfo',
            'dermnet'
            ]

disease = {

    'Urticaria Hives': ['Urticaria', 'Dermatographism', 'Angiodema', 'Urticarial vasculitis','Cholinergic urticaria'],
    'Benign Tumors': ['Seborrheic Keratosis', 'Dermatofibroma', 'Chondrodermatitis', 'Epidermal Cyst', 'Keratoacanthoma', 'Sebaceous Hyperplasia', 'Keloid'],
    'Poison Ivy and Contact Dermatitis': ['Poison Ivy', 'Contact Dermatitis'],
    'Acne and Rosacea': ['Acne', 'Rosacea', 'Hidradenitis suppurativa', 'Perioral Dermatitis'],
    'Vascular Tumors': ['Hemangioma', 'Kaposi sarcoma', 'Angiokeratoimas', 'Angioma', 'Pyogenic granulomas', 'Telangiectasia'],
    'Eczema': ['Dermatitis', 'Chapped', 'Fissured', 'Desquamation', 'Dyshidrosis', 'Asteatotic', 'Nummular', 'Factitial', 'Dry', 'Iododerma', 'Keratolysis Exfoliativa', 'Lichen Simplex Chronicus', 'Maceration', 'Milroy Disease', 'Neurotic Excoriations', 'Parasitosis Psychogenic', 'Phlesbitis Superficial', 'Pompholyx', 'Prurigo Nodularis'],
    'Psoriasis or Lichen Planus': ['Pinking', 'Amiantacea', 'Axillary Granular Parakeratosis', 'Lichen Nitidus', 'Lichen Planus', 'Sclerosis', 'Pityriasis', 'Psoriasis', 'Reiter syndrome', 'Seborrheic Dermatitis'],
    'Exanthems and Drug Eruptions': ['Desquamation', 'Entrerovirus', 'Erythema Infectiosum', 'Exfoliative Dermatitis', 'Gianotti Crosti', 'Hand Foot Mouth Disease', 'Kawasaki Syndrome', 'Minocycline Pigmentation', 'Roseola Infantum', 'Scarlet Fever', 'Viral Exanthems'],
    'Lupus and other Connective Tissue diseases': ['Acroyanosis', 'Chilblains Perniosis', 'Crest Syndrome', 'Dermatomyositis', 'Erythromelagia', 'Morphea', 'Mucinosis', 'Raynaud Disease', 'Rjeumtoid nodule', 'scleroderma'],
    'Scabies Lyme Diease and other Infestations and Bites': ['Biting insects', 'Cactus Granuloma', 'Cat bite', 'caterpillar dermatitis', 'Chigger bites bullous', 'coral poisoning', 'cutaneous larva migrans', 'duck itch', 'fire ants', 'flea bites', 'jelly fish sting', 'leishamaniasis', 'Maculae Cerulea', 'Myiasis', 'pediculosis', 'public lice', 'Spider bite', 'tick bite'],
    'Pigmentation Disorders': ['Vitiligo','Albinism', 'Melasma', 'Freckles', 'Hypopigmentation', 'Hyperpigmentation'],
    'Cellulitis Impetigo and other Bacterial Infections': ['Cellulitis', 'Impetigo','Eczema Staph', 'Pseudomonfoll', 'Balanitis Bacterial', 'Botryomycosis Staph','Ecthyma','Erysipelas', 'Erysipeloid','Folliculitis', 'Furuncles Carbuncles', 'Leprosy', 'Pseudomonas Cellulitis', 'Staphylococcal Folliculitis', 'Sycosis Barbae', 'atypical mycobacterium', 'meningococcemia','otitis externa', 'pitted keratolysis'],
    'Hair Loss Alopecia and other Hair Diseases': ['Alopecia Areata', 'Androgenetic Alopecia', 'Telogen Effluvium', 'acne keloidalis', 'discoid lupus', 'dissecting cellulitis', 'folliculitis decalvans', 'hirsutism', 'hot comb alopecia', 'lichen planopilaris', 'pili torti', 'pseudopelade', 'telogen effluvium', 'trichorrhexis nodosa', 'trichotillomania', 'tufted folliculitis'],
    'Herpes HPV and other STDs': ['Herpes Simplex', 'HPV (Human Papillomavirus)', 'Syphilis','AIDS', 'bacterial vaginosis', 'chancroid', 'genital herpes simplex', 'genital ulcers', 'genital warts', 'gonorrhea', 'herpes type 2 primary', 'molluscum contagiosum', 'pearly penile papules', 'warts mouth'],
    'Bullous Disease': ['Pemphigus', 'Bullous Pemphigoid', 'Epidermolysis Bullosa'],
    'Nail Fungus and other Nail Disease': ['Onychomycosis', 'Paronychia','Onychorrhexis','Alopecea Areata'],
    'Tinea Ringworm Candidiasis and other Fungal Infections': ['Ringworm (Tinea Corporis)', 'Candidiasis', 'Tinea Versicolor','Cheilitis','Candida','Armpit Yeast Infection','Tinea Incognito','Intertrigo','Oral thrush','actinomycosis','coccidiomycosis','Confluent and Reticulated Papillomatosis','Erosio interdigitalis blastomycetica','erythrasma','kerion','Blastomycosis','Angular Cheilitis','Pitted Keratolysis','Pityrosporum','Tinea barbae','ringworm','Tinea Faciei','Athletes foot','jock itch','Tinea Manuum','Tinea Capitis'],
    'Systematic Diseases': {'Acanthosis nigricans','Acrodermatitis enteropathica','amyloidosis','Cowden Syndrome','Diabetes','Elastosis Perforans Serpiginosa','Glucagonoma','Granuloma Annulare','Lichen amyloidosis','Lichen Myxedematosus','lipoid proteinosis','myxedema','Necrobiosis Lipoidica Diabeticorum','Neurofibromatosis','Endocarditis','pellagra','Pretibial Myxedema','rheumatoid nodule','Sarcoidosis','Sebaceous Adenoma','Tuberous sclerosis','Xanthoma'},
    'Light Diseases and Disorders of Pigmentation': {'Actinic keratosis','Solar comedones','Albinism','Colloid milium','Erythema ab igne','Erythema dyschromicum perstans','Hydroa vacciniforme','Idiopathic guttate hypomelanosis','lentigo','Melasma','Millia','Mongolian Blue Spots','Nevus Anemicus','Photosensitivity','piebaldism','Poikiloderma of Civatte','Polymorphous light eruption','Porphyria ','Post Inflammatory Hyperpigmentation','Pseudoporphyria','Sun Damaged Skin','Vitiligo'}
    
    }



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
                #print(search_url)  
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
        page_response = requests.get(link_url, verify=False)
        time.sleep(2)
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

            elif "medlineplus.gov" in link_url: 
                df = add_to_df(df, disease_name, keyword, link_url, scrape_medline(page_soup))

            elif "msdmanuals.com" in link_url: 
                df = add_to_df(df, disease_name, keyword, link_url, scrape_msdmanuals(page_soup))

            elif "patient.info" in link_url:
                df = add_to_df(df, disease_name, keyword, link_url, scrape_patientinfo(page_soup))
		    
	        # elif "webmd.com" in link_url:
            #   df = add_to_df(df, disease_name, keyword, link_url, scrape_webmd(page_soup))
		    
            elif "cedars-sinai.org" in link_url:
                df = add_to_df(df, disease_name, keyword, link_url, scrape_cedars_sinai(page_soup))
		    
            elif "skinsight.com" in link_url:
                df = add_to_df(df, disease_name, keyword, link_url, scrape_skinsight(page_soup))
            
            elif "dermnetnz.org" in link_url:
                df = add_to_df(df, disease_name, keyword, link_url, scrape_dermnet(page_soup))

            # elif "health.harvard.edu" in link_url:
            #     df = add_to_df(df, disease_name, keyword, link_url, scrape_harvardhealth(page_soup))

	
    return df


scraped_data = (scrape_data(get_websites(disease,websites)))

scraped_data.to_csv('scraped_data.csv')


# test code
# print(get_websites(disease,websites))
# query = 'Mayoclinic Lupus symptoms'
# search_url = f'https://www.google.com/search?q={query}'
# response = requests.get(search_url)
# print(extract_first_url(BeautifulSoup(response.content, 'html.parser')))
