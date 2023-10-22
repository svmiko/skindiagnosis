# test

import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv
import time


# keywords = ['pigmentation',
#             'pigmentation disorders',
#             'Skin Pigmentation Disorders',
#             'Lupus',
#             'Systemic Lupus Erythematosus',
#             'Acne',
#             'Rosacea',
#             'Acne Rosacea',
#             'Poison Ivy',
#             'Hives',
#             'Eczema',
#             'Psoriasis']

# disease = {
#     'Pigmentation Disorders': ['Vitiligo', 'Albinism', 'Melasma', 'Freckles', 'Hypopigmentation', 'Hyperpigmentation'],
#     'Connective Tissue Diseases': ['Lupus', 'Scleroderma', 'Dermatomyositis'],
#     'Acne': ['Acne Vulgaris', 'Acne Rosacea'],
#     'Contact Dermatitis': ['Poison Ivy Dermatitis', 'Contact Dermatitis'],
#     'Vascular Tumors': ['Hemangioma', 'Kaposiform Hemangioendothelioma'],
#     'Urticaria Hives': ['Chronic Idiopathic Urticaria', 'Physical Urticaria'],
#     'Atopic Dermatitis': ['Eczema', 'Contact Dermatitis'],
#     'Bullous Disease': ['Pemphigus', 'Bullous Pemphigoid', 'Epidermolysis Bullosa'],
#     'Hair Loss': ['Alopecia Areata', 'Androgenetic Alopecia', 'Telogen Effluvium'],
#     'Fungal Infections': ['Ringworm (Tinea Corporis)', 'Candidiasis', 'Tinea Versicolor'],
#     'Psoriasis': ['Plaque Psoriasis', 'Guttate Psoriasis', 'Inverse Psoriasis'],
#     'Melanoma': ['Superficial Spreading Melanoma', 'Nodular Melanoma', 'Lentigo Maligna Melanoma'],
#     'Nail Fungus': ['Onychomycosis', 'Paronychia'],
#     'Infestations and Bites': ['Scabies', 'Lyme Disease'],
#     'Eczema': ['Atopic Dermatitis', 'Contact Dermatitis'],
#     'Exanthems and Eruptions': ['Measles', 'Roseola'],
#     'Herpes and STDs': ['Herpes Simplex', 'HPV (Human Papillomavirus)', 'Syphilis'],
#     'Benign Tumors': ['Seborrheic Keratosis', 'Dermatofibroma'],
#     'Malignant Lesions': ['Basal Cell Carcinoma', 'Squamous Cell Carcinoma', 'Merkel Cell Carcinoma'],
#     'Vasculitis': ['Hypersensitivity Vasculitis', 'Granulomatosis with Polyangiitis'],
#     'Bacterial Infections': ['Cellulitis', 'Impetigo'],
#     'Viral Infections': ['Warts', 'Molluscum Contagiosum'],
# }

### ADD NAME OF WEBSITE HERE!!!!!!
websites = ['Mayo Clinic', 
            'Cleveland Clinic',
            'WebMD',
            'Healthline',
            'NIAMS',
            'Harvard Health'
            'AAD',
            'cedars-sinai',
	    'Wikipedia',
	    'Skinsight',
            'Dermnetnz',
	    'NHS']

disease = {
    'Pigmentation Disorders': ['Vitiligo', 'Albinism', 'Melasma', 'Freckles', 'Hypopigmentation', 'Hyperpigmentation']}

data = {
    'Disease': [],
    'Keyword': [],
    'Website': [],
    'Symptoms':[]
}
df = pd.DataFrame(data)


for website in websites:
    for disease_name, keywords in disease.items():
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
                result_links = soup.find_all('a')
                url_list =[]
                for link in result_links:
                    if link.get("href").startswith("/url"):
                        link_url = link.get("href")[7:-86]
                        if len(url_list) <1:
                            url_list.append(link_url)

                #print(url_list)

                for link_url in url_list:
                    # visit page
                    page_response = requests.get(link_url)
                    if page_response.status_code == 200:
                        page_soup = BeautifulSoup(page_response.content, 'html.parser')
                        # mayoclinic
                        if "mayoclinic.org" in link_url:
                            symptom_h = page_soup.find(lambda tag: (tag.name in ['h2'])
                                                            and 'symptoms' in tag.get_text().lower()
                                                        )
                            # print(f"{keyword} {link_url} symptoms:")
                            symptoms_components = symptom_h.find_next_siblings(lambda tag: (tag.name in ['p','ul']))
                            if not symptoms_components:
                                symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
                                while not symptoms_components:
                                    symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
                            symptoms_text = ''
                            for sym_com in symptoms_components:
                                symptoms_text += sym_com.get_text()

                            # for sym_com in symptoms_components:
                            #     print(sym_com.get_text())

                        elif "clevelandclinic.org" in link_url:
                            symptom_h = page_soup.find(lambda tag: (tag.name in ['h1','h2','h3','section','div','p'])
                                                            and 'symptoms' in tag.get_text().lower()
                                                            and 'of' in tag.get_text().lower()
                                                        )
                            # print(f"{keyword} {link_url} symptoms:")
                            symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['p','ul','h4']))
                            if not symptoms_components:
                                symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
                                while not symptoms_components:
                                    symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
                        
                            symptoms_text = ''
                            for sym_com in symptoms_components:
                                symptoms_text += sym_com.get_text()

                        elif "webmd.com" in link_url:
                            symptom_h = page_soup.find(lambda tag: (tag.name in ['h1','h2','h3','section','div','p'])
                                                            and 'symptoms' in tag.get_text().lower()
                                                            and 'of' in tag.get_text().lower()
                                                        )
                            # print(f"{keyword} {link_url} symptoms:")
                            symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['p','ul','h4']))
                            if not symptoms_components:
                                symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
                                while not symptoms_components:
                                    symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
                        
                            symptoms_text = ''
                            for sym_com in symptoms_components:
                                symptoms_text += sym_com.get_text()

                        elif "healthline.com" in link_url:
                            symptom_h = page_soup.find(lambda tag: (tag.name in ['h1','h2','h3','section','div','p'])
                                                            and 'symptoms' in tag.get_text().lower()
                                                            and 'of' in tag.get_text().lower()
                                                        )
                            # print(f"{keyword} {link_url} symptoms:")
                            symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['p','ul','h4']))
                            if not symptoms_components:
                                symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
                                while not symptoms_components:
                                    symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
                        
                            symptoms_text = ''
                            for sym_com in symptoms_components:
                                symptoms_text += sym_com.get_text()

                        elif "niams.nih.gov" in link_url:
                            symptom_h = page_soup.find(lambda tag: (tag.name in ['h1','h2','h3','section','div','p'])
                                                            and 'symptoms' in tag.get_text().lower()
                                                            and 'of' in tag.get_text().lower()
                                                        )
                            # print(f"{keyword} {link_url} symptoms:")
                            symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['p','ul','h4']))
                            if not symptoms_components:
                                symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
                                while not symptoms_components:
                                    symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
                        
                            symptoms_text = ''
                            for sym_com in symptoms_components:
                                symptoms_text += sym_com.get_text()

                        elif "health.harvard.edu" in link_url:
                            symptom_h = page_soup.find(lambda tag: (tag.name in ['h1','h2','h3','section','div','p'])
                                                            and 'symptoms' in tag.get_text().lower()
                                                            and 'of' in tag.get_text().lower()
                                                        )
                            # print(f"{keyword} {link_url} symptoms:")
                            symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['p','ul','h4']))
                            if not symptoms_components:
                                symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
                                while not symptoms_components:
                                    symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
                        
                            symptoms_text = ''
                            for sym_com in symptoms_components:
                                symptoms_text += sym_com.get_text()

                        elif "aad.org" in link_url:
                            symptom_h = page_soup.find(lambda tag: (tag.name in ['h1','h2','h3','section','div','p'])
                                                            and 'symptoms' in tag.get_text().lower()
                                                            and 'of' in tag.get_text().lower()
                                                        )
                            # print(f"{keyword} {link_url} symptoms:")
                            symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['p','ul','h4']))
                            if not symptoms_components:
                                symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
                                while not symptoms_components:
                                    symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
                        
                            symptoms_text = ''
                            for sym_com in symptoms_components:
                                symptoms_text += sym_com.get_text()



                        # wikipedia
                        elif "wikipedia" in link_url:
                            symptom_h = page_soup.find(lambda tag: (tag.name in ['h2'])
                                and 'symptoms' in tag.get_text().lower()
                            )
                            # Check if symptom_h is not None
                            if symptom_h:
                                symptoms_components = symptom_h.find_next('p')
                                if symptoms_components:
                                    symptoms_text = symptoms_components.get_text()
                                else: 
			    	                symptoms_components = page_soup.find('p')
				                    symptoms_text = symptoms_components.get_text()


			        elif "skinsight" in link_url:
                            symptom_h = page_soup.find(lambda tag: (tag.name in ['h1','h2','h3','section','div','p'])
                                                            and 'symptoms' in tag.get_text().lower()
                                                            and 'of' in tag.get_text().lower()
                                                        )
                            # print(f"{keyword} {link_url} symptoms:")
                            symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['p','ul','h4']))
                            if not symptoms_components:
                                symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
                                while not symptoms_components:
                                    symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
                        
                            symptoms_text = ''
                            for sym_com in symptoms_components:
                                symptoms_text += sym_com.get_text()
                        
                        #dermnetnz
                        elif "dermnetnz" in link_url:
                            symptom_h = page_soup.find(lambda tag: (tag.name in ['h1','h2','h3','section','div','p'])
                                                            and 'symptoms' in tag.get_text().lower()
                                                            and 'of' in tag.get_text().lower()
                                                        )
                            # print(f"{keyword} {link_url} symptoms:")
                            symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['p','ul','h4']))
                            if not symptoms_components:
                                symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
                                while not symptoms_components:
                                    symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
                        
                            symptoms_text = ''
                            for sym_com in symptoms_components:
                                symptoms_text += sym_com.get_text()
			elif "nhs" in link_url: 
			    symptom_h = page_soup.find(lambda tag: (tag.name in ['h2'])
                                and 'symptoms' in tag.get_text().lower()
                            )
                            # Check if symptom_h is not None
                            if symptom_h:
                                next_ele = symptom_h.find_next()
                                while next_ele.name != 'h2' and next_ele.name != 'h3':
                                    symptoms_components = next_ele
                                    next_ele = next_ele.find_next()
                                    symptoms_text += symptoms_components.get_text()
                                
                            else:
                                symptom_h = page_soup.find('h1')
                                if symptom_h:
                                    
                                    
                                    symptoms_components = symptom_h.find_next('p')
                                    symptoms_text = symptoms_components.get_text()
                                    
			###### ADD ELIF HERE!!!!


                    new_data = {
                        'Disease': [disease_name],
                        'Keyword': [keyword],
                        'Website': [website],
                        'Symptoms': [symptoms_text]
                    }
                    new_df = pd.DataFrame(new_data)
                    df = pd.concat([df, new_df])

print(df)


websites = ['cedars-sinai',
            'mayoclinic',
            # 'cdc.gov',
            'rarediseases']
disease_2 = {
    'Connective Tissue Diseases': ['Lupus', 'Scleroderma', 'Dermatomyositis']}
data = {
    'Disease': [],
    'Keyword': [],
    'Website': [],
    'Symptoms':[]
}
df = pd.DataFrame(data)

for website in websites:
    for disease_name, keywords in disease_2.items():
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
                result_links = soup.find_all('a')
                url_list =[]
                for link in result_links:
                    if link.get("href").startswith("/url"):
                        link_url = link.get("href")[7:-86]
                        if len(url_list) <1:
                            url_list.append(link_url)

                # print(url_list)

                for link_url in url_list:
                    # visit page
                    page_response = requests.get(link_url)
                    if page_response.status_code == 200:
                        page_soup = BeautifulSoup(page_response.content, 'html.parser')
                        # print (page_soup)
                        if "cedars-sinai.org" in link_url:
                            symptom_h = page_soup.find(lambda tag: (tag.name in ['h2'])
                                                            and 'symptoms' in tag.get_text().lower()
                                                        )
                            # print(symptom_h)
                            print(f"{keyword} {link_url} symptoms:")
                            symptoms_components = symptom_h.find_next_siblings(lambda tag: (tag.name in ['p','ul']))
                            if not symptoms_components:
                                symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
                                while not symptoms_components:
                                    symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
                            symptoms_text = ''
                            for sym_com in symptoms_components:
                                symptoms_text += sym_com.get_text()

                        elif "mayoclinic.org" in link_url:
                            symptom_h = page_soup.find(lambda tag: (tag.name in ['h2'])
                                                            and 'symptoms' in tag.get_text().lower()
                                                        )
                            # print(f"{keyword} {link_url} symptoms:")
                            symptoms_components = symptom_h.find_next_siblings(lambda tag: (tag.name in ['p','ul']))
                            if not symptoms_components:
                                symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
                                while not symptoms_components:
                                    symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
                            symptoms_text = ''
                            for sym_com in symptoms_components:
                                symptoms_text += sym_com.get_text()

                        # elif "cdc.gov" in link_url:
                        #     symptom_h = page_soup.find(lambda tag: (tag.name in ['h1','h2','h3','section','div','p'])
                        #                                     and 'symptoms' in tag.get_text().lower()
                        #                                     and 'of' in tag.get_text().lower()
                        #                                 )
                        #     print(f"{keywords} {link_url} symptoms:")
                        #     symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['p','ul','h4']))
                        #     if not symptoms_components:
                        #         symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
                        #         while not symptoms_components:
                        #             symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
                        
                        #     symptoms_text = ''
                        #     for sym_com in symptoms_components:
                        #         symptoms_text += sym_com.get_text()

                        elif "rarediseases.info.nih.gov" in link_url:
                            symptom_h = page_soup.find(lambda tag: (tag.name in ['h1','h2','h3','h4','h5','section','div','p'])
                                                            and 'symptoms' in tag.get_text().lower()
                                                        )
                            # print(f"{keyword} {link_url} symptoms:")
                            symptoms_components = symptom_h.find_next_siblings(lambda tag: (tag.name in ['p','ul']))
                            if not symptoms_components:
                                symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
                                while not symptoms_components:
                                    symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
                            symptoms_text = ''
                            for sym_com in symptoms_components:
                                symptoms_text += sym_com.get_text()

                        # elif "cdc.gov" in link_url:
                        #     symptom_h = page_soup.find(lambda tag: (tag.name in ['h2'])
                        #                                     and 'symptoms' in tag.get_text().lower()
                        #                                 )
                        #     # print(f"{keyword} {link_url} symptoms:")
                        #     symptoms_components = symptom_h.find_next_siblings(lambda tag: (tag.name in ['p','ul']))
                        #     if not symptoms_components:
                        #         symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
                        #         while not symptoms_components:
                        #             symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
                        #         else:
                        #     # Disease is not present, skip scraping symptoms
                        #             print(f"{keyword} not found on this page. Skipping symptoms scraping.")

                        #     symptoms_text = ''
                        #     for sym_com in symptoms_components:
                        #         symptoms_text += sym_com.get_text()
                            
                    new_data = {
                        'Disease': [disease_name],
                        'Keyword': [keyword],
                        'Website': [website],
                        'Symptoms': [symptoms_text]
                    }
                    new_df = pd.DataFrame(new_data)
                    df = pd.concat([df, new_df])

print(df)

import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv
import time

websites = ['msdmanuals',
            'pennmedicine']

disease_3 = {
    'Acne': ['Acne Vulgaris', 'Acne Rosacea']}
data = {
    'Disease': [],
    'Keyword': [],
    'Website': [],
    'Symptoms':[]
}
df = pd.DataFrame(data)
for website in websites:
    for disease_name, keywords in disease_3.items():
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
                result_links = soup.find_all('a')
                url_list =[]
                for link in result_links:
                    if link.get("href").startswith("/url"):
                        link_url = link.get("href")[7:-86]
                        if len(url_list) <1:
                            url_list.append(link_url)

                #print(url_list)

                for link_url in url_list:
                    # visit page
                    page_response = requests.get(link_url)
                    if page_response.status_code == 200:
                        page_soup = BeautifulSoup(page_response.content, 'html.parser')
                       
                        if "msdmanuals" in link_url:
                            symptom_h = page_soup.find(lambda tag: (tag.name in ['h2'])
                                                            and 'symptoms' in tag.get_text().lower()
                                                        )
                            # print(f"{keyword} {link_url} symptoms:")
                            symptoms_components = symptom_h.find_next_siblings(lambda tag: (tag.name in ['p','ul']))
                            if not symptoms_components:
                                symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
                                while not symptoms_components:
                                    symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
                            symptoms_text = ''
                            for sym_com in symptoms_components:
                                symptoms_text += sym_com.get_text()

        

                        if "pennmedicine.org" in link_url:
                            symptom_h = page_soup.find(lambda tag: (tag.name in ['h2'])
                                                            and 'symptoms' in tag.get_text().lower()
                                                            and 'include' in tag.get_text().lower()
                                                        )
                            # print(f"{keyword} {link_url} symptoms:")
                            symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['p','ul','h4']))
                            if not symptoms_components:
                                symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
                                while not symptoms_components:
                                    symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
                            symptoms_text = ''
                            for sym_com in symptoms_components:
                                symptoms_text += sym_com.get_text()

                    new_data = {
                        'Disease': [disease_name],
                        'Keyword': [keyword],
                        'Website': [website],
                        'Symptoms': [symptoms_text]
                    }
                    new_df = pd.DataFrame(new_data)
                    df = pd.concat([df, new_df])

print(df)
