from PyQt4 import QtCore, QtGui
import sys
import pickle

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
        Dialog.resize(495, 466)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        # self.listWidget = QtGui.QListWidget(Dialog)
        # self.listWidget.setObjectName(_fromUtf8("listWidget"))
        # self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 1)

        self.label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label)

        self.label2 = QtGui.QLabel(Dialog)
        # font = QtGui.QFont()
        # font.setPointSize(10)
        # self.label2.setFont(font)
        self.label2.setObjectName(_fromUtf8("label2"))
        self.gridLayout.addWidget(self.label2)

        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar)

        # self.verticalScrollBar = QtGui.QScrollBar(Dialog)
        # self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        # self.verticalScrollBar.setObjectName(_fromUtf8("verticalScrollBar"))
        # self.gridLayout.addWidget(self.verticalScrollBar, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        read_results(self)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("Results")
        Dialog.setWindowIcon(QtGui.QIcon('plagiarism-image.png'))
        self.label.setText(_translate("Dialog", "Documents and their similarity with original document", None))

def read_results(ui):
    scores = pickle.load(open('results', 'rb'))

    import matplotlib.pyplot as plt
    import numpy as np
    n = 10
    x_pos = np.arange(n)
    y_pos = np.arange(10)

    fig, ax = plt.subplots()
    plt.subplots_adjust(left = 0.25, bottom = 0.25)
    plt.xlim(0, 1)
    plt.yticks(y_pos, [score[0] for score in scores])
    bars = plt.barh(x_pos, [0]*n)
    for i in range(n):
        bars[i].set_width(scores[i][1])
    plt.savefig('plot.jpg')


    for score in scores:
        # ui.listWidget.addItem(str(score[0]) + ' : ' + str(score[1]))
        ui.label2.setPixmap(QtGui.QPixmap('plot.jpg'))
    pass

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Ui_Dialog()
    ex.show()
    sys.exit(app.exec_())
