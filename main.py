from tkinter import Tk, filedialog, Button, Label, Entry
import tkinter.font as tkfont
from tkinter.messagebox import showinfo
from tkinter import ttk

from os import listdir
from os.path import isfile, join
import os

# Commandes

def select_folder():
	try:
		path_file = filedialog.askdirectory(initialdir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), title = "Choissisez un dossier contenant vos vidéos")
		openfile(path_file)
	except:
		pass

def openfile(path):
	global listeCombo, filename_premier, serie, serie_num
	files = [f for f in listdir(path) if isfile(join(path, f))]
	if files == []:
		return showinfo("Erreur", "Ce dossier est vide.")
	filenames = []
	file_extensions = []
	for i in range(len(files)):
		filename, file_extension = os.path.splitext(files[i])
		if file_extension not in ['.mkv','.mp4','.avi']:
			file_imcompatible = True
		filenames.append(filename)
		file_extensions.append(file_extension)

	filename_premier_nom, file_extension = os.path.splitext(files[0])
	del file_extension
	
	try:
		if file_imcompatible == True:
			showinfo("Erreur", f"Un fichier n'est pas compatible.\nVeuillez n'utiliser que des .mp4, .avi ou des .mkv.")
			root.destroy()
	except:
		pass
	try:
		del file_imcompatible
	except:
		pass
		 
	try:
		nettoyage()
	except:
		pass
	try:
		nettoyage2()
	except:
		pass

	Label(root, text = "Nom 1er fichier :").place(x = 5, y = 13)

	filename_premier = Entry(root, width = len(filename_premier_nom))
	filename_premier.insert(0, filename_premier_nom)
	filename_premier.place(x = 100, y = 15)

	Label(root, text = "Contenu du dossier actuel").place(x = 50, y = 50)

	listeCombo = ttk.Combobox(root, values=filenames, width=len(max(filenames, key=len)))
	listeCombo.current(0)
	listeCombo.place(x = 50, y = 80)

	Label(root, text = "Titre de la série :").place(x = 30, y = 120)
	serie = Entry(root, width = 80)
	serie.place(x = 120, y = 120)

	Label(root, text = "Numéro de la série :").place(x = 9, y = 170)
	serie_num = Entry(root, width = 10)
	serie_num.place(x = 120, y = 170)

	Button(root, text = "Voir la prévisualisation", command = lambda : previsualisation(files, file_extensions, path)).place(x = 30, y = 200)

def nettoyage():
	listeCombo.destroy()
	filename_premier.destroy()
	serie.destroy()
	serie_num.destroy()

def nettoyage2():
	listeCombo_new.destroy()
	listeCombo_label_new.destroy()
	valider.destroy()

def previsualisation(files, extensions, path):
	global listeCombo_new, listeCombo_label_new, valider
	try:
		nettoyage2()
	except:
		pass
	serie_nom = serie.get()
	serie_numero = serie_num.get()
	try:
		if len(serie_nom) > 0 and int(serie_numero) > 0:
			if int(serie_numero) < 10:
				serie_numero = f"0{serie_numero}"
			filenames_new = []
			for i in range(len(files)):
				i += 1
				if i < 10:
					i = f"0{i}"
				filenames_new.append(f"{serie_nom} - s{serie_numero}e{i}")

			listeCombo_label_new = Label(root, text = "Contenu du dossier si renommé")
			listeCombo_label_new.place(x = 50, y = 240)

			listeCombo_new = ttk.Combobox(root, values=filenames_new, width=len(max(filenames_new, key=len)))
			listeCombo_new.current(0)
			listeCombo_new.place(x = 50, y = 270)

			valider = Button(root, text = "Confirmer et renommer les fichiers", command = lambda : rename(files, filenames_new, extensions, path))
			valider.place(x = 50, y = 300)

		else:
			showinfo("Erreur", "Le nom de la série et/ou son numéro n'est pas renseigné.")
	except:
		showinfo("Erreur", "Le numéro de la série DOIT être un numéro")

def rename(files, new_files, extensions, path):
	try:
		for i in range(len(extensions)):
			os.rename(f"{path}/{files[i]}",f"{path}/{new_files[i]}{extensions[i]}")
		showinfo("Succès", "Les fichiers ont bien été renommés.")
	except:
		showinfo("Erreur", "Un nom de fichier ne peut pas contenir les caractères suivants :\n\\ / : * ? < > |")

# Affichage

root=Tk()
root.geometry("700x350")
root.title("Renommer des fichiers pour Plex")
root.resizable(False, False)

Button(root, text = "Choisis un dossier", command = select_folder).place(x = 570, y = 10)

root.mainloop()