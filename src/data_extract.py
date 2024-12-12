#Gets current data into a df
import duckdb
conn = duckdb.connect('music.db')
df = conn.execute("""
select s.id, s.date_created, s.song, s.artist, u."real_nigga?" from songs s inner join usernames u on s.date_created = u.date_created where u."real_nigga?" = 'Y';
""").df()
