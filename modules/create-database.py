import sqlite3

# Connect to the database
conn = sqlite3.connect("../carrier-data/cargo_cloud.db")
cursor = conn.cursor()

# Backup the current tables
# cursor.execute("CREATE TABLE IF NOT EXISTS carrier_info_backup AS SELECT * FROM carrier_info")
# cursor.execute("CREATE TABLE IF NOT EXISTS carrier_rating_backup AS SELECT * FROM carrier_rating")
#
# # Drop the existing tables
# cursor.execute("DROP TABLE IF EXISTS carrier_info")
# cursor.execute("DROP TABLE IF EXISTS carrier_rating")
#
# # Create a new carrier_info table with the updated structure
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS carrier_info (
#         mc_number TEXT PRIMARY KEY,
#         carrier_name TEXT,
#         phone_number TEXT,
#         homebase_zip TEXT,
#         equip_length TEXT,
#         equip_type TEXT,
#         insurance_amount TEXT,
#         role TEXT,
#         hazmat TEXT,
#         us_citizen TEXT,
#         rating NUMERIC
#     )
# ''')
#
# # Create a new carrier_rating table with the updated structure
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS carrier_rating (
#         mc_number INTEGER,
#         pro_number INTEGER PRIMARY KEY,
#         english INTEGER,
#         communication INTEGER,
#         reachability INTEGER,
#         punctuality INTEGER,
#         macropoint INTEGER,
#         blacklist INTEGER,
#         total_rating NUMERIC
#     )
# ''')
#
# # Create a trigger to update carrier_info rating when carrier_rating is updated
# cursor.execute('''
#     CREATE TRIGGER IF NOT EXISTS update_carrier_info_rating
#     AFTER INSERT ON carrier_rating
#     BEGIN
#         UPDATE carrier_info
#         SET rating = (SELECT total_rating FROM carrier_rating WHERE mc_number = NEW.mc_number)
#         WHERE mc_number = NEW.mc_number;
#     END;
# ''')
#
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS carrier_phone2 (
#     mc_number TEXT PRIMARY KEY,
#     phone2 TEXT
# );
#
# ''')

cursor.execute('''
    DELETE FROM carrier_rating WHERE pro_number = 1
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
