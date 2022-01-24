// ***********************************************************
// This example support/index.js is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

import './commands'

Cypress.Cookies.defaults({
  preserve: ['csrftoken', 'session_id']
})

Cypress.Commands.overwrite('request', (originalFn, ...args) => {
  let options = {}
  if (typeof args[0] === 'object' && args[0] !== null) {
    options = args[0]
  } else if (args.length === 1) {
    [options.url] = args
  } else if (args.length === 2) {
    [options.method, options.url] = args
  } else if (args.length === 3) {
    [options.method, options.url, options.body] = args
  }
  cy.getCookie('csrftoken')
    .should('exist')
    .then((csrftoken) => {
      const defaults = {
        headers: {
          'X-CSRFToken': csrftoken.value
        }
      }
      return originalFn({ ...defaults, ...options, ...{ headers: { ...defaults.headers, ...options.headers } } })
    })
})
