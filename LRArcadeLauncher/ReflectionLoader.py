from LRArcadeLauncher import GameCaller
import imp

def LaunchGameFromFile(filename,classname,modulename):
	loaded = imp.load_source(modulename,filename)
	toLoad = eval("loaded."+classname)()
	print(toLoad.Go)
	print(loaded)
	print(toLoad)
	caller = GameCaller()
	caller.GameCall(toLoad,True)
