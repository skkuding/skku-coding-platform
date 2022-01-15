import { describe, expect, test } from 'vitest'
import { render } from '@testing-library/vue'
import FooterIconKakao from './FooterIconKakao.vue'

describe('Atom - FooterIconKakao', () => {
  test('should render', () => {
    const { html } = render(FooterIconKakao)
    expect(html()).toMatchSnapshot()
  })
})
