import { ref, reactive } from 'vue'
import { useLocalStorage } from '@vueuse/core'
import api from '~/modules/axios'
import { useToast } from '~/composables/toast'
import type { Router } from 'vue-router'

export const isAuthenticated = useLocalStorage('isAuthenticated', false)

export const useLogin = (router: Router) => {
  const loading = ref(false)
  const form = reactive({ username: '', password: '' })

  const login = async () => {
    loading.value = true

    const { data, error } = await api.post('login/', form)

    if (error) {
      useToast().addToast({ message: data, variant: 'danger' })
    } else {
      isAuthenticated.value = true
      await router.push('/')
    }

    loading.value = false
  }

  return { loading, form, login }
}

export const useLogout = (router: Router) => {
  const loading = ref(false)

  const logout = async () => {
    loading.value = true

    await api.get('logout/')
    isAuthenticated.value = false
    router.push('/')

    loading.value = false
  }

  return { loading, logout }
}
