import { createEventHook } from '@vueuse/core'

export interface Toast {
  message: string
  variant?: 'info' | 'success' | 'warning' | 'danger'
  duration?: number
}

const triggerToast = createEventHook<Toast>()

export const useToast = () => {
  const addToast = (option: Toast) => {
    triggerToast.trigger(option)
  }

  return {
    onTrigger: triggerToast.on,
    addToast
  }
}
