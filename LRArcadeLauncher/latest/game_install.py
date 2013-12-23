import GameList as GL
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--install", help="Registers the given path")
parser.add_argument("-l","--list", action="store_true",help="Lists currently installed games")
parser.add_argument("-u","--uninstall",help="Unregisters game given its code")
args = parser.parse_args()

xmlPath = 'GameList_example.xml'
games = GL.GameList(xmlPath)
if args.list:
	print(games)
if args.install:
	games.addGame(args.install)
	games.saveToXml(xmlPath)
if args.uninstall:
	games.removeByCode(args.uninstall)
	games.saveToXml(xmlPath)