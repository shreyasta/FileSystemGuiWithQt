import re
import sys
import os
import glob
from pathlib import Path
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QWidget, QListWidget, QHBoxLayout, QLabel, \
    QFileDialog, \
    QSlider, QVBoxLayout, QListWidgetItem, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal, QObject, pyqtSlot, QDir
from FACSAUGUI.src.samples.FileExamples import Player




class Example(QWidget):

    # Adding signals
    externalSignal = QtCore.pyqtSignal([str])
    direxternalSignal = QtCore.pyqtSignal([str])
    listpathSignal = QtCore.pyqtSignal([str])
    listpath31MaxSignal = QtCore.pyqtSignal([int])
    itemDoubleClickedSignal = QtCore.pyqtSignal([int])
    listpathnextSignal = QtCore.pyqtSignal([str])

    def __init__(self):
        super().__init__()
        self.initUI()
        self.buttonLayout = ""

    def initUI(self):
        # defining layouts and components
        self.vbox = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.listwidget = QListWidget()
        self.label = QLabel()
        self.Addbtn = QPushButton("Add")
        self.Removebtn = QPushButton("Remove")
        self.Nextbtn = QPushButton("Next")
        self.Previousbtn = QPushButton("Previous")
        self.Slider = QSlider(Qt.Horizontal)
        self.lineEditResult = QLineEdit()
        self.a = self.listwidget.currentRow()
        self.b = self.listwidget.count()




        # adding buttons components to buttonlayout
        self.buttonLayout.addWidget(self.Addbtn)
        self.buttonLayout.addWidget(self.Removebtn)


        # connecting buttons to their resp. functions
        self.Addbtn.clicked.connect(self.getFile)
        self.Removebtn.clicked.connect(self.remFile)
        self.listwidget.itemDoubleClicked.connect(self.itemDoubleClick)
        self.listwidget.itemClicked.connect(self.itemSingleClick)
        #self.externalSignal.connect(self.showItem)
        self.direxternalSignal.connect(self.updateLoad)



        self.vbox.addWidget(self.listwidget)
        self.vbox.addWidget(self.label)
        self.vbox.addLayout(self.buttonLayout)
        self.setLayout(self.vbox)


    def getFile(self):
        self.fnameOpen, filter = QFileDialog.getOpenFileNames(self, 'Open file', 'C:\\', " Image files (*.jpg *.gif *.png *.bmp)")

        self.files_in_path = []

        for f in self.fnameOpen:
                self.files_in_path.append(f)

        self.listwidget.addItems(self.files_in_path)
        self.listwidget.update()
        self.externalSignal[str].emit(self.listwidget.item(0).text())
        self.count = self.listwidget.count()
        self.listpath31MaxSignal[int].emit(self.count-1)

    # removes the selected row displayed in the listwidget

    def remFile(self):
        self.a = self.listwidget.currentRow()
        self.b = self.listwidget.count()

        #if self.b > 0:

        if self.a == 0:
            self.listwidget.takeItem(self.a)
            if self.b>1:
                self.listpathSignal.emit(self.listwidget.currentItem().text())
            else:
                self.listpathSignal.emit('')

            #self.listpath31MaxSignal[int].emit(0)

            #self.listpath31MaxSignal[int].emit(self.listwidget.currentRow())
            #self.listpathnextSignal[str].emit(self.listwidget.currentItem().text())
            print("GRAY 0th row removed, the next highlighted row is " + str(self.listwidget.currentRow()) )
            #print("the highlighted text is " + self.listwidget.currentItem().text() )
            #
            if self.a == -1:
                self.listwidget.clear()
                #self.listwidget.takeItem(self.a)
                print("GRAY 0th row removed, the next highlighted row is " + str(self.listwidget.currentRow()))

            #     #print("GRAY 0th row removed, the next highlighted row is " + str(self.listwidget.currentRow()))
            #     #print("the highlighted text is " + self.listwidget.currentItem().text())
            #     self.listwidget.takeItem(self.a)


        else:
            self.listwidget.takeItem(self.a)
            self.listwidget.update()
            #print("Count after removing removing file: "+ str(self.a))
            #self.listpath31MaxSignal[int].emit(self.b -1)
            self.listpath31MaxSignal[int].emit(self.listwidget.currentRow())

            self.listpathSignal[str].emit(self.listwidget.currentItem().text())
            print("GRAY The current row is " + str(self.listwidget.currentRow()) + " the highlighted text is  " + self.listwidget.currentItem().text() )

        self.listpath31MaxSignal[int].emit(max(self.listwidget.count() - 1, 0))

    @pyqtSlot()
    def NextFile(self):
        self.a = self.listwidget.currentRow()
        self.b = self.listwidget.count()
        if self.b == 0:
            return
        if self.a == (self.b - 1):
            self.listwidget.setCurrentItem(self.listwidget.item(0))
            self.listwidget.setFocus()
            self.listpathnextSignal[str].emit(self.listwidget.currentItem().text())
            self.itemDoubleClickedSignal[int].emit(self.listwidget.currentRow())

        else:
            self.listwidget.setCurrentItem(self.listwidget.item(self.a + 1))
            self.listwidget.setFocus()
            self.listpathnextSignal[str].emit(self.listwidget.currentItem().text())
            print(self.listwidget.currentRow())
            self.itemDoubleClickedSignal[int].emit(self.listwidget.currentRow())


    @pyqtSlot()
    def PreviousFile(self):
        self.a = self.listwidget.currentRow()
        self.b = self.listwidget.count()

        if self.a == 0 or self.a == -1 :
            self.listwidget.setCurrentItem(self.listwidget.item(self.b - 1))
            self.listpathnextSignal[str].emit(self.listwidget.currentItem().text())
            self.itemDoubleClickedSignal[int].emit(self.listwidget.currentRow())

            #self.Slider.setSliderPosition(self.a)

        else:
            d = self.listwidget.setCurrentItem(self.listwidget.item(self.a - 1))
            self.listpathnextSignal[str].emit(self.listwidget.currentItem().text())
            self.itemDoubleClickedSignal[int].emit(self.listwidget.currentRow())
            #self.component3.Slider.setSliderPosition(self.a)

    @pyqtSlot(int)
    def intValueToText(self, value):
        #print("Item clicked in a list: "+ str(self.count))
        self.listwidget.item(value).setSelected(True)
        self.listwidget.setFocus()
        self.listwidget.setCurrentItem(self.listwidget.item(value))
        self.listpathSignal.emit(self.listwidget.item(value).text())


    @pyqtSlot(int)
    def disValue(self, value):
        print(("The value is: " + str(value)))

    @pyqtSlot()
    def itemSingleClick(self):
        self.externalSignal[str].emit(self.listwidget.currentItem().text())
        self.itemDoubleClickedSignal[int].emit(self.listwidget.currentRow())
        print("DARK BLUE, Single click: The highlighted item path is:  " + self.listwidget.currentItem().text())

    @pyqtSlot()
    def itemDoubleClick(self):
        self.externalSignal[str].emit(self.listwidget.currentItem().text())
        self.itemDoubleClickedSignal[int].emit(self.listwidget.currentRow())
        print("DARK BLUE, Double click: The blue highlighted item path is:  " + self.listwidget.currentItem().text() )


    @pyqtSlot()
    def updateLoad(self):
        print(self.listwidget.update())
        print(self.listwidget.item(0).text())


    @pyqtSlot(str)
    def showItem(self, text):
        print(text)

    @pyqtSlot()
    def dirLoad(self):
        self.direxternalSignal[str].emit(self.listwidget.item(0).text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
