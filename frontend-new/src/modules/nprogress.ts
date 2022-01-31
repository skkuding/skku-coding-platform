import NProgress from 'nprogress'
import type { ViteSSGContext } from 'vite-ssg'

export const install = ({ isClient, router }: ViteSSGContext) => {
  if (isClient) {
    router.beforeEach(() => { NProgress.start() })
    router.afterEach(() => { NProgress.done() })
  }
}
