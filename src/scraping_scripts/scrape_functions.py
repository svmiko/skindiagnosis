def scrape_mayoclinic(page):
    try:
        symptom_h = page.find(lambda tag: (tag.name in ['h2'])
                                        and 'symptoms' in tag.get_text().lower()
                                    )
        symptoms_components = symptom_h.find_next_siblings(lambda tag: (tag.name in ['p','ul']))
        if not symptoms_components:
            symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
            while not symptoms_components:
                symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
        symptoms_text = ''
        for sym_com in symptoms_components:
            symptoms_text += sym_com.get_text()
        return symptoms_text
    except:
        pass

def scrape_cleveland(page):
    try:
        symptom_h = page.find(lambda tag: (tag.name in ['h1','h2','h3','section','div','p'])
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
        return symptoms_text
    except:
        pass

def scrape_healthline(page):
    try:
        symptom_h = page.find('a', attrs={"name" : ["Symptoms", "symptoms"]})

        # print(f"{keyword} {link_url} symptoms:")
        symptoms_components = symptom_h.find_parent('div')

        symptoms_components = symptoms_components.find_parent('h2')
        symptoms_components = symptoms_components.find_parent('div')

        symptoms_components = symptoms_components.find_next_siblings(lambda tag: (tag.name in ['p','ul','h4']))
        if not symptoms_components:
            symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['p','ul']))
            while not symptoms_components:
                symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
        symptoms_text = ''
        for sym_com in symptoms_components:
            if "Continue reading about the symptoms" not in sym_com.get_text():
                symptoms_text += sym_com.get_text()
        return symptoms_text
    except:
        pass

def scrape_niams(page):
    try:
        symptom_h = page.find(lambda tag: (tag.name in ['h2'])
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
        return symptoms_text
    except:
        pass



#test 
# import requests
# from bs4 import BeautifulSoup

# page_response = requests.get("https://www.healthline.com/health/dermatomyositis")

# page_soup = BeautifulSoup(page_response.content, 'html.parser')
#     # symptom_h = page.find(lambda tag: (tag.name in ['a'])
#     #                                 and 'symptoms' in tag.get_text().lower()
#     #                             )
# symptom_h = page_soup.find('a', attrs={"name" : ["symptoms", "Symptoms"]})

# # print(f"{keyword} {link_url} symptoms:")
# symptoms_components = symptom_h.find_parent('div')
# symptoms_components = symptoms_components.find_parent('h2')
# symptoms_components = symptoms_components.find_parent('div')

# symptoms_components = symptoms_components.find_next_siblings(lambda tag: (tag.name in ['p','ul','h4']))
# if not symptoms_components:
#     symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['p','ul']))
#     while not symptoms_components:
#         symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
# symptoms_text = ''
# for sym_com in symptoms_components:
#     if "Continue reading about the symptoms" not in sym_com.get_text():
#         symptoms_text += sym_com.get_text()

# print(symptoms_text)