""" IRS Form Search """

from requests_html import HTMLSession
from form_scraper import dict_list_to_json
import json

# requests-html object
session = HTMLSession()

requested_forms = []


def search_prompt():
    """Gets user tax forms names and formats for IRS url"""

    print('\nPlease enter the tax form number separated by a comma followed by a space: ')
    print('(ex: Form W-2, Form 1095-C, Form W-3, etc)\n')
    form_names = input('>> Forms: ').split(', ')
    if form_names == ['']:
        return "\nInvalid entry."
    else:
        requested_forms.extend(form_names) 
        return requested_forms


def jsonify_list_of_dicts(dict_list):
    """Convert list of dictionaries to JSON"""

    if dict_list == []:
        return "\nInvalid entry. Search unsuccessful.\n"
       
    else:
        json_format = json.dumps(dict_list, indent=4)
        print('\n************************************')
        print('********* Search Completed *********')
        print('************************************\n')
        return json_format