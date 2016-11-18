import demoapp
import unittest
import os
import requests

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        demoapp.app.config['TESTING'] = True
        self.app = demoapp.app.test_client()

    # Test to confirm Flask is running
    def test_alert_response(self):
        resp = self.app.get('/alert')
        self.assertEquals(resp.status_code, 200)

    def test_alert_content(self):
        resp = self.app.get('/alert')
        self.assertEquals(resp.data, '"Alert Received on Master Branch"\n')

    # Test to confirm that the initial database exists
    def test_db_exist(self):
        database = os.path.isfile('ahod.db')
        self.assertEquals(database,True)

    # Test to confirm Spark Room Exists

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
