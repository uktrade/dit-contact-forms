import pytest
from ui_test.selectors.questionnaire import QUESTIONNAIRE


def test_export_from_uk_custom(browser):
    select_questionnaire(browser, {'step1': 'export_from_uk', 'step2': 'custom'})

    assert(browser.is_text_present('Customs General Enquiry Form'))

def select_questionnaire(browser, options):
    for key, value in options.items():
        browser.find_by_css(QUESTIONNAIRE[key][value]).click()
        browser.find_by_css(QUESTIONNAIRE['continue']).click()
