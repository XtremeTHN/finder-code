import sqlite3, glob, zipfile, random
from progress.counter import Countdown
from multiprocessing import Pipe, Process 
def sq_connect(db):
	try:
		f = sqlite3.connect(db)
		c = f.cursor()
		return f, c
	except sqlite3.Error as er:
		print('SQLite error: %s' % (' '.join(er.args)))
		contador = Countdown("Reintentando en:")
		for num in range(5):
			contador.next()
			time.sleep(1)
		sq_connect(db)


def find_withSubFolders(conn, npath, ext):
	targetPattern = npath + "/**/*" + ext
	s = glob.glob(targetPattern)
	conn.send(s)

def find_noSubFolders(conn, npath, ext):
	targetPattern = npath + "/*" + ext
	s = glob.glob(targetPattern)
	conn.send(s)

def start_multithreading(path, cext, function):

	parent_conn, child_conn = Pipe()
	
	if function == "find_withSubFolders":
		p = Process(target=find_withSubFolders, args=(child_conn, path, cext))

	elif function == "find_noSubFolders":
		p = Process(target=find_noSubFolders, args=(child_conn, path, cext))

	p.start()
	spinner = Spinner('Buscando... ')
	while True:
		print(str())
		if parent_conn.recv == "":
			time.sleep(0.09)
			spinner.next
		else:
			paths = parent_conn.recv()
			if paths == " ":
				print("No se ha encontrado nada")
				return False
		
			print("Esto se ha encontrado")
			for i in paths:
				print(i)
			break
	p.join()
	return paths

def sql_fetch(con, table): 
	if table == "Categoria":
		return False
	else:
		con.row_factory = lambda cursor, row: row[0]
		c = con.cursor()
		ids = c.execute(f'SELECT exts FROM {table}').fetchall()
		return ids

def sql_close(con):
	con.close()
	
def sub_find(npath, ext):
	targetPattern = npath + "/**/*" + ext
	s = glob.glob(targetPattern)
	return s

def find(npath, ext):
	targetPattern = npath + "/*" + ext
	s = glob.glob(targetPattern)
	return s
