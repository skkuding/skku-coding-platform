/// <reference types="cypress" />

// describe -> context -> it
context('When user tries to submit a problem (not in contest)', () => {
  beforeEach(() => {
    cy.loginSuperAdmin()
    cy.visit('problem')
  })
  // TODO: make it independent from admin_problem_spec (anti-pattern)
  it('Submit Code', () => {
    cy.fixture('problem-example').then((problemExample) => {
      cy.get('tbody > tr > .problem-title-field').contains(problemExample.problem.title).click()
      cy.get('[data-cy="toggle-language"] > .dropdown-toggle-split').click()
      cy.get('[data-cy="select-langauge"]').contains(problemExample.solution.language).click()
      cy.get('.CodeMirror-code').click().type(problemExample.solution.code, { delay: 0 })
      cy.get('[data-cy="button-submit"]').click()
    })
  })
})
