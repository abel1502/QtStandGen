# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import urllib.parse
import urllib.request
import json
import random
import re


class STYLE:
    # ?font-size: 13px;
    GENERAL = """font-family: Verdana, Arial, Helvetica, sans-serif;background-color: #CDCDCD;"""
    TEXT_FIELD = """background-color: #FFFFFF;"""
    ABILITY_LINK = """font-weight: bold;text-decoration: none;color: #FF0000;"""
    STAND = """"""
    
    def get(name):
        return getattr(STYLE, name)


class PREF:
    VERSION = "0.1a"
    NAME = "Abel Stand Generator v{}".format(VERSION)
    REFERENCE_URL = "http://www.pages.drexel.edu/~dft29/Stand_Generator/Stand-Generation-Overdrive.html"
    GITHUB_URL = "https://github.com/abel1502/QtStandGen"
    LINK = "<a href=\"{0}\">{0}</a>"
    ABILITY_LINK = "<a href=\"{0}\" style=\"color: red\">Link to Ability Page</a>"
    ABOUT = "Abel Stand Generator is a replica of {}.<br><br>The project is hosted on GitHub at {}".format(LINK.format(REFERENCE_URL), LINK.format(GITHUB_URL))
    ITUNES_URL = "http://itunes.apple.com/search?{}"
    POWER_URL = "https://powerlisting.fandom.com/wiki/{}"
    RANDOM_POWER_URL = POWER_URL.format("Special:Random")
    STAND = "Stand Name: {0}\n\nStand Ability: [{1}]({2})\n\nPower - {3[0]}\n\nSpeed - {3[1]}\n\nRange - {3[2]}\n\nDurability - {3[3]}\n\nPrecision - {3[4]}\n\nPotential - {3[5]}\n\nDescription: {4}"


class MainWidget(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init()
    
    def init(self):
        self.initUI()
        
        self.btnGenName.clicked.connect(self.generateName)
        self.btnGenStand.clicked.connect(self.generateStand)
        self.btnCopy.clicked.connect(self.copyStand)
        
        self.curNames = []
        self.curBandName = []
        self.lastSearchSucceeded = False
   
    def initUI(self):
        self.setWindowTitle(PREF.NAME)
        
        self.cw = QWidget(self)
        self.setCentralWidget(self.cw)
        self.cw.setStyleSheet(STYLE.get("GENERAL"))
        
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
        self.inputName.setStyleSheet(STYLE.get("TEXT_FIELD"))
        #self.inputName.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.labelOutputName = QLabel("Expected Name:")
        self.outputName = QLineEdit(self)
        self.outputName.setPlaceholderText("Press the \"Generate Name\" button again if its wrong")
        self.outputName.setReadOnly(True)
        self.outputName.setStyleSheet(STYLE.get("TEXT_FIELD"))
        self.btnGenName = QPushButton("Generate Name", self)
        self.btnGenStand = QPushButton("Generate Stand", self)
        self.labelAbilityLink = QLabel("Link to Ability Page", self)
        self.labelAbilityLink.setStyleSheet(STYLE.get("ABILITY_LINK"))
        self.labelAbilityLink.setOpenExternalLinks(True)
        self.outputStand = QTextEdit(self)
        self.outputStand.setReadOnly(True)
        self.outputStand.setStyleSheet(STYLE.get("STAND"))
        self.outputStand.setStyleSheet(STYLE.get("TEXT_FIELD"))
        self.btnCopy = QPushButton("Copy to Clipboard", self)
        
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
        VGeneralLayout.addWidget(self.labelAbilityLink)
        VGeneralLayout.addWidget(self.outputStand)
        HCopyLayout = QHBoxLayout()
        HCopyLayout.addStretch()
        HCopyLayout.addWidget(self.btnCopy)
        VGeneralLayout.addLayout(HCopyLayout)
        self.cw.setLayout(VGeneralLayout)
    
    def handleError(self, err):
        # TODO: Handle str and Exception differently?
        QMessageBox.warning(self, "Error", "{}".format(err))
    
    def generateName(self):
        try:
            if self.curBandName != self.inputName.text() or not self.lastSearchSucceeded:
                self.curBandName = self.inputName.text()
                lUrl = PREF.ITUNES_URL.format(urllib.parse.urlencode({"term" : self.curBandName}))
                lResults = json.loads(urllib.request.urlopen(lUrl).read().decode())
                self.curNames = self.handleItunesResults(lResults)
            if len(self.curNames) == 0:
                self.handleError("Search was unsuccessful, try again")
                self.lastSearchSucceeded = False
            else:
                self.curName = random.choice(self.curNames)
                self.outputName.setText(self.curName)
                self.lastSearchSucceeded = True
        except:
            self.handleError("Something went wrong when generating name, try again")
            self.lastSearchSucceeded = False
    
    def handleItunesResults(self, results):
        #if results["resultCount"] == 0:
        #    # TODO: handle no results
        #    return
        lNames = []
        for lItem in results["results"]:
            lCurName = lItem["trackCensoredName"]
            if "(" in lCurName:
                lCurName = lCurName[:lCurName.find("(")]
            if lCurName == "Intro":  # ?
                continue
            lNames.append(lCurName)
        return lNames
    
    def generateStand(self):
        try:
            lAbilityName, lAbilityUrl, lAbilityDescription = self.generateAbility()
            lStats = self.generateStats()
            self.outputStand.setText(PREF.STAND.format(self.curName if self.curName else "undefined", lAbilityName, lAbilityUrl, lStats, lAbilityDescription))
        except:
            pass
    
    def copyStand(self):
        try:
            lText = self.outputStand.toPlainText()
            if len(lText) == 0:
                return
            QGuiApplication.clipboard().setText(lText)
        except Exception as e:
            self.handleError(str(e))
    
    def generateStats(self):
        lStats = ["EDCBA"[random.randint(0, 4)] for _ in range(6)]
        return lStats
    
    def generateAbility(self):
        try:
            lData = urllib.request.urlopen(PREF.RANDOM_POWER_URL).read().decode()
            lMetaTagStart = lData.find("og:description")
            assert lMetaTagStart >= 0
            lContentStart = lData.find("content", lMetaTagStart)
            assert lContentStart >= 0
            lDescriptionStart = lData.find("\"", lContentStart) + 1
            assert lDescriptionStart >= 1
            lMetaTagEnd = lData.find("\" />", lDescriptionStart)
            assert lMetaTagEnd >= 0
            lAbilityDescription = lData[lDescriptionStart:lMetaTagEnd]
            lAbilityDescription = lAbilityDescription.replace("&quot;", "\"").replace("&amp;", "&")
            
            # This part differs from the original, might need some testing
            lHeaderStart = lData.find(">", lData.find("<h1")) + 1
            lHeaderEnd = lData.find("</h1>", lHeaderStart)
            lAbilityName = lData[lHeaderStart:lHeaderEnd]
            lAbilityName = lAbilityName.replace("&quot;", "\"").replace("&amp;", "&")
            # TODO: Handle "weird foreign letter"?)
            # This part differs as well: I'm being stricter
            if "Admins" in lAbilityName:
                raise Exception("")
            
            lAbilityUrl = PREF.POWER_URL.format(lAbilityName.replace(" ", "_"))
            self.updateAbilityLink(lAbilityUrl)
            return lAbilityName, lAbilityUrl, lAbilityDescription
        except Exception as e:
            self.handleError("Something went wrong when generating ability, try again"+repr(e))
            raise Exception("")
    
    def updateAbilityLink(self, url):
        self.labelAbilityLink.setText(PREF.ABILITY_LINK.format(url))


def main():
    lApplication = QApplication(sys.argv)
    lMainWidget = MainWidget()
    lMainWidget.show()
    sys.exit(lApplication.exec())


if __name__ == "__main__":
    main()