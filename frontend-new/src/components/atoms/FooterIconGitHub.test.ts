import { describe, expect, test } from 'vitest'
import { render } from '@testing-library/vue'
import FooterIconGitHub from './FooterIconGitHub.vue'

describe('Atom - FooterIconGitHub', () => {
  test('should render', () => {
    const { html } = render(FooterIconGitHub)
    expect(html()).toMatchSnapshot()
  })
})
