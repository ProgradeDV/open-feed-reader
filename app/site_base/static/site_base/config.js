// config for htmx
if (!(typeof htmx === 'undefined')) {
    htmx.config.includeIndicatorStyles = false
    htmx.config.allowEval = false
    htmx.config.selfRequestsOnly = true
}

// enable bootstrap popups
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
