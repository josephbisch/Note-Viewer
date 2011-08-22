#!/usr/bin/env python

import os
import sys
import urllib
from PyQt4 import Qt
from BeautifulSoup import BeautifulSoup

class HelloApplication(Qt.QApplication):

    fileList = 0
    html_files = []

    def __init__(self, args):
        """ In the constructor we're doing everything to get our application
            started, which is basically constructing a basic QApplication by 
            its __init__ method, then adding our widgets and finally starting 
            the exec_loop."""
        Qt.QApplication.__init__(self, args)
        self.fileList = self.listFiles("/home/joseph/Desktop/markdown",".html",0)
        self.addWidgets()
        self.addFiles()
        self.displayPage(0)
        self.diagnostics()
        self.exec_()        

    def addWidgets(self):
        """ In this method, we're adding widgets and connecting signals from 
            these widgets to methods of our class, the so-called "slots" 
        """
        #self.hellobutton = Qt.QPushButton("Say 'Hello world!'",None)
        #self.connect(self.hellobutton, Qt.SIGNAL("clicked()"), self.slotSayHello)
        #self.hellobutton.show()
        self.window = Qt.QWidget()
        self.window.setWindowTitle("Joe's Notes Viewer")
        self.layout = Qt.QBoxLayout(Qt.QBoxLayout.LeftToRight)

        self.leftBar = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom)

        self.search = Qt.QLineEdit()
        self.search.setPlaceholderText("Search")
        Qt.QObject.connect(self.search, Qt.SIGNAL("textEdited(const QString&)"), self.getResults)
        
        self.selector = Qt.QListWidget()
        self.selector.setMaximumWidth(170)
        Qt.QObject.connect(self.selector, Qt.SIGNAL("currentRowChanged(int)"), self.displayPage)
        
        self.view = Qt.QWebView()
        #self.view.load(Qt.QUrl("http://qt.nokia.com/"))
        
        self.leftBar.addWidget(self.search)
        self.leftBar.addWidget(self.selector)
        self.layout.addLayout(self.leftBar)
        self.layout.addWidget(self.view,1)
        self.window.setLayout(self.layout)
        self.window.show()

    def listFiles(self,direct,extension,time,query=""):
        """ In this method, we're getting a list of files in directory direct with
            file extension extension."""
        global html_files
        print direct
        print query+extension+"$$$$$$$$$$$$$$$"
        if time == 0:
            html_files = [direct+"/"+x for x in os.listdir(direct) if x.endswith(extension) and (self.queryCheck(self.isTextInSource(self.getSource(direct+"/"+x),query)) or query=="")]
            print html_files
        else:
            print "here"
            html_files += [direct+"/"+x for x in os.listdir(direct) if x.endswith(extension) and (self.queryCheck(self.isTextInSource(self.getSource(direct+"/"+x),query)) or query=="")]
            print html_files
        for x in os.listdir(direct):
            print x
            if os.path.isdir(direct+"/"+x):
                print x
                self.listFiles(direct+"/"+x,".html",1,query)
                break
        return html_files

    def addFiles(self):
        """ In this method, we're adding html files to the list widget on the left."""
        self.selector.addItems(self.getBaseNames())
        self.resizeFont()
        if not self.selector.item(0) is None:
            self.selector.item(0).setSelected(True)
            self.displayPage(0)
        else:
            self.displayPage(-1)

    def resizeFont(self):
        for i in range(self.selector.count()):
            font = self.selector.item(i).font()
            font.setPointSize(16)
            self.selector.item(i).setFont(font)

    def getBaseNames(self):
        tempList = []
        for x in self.fileList:
            tempList.append(os.path.splitext(os.path.basename(x))[0])
        return tempList

    def displayPage(self, fileNum):
        #if not isinstance(fileNum, int):
        #    fileNum = self.selector.row(fileNum)
        if fileNum==-1:
            self.window.setWindowTitle("Joe's Notes Viewer")
            self.view.load(Qt.QUrl("about:blank"))
        else:
            self.window.setWindowTitle(self.getBaseNames()[fileNum]+" - Joe's Notes Viewer")
            self.view.load(Qt.QUrl.fromLocalFile(self.fileList[fileNum]))

    def getResults(self, query):
        print query+"************************"
        self.selector.clear()
        self.fileList = self.listFiles("/home/joseph/Desktop/markdown",".html",0,query)
        self.addFiles()

    def getSource(self, htmlFile):
        print htmlFile
        sock = urllib.urlopen(htmlFile)
        source = sock.read()
        sock.close()
        print source+"&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
        return source

    def isTextInSource(self, source, text):
        text = text.lower()
        textStr = BeautifulSoup(source).findAll(text=True)
        textStr = ', '.join(textStr)
        return textStr.lower().find(text)

    def queryCheck(self, num):
        if num==-1:
            return False
        else:
            return True

    def diagnostics(self):
        print self.selector.width()
        print self.window.width()
        #print self.getSource(self.fileList[0])

# Only actually do something if this script is run standalone, so we can test our 
# application, but we're also able to import this program without actually running
# any code.
if __name__ == "__main__":
    app = HelloApplication(sys.argv)
