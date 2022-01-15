import { describe, expect, test } from 'vitest'
import { render } from '@testing-library/vue'
import FooterIconLink from './FooterIconLink.vue'

describe('Atom - FooterIconLink', () => {
  test('should render', () => {
    const { html } = render(FooterIconLink)
    expect(html()).toMatchSnapshot()
  })
})
