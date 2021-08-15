// Example navigatorPush.service.js file
var getTitle = title => {
  if (title === '') {
    title = 'New accouncement'
  }
  return title
}
var getNotificationOptions = (message, messageTag) => {
  var options = {
    body: message,
    icon: './img/logo.4d5d9bff.png',
    tag: messageTag,
    vibrate: [200, 100, 200, 100, 200, 100, 200]
  }
  return options
}
self.addEventListener('install', function (event) {
  self.skipWaiting()
})
self.addEventListener('push', function (event) {
  console.log('Push is successful')
  try {
  // Push is a JSON
    var responseJson = event.data.json()
    var title = responseJson.title
    var message = responseJson.message
    var messageTag = responseJson.tag
  } catch (err) {
    // Push is a simple text
    title = ''
    message = event.data.text()
    messageTag = ''
  }
  self.registration.showNotification(getTitle(title), getNotificationOptions(message, messageTag))
  // Optional: Comunicating with our js application. Send a signal
  self.clients.matchAll({ includeUncontrolled: true, type: 'window' }).then(function (clients) {
    clients.forEach(function (client) {
      client.postMessage({
        data: messageTag,
        data_title: title,
        data_body: message
      })
    })
  })
})
