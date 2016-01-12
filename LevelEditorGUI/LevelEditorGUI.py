from copy import *
import time
import pymel.core as pm
import pymel.core.datatypes as dtype
import maya.cmds as cmds
import maya.mel as mel

from maya import OpenMayaUI as omui
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
from shiboken import wrapInstance
from sys import path as pythonPath

pythonPath.append('C:/Users/Joakim/Documents/GitHub/LevelEditorGUI/LevelEditorGUI')


def getMayaWin():
	#get maya window reference
	mayaWinPtr	= omui.MQtUtil.mainWindow()
	mayaWin		= wrapInstance(long(mayaWinPtr), QWidget)

def loadUI(uiName):
	# object to load ui files
	loader = QUiLoader()

	fileDir = ""

	XMLbuffer = None

	for p in pythonPath:
		fname = p + '/' + uiName
		uiFile = QFile(fname)

		if uiFile.exists():
			fileDir = p
			uiFile.open(QFile.ReadOnly)
			XMLbuffer = QByteArray(uiFile.readAll())
			uiFile.close()
			print 'Found UI file path ' + fileDir
			break
		else:
			print 'UI file' + uiName + ' not found ( ' + p + ' )'

	fixXML(XMLbuffer, p)
	qbuff = QBuffer()
	qbuff.open(QBuffer.ReadOnly|QBuffer.WriteOnly)
	qbuff.write(XMLbuffer)
	qbuff.seek(0)
	ui = loader.load(qbuff,parentWidget = getMayaWin())
	ui.path = p
	return ui

def fixXML(qbyteArray, path):
	if path[-1] != '/':
		path = path+'/'
	path = path.replace("/","\\")

	tempArr = QByteArray("<pixmap>" + path + "\\")
	lastPos = qbyteArray.indexOf("<pixmap>", 0)
	while(lastPos!= -1):
		qbyteArray.replace(lastPos,len("<pixmap>"),tempArr)
		lastPos = qbyteArray.indexOf("<pixmap>", lastPos+1)
	return

class UIController(QObject):
	def __init__(self, ui, mainObject):
		self.mainObject = mainObject
		QObject.__init__(self)
		ui.closeButton.clicked.connect(self.closeUI)
		ui.runButton.clicked.connect(self.runPlugin)
		ui.stopButton.clicked.connect(self.unloadPlugin)
        
		self.ui = ui
		self.ui.show()

	def closeUI(self):
		self.ui.close()
	def showUI(self):
		self.ui.show()
	def runPlugin(self):
	    cmds.loadPlugin("C:/Users/Joakim/Documents/GitHub/UD1414LevelEditorMayaPlugin/UD1414_PluginEditor/x64/Debug/UD1414_Ass02_MayaPlugin_JW.mll")
	def unloadPlugin(self):
	    mel.eval("unloadPluginWithCheck( `C:/Users/Joakim/Documents/GitHub/UD1414LevelEditorMayaPlugin/UD1414_PluginEditor/x64/Debug/UD1414_Ass02_MayaPlugin_JW.mll` );")

class MainObject(object):
	def __init__(self):
		self.beep = 0

mainObj = MainObject()
cont = UIController(loadUI('testWindow.ui'), mainObj)

"""waitCursor -state on;								
$ignoreUpdateCallback = true;						
catch(`loadPlugin "C:/Users/Joakim/Documents/GitHub/UD1414LevelEditorMayaPlugin/UD1414_PluginEditor/x64/Debug/UD1414_Ass02_MayaPlugin_JW.mll"`);				
updatePluginUI( "56" );				
$ignoreUpdateCallback = false;						
waitCursor -state off;"""