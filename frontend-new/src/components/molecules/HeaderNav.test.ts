import { describe, test, expect } from 'vitest'
import { render } from '@testing-library/vue'
import HeaderNav from './HeaderNav.vue'

describe('Molecule - HeaderNav.vue', () => {
  test('should render', () => {
    const { html } = render(HeaderNav)
    expect(html()).toMatchSnapshot()
  })
})
