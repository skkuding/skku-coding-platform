export type AdminType = 'Regular User' | 'Admin' | 'Super Admin'
export type ProblemPermission = 'None' | 'Own' | 'All'

export interface User {
  // User
  id: number,
  username: string,
  email: string,
  major: string,
  admin_type: AdminType,
  problem_permission: ProblemPermission,
  create_time: string,
  last_login: string,
  is_disabled: boolean,

  // UserProfile
  acm_problems_status: object,
  oi_problems_status: object,
  real_name: string,
  avatar: string,
  language: string,
  accepted_number: number,
  total_score: number,
  submission_number: number
}

export interface Profile {
  user?: User
}
