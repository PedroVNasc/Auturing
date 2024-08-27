import sys
from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QPushButton
from graph import random_point
from mainwindow import MainWindow

if __name__ == '__main__':
    app = QApplication([])

    main_window = MainWindow()

    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        nodes: list[QPointF] = [QPointF(200, 200)]
    
        for i in range(1, 12):
            nodes.append(random_point(nodes[0], min=200, max=400, name=f"Q{i}"))

        for i in range(len(nodes)):
            main_window.graph.addNode(nodes[i], f"Q{i}")

        for i in range(1, len(nodes)):
            main_window.graph.addConnection("Q0", f"Q{i}", "Teste tetstestets")
    
    
    main_window.show()

    sys.exit(app.exec())
