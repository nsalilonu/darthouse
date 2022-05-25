import sqlite3

DATABASE_NAME = "darthouseSQLite.db"
connection = sqlite3.connect(DATABASE_NAME)
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS reviews")

createTable = '''CREATE TABLE reviews (
					request_id TEXT PRIMARY KEY,
					address TEXT NOT NULL,
					start_date TEXT NOT NULL,
					end_date TEXT NOT NULL,
					cleanliness TEXT,
					cleanliness_comments TEXT,
					noise TEXT,
					noise_comments TEXT,
					responsive TEXT,
					responsive_comments TEXT,
					landlord TEXT,
					landlord_comments TEXT,
					pest TEXT,
					pest_comments TEXT,
					safety TEXT,
					safety_comments TEXT,
					appliance TEXT,
					appliance_comments TEXT,
					transportBool INTEGER,
					transport TEXT,
					transport_comments TEXT,
					furnishedBool INTEGER,
					furnished TEXT,
					furnished_comments TEXT,
					utility INTEGER,
					final_thoughts TEXT
					 ); '''
cursor.execute(createTable)
print("Table is ready")
connection.close()
