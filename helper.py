""" Helper functions to format input """


def strip_format(form):
    """Clear formatting from requested form"""

    form = form.replace('+', ' ')
    return form  


def format_form_request(requested_forms):
    """Formats list of forms for url"""

    if len(requested_forms) > 1:
        forms_for_url = [form.replace(' ', '+') for form in requested_forms]
    elif len(requested_forms) == 1:
        forms_for_url = [str(form).replace(' ', '+') for form in requested_forms]
    else:
        print("\nNo forms requested.")
        return
    return forms_for_url


def clear_list(lst):
    """Clears list for next query"""
    lst.clear()
    return


