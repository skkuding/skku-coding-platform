import { describe, test } from 'vitest'
import { render } from '@testing-library/vue'
import HeaderMobileButton from './HeaderMobileButton.vue'

describe.only('Atom - HeaderMobileButton.vue', () => {
  test('should render', () => {
    const { getByRole } = render(HeaderMobileButton)
    getByRole('button')
  })
})
