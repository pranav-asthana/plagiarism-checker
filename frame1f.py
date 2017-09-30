from PyQt4 import QtCore, QtGui
import sys,os

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(QtGui.QWidget):

    def __init__(self):
        super(Ui_Dialog,self).__init__()
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(407, 431)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtGui.QPushButton(Dialog)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.verticalLayout.addWidget(self.pushButton_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("Plagiarism Checker")
        self.label.setText(_translate("Dialog", "enter the document and corpus location", None))
        self.pushButton.setText(_translate("Dialog", "document", None))
        self.pushButton_2.setText(_translate("Dialog", "corpus", None))
        self.pushButton_3.setText(_translate("Dialog", "run", None))
        self.pushButton.clicked.connect(self.docBrowse)
        self.pushButton_2.clicked.connect(self.corpBrowse)
        self.pushButton_3.clicked.connect(self.runCode)
        self.setWindowIcon(QtGui.QIcon('plagiarism-image.png'))
        
    def docBrowse(self):
        filepath = QtGui.QFileDialog.getOpenFileName(self,
                                                          'Single File',
                                                          "C:/",'*.txt')
        print(filepath)
    #select corpus folder
    def corpBrowse(self):
        filepaths = QtGui.QFileDialog.getExistingDirectory(None,
                                                           'Select a folder:',
                                                           'C:/',
                                                           QtGui.QFileDialog.ShowDirsOnly)
        print(filepaths)

    def runCode(self):
        os.system('frame2f.py')

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Ui_Dialog()
    ex.show()
    sys.exit(app.exec_())

