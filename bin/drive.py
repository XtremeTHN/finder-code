from asyncio import gather
from typing import Type
from pydrive2.auth import GoogleAuth, RefreshError
from pydrive2.drive import GoogleDrive
import os

dir_credenciales = "credentials_module,json"

def login():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(dir_credenciales)
    
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
        
    gauth.SaveCredentialsFile(dir_credenciales)
    credenciales = GoogleDrive(gauth)
    return credenciales


def FileCreate(file_name, content, folder_id):
	credential = login()
	file = credential.CreateFile({'title': file_name,
									'parents': [{'kind': 'drive=fileLink', 'id': folder_id}]})
	file.SetContentString(content)
	file.Upload()

def ListFolders(b):
	#Si bol no es True (indicador de interfaz grafica), se regresara el valor ids y name, si es False solo se devolvera ids
	ids = []
	name = []
	gauth = GoogleAuth()
	drive = GoogleDrive(gauth)
	file_list = drive.ListFile({'q': "mimeType = 'application/vnd.google-apps.folder'"}).GetList()
	return file_list
	#for file1 in file_list:
		#ids.append(file1['id'])
		#name.append(file1['title'])
        
	if b == True:
		return ids, name
	else:
		return ids
def FileUpload(path, id):
	gauth = GoogleAuth()
	drive = GoogleDrive(gauth)
	f = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": id}]})
	f.SetContentFile(path)
	f.Upload()
        

def MkFolder(folder_name,folder_id):
    credential = login()
    folder = credential.CreateFile({'title': folder_name, 
                               'mimeType': 'application/vnd.google-apps.folder',
                               'parents': [{"kind": "drive#fileLink",\
                                                    "id": folder_id}]})
    folder.Upload()


if __name__ == "__main__":
	idfolder = '1RGMZWBGN7KBB3l_QambUyBoqiJUMEnL8'
	login()
	df = ListFiles()
	print(df)

