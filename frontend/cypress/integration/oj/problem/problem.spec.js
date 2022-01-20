/// <reference types="cypress" />

context('Problem', () => {
  beforeEach(() => {
    cy.loginSuperAdmin()
    cy.visit('problem')
  })
  it('Submit Code', () => {
    cy.get('.thead-light > tr > .problem-title-field').click()
  })
  // it('Make New problem - Minimum fields included', () => {
  //   cy.get('.list-group-item').contains('Problem').click()
  //   cy.get('.list-group-item').contains('Problem List').click()
  //   cy.contains('+ Create').click()
  //   const randomString = Math.random().toString(36)
  //   cy.get('#input-display-id').type(randomString.substring(3, 10))
  //   cy.get('#input-title').type('Make problem Test' + randomString.substring(3, 20))
  //   cy.get('[data-cy="input-description"] > .ProseMirror').type('Problem Description' + randomString.substring(3, 100))
  //   cy.get('[data-cy="input-input-description"] > .ProseMirror').type('Problem Input Description' + randomString.substring(3, 100))
  //   cy.get('[data-cy="input-output-description"] > .ProseMirror').type('Problem Output Description' + randomString.substring(3, 100))

  //   cy.get('.tag-dropdown').contains('tag').click()
  //   cy.get('[data-cy="input-add-tag"]').type(randomString.substring(3, 6))
  //   cy.get('[data-cy="button-add-tag"]').click()

  //   cy.get('[data-cy="input-input-samples1"]').type('Problem Input Description' + randomString.substring(3, 100))
  //   cy.get('[data-cy="input-output-samples1"]').type('Problem Output Description' + randomString.substring(3, 100))

  //   cy.get('[data-cy="input-input-testcase1"]').type('Problem Input Description' + randomString.substring(3, 100))
  //   cy.get('[data-cy="input-output-testcase1"]').type('Problem Output Description' + randomString.substring(3, 100))

  //   cy.get('[data-cy="button-save"]').click()
  // })
})
