import axios from 'axios'

const api = axios.create({
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
