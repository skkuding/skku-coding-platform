import { describe, expect, test } from 'vitest'
import { render } from '@testing-library/vue'
import FooterIconMail from './FooterIconMail.vue'

describe('Atom - FooterIconMail', () => {
  test('should render', () => {
    const { html } = render(FooterIconMail)
    expect(html()).toMatchSnapshot()
  })
})
