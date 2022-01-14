import { describe, test, expect } from 'vitest'
import { render } from '@testing-library/vue'
import HeaderMain from './HeaderMain.vue'

describe('Organism - HeaderMain.vue', () => {
  test.todo('should render', () => {
    const { html } = render(HeaderMain)
    expect(html()).toMatchSnapshot()
  })

  test('toggle mobile navigation', () => {
    const { html, getByRole } = render(HeaderMain)
    getByRole('button').click()
    expect(html()).toMatchSnapshot()
  })
})
