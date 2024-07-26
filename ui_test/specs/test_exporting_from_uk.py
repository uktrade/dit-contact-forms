from ui_test.selectors.questionnaire import QUESTIONNAIRE
from ui_test.selectors.form import FORM
from ui_test.user_flows import select_questionnaire
import pytest


def test_export_from_uk_validation_form(browser):
    select_questionnaire(browser, {"step1": "export_from_uk", "step2": "other"})
    browser.find_by_css(QUESTIONNAIRE["continue"]).click()
    assert browser.is_element_present_by_css(FORM["validation"]["message"])
    assert browser.is_element_present_by_css(FORM["validation"]["email"])
    assert browser.is_element_present_by_css(FORM["validation"]["name"])


@pytest.mark.skip(reason="Renable this test once sandbox is setup")
def test_export_from_uk_custom(browser):
    select_questionnaire(browser, {"step1": "export_from_uk", "step2": "custom"})
    assert browser.is_text_present("Sorry, this form is now unavailable.", wait_time=10)
