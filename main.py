import sys
from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QPushButton
from graph import Node, GraphHandler, random_node
from mainwindow import MainWindow

if __name__ == '__main__':
    app = QApplication([])

    nodes: list[Node] = [
        Node(
            center=QPointF(400, 400),
            text="Q0"
        ),
    ]
    
    for i in range(1, 12):
        nodes.append(random_node(nodes[0].center, min=100, max=400, name=f"Q{i}"))

    graph = GraphHandler()

    for node in nodes:
        graph.addNode(node)

    for i in range(1, len(nodes)):
        graph.addConnection(nodes[0], nodes[i], "Teste tetstestets")
    
    main_window = MainWindow(graph)
    main_window.show()

    sys.exit(app.exec())
