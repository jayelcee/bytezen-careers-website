import psycopg2

try:
    conn = psycopg2.connect(
        dbname='postgres',
        user='bytezen_careers_db_user',
        password='tQMQEPV4eK0QB8AvL7EhTDVS2YrmXRQt',
        host='dpg-cmp6tqol5elc73fn9e20-a.singapore-postgres.render.com',
        port='5432'
    )
    print("Connected to the database successfully.")
    # Rest of your code to work with the database
except psycopg2.OperationalError as e:
    print(f"Failed to connect to database: {e}")
