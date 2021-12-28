import type { AdminType, ProblemPermission } from './types'

export const ADMIN_TYPE: Record<string, AdminType> = {
  REGULAR_USER: 'Regular User',
  ADMIN: 'Admin',
  SUPER_ADMIN: 'Super Admin'
}

export const PROBLEM_PERMISSION: Record<string, ProblemPermission> = {
  NONE: 'None',
  OWN: 'Own',
  ALL: 'All'
}
