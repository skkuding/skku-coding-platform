import { describe, test, expect } from 'vitest'
import { render } from '@testing-library/vue'
import HeaderMobileNav from './HeaderMobileNav.vue'

describe('Molecule - HeaderMobileNav.vue', () => {
  test('should render', () => {
    const { html } = render(HeaderMobileNav)
    expect(html()).toMatchSnapshot()
  })

  test('should show if active', () => {
    const { html } = render(HeaderMobileNav, {
      props: {
        active: true
      }
    })
    expect(html()).toMatchSnapshot()
  })
})
