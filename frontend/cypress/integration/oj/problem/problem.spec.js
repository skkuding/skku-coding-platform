/// <reference types="cypress" />

context('Problem', () => {
  beforeEach(() => {
    cy.visit('')
    cy.loginSuperAdmin()
  })
  it('equal', () => {
    cy.get('dropdown-item').contains('Management').click()
  })
})
