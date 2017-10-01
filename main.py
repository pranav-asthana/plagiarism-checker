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
    
    ## widget initialisation ##
    def __init__(self):
        super(Ui_Dialog,self).__init__()
        self.setupUi(self)
        self.target_path = None
        self.corpus_path = None

    def setupUi(self, Dialog):
        ## set layout of widget ##
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(407, 431)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        
        ## create labels ##
        self.label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        
        
        ## create radio buttons ##
        self.static = QtGui.QRadioButton('static corpus', self)
        self.dynamic = QtGui.QRadioButton('Dynamic corpus (google search, will be slower)', self)
        self.searchType = QtGui.QButtonGroup()
        self.searchType.addButton(self.static)
        self.searchType.addButton(self.dynamic)
        self.verticalLayout_2.addWidget(self.static)
        self.verticalLayout_2.addWidget(self.dynamic)

        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        
        ## create checkbox ##
        self.chkBoxItem = QtGui.QCheckBox()
        self.chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
        self.chkBoxItem.setText('Preprocess corpus')
        self.verticalLayout.addWidget(self.chkBoxItem)
        
        ##create push buttons ##
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
        ## binding ui elements with their functions ##
        Dialog.setWindowTitle("Plagiarism Checker")
        self.label.setText(_translate("Dialog", "enter the document and corpus location", None))
        self.pushButton.setText(_translate("Dialog", "document", None))
        self.pushButton_2.setText(_translate("Dialog", "corpus", None))
        self.pushButton_3.setText(_translate("Dialog", "run", None))
        self.pushButton.clicked.connect(self.docBrowse)
        self.pushButton_2.clicked.connect(self.corpBrowse)
        self.pushButton_3.clicked.connect(self.runCode)
        self.dynamic.clicked.connect(self.dynamicClicked)
        self.static.clicked.connect(self.staticClicked)

        self.setWindowIcon(QtGui.QIcon('plagiarism-image.png'))
    
    
    ## function to browse the document ##
    def docBrowse(self):
        self.target_path = QtGui.QFileDialog.getOpenFileName(self,
                                                          'Single File',
                                                          "C:/",'*')
        self.pushButton.setText("Document: " + self.target_path)
        print(self.target_path)
        
    ## function to select the corpus folder ##
    def corpBrowse(self):
        self.corpus_path = QtGui.QFileDialog.getExistingDirectory(None,
                                                           'Select a folder:',
                                                           'C:/',
                                                           QtGui.QFileDialog.ShowDirsOnly)
        self.pushButton_2.setText("Corpus: " + self.corpus_path)
        print(self.corpus_path)
        
    ## function to run the tf-idf code ##
    def runCode(self):
        if self.target_path == None or len(self.target_path) < 1:
            print('Please select a target document for checking!')
            return

        if self.static.isChecked():
            if self.corpus_path == None or len(self.corpus_path) < 1:
                print('Please select a corpus!')
                return

            preprocess = ''
            if self.chkBoxItem.isChecked():
                preprocess = '-p '

            print('running' + 'python tf_idf.py ' + preprocess  + self.corpus_path + ' ' + self.target_path)
            os.system('python tf_idf.py ' + preprocess  + self.corpus_path + ' ' + self.target_path)
            os.system('python frame2f.py')

        if self.dynamic.isChecked():
            os.system('python fetch.py ' + self.target_path)
            os.system('python tf_idf.py -p google_retrieved/' + ' ' + self.target_path)
            os.system('python frame2f.py')

    def dynamicClicked(self):
        self.pushButton_2.hide()
        self.chkBoxItem.hide()

    def staticClicked(self):
        self.pushButton_2.show()
        self.chkBoxItem.show()

## main method to create the gui app ##
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Ui_Dialog()
    ex.show()
    sys.exit(app.exec_())
