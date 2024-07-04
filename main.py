import sys
import random
import math
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from utils import Node, GraphHandler

def random_point(center : QPointF, min: int = 100, max: int = 800) -> QPointF:
    angle = random.uniform(0, 2) * math.pi
    dist = random.randint(min, max)
    
    return center + QPointF(math.cos(angle) * dist, -math.sin(angle) * dist)

if __name__ == '__main__':
    app = QApplication([])

    nodes: list[Node] = [
        Node(
            center=QPointF(400, 400),
            text="Q0"
        ),
    ]
    
    for i in range(1, 12):
        nodes.append(
            Node(
                center=random_point(nodes[0].center, 50, 200),
                text=f"Q{i}"
            )
        )

    scene = QGraphicsScene(0, 0, 800, 600)

    graph = GraphHandler()
    scene.addItem(graph)

    for node in nodes:
        graph.addNode(node)

    for i in range(1, len(nodes)):
        graph.addConnection(nodes[0], nodes[i], str("Teste tetstestets"))
    
    graph.show()

    view = QGraphicsView(scene)
    view.setRenderHint(QPainter.Antialiasing)
    view.show()

    sys.exit(app.exec())
