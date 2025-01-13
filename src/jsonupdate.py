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












def Update_spreadsheet(SERVICE_ACCOUNT_FILE):
   
    # Authenticate with Google Sheets API
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    client = gspread.authorize(credentials)
    service = build('sheets', 'v4', credentials=credentials)
    spreadsheetId = "1PwDUAK_xoLEpQ4-iulutSS29J9qtC7X1PwxwrVra9FU"
    RANGE = 'Results'  # Replace 'Sheet1' with your sheet name

    # Fetch the rows
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=RANGE).execute()
    rows = result.get('values', [])
    headers = rows[0]
    data = rows[1:]
    
    def convert_date(ts):
        try:
            return datetime.strptime(ts, "%m/%d/%Y %H:%M:%S").strftime('%Y-%m-%d')
        except ValueError as e:
            
            pass
            try:
                return datetime.strptime(ts, "%m/%d/%Y %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                raise ValueError(f"Invalid timestamp format: {ts}. Error: {e}")
                return 0
    def insertion_date(ts):
        try:
            return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
        except ValueError as e:
            print(f"Invalid timestamp format: {ts}. Trying other")
            try:
                return datetime.strptime(ts, "%m/%d/%Y %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                print(f"Invalid timestamp format: {ts}. ")
                return ts
           
    df_columns = ["Timestamp","username","song_name","artist_name","bad_artist"]
    df = pd.DataFrame(data,columns=df_columns)
    df['date_created'] = df['Timestamp'].apply(convert_date)
    dfval = conn.execute("Select SUBSTR(cast(s.date_created as STRING),1,10) as date_created,s.date_created  as Timestamp, s.username, s.artist,b.artist_name FROM songs s left join Bad_Rappers b on CAST(b.date_created as DATE) = CAST(b.date_created as DATE) and b.username = s.username UNION SELECT  SUBSTR(cast(b.date_created as STRING),1,10) as date_created,b.date_created  as Timestamp, b.username, s.artist,b.artist_name, FROM Bad_Rappers b left join songs s on CAST(b.date_created as DATE) = CAST(b.date_created as DATE)"  ).df()
    dfval  = dfval.loc[dfval.groupby(['date_created','username'])['Timestamp'].idxmax()]
    
    
    dfanti = df.merge(dfval, on=['date_created','username'], how='outer')
    dfanti = dfanti.replace(np.nan,' ')
    dfanti2 = dfval.merge(df, on=['date_created','username'], how='outer')
    values = []
    for _, row in dfanti.iterrows():
        try:
            Timestampx = insertion_date(row['Timestamp_x'])
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
        
        if Timestamp not in  df['Timestamp']:
            values.append([Timestamp, row['username'], row['song_name'], Artist_name, row['artist_name_y']])
            
        sheetupdate = input("Would you like to update the google sheets? Y or N?")
        if sheetupdate.lower() == 'n':
            values = []
        
        for value in values:
            
            body = {
                
                "values":[
                    value
                    ]
                
                }
        
            
            
            # Append data
            result = service.spreadsheets().values().append(
                spreadsheetId=spreadsheetId,
                range=RANGE,
                valueInputOption='RAW',  # 'RAW' or 'USER_ENTERED'
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
    


            print(f"{result.get('updates').get('updatedCells')} cells appended.")
            # Fetch the rows
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=RANGE).execute()
    rows = result.get('values', [])
    headers = rows[0]
    data = rows[1:]
    jsondf = pd.DataFrame(data,columns=df_columns)
    jsondf.to_json(json_file, orient='records')  
    return
