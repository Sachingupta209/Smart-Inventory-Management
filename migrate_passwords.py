import sqlite3

# Connect to the SQLite database (Change 'database.db' to your actual database file)
conn = sqlite3.connect('ims.db')
cursor = conn.cursor()

try:
    # Delete all data from the 'bills' table
    cursor.execute("DELETE FROM products;")

    # Reset the auto-increment ID counter
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='products';")

    # Commit changes
    conn.commit()
    print("All data from 'bills' table deleted successfully, and ID reset.")

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Close the database connection
    conn.close()
