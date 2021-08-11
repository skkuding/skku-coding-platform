
// Example navigatorPush.service.js file

var getTitle = function (title) {
    if (title === "") {
            title = "New announcement";
    }
    return title;
};

var getNotificationOptions = function (message, message_tag) {
    var options = {
            body: message,
            icon: './img/logo.4d5d9bff.png',
            tag: message_tag,
            vibrate: [200, 100, 200, 100, 200, 100, 200]
    };
    return options;
};

self.addEventListener('install', function (event) {
    self.skipWaiting();
});

self.addEventListener('push', function(event) {
    console.log("Push is successful");
    try {
            // Push is a JSON
            var response_json = event.data.json();
            var title = response_json.title;
            var message = response_json.message;
            var message_tag = response_json.tag;
    } catch (err) {
            // Push is a simple text
            var title = "";
            var message = event.data.text();
            var message_tag = "";
    }
    self.registration.showNotification(getTitle(title), getNotificationOptions(message, message_tag));
    // Optional: Comunicating with our js application. Send a signal
    self.clients.matchAll({includeUncontrolled: true, type: 'window'}).then(function (clients) {
            clients.forEach(function (client) {
                    client.postMessage({
                            "data": message_tag,
                            "data_title": title,
                            "data_body": message});
                    });
    });
});