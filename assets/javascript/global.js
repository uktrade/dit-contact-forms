var Button = require("govuk-frontend/govuk/components/button/button.js");
var ErrorSummary = require("govuk-frontend/govuk/components/error-summary/error-summary.js");
var CookiePolicy = require("./modules/cookie-policy");
var Sentry = require("@sentry/browser");

// include Sentry initialisation for frontend errors
// Next comment needed to define globals for format checks
/*global SENTRY_DSN, SENTRY_ENVIRONMENT*/
Sentry.init({
  dsn: SENTRY_DSN,
  environment: SENTRY_ENVIRONMENT,
  tracesSampleRate: 1.0,
});

var cookiePolicy = new CookiePolicy();
cookiePolicy.initBanner(".app-cookie-banner", ".js-accept-cookie", "cookies");

// accessibility feature
new Button(document).init();

// error summary focus on page load
var $errorSummary = document.querySelector('[data-module="error-summary"]');
if ($errorSummary) {
  new ErrorSummary($errorSummary).init();
}
