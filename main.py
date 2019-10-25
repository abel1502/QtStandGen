# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import urllib.parse
import urllib.request
import json



class STYLE:
    # Styles go here
    
    def get(name):
        return getattr(STYLE, name)


class PREF:
    VERSION = "0.1a"
    NAME = "Abel Stand Generator v{}".format(VERSION)
    REFERENCE_URL = "http://www.pages.drexel.edu/~dft29/Stand_Generator/Stand-Generation-Overdrive.html"
    GITHUB_URL = "https://github.com/abel1502/QtStandGen"
    LINK = "<a href=\"{0}\">{0}</a>"
    LINK_NAME = "<a href=\"{0}\">{1}</a>"
    ABOUT = "Abel Stand Generator is a replica of {}.<br><br>The project is hosted on GitHub at {}".format(LINK.format(REFERENCE_URL), LINK.format(GITHUB_URL))
    ITUNES_URL = "http://itunes.apple.com/search?{}"


class MainWidget(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init()
    
    def init(self):
        self.initUI()
        
        self.btnGenName.clicked.connect(self.generateName)
        self.btnGenStand.clicked.connect(self.generateStand)
   
    def initUI(self):
        self.setWindowTitle(PREF.NAME)
        
        self.cw = QWidget(self)
        self.setCentralWidget(self.cw)
        
        self.menuFile = self.menuBar().addMenu("&File")
        self.menuAbout = self.menuBar().addMenu("&About")
        self.actionExit = QAction("&Exit", self)
        self.actionExit.triggered.connect(lambda: sys.exit(0))
        self.actionAbout = QAction("&About", self)
        self.actionAbout.triggered.connect(lambda: QMessageBox.about(self, "About {}".format(PREF.NAME), PREF.ABOUT))
        self.menuFile.addAction(self.actionExit)
        self.menuAbout.addAction(self.actionAbout)
        
        self.labelInputName = QLabel("Enter the artist's name and the album you wish to use:", self)
        self.inputName = QLineEdit(self)
        self.inputName.setPlaceholderText("e.g. Gorillaz Demon Days")
        #self.inputName.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.labelOutputName = QLabel("Expected Name:")
        self.outputName = QLineEdit(self)
        self.outputName.setPlaceholderText("Press the \"Generate Name\" button again if its wrong")
        self.outputName.setReadOnly(True)
        self.btnGenName = QPushButton("Generate Name", self)
        self.btnGenStand = QPushButton("Generate Stand", self)
        self.labelAbilityLink = QLabel("Link to Ability Page:", self)
        self.outputAbilityLink = QLineEdit(self)
        self.outputAbilityLink.setReadOnly(True)
        self.outputStand = QTextEdit(self)
        self.outputStand.setReadOnly(True)
        
        VGeneralLayout = QVBoxLayout()
        VGeneralLayout.addWidget(self.labelInputName)
        VGeneralLayout.addWidget(self.inputName)
        VGeneralLayout.addWidget(self.labelOutputName)
        VGeneralLayout.addWidget(self.outputName)
        # ======
        #HBtnLayout = QHBoxLayout()
        #HBtnLayout.addWidget(self.btnGenName)
        #HBtnLayout.addWidget(self.btnGenStand)
        #VGeneralLayout.addLayout(HBtnLayout)
        # ======
        HNameBtnLayout = QHBoxLayout()
        HStandBtnLayout = QHBoxLayout()
        HNameBtnLayout.addWidget(self.btnGenName)
        HNameBtnLayout.addStretch()
        HStandBtnLayout.addWidget(self.btnGenStand)
        HStandBtnLayout.addStretch()
        VGeneralLayout.addLayout(HNameBtnLayout)
        VGeneralLayout.addLayout(HStandBtnLayout)
        # ======
        HAbilityLinkLayout = QHBoxLayout()
        HAbilityLinkLayout.addWidget(self.labelAbilityLink)
        HAbilityLinkLayout.addWidget(self.outputAbilityLink)
        VGeneralLayout.addLayout(HAbilityLinkLayout)
        VGeneralLayout.addWidget(self.outputStand)
        self.cw.setLayout(VGeneralLayout)
    
    def generateName(self):
        lUrl = PREF.ITUNES_URL.format(urllib.parse.urlencode({"term" : self.inputName.text()}))
        lResults = json.loads(urllib.request.urlopen(lUrl).read().decode())
        self.handleItunesResults(lResults)
    
    def handleItunesResults(self, results):
        print(results)
        if results["resultCount"] == 0:
            # TODO: handle no results
            return
        lNames = []
        for lItem in results["results"]:
            lNames.append(lItem["trackCensoredName"])
        print(lNames)
        sys.stdout.flush()
    
    def generateStand(self):
        pass


def main():
    lApplication = QApplication(sys.argv)
    lMainWidget = MainWidget()
    lMainWidget.show()
    sys.exit(lApplication.exec())


if __name__ == "__main__":
    main()