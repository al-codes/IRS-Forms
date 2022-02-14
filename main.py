from form_scraper import format_all_responses, filter_responses
from helper import *
from search_forms import *
from dl_forms import *

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

        search_prompt()
        forms_for_url = format_form_request(requested_forms)
        format_all_responses(forms_for_url)
        print(jsonify_list_of_dicts(dict_list_to_json))
        
        # clear lists for next query
        clear_list(requested_forms)
        clear_list(dict_list_to_json)
        

    # UTILITY 2 - DOWNLOAD FORMS TO PDF 
    elif user_request == '2':

        download_prompt()
        form_for_url = format_form_request(requested_dl_forms)
        parsed_forms = format_all_responses(form_for_url)
        filtered_pdfs = filter_responses(parsed_forms, requested_dl_forms)
        all_pdfs = collect_all_pdfs(filtered_pdfs)
        download_pdfs(all_pdfs)

        # clear lists for next query
        clear_list(requested_dl_forms)
        clear_list(desired_year_range)
        clear_list(dict_list_to_json)
        

    # QUIT PROGRAM
    elif user_request == 'quit':
        print('Bye!')
        break
    