import pytest
from ui_test.user_flows import select_questionnaire, submit_form


def test_brexit_enquires_goods(browser):
    select_questionnaire(browser, {'step1': 'brexit_enquiries', 'step2': 'goods'})
    submit_form(browser, {'message': 'Automated test message', 'name': 'Export goods', 'email': 'somegov@email.com'})
    assert(browser.is_text_present('Your enquiry has been submitted successfully'))
    assert(browser.is_text_present('Thank you for your enquiry'))


def test_brexit_enquires_other(browser):
    select_questionnaire(browser, {'step1': 'brexit_enquiries', 'step2': 'other'})
    submit_form(browser, {'message': 'Automated test message', 'name': 'Export other', 'email': 'somegov@email.com'})
    assert(browser.is_text_present('Your enquiry has been submitted successfully'))
    assert(browser.is_text_present('Thank you for your enquiry'))
