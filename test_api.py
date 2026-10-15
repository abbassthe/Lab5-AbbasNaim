"""API tests use a temporary database, leaving database.db untouched."""
import tempfile
import unittest
from pathlib import Path
import database
from app import app

USER = dict(name='Maya Haddad', email='maya@example.com', phone='01-555-0101',
            address='Hamra, Beirut', country='Lebanon')


class UserApiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.old_db = database.DATABASE
        database.DATABASE = Path(self.temp.name) / 'test.db'
        database.create_db_table()
        app.config['TESTING'] = True
        self.client = app.test_client()

    def tearDown(self):
        database.DATABASE = self.old_db
        self.temp.cleanup()

    def test_complete_crud(self):
        self.assertEqual(self.client.get('/api/users').json, [])
        response = self.client.post('/api/users/add', json=USER)
        self.assertEqual(response.status_code, 201)
        user = response.json
        self.assertIsInstance(user['user_id'], int)
        self.assertEqual(self.client.get(f"/api/users/{user['user_id']}").json, user)
        self.assertEqual(self.client.get('/api/users').json, [user])
        user['address'] = 'Achrafieh, Beirut'
        response = self.client.put('/api/users/update', json=user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, user)
        self.assertEqual(database.get_user_by_id(user['user_id']), user)
        self.assertEqual(self.client.delete(f"/api/users/delete/{user['user_id']}").status_code, 200)
        self.assertEqual(self.client.get('/api/users').json, [])
        self.assertEqual(self.client.get(f"/api/users/{user['user_id']}").status_code, 404)

    def test_missing_records(self):
        self.assertEqual(self.client.get('/api/users/999').status_code, 404)
        self.assertEqual(self.client.put('/api/users/update', json={**USER, 'user_id':999}).status_code, 404)
        self.assertEqual(self.client.delete('/api/users/delete/999').status_code, 404)

    def test_bad_json_and_content_type(self):
        self.assertEqual(self.client.post('/api/users/add', data='{', content_type='application/json').status_code, 400)
        self.assertEqual(self.client.post('/api/users/add', data='hello').status_code, 415)
        self.assertEqual(self.client.post('/api/users/add', json=[]).status_code, 400)
        self.assertEqual(database.get_users(), [])

    def test_required_fields(self):
        for field in database.FIELDS:
            for bad in (None, '', '  ', 42):
                with self.subTest(field=field, bad=bad):
                    self.assertEqual(self.client.post('/api/users/add', json={**USER, field:bad}).status_code, 400)
        self.assertEqual(database.get_users(), [])

    def test_update_rejects_bad_ids_without_changes(self):
        before = self.client.post('/api/users/add', json=USER).json
        for bad in (None, True, 0, -1, '1'):
            self.assertEqual(self.client.put('/api/users/update', json={**USER, 'user_id':bad}).status_code, 400)
        self.assertEqual(database.get_users(), [before])

    def test_sql_values_and_persistence(self):
        user = {**USER, 'name': "O'Neil'); DROP TABLE users; --"}
        saved = self.client.post('/api/users/add', json=user).json
        database.create_db_table()
        self.assertEqual(database.get_user_by_id(saved['user_id'])['name'], user['name'])
        self.assertEqual(len(database.get_users()), 1)

    def test_cors_and_method_handling(self):
        response = self.client.get('/api/users', headers={'Origin':'http://localhost:3000'})
        self.assertEqual(response.headers['Access-Control-Allow-Origin'], 'http://localhost:3000')
        response = self.client.post('/api/users')
        self.assertEqual(response.status_code, 405)
        self.assertIn('error', response.json)


if __name__ == '__main__':
    unittest.main()
