import { describe, expect, test } from 'vitest'
import { render } from '@testing-library/vue'
import FooterMain from './FooterMain.vue'

describe('Atom - FooterMain', () => {
  test('should render', () => {
    const { html } = render(FooterMain)
    expect(html()).toMatchSnapshot()
  })
})
