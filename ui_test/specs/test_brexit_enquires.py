import pytest
from ui_test.user_flows import select_questionnaire, submit_form


def test_brexit_enquires_goods(browser):
    select_questionnaire(browser, {'step1': 'brexit_enquiries', 'step2': 'goods'})
    assert(browser.is_text_present('Step 3 of 3'))
    assert(browser.is_text_present('Your details'))


def test_brexit_enquires_other(browser):
    select_questionnaire(browser, {'step1': 'brexit_enquiries', 'step2': 'other'})
    assert(browser.is_text_present('Step 3 of 3'))
    assert(browser.is_text_present('Your details'))
