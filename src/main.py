import duckdb
from datetime import datetime
import json
from datetime import datetime, timedelta
import pandas as pd
from datetime import datetime
import os



#import list for non real niggas 
"""
from bad artists.py import Bad_Artists
"""
# Connect to or create a DuckDB database
conn = duckdb.connect('music.db')

# Create sequences for auto-incrementing IDs
conn.execute("""
CREATE SEQUENCE IF NOT EXISTS usernames_id_sequence START 1 INCREMENT 1;
""")
conn.execute("""
CREATE SEQUENCE IF NOT EXISTS songs_id_sequence START 1 INCREMENT 1;
""")

conn.execute("""
CREATE SEQUENCE IF NOT EXISTS artists_id_sequence START 1 INCREMENT 1;
""")

create_usernames_table = """
CREATE TABLE IF NOT EXISTS usernames (
    id INTEGER DEFAULT nextval('usernames_id_sequence') PRIMARY KEY,
    date_created DATETIME NOT NULL,
    username NVARCHAR NOT NULL,
    "real_nigga?" CHAR(1) NULL 
);
"""
conn.execute(create_usernames_table)

# create songs tb
create_songs_table_query = """
CREATE TABLE IF NOT EXISTS songs (
    id INTEGER DEFAULT nextval('songs_id_sequence') PRIMARY KEY,
    date_created DATETIME NOT NULL,
    username NVARCHAR NOT NULL,
    song NVARCHAR NOT NULL,
    artist NVARCHAR NOT NULL,
     
);
"""
conn.execute(create_songs_table_query)


ass_query = ("""create TABLE IF NOT EXISTS Bad_Rappers (
             artists_id INTEGER DEFAULT nextval('usernames_id_sequence') PRIMARY KEY,
             date_created DATETIME NOT NULL,
             artist_name NVARCHAR NOT NULL,
             username NVARCHAR NOT NULL);""")

conn.execute(ass_query)

# Confirm the tables were created
print("Tables created successfully.")

def username_exists_recently(username):
    three_days_ago = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    query = """
    SELECT username FROM usernames
    WHERE username = ? AND CAST(date_created AS DATE) >= ?;
    """
    result = conn.execute(query, [username, three_days_ago]).fetchone()
    return result is not None

def username_exists(username):
    
    query = """
    SELECT username FROM usernames
    WHERE username = ? ;
    """
    result = conn.execute(query, [username]).fetchone()
    return result is not None


def song_exists(username, song, artist):
    query = """
    SELECT song_name FROM songs
    WHERE username = ? AND song = ? AND artist = ? AND CAST(date_created AS DATE) >= ?;
    """
    result = conn.execute(query, [username, song, artist]).fetchone()
    return result is not None
  
def insert_song(username, song, artist, real_nigga=None):
    insert_query = """
    INSERT INTO songs (username, song, artist, "real_nigga")
    VALUES (?, ?, ?, ?);
    """
    conn.execute(insert_query, [username, song, artist, real_nigga])          
            
def insert_username(username, is_real_nigga):
    date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    insert_query = """
    INSERT INTO usernames (date_created, username)
    VALUES (?, ?);
    """
    conn.execute(insert_query, [date_created, username])

def parse_and_insert_json(json_file):
    # Load the JSON file
    with open(json_file,"r") as file:
        data = json.load(file)
    
    # Convert JSON to a Pandas DataFrame
    df_columns = ["Timestamp","username","song_name","artist_name"]
    df = pd.DataFrame(data,columns=df_columns)
    # Drop the first row
    df= df.iloc[1:]
    df["Timestamp"] = df["Timestamp"].apply(format_timestamp)
    timestamp = datetime.now()
    
    #Bad Rappers
    bad_rapper(timestamp)
    
    Bad_Artists = conn.execute("Select artist_name from Bad_Rappers group by artist_name having count(*) >=5  ").df()  
    for username in df["username"].dropna().unique():
        timestamp = datetime.now()
        
    
    for username in df["username"].dropna().unique():
        if not username_exists(username):
            insert_username(username, None)  # Default "real_nigga?" to NULL
            print(f"Inserted: {username} into users db")
        else:
            print(f"Skipped: {username} (already in table)")
    #Real nigga check
        
    for _, row in df.iterrows():
        if row["song_name"].lower().strip() in Bad_Artists:
            row["real_nigga?"] = 'N'
        else:   
            row["real_nigga?"] = 'Y'
        upsert_username(row["Timestamp"], row["username"], row["real_nigga?"])   
        upsert_song(row["Timestamp"], row["username"],row["song_name"], row["artist_name"])

def format_timestamp(ts):
    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%m/%d/%Y %H:%M:%S')
    except ValueError as e:
        raise ValueError(f"Invalid timestamp format: {ts}. Error: {e}")

def upsert_username(timestamp, username, real_nigga=None):
    # Extract the date from the Timestamp
   

    
    try:
        Timestamp = datetime.strptime(timestamp, "%m/%d/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        Timestamp_Date = datetime.strptime(Timestamp, "%Y-%m-%d  %H:%M:%S").strftime("%Y-%m-%d")
    except Exception as e:
        print(e)
        pass
    
 


    # Check if the username already exists for the same date
    existing_query = """
    SELECT id FROM usernames
    WHERE username = ? AND CAST(date_created AS DATE) = ?;
    """
    existing_id = conn.execute(existing_query, [username, Timestamp_Date]).fetchone()
   
    #updates db if its a different song
    if existing_id:
        # Update the existing row
        update_query = """
        UPDATE usernames
        SET  
        "date_created" = ?,
        "real_nigga?" = ?,
        WHERE id = ?;
        """
        conn.execute(update_query, [Timestamp, real_nigga, existing_id[0]])
        print(f"Updated: {username} for date {Timestamp}")
    else:
        # Insert a new row
        insert_query = """
        INSERT INTO usernames (date_created, username, "real_nigga?")
        VALUES (?, ?, ?);
        """
        conn.execute(insert_query, [Timestamp, username, real_nigga])
        print(f"Inserted: {username} for date {Timestamp}")    



def upsert_song(timestamp, username, song, artist):
    # Ensure timestamp is in the correct format
    try:
        formatted_timestamp = datetime.strptime(timestamp, "%m/%d/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        raise ValueError(f"Invalid timestamp format: {timestamp}. Error: {e}")
    
    # Extract the date from the timestamp and today's date
    record_date = formatted_timestamp.split(" ")[0]  # Date portion of the timestamp
    today_date = datetime.now().strftime("%Y-%m-%d")  # Today's date

    # Proceed only if the record's date is today
    if record_date != today_date:
        
        return

    # Check if the username already exists for today
    existing_query = """
    SELECT id, song, artist FROM songs
    WHERE username = ? AND CAST(date_created AS DATE) = ?;
    """
    existing_entry = conn.execute(existing_query, [username, today_date]).fetchone()

    if existing_entry:
        # If the song or artist is different, update the entry
        existing_id, existing_song, existing_artist = existing_entry
        if existing_song != song or existing_artist != artist:
            update_query = """
            UPDATE songs
            SET date_created = ?, song = ?, artist = ?, 
            WHERE id = ?;
            """
            conn.execute(update_query, [formatted_timestamp, song, artist, existing_id])
            print(f"Updated: {username}'s song to '{song}' by {artist} for today ({today_date})")
        else:
            print(f"No update needed: {username} already has the same song '{song}' by {artist} for today ({today_date})")
    else:
        # Insert a new row
        insert_query = """
        INSERT INTO songs (date_created, username, song, artist)
        VALUES (?, ?, ?, ?);
        """
        conn.execute(insert_query, [formatted_timestamp, username, song, artist])
        print(f"Inserted: {username}'s song '{song}' by {artist} for today ({today_date})\n")
      
def bad_rapper(timestamp):
    
    
    insert_query = """
    INSERT INTO Bad_Rappers (date_created, artist_name, username)
    VALUES (?, ?, ?, );
    """
    bad_rapper  = input("Are there any bad rappers you want to contribute? Y or N \n")
    if bad_rapper == "Y":
        username = input("What is your username?\n") 
        date = datetime.now()
        bad_art = input("Enter Artist Name:\n")
        conn.execute(insert_query, [date,bad_art,username])
        print(f"Thank you, {bad_art} was inseerted\n")
    

json_file = "music_data.json"

def main():
    
    parse_and_insert_json(json_file)




#Gets current data into a df
import duckdb
conn = duckdb.connect('music.db')
df = conn.execute().df()