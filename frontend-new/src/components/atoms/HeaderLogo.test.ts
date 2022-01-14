import { describe, test } from 'vitest'
import { render } from '@testing-library/vue'
import HeaderLogo from './HeaderLogo.vue'
import { createRouter, createWebHistory, RouterView } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: {
        template: 'home'
      }
    },
    {
      path: '/foo',
      component: {
        template: 'bar'
      }
    }
  ]
})

describe('Atom - HeaderLogo.vue', () => {
  // TODO: DOM render is not cleared correctly before each test.
  // This issue is due to Vitest.
  test.todo('should render', () => {
    const { getByRole } = render(HeaderLogo)
    getByRole('img')
  })

  test('should navigate', async () => {
    router.push('/foo')
    await router.isReady()

    const { findByText, getByAltText } = render(
      {
        template: `
          <HeaderLogo />
          <RouterView />
        `,
        components: { HeaderLogo, RouterView }
      },
      {
        global: {
          plugins: [router]
        }
      }
    )

    await findByText('bar')
    getByAltText('Sungkyunkwan University').click()
    await findByText('home')
  })
})
