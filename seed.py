"""Add one fictional sample user if the database is empty."""
import database

database.create_db_table()
if not database.get_users():
    database.insert_user(dict(name='Maya Haddad', email='maya@example.com',
                              phone='01-555-0101', address='Hamra, Beirut', country='Lebanon'))
print(f'{len(database.get_users())} user(s) in {database.DATABASE.name}')
