""" IRS Form Scraper """

from requests_html import HTMLSession 
from helper import strip_format
import requests


# requests-html object
session = HTMLSession()

dict_list_to_json = []


def get_website_data(form_for_url):
    """Searches for form and gets response from IRS website"""

    if type(form_for_url) == list:
        form_for_url = form_for_url[0]
    url_start = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html'   
    url_end = f'?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&value={form_for_url}&criteria=formNumber&submitSearch=Find&isDescending=false'
    
    try:
        response = session.get(url_start + url_end)
    
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)
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
        if form_dict not in dict_list_to_json and form_dict['form_number'] != "":
            dict_list_to_json.append(form_dict)
        else:
            pass
    return parsed_forms


def format_all_responses(form_names):
    """Formats all requested form responses and adds to dict"""

    formatted_responses = []
    if form_names == None:
        return
    else:
        for form in form_names:
            response = get_website_data(form)
            formatted_dicts = format_response(response, form)

            if len(form_names) == 1:
                formatted_responses.extend(formatted_dicts)
                return formatted_responses         


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


