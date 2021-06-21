var Button = require("govuk-frontend/govuk/components/button/button.js");
var ErrorSummary = require("govuk-frontend/govuk/components/error-summary/error-summary.js");
var CookiePolicy = require("./modules/cookie-policy");

var cookiePolicy = new CookiePolicy();
cookiePolicy.initBanner(".app-cookie-banner", ".js-accept-cookie", "cookies");

// accessibility feature
new Button(document).init();

/* eslint-disable-next-line */
broke_call();

// error summary focus on page load
var $errorSummary = document.querySelector('[data-module="error-summary"]');
if ($errorSummary) {
  new ErrorSummary($errorSummary).init();
}
