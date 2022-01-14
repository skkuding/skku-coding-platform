import { describe, test } from 'vitest'
import { render } from '@testing-library/vue'
import NavItem from './NavItem.vue'
import { createRouter, createWebHistory, RouterView } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: {
        template: 'Home Page'
      }
    },
    {
      path: '/somewhere',
      component: {
        template: 'Lead me to somewhere...'
      }
    }
  ]
})

describe('Atom - NavItem.vue', () => {
  test('should navigate', async () => {
    router.push('/')
    await router.isReady()

    const { findByText, getByText } = render(
      {
        template: `
          <NavItem to="/somewhere">
            Where?
          </NavItem>
          <RouterView />
        `,
        components: { NavItem, RouterView }
      },
      {
        global: {
          plugins: [router]
        }
      }
    )

    await findByText('Home Page')
    getByText('Where?').click()
    await findByText('Lead me to somewhere...')
  })
})
