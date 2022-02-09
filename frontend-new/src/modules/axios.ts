import axios, { AxiosInstance, AxiosRequestConfig } from 'axios'

type APIResponse<T> = {
  error: string
  data: T
}

interface APIInstance extends AxiosInstance {
  get<T = string, R = APIResponse<T>>(
    url: string,
    config?: AxiosRequestConfig
  ): Promise<R>
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  post<T = string, R = APIResponse<T>, D = any>(
    url: string,
    data?: D,
    config?: AxiosRequestConfig<D>
  ): Promise<R>
}

const api: APIInstance = axios.create({
  baseURL: '/api',
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken'
})

api.interceptors.response.use(
  (response) => {
    // TODO: handle authorization required api
    return response.data
  },
  (error) => {
    throw new Error(error)
  }
)

export default api
