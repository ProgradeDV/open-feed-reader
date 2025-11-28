// config for htmx
// enable bootstrap popups
function enable_all_tooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
}
enable_all_tooltips()
// listen for events to re enable all tooltips
document.body.addEventListener('htmx:afterRequest', enable_all_tooltips)


if (!(typeof htmx === 'undefined')) {
    htmx.config.includeIndicatorStyles = false
    htmx.config.allowEval = false
    htmx.config.selfRequestsOnly = true
}
