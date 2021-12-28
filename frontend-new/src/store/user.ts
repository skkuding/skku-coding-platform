import { defineStore } from 'pinia'
import { reactive, computed } from 'vue'
import api from '~/modules/axios'
import { ADMIN_TYPE, PROBLEM_PERMISSION } from '~/constants'
import type { AdminType, User, Profile } from '~/types'

export const useUserStore = defineStore('user', () => {
  const profile = reactive<Profile>({})

  const user = computed<User | Record<string, never>>(() => profile.user || {})
  const isAuthenticated = computed<boolean>(() => !!user.value.id)
  const adminType = computed<AdminType>(() => user.value.admin_type)
  const isAdmin = computed<boolean>(() =>
    adminType.value === ADMIN_TYPE.ADMIN ||
    adminType.value === ADMIN_TYPE.SUPER_ADMIN
  )
  const isSuperAdmin = computed<boolean>(
    () => adminType.value === ADMIN_TYPE.SUPER_ADMIN
  )
  const hasProblemPermission = computed<boolean>(() =>
    user.value.problem_permission === PROBLEM_PERMISSION.NONE
  )

  const getProfile = async () => {
    const res = await api.get('profile/')
    Object.assign(profile, res || {})
  }

  const changeProfile = (newProfile: Profile) => {
    Object.assign(profile, newProfile)
    // TODO: assign `localStorage`
  }

  const clearProfile = async () => {
    Object.assign(profile, {})
    // TODO: clear `localStorage`
  }

  return {
    profile,
    user,
    isAuthenticated,
    isAdmin,
    isSuperAdmin,
    hasProblemPermission,
    getProfile,
    changeProfile,
    clearProfile
  }
})
