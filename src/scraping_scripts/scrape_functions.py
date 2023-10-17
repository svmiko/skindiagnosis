def scrape_mayoclinic(page):
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

def scrape_cleveland(page):
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