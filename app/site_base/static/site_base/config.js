// config for htmx
if (!(typeof myVar === 'undefined')) {
    htmx.config.includeIndicatorStyles = false
    htmx.config.allowEval = false
    htmx.config.selfRequestsOnly = false
}

// enable bootstrap popups
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
