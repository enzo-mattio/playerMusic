import tkinter as tk
import pygame
from pygame import mixer
import os
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter import ttk
import random

# Initialisation de Pygame
pygame.init()
pygame.mixer.init()

# Création de la fenêtre principale
root = tk.Tk()
root.title("Lecteur audio")


# Fonctions pour les événements
def play():
  global is_playing, current_track_index
  if current_track_index is not None and not is_playing:
    pygame.mixer.music.load(tracks[current_track_index])
    pygame.mixer.music.play(-1 if loop_var.get() else 0)
    is_playing = True


def pause():
  global is_playing
  if current_track_index is not None and is_playing:
    mixer.music.pause()
    is_playing = False
    pause_button.configure(text="Resume")
  elif current_track_index is not None and not is_playing:
    mixer.music.unpause()
    is_playing = True
    pause_button.configure(text="Pause")

    


def stop():
  global is_playing
  if current_track_index is not None and is_playing:
    pygame.mixer.music.stop()
    is_playing = False


def set_volume(volume):
  pygame.mixer.music.set_volume(float(volume) / 100)


def add():
  global tracks
  track = askopenfilename(filetypes=[("Fichiers audio", "*.mp3")])
  if track:
    tracks.append(track)
    listbox.insert(tk.END, track)


def delete():
  global tracks, current_track_index, is_playing
  selection = listbox.curselection()
  if selection:
    index = selection[0]
    del tracks[index]
    listbox.delete(index)
    if index == current_track_index:
      stop()


def on_select(event):
  global current_track_index, is_playing
  selection = listbox.curselection()
  if selection:
    index = selection[0]
    if index != current_track_index:
      if is_playing:
        stop()
      current_track_index = index
      play()
    # Démarre la mise à jour de la progressbar
    on_timer()

def on_timer():
  global is_playing
  if is_playing:
    current_time = pygame.mixer.music.get_pos() / 1000
    progress_bar['value'] = current_time
  root.after(1000, on_timer)


def play_random_track():
  global current_track_index, is_playing
  if tracks:
    new_track_index = random.randint(0, len(tracks) - 1)
    if new_track_index != current_track_index:
      if is_playing:
        stop()
      current_track_index = new_track_index
      play()
      
      


# Chargement des pistes audio
listbox = tk.Listbox(root)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
os.chdir(askdirectory())
tracks = os.listdir()
for track in tracks:
    listbox.insert(tk.END, track)

# Configuration initiale
current_track_index = None
is_playing = False

status = "Play"

# Création des widgets




play_button = tk.Button(root, text="Lecture")
play_button.pack(side=tk.TOP)

pause_button = tk.Button(root, text="Pause")
pause_button.pack(side=tk.TOP)

stop_button = tk.Button(root, text="Arrêt")
stop_button.pack(side=tk.TOP)

volume_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL)
volume_scale.pack(side=tk.TOP)

loop_var = tk.BooleanVar()
loop_checkbutton = tk.Checkbutton(root, text="Boucle", variable=loop_var)
loop_checkbutton.pack(side=tk.TOP)

add_button = tk.Button(root, text="Ajouter")
add_button.pack(side=tk.TOP)

delete_button = tk.Button(root, text="Supprimer")
delete_button.pack(side=tk.TOP)


# Configuration des événements
play_button.config(command=play)
pause_button.config(command=pause)
stop_button.config(command=stop)
volume_scale.config(command=set_volume)
add_button.config(command=add)
delete_button.config(command=delete)
listbox.bind("<<ListboxSelect>>", on_select)
progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=200, mode="determinate")
progress_bar.pack(side=tk.TOP)
random_button = tk.Button(root, text="Lecture aléatoire", command=play_random_track)
random_button.pack(side=tk.TOP)
volume_scale.set(50)


# Lancement de la boucle principale
root.after(1000, on_timer)
root.mainloop()