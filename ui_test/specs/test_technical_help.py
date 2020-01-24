import pytest
from ui_test.user_flows import select_questionnaire, submit_form


def test_technical_help(browser):
    select_questionnaire(browser, {'step1': 'help'})
    submit_form(browser, {'message': 'Automated test message', 'name': 'Export goods', 'email': 'somegov@email.com'})

    assert(browser.is_text_present('Your enquiry has been submitted successfully'))
    assert(browser.is_text_present('Thank you for your enquiry'))


def test_success_page_back_link(browser):
    select_questionnaire(browser, {'step1': 'help'})
    submit_form(browser, {'message': 'Automated test message', 'name': 'Export goods', 'email': 'somegov@email.com'})
    browser.links.find_by_text('find information about exporting to the UK').click()
    
    assert(browser.is_text_present('What would you like to ask us about or give feedback on?'))
