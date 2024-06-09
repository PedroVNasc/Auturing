import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class Test(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.hello = ['Hello World', 'Olá Mundo']
        
        self.button = QtWidgets.QPushButton('Click')
        self.text = QtWidgets.QLabel("Teste", alignment=QtCore.Qt.AlignCenter)
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        
        self.button.clicked.connect(self.magic)
        
    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    
    widget = Test()
    
    widget.resize(800, 600)
    widget.show()
    
    sys.exit(app.exec())
    # print('Hello, World!')