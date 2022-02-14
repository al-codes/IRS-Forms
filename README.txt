IRS Form Scraper Coding Challenge


Python Version
Python 3.8.5


Libraries Used
requests-HTML
Requests
JSON
OS 


Installation Guide

Set Up

1. Download zip drive to your hard drive. The zip file contains this README, 5 python files
   and a requirements.txt file.

2. In the tereminal, under the project directory, you can set up a virtual environment by entering:
   $ virtualenv env
   $ source env/bin/activate

   * If you don't have virtualenv installed, you can install by entering the following:
   $ pip install virtualenv   (or pip3 depending on your version of pip installer)

3. Install dependencies from requirements.txt with:
   $ pip install -r requirements.txt

* If you choose not to set up this way, you can download the libraries needed by entering:
    $ pip install requests
    $ pip install requests-HTML


Running the Script

Once you have downloaded the files and downloaded all of the necessary libraries, 
run the script by entering:
       
       $ python3 main.py 


A menu will be displayed, prompting you to select which utility you would like to use -

        Please select which utility you would like to use:

        1)View tax form details in json format
        2)Download a tax form given a range of years

        (Enter 1, 2 or type QUIT to exit program)

Utility 1 

Enter '1' to view tax form details. Inputs are described by the following prompt:

        Please enter the tax form number separated by a comma followed by a space: 
        (ex: Form W-2, Form 1095-C, Form W-3, etc)

        >> Forms: Form W-2

Output will display a success message and all forms requested as json in this format:

        [
            {
                "form_number": "Form W-2",
                "form_title": "Wage and Tax Statement (Info Copy Only)",
                "min_year": 1954,
                "max_year": 2022
            },
            ...
        ]


Utility 2

Enter '2' to enter a tax form name and a range of years (inclusive) to be downloaded.

Prompts for input are provided as in the exampled below -

            Please enter a tax form you would like to download to a pdf format.
            (ex. Form: Form W-3  --  year format is: YYYY)

            >> Form: Form W-2

            >> Please enter the minimum year: 2020

            >> Please enter the maximum year: 2022

Output will display a success message and pdf file(s) will be downloaded to a 
subdirectory under the script's main directory.


To QUIT the program, you can type 'quit' (not case sensitive).


Improvements and Feedback 

My next steps towards improving the script would be to add code to 
handle errors for an invalid year range and invalid form inputs. 

I enjoyed this challenge as it was a good review of Python and I 
got to use a library that I had never used before, requests-HTML,
which I found to be a great tool for this project. 

Thank you for the opportunity!






