from locust import HttpUser, task, between

class MyLocust(HttpUser):
    wait_time = between(0,1)
    userid = 1

    def on_start(self):
        self.testcode = 1
        
    @task
    def index(self):
        temp = "root" + str(self.userid)
        self.userid = (self.userid) % 100 + 1
        print(temp)

        response = self.client.get("/api/profile")
        self.csrftoken = response.cookies["csrftoken"]

        response = self.client.post("/api/login", data = {"username":temp, "password":"1"}, headers={'X-CSRFToken': self.csrftoken, 'Referer': 'http://127.0.0.1/'})
        print(response.json())

        sessionid = response.cookies["sessionid"]
        response = self.client.post("/api/submission", data = {"problem_id" : 1, "language" : "C", "code":f"{self.testcode}"}, headers={'X-CSRFToken': self.csrftoken, 'Cookie': f"sessionid={sessionid}; csrftoken={self.csrftoken}", 'Referer': 'http://127.0.0.1/'})
        self.testcode += 1
        print(response.json())

        self.client.get("/logout")
