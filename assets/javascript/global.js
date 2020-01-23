var Details = require('govuk-frontend/govuk/components/details/details.js')
var Button = require('govuk-frontend/govuk/components/button/button.js')
var Accordion = require('govuk-frontend/govuk/components/accordion/accordion.js')
var ErrorSummary = require('govuk-frontend/govuk/components/error-summary/error-summary.js')
var common = require('govuk-frontend/govuk/common')
var Modal = require('./modules/modal')
var nodeListForEach = common.nodeListForEach
var CookiePolicy = require('./modules/cookie-policy');

var cookiePolicy = new CookiePolicy();
cookiePolicy.initBanner('.app-cookie-banner', '.js-accept-cookie', 'cookies');

// accessibility feature
new Button(document).init()

// details polyfill for MS browsers
var $details = document.querySelectorAll('details')
if ($details) {
    nodeListForEach($details, function ($detail) {
        new Details($detail).init()
    })
}

// Find all global accordion components to enhance.
var $accordions = document.querySelectorAll('[data-module="accordion"]')
nodeListForEach($accordions, function ($accordion) {
    new Accordion($accordion).init()
})



// error summary focus on page load
var $errorSummary = document.querySelector('[data-module="error-summary"]')
if ($errorSummary) {
    new ErrorSummary($errorSummary).init()
}

var $modals = document.querySelectorAll('[data-module="modal-dialogue"]')
if ($modals) {
    nodeListForEach($modals, function ($modal) {
        new Modal($modal).start()
    })
}

module.exports = {
    bindCookiePolicyForm: cookiePolicy.bindForm

}
