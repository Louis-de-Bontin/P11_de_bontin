from locust import HttpUser, task


class ServerPerfTest(HttpUser):
    @task
    def index(self):
        response = self.client.get('/')

    @task
    def login(self):
        response = self.client.post('/showSummary', data={
            'email': 'john@simplylift.co'
        })

    @task
    def purchase_places(self):
        response = self.client.post('/purchasePlaces',data={
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '1'
        })