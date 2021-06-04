from ui_test.selectors.questionnaire import QUESTIONNAIRE
from ui_test.selectors.form import FORM


def select_questionnaire(browser, options):
    for key, value in options.items():
        browser.find_by_css(QUESTIONNAIRE[key][value]).click()
        browser.find_by_css(QUESTIONNAIRE["continue"]).click()


def submit_form(browser, options):
    browser.find_by_css(FORM["message"]).first.type(options["message"])
    browser.find_by_css(FORM["name"]).first.type(options["name"])
    browser.find_by_css(FORM["email"]).first.type(options["email"])
    browser.find_by_css(FORM["accept_terms"]).click()
    browser.find_by_css(QUESTIONNAIRE["continue"]).click()
