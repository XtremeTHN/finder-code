from curses.ascii import SP
import sys, os, sqlite3, time
from progress.spinner import Spinner
from simple_term_menu import TerminalMenu

sys.path.append("..")
from bin.drive import *
from bin.functions import *


yes_no = ["[Y] Si", "[N] No"]
titleTables = ["audio", "compressed", "docs", "images", "others", "user_exts", "video"]
menu = ["[a] Audio", "[b] Compressed Files", "[c] Text Documents", "[d] Images", "[e] Others", "[f] Videos", "[g] Buscar otra extension", "[Exit] Salir"]

def another_menu(table, con):
	sub_menu, cur = sql_fetch(con, titleTables[table])
	choice = sub_menu[TerminalMenu(sub_menu).show()]
	dc = input("Escribe un directorio en donde quieras buscar la extension " + choice + " :")
	ex = choice
	print("Espera...")
	time.sleep(1.2)
	print("Quieres buscar en subcarpetas?")
	choice = yes_no[TerminalMenu(yes_no, title = "Quieres buscar en subcarpetas?").show()]
	if choice == "[N] No":
		if __name__ == "__main__":
			file_list = start_multithreading(dc, ex, "find_noSubFolders")
			return file_list
	elif choice == "[Y] Si":
		if __name__ == "__main__":
			file_list = start_multithreading(dc, ex, "find_withSubFolders")
			return file_list

def choice_Drive(file_list):
	choice = yes_no[TerminalMenu(yes_no, title = "Deseas subir estos archivos a Google Drive?").show()]
	if choice == "[N] No":
		main_menu(con)
	elif choice == "[Y] Si":
		choice = yes_no[TerminalMenu(yes_no, title = "Deseas comprimirlo a un archivo zip?").show()]
		if choice == "[Y] Si":
			name = 'Archivos Comprimidos ' + str(random.randrange(0, 999))
			with zipfile.ZipFile('' + name + '.zip', 'w') as myzip:
				bar2 = ChargingBar('Comprimiendo:', max=len(file_list))
				for file_path in file_list:
					myzip.write(file_path,compress_type=zipfile.ZIP_DEFLATED)
					bar2.next()

				bar2.finish()
				myzip.close
				folders_name = ListFiles()
				choice = folders_name[TerminalMenu(folders_name, title = 'Elige el id de la carpeta en la que quieras subir tus archivos').show()]
				print("Subiendo archivo...")
				FileUpload(name + '.zip', choice)
				os.remove(name + '.zip')
				main_menu(con)
		else:
			folders_name = ListFiles()
			choice = folders_name[TerminalMenu(folders_name, title = 'Elige el id de la carpeta en la que quieras subir tus archivos').show()]
			bar = ChargingBar('Subiendo:', max=len(file_list))
			for file_path in file_list:
				FileUpload(file_path, choice)
				bar.next()
			main_menu(con)

def main_menu(con):
	choice = menu[TerminalMenu(menu, title = "Buscador de archivos, opciones debajo de este texto").show()]

	if choice == "[a] Audio":
		file_list = another_menu(1, con)
		choice_Drive(file_list)

	if choice == "[b] Compressed Files":
		file_list = another_menu(2, con)
		choice_Drive(file_list)

	if choice == "[c] Text Documents":
		file_list = another_menu(3, con)
		choice_Drive(file_list)

	if choice == "[d] Images":
		file_list = another_menu(4, con)
		choice_Drive(file_list)

	if choice == "[e] Others":
		file_list = another_menu(5, con)
		choice_Drive(file_list)

	if choice == "[f] Videos":
		file_list = another_menu(7, con)
		choice_Drive(file_list)

	if choice == "[g] Buscar otra extension":
		sub_menu, cursorObj = sql_fetch(con, titleTables[6])
		ex = input("Escribe la extencion que quieres buscar")
		choice = yes_no[TerminalMenu(yes_no, title = "Deseas guardar esta extension en la base de datos?").show()]
		if choice == "[Y] Si":
			ext = ex.replace(".", "")
			sql = f"INSERT INTO others VALUES ('{ext}')"
			cursorObj.execute(sql)
			con.commit()
			print("Extension guardada en la tabla 'Others'")

		dc = input("Escribe un directorio en donde quieras buscar la extension " + ex + " :")
		print("Espera...")
		time.sleep(1.2)
		print("Quieres buscar en subcarpetas? (Si pones algo no relacionado con No, se buscara en subcarpetas)")
		g = input()
		if g == "N" or "n" or "no" or "No":
			if __name__ == "___main___":
				file_list = start_multithreading(dc, ex, "find_noSubFolders")
				choice_Drive(file_list)
		else:
			if __name__ == "__main__":
				file_list = start_multithreading(dc, ex, "find_withSubFolders")
				choice_Drive(file_list)

	if choice == "[Exit] Salir":
		print("Cerrando conexion a la base de datos...")
		sql_close(con)
		exit()

if len(sys.argv) > 1:
	args = sys.argv[1]
	if args == "--ui" or "-ui" or "/ui":
		print("Importando librerias...")
		from PyQt5 import QtCore, QtGui, QtWidgets
		from PyQt5.QtWidgets import *
		from PyQt5.QtCore import QDir, QUrl
		from bin.functions import *
		from bin.ui import *
		from pathlib import Path
		import sqlite3, os, zipfile, os.path
		print("Realizando conexion a base de datos...")
		connection, c = sq_connect("bin/data.db")
		print("Iniciando ventana...")
		global init_this
		init_this = ""
		class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
			def __init__(self, *args, **kwargs):
				QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
				self.setupUi(self)
				for i in titleTables:
					self.comboBox.addItem(i)
				self.treeWidget.setHeaderLabels(['Nombre','Ruta','Extension'])
				self.pushButton.clicked.connect(self.show_diag)
				self.exa.clicked.connect(self.show_FolderBrowse)
				self.comboBox.activated[str].connect(self.onChanged)
				self.comboBox_2.activated[str].connect(self.chang)

			def show_diag(self):
				print("Mostrando cuadro de dialogo...")
				reply = QMessageBox.question(self, "Find.py",
						"¿Deseas buscar en subcarpetas? Si buscas en subcarpetas \n en una carpeta sin subcarpetas, no devolvera ningun resultado",
						QMessageBox.Yes | QMessageBox.No)
				if reply == QMessageBox.Yes:
					self.treeWidget.clear()
					global dir
					dir = sub_find(self.lineEdit.text(), ext)
					self.treeWidget.setColumnCount(len(dir))
					root=QTreeWidgetItem(self.treeWidget)
					root.setText(0,'Archivos')
					for e, n in enumerate(dir):
						name = os.path.basename(n)
						folder = os.path.dirname(n)
						exten = os.path.splitext(name)
						child=QTreeWidgetItem()
						child.setText(0,name)
						child.setText(1,folder)
						child.setText(2,exten[1])
						root.addChild(child)
					self.progressBar.setMaximum(len(dir))


					if self.google_check.isChecked():
						reply = QMessageBox.about(self, "Find.py",
						"Se abrira una ventana para autenticarte")
						login()
						reply = QMessageBox.about(self, "Find.py",
						"Autenticacion exitosa")
						global folders
						folders = ListFolders(True)
						self.treeWidget.clear()
						self.treeWidget.setHeaderLabels(['Nombre','ID'])
						root=QTreeWidgetItem(self.treeWidget)
						root.setText(0,'Carpetas de google drive')
						for main_value in folders:
							val=QTreeWidgetItem()
							val.setText(0,main_value['title'])
							val.setText(1,main_value['id'])
							root.addChild(val)
						self.treeWidget.clicked.connect(self.clicked_id)
						init_this = True
				else:
					find(self.lineEdit.text(), ext)

			def clicked_id(self, text):
				reply = QMessageBox.question(self, "Find.py",
						"Antes de subir tus archivos, ¿Deseas comprimirlos a un fichero zip?",
						QMessageBox.Yes | QMessageBox.No)
				if reply == QMessageBox.Yes:
					self.status.setText("Comprimiendo archivos...")
					file_nam = 'Archivos Comprimidos ' + str(random.randrange(0, 999)) + ".zip"
					zip = zipfile.ZipFile(os.path.join(self.lineEdit.text(), file_nam), 'w')
					for z, i in enumerate(dir):
						zip.write(i, compress_type=zipfile.ZIP_DEFLATED)
						self.progressBar.setValue(z)
					zip.close()
					self.status.setText("Subiendo archivos...")
					item=self.treeWidget.currentItem()
					FileUpload(os.path.join(self.lineEdit.text(), file_nam), item.text(1))

					self.status.setText("------------")
					reply = QMessageBox.about(self, "Find.py",
							"Archivos subidos")
					self.progressBar.setValue(0)
					self.treeWidget.clear()
					root=QTreeWidgetItem(self.treeWidget)
					root.setText(0,'Archivos')
					for e, n in enumerate(dir):
						name = os.path.basename(n)
						folder = os.path.dirname(n)
						exten = os.path.splitext(name)
						child=QTreeWidgetItem()
						child.setText(0,name)
						child.setText(1,folder)
						child.setText(2,exten[1])
						root.addChild(child)
				else:
					currNode = self.treeWidget.currentItem
					ID = currNode.text(1)
					self.treeWidget.clear()
					root=QTreeWidgetItem(self.treeWidget)
					for e, n in enumerate(dir):
						name = os.path.basename(n)
						folder = os.path.dirname(n)
						exten = os.path.splitext(name)
						child=QTreeWidgetItem()
						child.setText(0,name)
						child.setText(1,folder)
						child.setText(2,exten[1])
						root.addChild(child)

					for i, value in enumerate(dir):

						FileUpload(os.path.join(Path.home(), value), ID)
						self.progressBar.setValue(i)
						print(i)
						root.removeChild(i)

			def show_FolderBrowse(self):
				self.lineEdit.clear()
				file = QFileDialog.getExistingDirectory(self, 'Busca la carpeta en donde quieras buscar', QDir.homePath().replace('/', os.sep), QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
				if file:
					self.lineEdit.insert(str(file))

			def onChanged(self, text):
				print("Realizando consulta a base de datos...")
				exts = sql_fetch(connection, text)
				if exts == False:
					pass
				else:
					self.comboBox_2.clear()
					self.comboBox_2.addItems(exts)

			def chang(self, text):
				global ext
				ext = text

			def pas(self):
				pass


		if __name__ == "__main__":
			app = QtWidgets.QApplication([])
			window = MainWindow()
			window.show()
			app.exec_()
	else:
		print("Este ejecutable solo acepta el comando --ui")
else:
	print("Estableciendo conexion a Google Drive: ")
	login()
	print("Estableciendo conexion a la base de datos...")
	con = sq_connect('data.db')
	print(" ✓", end=" ")
	time.sleep(1)
	spinner = Spinner("Iniciando... ")
	for i in range(50):
		time.sleep(0.09)
		spinner.next()
	from progress.counter import Countdown
	from progress.bar import ChargingBar
	from multiprocessing import Pipe, Process
	import glob, zipfile, random

	main_menu(con)
