Cypress.Commands.add('loginSuperAdmin', () => {
  cy.visit('')
  cy.getCookie('csrftoken')
    .should('exist')
    .then((csrftoken) => {
      cy.request({
        method: 'post',
        url: 'api/login/',
        body: {
          username: 'root',
          password: 'rootroot'
        },
        headers: {
          'X-CSRFToken': csrftoken.value
        }
      })
    })
  const getStore = () => cy.window().its('app.$store')
  getStore().then(store => {
    store.dispatch('getProfile')
  })
})

// TODO: Register, Login by general user
