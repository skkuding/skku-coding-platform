/// <reference types="cypress" />

describe('General Problem', () => {
  context('When Admin tries to go Problem Tab', () => {
    before(() => {
      cy.loginSuperAdmin()
      cy.visit('admin')
    })
    it('should go to problem list page', () => {
      cy.get('.list-group-item').contains('Problem').click()
      cy.get('.list-group-item').contains('Problem List').click()
      cy.url().should('include', '/admin/problems')
    })
  })
  context('When Admin tries to create problem', () => {
    beforeEach(() => {
      cy.loginSuperAdmin()
      let id = -1
      cy.intercept('GET', '/api/admin/problem/*', (req) => {
        req.continue((res) => {
          for (const result of res.body.data.results) {
            if (result._id === 'C1') {
              id = result.id
              res.send()
            }
          }
        })
      }).as('getAdminProblem')
      cy.visit('/admin/problems')
      // TODO: Make initial state using db conmmand, not using conditional API or UI control -- This code little bit anti-pattern
      cy.wait('@getAdminProblem').then(() => {
        if (id !== -1) {
          cy.request('DELETE', 'api/admin/problem/?id=' + id).as('initiate')
        }
      })
      cy.contains('+ Create').click()
    })
    // TODO: Validate problem form
    it('should create a new problem - with minimum fields', () => {
      cy.intercept('GET', '/api/admin/problem/?*', (req) => {
        req.reply()
      }).as('getAdminProblem')

      cy.fixture('problem-example').then((problemExample) => {
        cy.get('#input-display-id').type('C1')
        cy.get('#input-title').type(problemExample.problem.title)
        cy.get('[data-cy="input-description"] > .ProseMirror').invoke('text', problemExample.problem.description)
        cy.get('[data-cy="input-input-description"] > .ProseMirror').invoke('text', problemExample.problem.input_description)
        cy.get('[data-cy="input-output-description"] > .ProseMirror').invoke('text', problemExample.problem.output_description)

        cy.get('.tag-dropdown').contains('tag').click()
        for (const tag of problemExample.problem.tags) {
          cy.get('[data-cy="input-add-tag"]').type(tag)
          cy.get('[data-cy="button-add-tag"]').click()
        }

        cy.get('[data-cy="input-input-samples1"]').type(problemExample.problem.samples[0].input)
        cy.get('[data-cy="input-output-samples1"]').type(problemExample.problem.samples[0].output)

        cy.get('[data-cy="input-input-testcase1"]').type(problemExample.problem.testcases[0].input)
        cy.get('[data-cy="input-output-testcase1"]').type(problemExample.problem.testcases[0].output)

        cy.get('[data-cy="button-save"]').click()

        cy.url().should('include', '/admin/problems')

        cy.visit('admin/problems')
        cy.wait('@getAdminProblem')
        cy.contains('C1').parent()
          .next().should('have.text', problemExample.problem.title)
          .next().should('have.text', 'root')
      })
    })
    // TODO: Make test that posts a problem with maximum fields
  })
})
