from requests_html import HTMLSession 
import requests
import json
import os
from helper import *

# requests-html object
session = HTMLSession()


requested_forms = []
dict_list_to_json = []

# min_year [0], max_year[1]
desired_year_range = []


def search_prompt():
    """Gets user tax forms names and formats for IRS url"""

    print('\nPlease enter the tax form number separated by a comma followed by a space: ')
    print('(ex: Form W-2, Form 1095-C, Form W-3, etc)\n')
    form_names = input('Forms: ').split(', ')
    requested_forms.extend(form_names)
    return requested_forms


def download_prompt():
    """Gets tax form name and year range for download"""
    
    print('\nPlease enter a tax form you would like to download to a pdf format.\n')
    requested_form = input('Form: ')
    min_year = input('\nPlease enter the minimum year: ')
    max_year = input('\nPlease enter the maximum year: ')
    requested_forms.append(requested_form)
    desired_year_range.append(min_year)
    desired_year_range.append(max_year)
    return 


def get_website_data(form_for_url):
    """Searches for form and gets response from IRS website"""

    if type(form_for_url) == list:
        form_for_url = form_for_url[0]
    url_start = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html'   
    url_end = f'?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&value={form_for_url}&criteria=formNumber&submitSearch=Find&isDescending=false'
    response = session.get(url_start + url_end)
    return response


def format_response(response, form):
    """Parses and formats response to create a dictionary"""
  
    form_dict = {
            'form_number': '',
            'form_title': '',
            'min_year': 0,
            'max_year': 0
            }

    forms_odd = response.html.find('.odd')
    forms_even = response.html.find('.even')
    parsed_forms = forms_odd + forms_even
    
    for obj in parsed_forms:
        form_details = obj.text.split('\n')
        form_number = form_details[0]
        form_title = form_details[1]
        year = int(form_details[2])
        
        # check for correct form
        if form_number == form.replace('+', ' '): 
            form_dict['form_number'] = form_number
            form_dict['form_title'] = form_title
            form_dict['min_year'] = year
            
            if year >= form_dict['max_year']:
                form_dict['max_year'] = year
            elif year <= form_dict['max_year'] and year <= form_dict['min_year']:
                form_dict['min_year'] = year
            elif year >= form_dict['min_year']:
                pass

        # check for duplicates  
        if form_dict not in dict_list_to_json:
            dict_list_to_json.append(form_dict)
    return parsed_forms


def format_all_responses(form_names):
    """Formats all requested form responses and adds to dict"""

    formatted_responses = []
    for form in form_names:
        response = get_website_data(form)
        formatted_dicts = format_response(response, form)

        if len(form_names) == 1:
            formatted_responses.extend(formatted_dicts)
            return formatted_responses         


def jsonify_list_of_dicts(dict_list):
    """Convert list of dictionaries to JSON"""

    json_format = json.dumps(dict_list, indent=4)
    return json_format


def filter_responses(parsed_forms, requested_form):
    """Filters for correct form responses"""
    
    requested_form = strip_format(requested_form[0])

    filtered_form_response = []

    for obj in parsed_forms:
        form_details = obj.text.split('\n')
        form_number = form_details[0]
        # check for duplicates
        if form_number == requested_form:    
            filtered_form_response.append(obj)
    return filtered_form_response


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


if __name__ == '__main__':
    user_request = ""
    
    # BEGIN HERE
    while user_request != 'quit':
        print('\nPlease select which utility you would like to use:\n')
        print('1)View tax form details in json format')
        print('2)Download a tax form given a range of years\n')
        print('(Enter 1, 2 or type QUIT to exit program)')
        user_request = input('\n>> ').lower().strip()


        # UTILITY 1 - SEARCH FORMS AND RETURN JSON DATA
        if user_request == '1':
            requested_forms = search_prompt()
            forms_for_url = format_form_request(requested_forms)
            format_all_responses(forms_for_url)
            print(jsonify_list_of_dicts(dict_list_to_json))
            # clear lists for next query
            clear_list(requested_forms)
            clear_list(dict_list_to_json)
            

        # UTILITY 2 - DOWNLOAD FORMS TO PDF 
        elif user_request == '2':
            download_prompt()
            form_for_url = format_form_request(requested_forms)
            parsed_forms = format_all_responses(form_for_url)
            filtered_pdfs = filter_responses(parsed_forms, requested_forms)
            all_pdfs = collect_all_pdfs(filtered_pdfs)
            download_pdfs(all_pdfs)
            # clear lists for next query
            clear_list(dict_list_to_json)
            clear_list(desired_year_range)
            
        # EXIT PROGRAM
        elif user_request == 'quit':
            print('Bye!')
            break
       
            
