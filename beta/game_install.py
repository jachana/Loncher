import system.game_man.gamelist as GL
import system.launcher_config as AC
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--install", help="Registers the given path")
parser.add_argument("-l","--list", action="store_true",help="Lists currently installed games")
parser.add_argument("-u","--uninstall",help="Unregisters game given its code")
args = parser.parse_args()

cfg = AC.Loadcfg()
xmlPath = AC.gameList
games = GL.GameList(xmlPath)
if args.list:
	print(games)
if args.install:
	games.add_game(args.install)
	games.save_xml(xmlPath)
	print("Added "+args.install+" to the registry")
if args.uninstall:
	print("Removing "+args.uninstall+"...")
	games.remove_code(args.uninstall)
	games.save_xml(xmlPath)
	print("Done.")