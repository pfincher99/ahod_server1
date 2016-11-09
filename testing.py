import demoapp
import unittest


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        demoapp.app.config['TESTING'] = True
        self.app = demoapp.app.test_client()

    def test_correct_response(self):
        resp = self.app.get('/hello/world')
        self.assertEquals(resp.status_code, 200)

    def test_correct_content(self):
        resp = self.app.get('/hello/world')
        self.assertEquals(resp.data, '"Hello World! This is the dev site"\n')

    def test_alert_response(self):
        resp = self.app.get('/alert')
        self.assertEquals(resp.status_code, 200)

    def test_alert_content(self):
        resp = self.app.get('/alert')
        self.assertEquals(resp.data, '"Alert Received"\n')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()