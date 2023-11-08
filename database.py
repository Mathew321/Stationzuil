import psycopg2

hostname = "localhost"
database = "postgres"
username = "postgres"
pwd = ""
port_id = "5432"
conn = None
cur = None

def data_manipulation(operation):
    try:
        conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id)
        cur = conn.cursor()

        # Fetch login records
        if operation == 0:
            cur.execute("""SELECT station_city FROM station_service;""")
            listOfRecords = []
            for record in cur.fetchall():
                listOfRecords.append(record[0])
            return listOfRecords
        elif operation == 1:
            script = """SELECT * FROM gebruiker;"""
            cur.execute(script)
            listOfRecords = []
            for record in cur.fetchall():
                listOfRecords.append(record)
            return listOfRecords
        elif operation == 2:
            pass # TODO SEND TO DATABASE

        conn.commit()
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
data_manipulation(0)