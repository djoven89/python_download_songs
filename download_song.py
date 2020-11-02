# -*- coding: utf-8 -*-

from os import path, remove, mkdir, chdir
from sys import exit
from pytube import YouTube, Playlist
from unidecode import unidecode
from moviepy.editor import AudioFileClip

def convert_mp3(song_name: str):
    """Función que convierte el formato MP4 a MP3"""

    print("\nConviertiendo la canción a formato 'mp3...")

    try:
        clip = AudioFileClip(song_name)
        clip.write_audiofile(song_name.replace('mp4', 'mp3'))
    except Exception as e:
        print("Hubo un error al convertir la cancación:", e)
        exit(1)

    if song_name.endswith('mp4'):
        remove(song_name)

def download_song(s: object, s_size: int, s_format: str, s_long: str, s_short: str):
    """Función que se encarga de descargar la canción"""

    print(f"\nDescargando la canción: {s_short}")

    if not path.exists(song_dest):
        mkdir(song_dest)

    chdir(song_dest)

    if path.exists(s_long):
        print("La canción ya existe, saliendo...")
        exit(0)

    try:
        s.download(song_dest, filename=s_short)
    except Exception as e:
        print(f"Hubo un error al descargar el archivo, error:\n\t {e}")
        exit(1)

    if path.exists(s_long) and path.getsize(s_long) == s_size:
        print(f"Canción descargada con éxito en formato: {s_format}")
    else:
        print("La canción no se descargó con éxito. Pudo haber sido porque el tamaño no concuerda.")
        exit(1)

    if s_format == 'mp4':
        convert_mp3(s_long)

def song_rename(song: any):
    """Función que renombra una canción y la deja lista para descargar"""

    song_long_name = song.default_filename

    for ch in song_long_name:
        if ch == ' ':
            song_long_name = song_long_name.replace(ch, '_')
        elif ch == '.':
            continue
        elif ch == '-':
            pass
        elif not ch.isalnum():
            song_long_name = song_long_name.replace(ch, '')

    song_long_name = unidecode(song_long_name.replace('__', '').replace('_-_', '-'))

    song_size = song.filesize
    song_format_index = song_long_name.rfind('.mp')
    song_format = song_long_name[song_format_index + 1:]
    song_short_name = song_long_name[:song_format_index]

    download_song(song, song_size, song_format, song_long_name, song_short_name)

def get_playlist(song_url: str) -> str:
    """Función que obtiene todos las canciones de una playlist"""

    try:
        pl = Playlist(song_url)
    except Exception as e:
        print(f"Hubo un error al procesar la URL del vídeo:\n\t {e}")
        exit(1)

    song = []

    for url in pl.video_urls:
        song.append(url)

    return song

def get_song(song_url: any) -> object:
    """Función que obtiene el enlace de la/s canciones"""

    try:
        yt = YouTube(song_url)
    except Exception as e:
        print(f"Hubo un error al procesar la URL del vídeo:\n\t {e}")
        exit(1)

    song = yt.streams.get_audio_only()

    return song

song_dest = "/home/daniel/Music/"
song_url = str(input("URL de la cancion: "))

if '&list=' not in song_url:
    song_name = get_song(song_url)
    song_rename(song_name)

else:
    song_dest += str(input("Nombre del directorio: "))

    songs = get_playlist(song_url)
    for song in songs:
        song_name = get_song(song)
        song_rename(song_name)
