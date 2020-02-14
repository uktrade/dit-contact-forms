import pytest
from ui_test.selectors.questionnaire import QUESTIONNAIRE
from ui_test.selectors.form import FORM
from ui_test.user_flows import select_questionnaire, submit_form


def test_export_from_uk_custom(browser):
    select_questionnaire(browser, {'step1': 'export_from_uk', 'step2': 'custom'})
    assert(browser.is_text_present('Customs General Enquiry Form'))


def test_export_from_uk_validation_form(browser):
    select_questionnaire(browser, {'step1': 'export_from_uk', 'step2': 'other'})
    browser.find_by_css(QUESTIONNAIRE['continue']).click()
    assert(browser.is_element_present_by_css(FORM['validation']['message']))
    assert(browser.is_element_present_by_css(FORM['validation']['email']))
    assert(browser.is_element_present_by_css(FORM['validation']['name']))
