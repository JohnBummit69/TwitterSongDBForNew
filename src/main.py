import duckdb
from datetime import datetime
import json
from datetime import datetime, timedelta
import pandas as pd
from datetime import datetime
import os
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


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
    df_columns = ["Timestamp","username","song_name","artist_name","bad_artist"]
    df = pd.DataFrame(data,columns=df_columns)
    # Drop the first row
    df= df.iloc[1:]
    df["Timestamp"] = df["Timestamp"].apply(format_timestamp)
    timestamp = datetime.now()
    
    #Bad Rappers
    
    bad_rapper(df)
    
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
        song_name = row["song_name"]
        Timestamp = row["Timestamp"]
        
        if not isinstance(song_name,int):
            row["song_name"].lower().strip()
       
            
        if row["song_name"] in Bad_Artists:
            row["real_nigga?"] = 'N'
        else:   
            row["real_nigga?"] = 'Y'
        
        upsert_username(Timestamp, row["username"], row["real_nigga?"])   
        upsert_song(Timestamp, row["username"],row["song_name"], row["artist_name"])

def format_timestamp(ts):
    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%m/%d/%Y %H:%M:%S')
    except ValueError as e:
        raise ValueError(f"Invalid timestamp format: {ts}. Error: {e}")

def upsert_username(timestamp, username, real_nigga=None):
    # Extract the date from the Timestamp
   

    
    try:
        Timestamp = datetime.strptime(timestamp, '%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        Timestamp_Date = datetime.strptime(timestamp, '%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d')
    except Exception as e:
        print(e)
        Timestamp_Date = timestamp
        pass
    
 


    # Check if the username already exists for the same date
    existing_query = """
    SELECT id FROM usernames
    WHERE username = ?;
    """
    existing_id = conn.execute(existing_query, [username]).fetchone()
   
    #updates db if its a different song
    if existing_id:
        # Update the existing row
        update_query = """
        UPDATE usernames
        SET  
        
        "real_nigga?" = ?,
        WHERE id = ?;
        """
        conn.execute(update_query, [real_nigga, existing_id[0]])
        print(f"Updated: {username} for date {timestamp}")
    else:
        # Insert a new row
        insert_query = """
        INSERT INTO usernames (date_created, username, "real_nigga?")
        VALUES (?, ?, ?);
        """
        conn.execute(insert_query, [Timestamp, username, real_nigga])
        print(f"Inserted: {username} for date {timestamp}")    



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
      
def bad_rapper():
    
    
    insert_query = """
    INSERT INTO Bad_Rappers (date_created, artist_name, username)
    VALUES (?, ?, ?, );
    """
    bad_rapper  = input("Are there any bad rappers you want to contribute? Y or N \n")
    
    username = input("What is your username?\n") 
    
    date = datetime.now().strftime("%Y-%m-%d")
    Date = conn.execute(f"SELECT MAX(cast(date_created as DATE)) from Bad_Rappers where  username = '{username}'").fetchone()
    Date = Date[0]
    if Date == date:
        print("you already submitted, thug")
        return
    if bad_rapper == "Y":
        bad_art = input("Enter Artist Name:\n")
        conn.execute(insert_query, [date,bad_art,username])
        print(f"Thank you, {bad_art} was inserted\n")
    else:
        pass


def update_db(json_file):
    # Load the JSON file
    with open(json_file,"r") as file:
        data = json.load(file)
    
    # Convert JSON to a Pandas DataFrame
    df_columns = ["Timestamp","username","song_name","artist_name","bad_artist"]
    df = pd.DataFrame(data,columns=df_columns)
    # Drop the first row
    df= df.iloc[1:]
    def convert_date(ts):
        try:
            return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%Y-%m-%d')
        except ValueError as e:
            raise ValueError(f"Invalid timestamp format: {ts}. Error: {e}")
            try:
                return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d')
            except ValueError as e:
                raise ValueError(f"Invalid timestamp format: {ts}. Error: {e}")
                return 0
    df['date_created'] = df['Timestamp'].apply(convert_date)
    
    dfval = conn.execute("Select SUBSTR(cast(s.date_created as STRING),1,10) as date_created,s.date_created  as Timestamp, s.username, s.artist,b.artist_name FROM songs s left join Bad_Rappers b on CAST(b.date_created as DATE) = CAST(b.date_created as DATE) and b.username = s.username UNION SELECT  SUBSTR(cast(b.date_created as STRING),1,10) as date_created,b.date_created  as Timestamp, b.username, s.artist,b.artist_name, FROM Bad_Rappers b left join songs s on CAST(b.date_created as DATE) = CAST(b.date_created as DATE)"  ).df()
    dfval  = dfval.loc[dfval.groupby(['date_created','username'])['Timestamp'].idxmax()]
    
    
    dfanti = df.merge(dfval, on=['date_created','username'], how='outer')
    
    
    for _, row in dfanti.iterrows():
        try:
            Timestampx = format_timestamp(row['Timestamp_x'])
            Timestamp = Timestampx
        except TypeError:
                Timestamp = row['Timestamp_y'].strftime("%m/%d/%Y %H:%M:%S")
                Artist_name = row['artist']
        try: 
            if Timestampx > row['Timestamp_y']:
                Timestamp = Timestampx
                Artist_name = row['artist_name_x']
            else:
                Timestamp = row['Timestamp_y']
                Artist_name = row['artist']
        except TypeError:
            
            Artist_name = row['artist_name_x']
         
        upsert_song(Timestamp, row['username'], row['song_name'], Artist_name)
        print("DB Updated")
        df = conn.execute("Select SUBSTR(cast(s.date_created as STRING),1,10) as date_created,s.date_created  as Timestamp, s.username, s.artist,b.artist_name as bad_artist FROM songs s left join Bad_Rappers b on CAST(b.date_created as DATE) = CAST(b.date_created as DATE) and b.username = s.username UNION SELECT  SUBSTR(cast(b.date_created as STRING),1,10) as date_created,b.date_created  as Timestamp, b.username, s.artist,b.artist_name as bad_artist , FROM Bad_Rappers b left join songs s on CAST(b.date_created as DATE) = CAST(b.date_created as DATE) "  ).df()
        df  = df.loc[df.groupby(['date_created','username'])['Timestamp'].idxmax()]
        dfjson = df
        dfjson.to_json(json_file)





def Update_spreadsheet(SERVICE_ACCOUNT_FILE):
   
    # Authenticate with Google Sheets API
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    client = gspread.authorize(credentials)
    service = build('sheets', 'v4', credentials=credentials)
    spreadsheetId = "1PwDUAK_xoLEpQ4-iulutSS29J9qtC7X1PwxwrVra9FU"
    RANGE = 'Sheet1!'  # Replace 'Sheet1' with your sheet name

    

    # Fetch the rows
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=RANGE).execute()
    rows = result.get('values', [])
    
    # Body of the request
    body = {
        'values': values
    }
    
    # Append data
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_ID,
        range=RANGE,
        valueInputOption='RAW',  # 'RAW' or 'USER_ENTERED'
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()
    
    print(f"{result.get('updates').get('updatedCells')} cells appended.")

json_file = "music_data.json"

def main():
    
    parse_and_insert_json(json_file,bad_rappers)




    #Gets current data into a df
    import duckdb
    conn = duckdb.connect('music.db')
    df = conn.execute("Select s.date_created, s.username, song, artist, u.'real_nigga?' FROM songs s inner join usernames u on u.username = s.username").df()
    df2 = conn.execute("select * from usernames").df()
    df2 = df.drop('real_nigga?')
    df2.to_json('music_datacloud.json', orient="records", indent=4)
    conn.close()
