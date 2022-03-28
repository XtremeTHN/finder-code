titleTables = ["audio", "compressed", "docs", "images", "others", "user_exts", "video"]
import sqlite3

data_base = sqlite3.connect("data.db")
cur = data_base.cursor()
for v in titleTables:
	data_base.row_factory = lambda cursor, row: row[0]
	c = data_base.cursor()
	ids = c.execute(f'SELECT exts FROM {v}').fetchall()
	print(ids)
