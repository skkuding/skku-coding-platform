import { ref, reactive } from 'vue'
import { useLocalStorage } from '@vueuse/core'
import api from '~/modules/axios'
import type { Router } from 'vue-router'
import type { Profile } from '~/types'

export const isAuthenticated = useLocalStorage('isAuthenticated', false)

export const useLogin = (router: Router) => {
  const loading = ref(false)
  const errorMessage = ref('')
  const form = reactive({ username: '', password: '' })

  const login = async () => {
    loading.value = true

    const { data, error } = await api.post('login/', form)

    if (error) {
      errorMessage.value = data
    } else {
      errorMessage.value = ''
      isAuthenticated.value = true
      await api.get<Profile>('profile/').then((x) => x.data)
      await router.push('/')
    }

    loading.value = false
  }

  return { loading, errorMessage, form, login }
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
