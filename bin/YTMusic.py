#!/bin/python

import mechanize
from bs4 import BeautifulSoup as soup
import pafy
import os

if not os.path.exists("Music"):
	os.makedirs("Music")
print ''

avconv = 1

if os.name == 'nt':
	opsys = 'win'
	if not os.path.isfile('avconv.exe'):
		print 'avconv not found, will not convert to mp3 (from m4a). download from https://builds.libav.org/windows/ to be able to convert them'
		avconv = 0
else:
	opsys = 'linux'
	check_install = os.system('which avconv > /dev/null')
	if check_install == '':
		print 'avconv not found, will not convert to mp3 (from m4a). use sudo apt-get install libav-tools to install it'
		avconv = 0

def Main():
	script_dir = os.getcwd()
	Title = ''
	while True:
		try:
			print('')
			print('')
			raw_song = raw_input('Enter a song/cmd: ')
			if raw_song == "exit":
				exit()
			elif raw_song == "play":
				if not Title == '':
					if opsys == 'win':
						if os.path.isfile(script_dir + "\Music\\" + Unencoded_Title + ".mp3"):
							os.system('"' + script_dir + "\Music\\" + Unencoded_Title + ".mp3" + '"')
						else:
							os.system('"' + script_dir + "\Music\\" + Unencoded_Title + ".m4a" + '"')
					elif opsys == 'linux':
						if os.path.isfile(script_dir + '/Music/' + Unencoded_Title + '.mp3'):
							os.system('mplayer "' + script_dir + '/Music/' + Unencoded_Title + '.mp3"')
						else:
							os.system('mplayer "' + script_dir + '/Music/' + Unencoded_Title + '.m4a"')

				else:
					print 'No log to read from..'
			elif raw_song == "convert":

				print ''
				if opsys == 'win':
					if avconv == 1:
						y = 1
						x = 0
						for m in os.listdir(script_dir + '/Music/'):
							if m.endswith(".m4a"):
								x = x + 1
						print 'Total songs to convert = ' + str(x) + ' songs'
						for m in os.listdir(script_dir + '/Music/'):
							if m.endswith(".m4a"):
								print ''
								print str(y) + '. ' 'Converting ' + m + ' to mp3..'
								y = y + 1
								song = m.replace(".m4a", "")
								os.system('avconv.exe -loglevel 0 -i "Music\\' + song + '.m4a" ' + '"Music\\' + song + '.mp3"')
								os.remove("Music/" + m)
					else:
						print 'avconv is not installed, cant convert to mp3'
				elif opsys == 'linux':
					if avconv == 1:
						y = 1
						x = 0
						for m in os.listdir(script_dir + '/Music/'):
							if m.endswith(".m4a"):
								x = x + 1
						print 'Total songs to convert = ' + str(x) + ' songs'
						for m in os.listdir(script_dir + '/Music/'):
							if m.endswith(".m4a"):
								print ''
								print str(y) + '. ' 'Converting ' + m + ' to mp3..'
								y = y + 1
								song = m.replace(".m4a", "")
								os.system('sudo avconv -loglevel 0 -i "Music/' + song + '.m4a" ' + '"Music/' + song + '.mp3"')
								os.remove("Music/" + m)
				else:
					print 'avconv is not installed, cant convert to mp3'
			elif raw_song == "spotify":
				print ''
				f = open(script_dir + '/Music/spotify.txt')
				lines = f.readlines()
				print 'Total songs in spotify.txt = ' + str(len(lines)) + ' songs'
				y = 1
				for x in lines:
					print ''
					song = x.replace(" ", "%20")
					br = mechanize.Browser()
					br.set_handle_robots(False)
					br.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]
					URL = "https://www.youtube.com/results?search_query=" + song
					items = br.open(URL).read()

					items_parse = soup(items, "html.parser")
					br.close()
					first_result = items_parse.find(attrs={'class':'yt-uix-tile-link'})['href']

					full_link = "youtube.com" + first_result
					#print full_link

					video = pafy.new(full_link)
					Unencoded_Title = ((video.title).replace("\\", "_").replace("/", "_").replace(":", "_").replace("*", "_").replace("?", "_").replace('"', "_").replace("<", "_").replace(">", "_").replace("|", "_").replace(" ", "_"))
					Title = Unencoded_Title.encode("utf-8")
					print str(y) + '. ' + Title
					y = y + 1
					if os.path.exists("Music/" + Unencoded_Title + ".m4a.temp"):
						os.remove("Music/" + Unencoded_Title + ".m4a.temp")
					if os.path.exists("Music/" + Unencoded_Title + ".m4a") or os.path.exists("Music/" + Unencoded_Title + ".mp3"):
						with open('Music/spotify.txt', 'r') as fin:
							data = fin.read().splitlines(True)
						with open('Music/spotify.txt', 'w') as fout:
							fout.writelines(data[1:])
					else:
						audiostreams = video.audiostreams
						for a in audiostreams:
							if a.bitrate == "128k" and a.extension == "m4a":
								a.download(filepath="Music/" + Unencoded_Title + ".m4a")
								with open('Music/spotify.txt', 'r') as fin:
									data = fin.read().splitlines(True)
								with open('Music/spotify.txt', 'w') as fout:
									fout.writelines(data[1:])
								print ''

			else:
				song = raw_song.replace(" ", "%20")

				br = mechanize.Browser()
				br.set_handle_robots(False)
				br.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]
				URL = "https://www.youtube.com/results?search_query=" + song
				items = br.open(URL).read()

				items_parse = soup(items, "html.parser")
				br.close()
				first_result = items_parse.find(attrs={'class':'yt-uix-tile-link'})['href']

				full_link = "youtube.com" + first_result
				#print full_link

				video = pafy.new(full_link)
				Unencoded_Title = ((video.title).replace("\\", "_").replace("/", "_").replace(":", "_").replace("*", "_").replace("?", "_").replace('"', "_").replace("<", "_").replace(">", "_").replace("|", "_").replace(" ", "_"))
				Title = Unencoded_Title.encode("utf-8")
				print Title
				trespass = 0
				if os.path.exists("Music/" + Unencoded_Title + ".m4a.temp"):
					os.remove("Music/" + Unencoded_Title + ".m4a.temp")

				if os.path.exists("Music/" + Unencoded_Title + ".m4a") or os.path.exists("Music/" + Unencoded_Title + ".mp3"):
						prompt = raw_input('Song with same name has already been downloaded.. re-download? (y/n/play): ')
						if prompt == "y":
							if os.path.exists("Music/" + Unencoded_Title + ".mp3"):
								os.remove("Music/" + Unencoded_Title + ".mp3")
							else:
								os.remove("Music/" + Unencoded_Title + ".m4a")
							audiostreams = video.audiostreams
							for a in audiostreams:
								if a.bitrate == "128k" and a.extension == "m4a":
									a.download(filepath="Music/" + Unencoded_Title + ".m4a")
							print '' 
						elif prompt =="play":
							if opsys == 'win':
								if os.path.isfile(script_dir + "\Music\\" + Unencoded_Title + ".mp3"):
									os.system('"' + script_dir + "\Music\\" + Unencoded_Title + ".mp3" + '"')
								else:
									os.system('"' + script_dir + "\Music\\" + Unencoded_Title + ".m4a" + '"')
							elif opsys == 'linux':
								if os.path.isfile(script_dir + '/Music/' + Unencoded_Title + '.mp3'):
									os.system('mplayer "' + script_dir + '/Music/' + Unencoded_Title + '.mp3"')
								else:
									os.system('mplayer "' + script_dir + '/Music/' + Unencoded_Title + '.m4a"')
						else:
							pass

				else:
					audiostreams = video.audiostreams
					for a in audiostreams:
						if a.bitrate == "128k" and a.extension == "m4a":
							a.download(filepath="Music/" + Unencoded_Title + ".m4a")
							print ''
		except KeyboardInterrupt:
			pass

Main()