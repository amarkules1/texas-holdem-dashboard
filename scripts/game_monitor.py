import os
import time
import requests
import sqlite3
from datetime import datetime

# author: Google Gemini

def check_directory(directory, api_url, db_path):
    """
    Checks a directory for new or updated files and sends them to an API.

    Args:
        directory (str): The directory to monitor.
        api_url (str): The API endpoint to send files to.
        db_path (str): Path to the SQLite database.
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the 'files' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            filename TEXT PRIMARY KEY,
            last_modified TEXT
        )
    ''')
    conn.commit()

    try:
        while True:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    modified_time = datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()

                    cursor.execute("SELECT last_modified FROM files WHERE filename = ?", (filename,))
                    result = cursor.fetchone()

                    if result is None:
                        # New file
                        send_file_to_api(filepath, api_url)
                        cursor.execute("INSERT INTO files (filename, last_modified) VALUES (?, ?)", (filename, modified_time))
                        conn.commit()
                        print(f"New file uploaded: {filename}")
                    elif result[0] != modified_time:
                        # Updated file
                        send_file_to_api(filepath, api_url)
                        cursor.execute("UPDATE files SET last_modified = ? WHERE filename = ?", (modified_time, filename))
                        conn.commit()
                        print(f"Updated file uploaded: {filename}")

            time.sleep(5)

    except KeyboardInterrupt:
        print("Monitoring stopped.")
    finally:
        conn.close()

def send_file_to_api(filepath, api_url):
    """
    Sends a file to the specified API endpoint.

    Args:
        filepath (str): The path to the file.
        api_url (str): The API endpoint.
    """
    try:
        with open(filepath, 'rb') as f:
            files = {'file': (os.path.basename(filepath), f)}
            response = requests.post(api_url, files=files)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            print(f"File {os.path.basename(filepath)} uploaded successfully. Response: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error uploading {os.path.basename(filepath)}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while uploading {os.path.basename(filepath)}: {e}")


if __name__ == "__main__":
    directory = input("Enter the directory to monitor: ")
    api_url = "https://pokersolver.xyz/game-file"
    db_path = "file_monitor.db"  # SQLite database in the same directory

    if not os.path.isdir(directory):
        print("Invalid directory.")
    else:
        check_directory(directory, api_url, db_path)