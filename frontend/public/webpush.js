import { register, unregister } from 'register-service-worker'

function loadVersionBrowser (userAgent) {
  const ua = userAgent
  let tem
  let M = ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || []
  if (/trident/i.test(M[1])) {
    tem = /\brv[ :]+(\d+)/g.exec(ua) || []
    return { name: 'IE', version: (tem[1] || '') }
  }
  if (M[1] === 'Chrome') {
    tem = ua.match(/\bOPR\/(\d+)/)
    if (tem != null) {
      return { name: 'Opera', version: tem[1] }
    }
  }
  M = M[2] ? [M[1], M[2]] : [navigator.appName, navigator.appVersion, '-?']
  if ((tem = ua.match(/version\/(\d+)/i)) != null) {
    M.splice(1, 1, tem[1])
  }
  return {
    name: M[0],
    version: M[1]
  }
};
function urlBase64ToUint8Array (base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4)
  var base64 = (base64String + padding)
    .replace(/-/g, '+')
    .replace(/_/g, '/')

  var rawData = window.atob(base64)
  var outputArray = new Uint8Array(rawData.length)

  for (var i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i)
  }
  return outputArray
};
function getCookie (cookieName) {
  var cookieValue = null
  if (document.cookie) {
    var array = document.cookie.split((escape(cookieName) + '='))
    if (array.length >= 2) {
      var arraySub = array[1].split(';')
      cookieValue = unescape(arraySub[0])
    }
  }
  return cookieValue
};
function requestPOSTTOServer (data) {
  return fetch('http://localhost/api/wp_device', {
    method: 'post',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
    body: JSON.stringify(data),
    credentials: 'include'
  })
};
const applicationServerPublicKey = 'BGF1mrCiiWOYNa2v0vOm4H0GqXTjnJLLxDo4ZFC55FDI0zop58HRrV1e1_Bz3-2eQ6YbG6QSKiXOVz8p2chqL3M'
let isSubscribe = false
export default {
  async subscribe (username) {
    const applicationServerKey = urlBase64ToUint8Array(applicationServerPublicKey)
    register(`${process.env.BASE_URL}sw.js`, {
      async ready (registration) {
        try {
          const browser = loadVersionBrowser(navigator.userAgent)
          const sub = await registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: applicationServerKey
          })
          const endpointParts = sub.endpoint.split('/')
          const registrationId = endpointParts[endpointParts.length - 1]
          const data = {
            browser: browser.name.toUpperCase(),
            p256dh: btoa(String.fromCharCode.apply(null, new Uint8Array(sub.getKey('p256dh')))),
            auth: btoa(String.fromCharCode.apply(null, new Uint8Array(sub.getKey('auth')))),
            name: username,
            registration_id: registrationId
          }
          const res = await requestPOSTTOServer(data)
          isSubscribe = res.ok // res.data.error가 안 돼있어서, 상태코드로 대충 처리해놓았다.
        } catch (err) {
        }
      }
    })
  },
  async unregister () {
    unregister()
    isSubscribe = false
  },
  isSubscribe () {
    return isSubscribe
  }
}
