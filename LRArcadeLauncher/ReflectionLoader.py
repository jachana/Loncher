from LRArcadeLauncher import GameCaller
import imp

def LaunchGameFromFile(filename,classname):
	imp.load_source(classname,filename)
	toLoad = classname()
	caller = GameCaller()
	caller.GameCall(toLoad,true)