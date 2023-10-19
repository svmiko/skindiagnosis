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


def scrape_wikipedia(page):
    try: 
        symptom_h = page.find(lambda tag: (tag.name in ['h2']) and 'symptoms' in tag.get_text().lower())
        # Check if symptom_h is not None
        if symptom_h:
            symptoms_components = symptom_h.find_next('p')
            if symptoms_components:
                symptoms_text = symptoms_components.get_text()
        else:
            symptoms_components = page.find('p')
            symptoms_text = symptoms_components.get_text()
        return(symptoms_text)
    except:
        pass

def scrape_rarediseases(page):
    try: 
        symptom_h = page.find(lambda tag: (tag.name in ['h1','h2','h3','h4','h5','section','div','p']) and 'symptoms' in 
                              tag.get_text().lower())
        # print(f"{keyword} {link_url} symptoms:")
        symptoms_components = symptom_h.find_next_siblings(lambda tag: (tag.name in ['p','ul']))
        if not symptoms_components:
            symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
            while not symptoms_components:
                symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
                symptoms_text = ''
                for sym_com in symptoms_components:
                    symptoms_text += sym_com.get_text()
        return(symptoms_text)
    except:
        pass
    
def scrape_aad(page):
    try: 
        symptoms_text = ""
        symptom_h = page.find('section', class_ = 'content')
        if symptom_h: 
            symptoms_components = symptom_h.find_all('p')
            for p in symptoms_components:
                symptoms_text += p.get_text() 
        else:
            symptoms_text = "not found"
        return symptoms_text
    except:
        pass

<<<<<<< HEAD
    
def scrape_medline(page):
    try: 
        symptom_h = page.find(lambda tag: (tag.name in ['h2']) and 'symptoms' in tag.get_text().lower())
        
        if symptom_h:
            symptoms_components = symptom_h.find_next('p')
            #print(f"symptoms_components: {symptoms_components}")
            if symptoms_components:
                symptoms_text = symptoms_components.get_text()
                #print(f"symptoms_text: {symptoms_text}")
        else:
            symptoms_components = page.find('p')
            symptoms_text = symptoms_components.get_text()
            symptoms_text = 'None'
        return(symptoms_text)
    except:
        pass

def scrape_msdmanuals(page):
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

def scrape_patientinfo(page):
    try:
        symptom_h = page.find(lambda tag: (tag.name in ['h2','p'])
                              and 'symptoms' in tag.get_text().lower())
                                                        
        # print(f"{keyword} {link_url} symptoms:")
        symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['p','ul']))
        if not symptoms_components:
            symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
            while not symptoms_components:
                symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
        symptoms_text = ''
        print(f"symptoms_text: {symptoms_text}")
        for sym_com in symptoms_components:
            symptoms_text += sym_com.get_text()
    except:
        pass
                

def scrape_harvardhealth(page):
    try: 
        symptom_h = page.find(lambda tag: (tag.name in ['h2'])
                                        and 'symptoms' in tag.get_text().lower()
                                        and 'of' in tag.get_text().lower()
                                    )
        # print(f"{keyword} {link_url} symptoms:")
=======

def scrape_dermnetnz(page):
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
    except:
        pass

def scrape_NHS(page):
    try:
        symptom_h = page.find(lambda tag: (tag.name in ['h2'])
                                        and 'symptoms' in tag.get_text().lower()
                                    )
                            # Check if symptom_h is not None
        if symptom_h:
            next_ele = symptom_h.find_next()
            while next_ele.name != 'h2' and next_ele.name != 'h3':
                symptoms_components = next_ele
                next_ele = next_ele.find_next()
                symptoms_text += symptoms_components.get_text()
            symptom_h = page.find(lambda tag: (tag.name in ['h1'])
                                        and 'symptoms' in tag.get_text().lower()
                                    )
            if symptom_h:
                
                
                symptoms_components = symptom_h.find_next('p')
                symptoms_text = symptoms_components.get_text()
    except:
        pass

def scrape_cdc(page):
    try:
        symptom_h = page.find(lambda tag: (tag.name in ['h1','h2','h3','section','div','p'])
                                and 'symptoms' in tag.get_text().lower()
                                and 'of' in tag.get_text().lower()
                            )
        #print(f"{keywords} {link_url} symptoms:")
>>>>>>> 9f48ec748bc04022b39ffd5b0c7fb2faaf737b52
        symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['p','ul','h4']))
        if not symptoms_components:
            symptoms_components = symptom_h.find_next(lambda tag: (tag.name in ['div']))
            while not symptoms_components:
                symptoms_components = symptoms_components.find_next(lambda tag: (tag.name in ['p','ul','div']))
    
        symptoms_text = ''
        for sym_com in symptoms_components:
            symptoms_text += sym_com.get_text()
    except:
        pass
<<<<<<< HEAD
=======


>>>>>>> 9f48ec748bc04022b39ffd5b0c7fb2faaf737b52
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
