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
        self.window = Qt.QWidget()
        self.window.setWindowTitle("Joe's Notes Viewer")
        self.layout = Qt.QBoxLayout(Qt.QBoxLayout.LeftToRight)

        self.leftBar = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom)
        self.rightBar = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom)

        self.search = Qt.QLineEdit()
        self.search.setPlaceholderText("Type to Search")
        self.searchShortcut = Qt.QShortcut(Qt.QKeySequence("ALT+S"), self.search)
        Qt.QObject.connect(self.searchShortcut, Qt.SIGNAL("activated()"), self.search.setFocus)
        Qt.QObject.connect(self.search, Qt.SIGNAL("textEdited(const QString&)"), self.getResults)
        
        self.selector = Qt.QListWidget()
        self.selector.setMaximumWidth(170)
        Qt.QObject.connect(self.selector, Qt.SIGNAL("currentRowChanged(int)"), self.displayPage)

        self.printButton = Qt.QPushButton("&Print")
        self.printButton.setMaximumWidth(self.printButton.sizeHint().width())
        Qt.QObject.connect(self.printButton, Qt.SIGNAL("clicked()"), self.printNote)
        
        self.view = Qt.QWebView()
        
        self.leftBar.addWidget(self.search)
        self.leftBar.addWidget(self.selector)
        self.rightBar.addWidget(self.printButton, 1, Qt.Qt.AlignRight)
        self.rightBar.addWidget(self.view, 2)
        self.layout.addLayout(self.leftBar)
        self.layout.addLayout(self.rightBar, 3)
        self.window.setLayout(self.layout)
        self.window.show()

    def listFiles(self,direct,extension,time,query=""):
        """ In this method, we're getting a list of files in directory direct with
            file extension extension."""
        global html_files
        if time == 0:
            html_files = [direct+"/"+x for x in os.listdir(direct) if x.endswith(extension) and (self.queryCheck(self.isTextInSource(self.getSource(direct+"/"+x),query)) or query=="")]
        else:
            html_files += [direct+"/"+x for x in os.listdir(direct) if x.endswith(extension) and (self.queryCheck(self.isTextInSource(self.getSource(direct+"/"+x),query)) or query=="")]
            print html_files
        for x in os.listdir(direct):
            if os.path.isdir(direct+"/"+x):
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
        """ Makes the font size of the items int he list widget big."""
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
        if fileNum==-1:
            self.window.setWindowTitle("Joe's Notes Viewer")
            self.view.load(Qt.QUrl("about:blank"))
        else:
            self.window.setWindowTitle(self.getBaseNames()[fileNum]+" - Joe's Notes Viewer")
            self.view.load(Qt.QUrl.fromLocalFile(self.fileList[fileNum]))

    def getResults(self, query):
        self.selector.clear()
        self.fileList = self.listFiles("/home/joseph/Desktop/markdown",".html",0,query)
        self.addFiles()

    def getSource(self, htmlFile):
        sock = urllib.urlopen(htmlFile)
        source = sock.read()
        sock.close()
        return source

    def isTextInSource(self, source, text):
        text = str(text).lower()
        textStr = BeautifulSoup(source).findAll(text=True)
        textStr = ''.join(textStr)
        if self.isSimpleSearch(text):
            text = text.strip().strip('\"')
            return str(textStr).lower().find(text)
        else:
            return self.complexFind(str(textStr).lower(),text)

    def isSimpleSearch(self, query):
        """ The space character causes a search to not be simple. Surrounding the search with quotes forces the search to be simple."""
        query = Qt.QString(query)
        tempQuery = Qt.QString(query)
        print tempQuery.compare(query.remove(Qt.QChar(' ')))
        if tempQuery!=query.remove(Qt.QChar(' ')) and not (query.trimmed().startsWith(Qt.QChar('\"')) and query.trimmed().endsWith(Qt.QChar('\"'))):
            return False
        else:
            return True

    def complexFind(self, source, text):
        """ If any word in the search text is not in the source of the html file, -1 is returned, otherwise, 0 is returned."""
        textArray = text.split(' ')
        for x in textArray:
            if (not x in source):
                return -1
        return 0

    def queryCheck(self, num):
        if num==-1:
            return False
        else:
            return True

    def printNote(self):
        printer = Qt.QPrinter()
        printDialog = Qt.QPrintDialog()
        if printDialog.exec_() == Qt.QDialog.Accepted:
            self.view.print_(printer)

    def diagnostics(self):
        """ For debugging perposes."""
        print self.selector.width()
        print self.window.width()

# Only actually do something if this script is run standalone, so we can test our 
# application, but we're also able to import this program without actually running
# any code.
if __name__ == "__main__":
    app = HelloApplication(sys.argv)
