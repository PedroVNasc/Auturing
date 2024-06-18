import sys
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from utils import Node


if __name__ == '__main__':
    app = QApplication([])

    nodes: list[Node] = [
        Node(
            center=QPointF(400, 400),
            text="Q0"
        ),

        Node(
            center=QPointF(120, 120),
            text="TEsteTEsteTEste"
        ),

        Node(
            center=QPointF(110, 90),
            text="Q2"
        )
    ]

    scene = QGraphicsScene(0, 0, 800, 600)

    for node in nodes:
        scene.addItem(node)

    view = QGraphicsView(scene)
    view.setRenderHint(QPainter.Antialiasing)
    view.show()

    sys.exit(app.exec())
