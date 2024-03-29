import psycopg2 as psql

class DATABASE:
    @staticmethod
    def connect(query, type):
        database = psql.connect(
            database = 'cm_system', # Card Management System Database
            host = 'localhost',
            user = 'postgres',
            password = '1605'
        )

        cursor = database.cursor()
        cursor.execute(query)

        if type in ['select']:
            selected_data = cursor.fetchall()
            return selected_data

        elif type in ['insert', 'delete', 'alter', 'create', 'update']:
            database.commit()
            return 'successful completion'