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
        """
        Constructor for the widget
        """
        super(Ui_Dialog, self).__init__()
        self.setupUi(self)

    def setupUi(self, Dialog):
        """
        Set up layout
        """
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(495, 466)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        # creating label (Documents and their similarity with original document)
        self.label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label)

        # creating label
        self.label2 = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label2.setFont(font)
        self.label2.setObjectName(_fromUtf8("label2"))
        self.gridLayout.addWidget(self.label2)

        # creating label (Extent of plagiarism)
        self.label3 = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label3.setFont(font)
        self.label3.setObjectName(_fromUtf8("label3"))
        self.label3.setText("Extent of plagiarism:")
        self.gridLayout.addWidget(self.label3)

        # creating a progress bar
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar)

        # creating a back button
        self.backButton = QtGui.QPushButton(Dialog)
        self.backButton.setObjectName(_fromUtf8("backButton"))
        self.backButton.setText('Back')
        self.backButton.clicked.connect(self.dispose)
        self.gridLayout.addWidget(self.backButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        read_results(self)

    def retranslateUi(self, Dialog):
        """
        Initialize ui elements
        """
        Dialog.setWindowTitle("Results")
        Dialog.setWindowIcon(QtGui.QIcon('plagiarism-image.png'))
        self.label.setText(_translate("Dialog", "Documents and their similarity with original document", None))

    def dispose(self):
        exit(0)


def read_results(ui):
    """
    Read generated results and display bar graph
    """
    scores = pickle.load(open('results', 'rb'))

    import matplotlib.pyplot as plt
    import numpy as np
    n = 10
    x_pos = np.arange(n)
    y_pos = np.arange(10)

    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.25, bottom=0.25)
    plt.xlim(0, 1)
    plt.yticks(y_pos, [score[0] for score in scores])
    bars = plt.barh(x_pos, [0]*n)
    for i in range(n):
        bars[i].set_width(scores[i][1])
    plt.savefig('plot.jpg')

    ui.label2.setPixmap(QtGui.QPixmap('plot.jpg'))

    ui.progressBar.setProperty("value", max([score[1] for score in scores]) * 100)


def main():
    """
    Main method to run the app
    """
    app = QtGui.QApplication(sys.argv)
    ex = Ui_Dialog()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
