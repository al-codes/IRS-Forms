import requests
import os
from helper import strip_format
from form_scraper import get_website_data, format_response, format_all_responses, filter_responses, dict_list_to_json


requested_dl_forms = []

# min_year [0], max_year[1]
desired_year_range = []

   
def download_prompt():
    """Gets tax form name and year range for download"""
    
    print('\nPlease enter a tax form you would like to download to a pdf format.\n')
    requested_form = input('Form: ')
    min_year = input('\nPlease enter the minimum year: ')
    max_year = input('\nPlease enter the maximum year: ')
    requested_dl_forms.append(requested_form)
    desired_year_range.append(min_year)
    desired_year_range.append(max_year)
    return 


def collect_all_pdfs(filtered_forms):
    """Collects pdfs within an inclusive range of years"""

    min_year = int(desired_year_range[0])
    max_year = int(desired_year_range[1])
    pdf_dict = {}

    for form in filtered_forms:
        pdfs = form.links
        pdfs = str(pdfs)
        form_details = form.text.split('\n')
        form_number = form_details[0]
        year = int(form_details[2])
        desired_form = form_number.replace('+', ' ')
        if form_number == desired_form and min_year <= year <= max_year:
            pdf_dict[f'{desired_form} - {year}'] = pdfs[2:-2]
    return pdf_dict
    

def download_pdfs(pdf_dict):
    """Download pdfs to correct directory"""

    for form, link in pdf_dict.items():
        form_name = form.split(' -')[0]
        url = link
        response = requests.get(url)
        if not os.path.exists(form_name):
            os.mkdir(form_name)
        with open(f'{form_name}/{form}.pdf', 'wb') as f:
            f.write(response.content)