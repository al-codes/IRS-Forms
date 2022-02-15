""" IRS Form Download """

import requests
import os


requested_dl_forms = []

# min_year [0], max_year[1]
desired_year_range = []

   
def download_prompt():
    """Gets tax form name and year range for download"""
    
    print('\nPlease enter a tax form you would like to download to a pdf format.')
    print('(ex. Form: Form W-3  --  year format is: YYYY)\n')
    requested_form = input('>> Form: ').rstrip()
    min_year = input('\n>> Please enter the minimum year: ')
    max_year = input('\n>> Please enter the maximum year: ')
    requested_dl_forms.append(requested_form)
    desired_year_range.append(min_year)
    desired_year_range.append(max_year)
    return 


def collect_all_pdfs(filtered_forms):
    """Collects pdfs within an inclusive range of years"""

    min_year = desired_year_range[0]
    max_year = desired_year_range[1]
    pdf_dict = {}
    try:
        if len(min_year) < 4 or len(max_year) < 4 or min_year.isalpha() or max_year.isalpha():
            print("\nInvalid year.")
    
        else:
            for form in filtered_forms:
                pdfs = form.links
                pdfs = str(pdfs)
                form_details = form.text.split('\n')
                form_number = form_details[0]
                year = int(form_details[2])
                desired_form = form_number.replace('+', ' ')
                if form_number == desired_form and int(min_year) <= year <= int(max_year):
                    pdf_dict[f'{desired_form} - {year}'] = pdfs[2:-2]
            return pdf_dict
    except ValueError: "invalid literal for int() with base 10:"
    

def download_pdfs(pdf_dict):
    """Download pdfs to correct directory"""

    if not pdf_dict:
        print('\nInvalid entry. Download unsuccessful.\n')
    elif desired_year_range == ['', ''] or len(desired_year_range[0]) < 4 or len(desired_year_range[1]) < 4:
        print('\nInvalid year range. Download unsuccessful.\n')
    else:
        for form, link in pdf_dict.items():
            form_name = form.split(' -')[0]
            url = link
            response = requests.get(url)

            if not os.path.exists(form_name):
                os.mkdir(form_name)

            with open(f'{form_name}/{form}.pdf', 'wb') as f:
                f.write(response.content)
                
        print('\n************************************')
        print('All pdf files have been downloaded.')
        print('************************************')