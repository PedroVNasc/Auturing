from PySide6.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QToolBar, QLabel
from PySide6.QtGui import QMouseEvent, QPainter, QAction, QIcon
from PySide6.QtCore import QPointF, QPoint,  Qt
from graph import GraphHandler, Node, Arrow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.graph = GraphHandler()
        self.graph.setParent(self)
        
        self.source_node: Node = None
        self.mode = "Normal"
        self.setGeometry(0, 0, 1366, 720)
        
        self.setup()

    def setup(self):
        self.scene = QGraphicsScene()
        self.scene.addItem(self.graph)
        
        self.toolbar = QToolBar("Teste", self)
        self.addToolBar(self.toolbar)

        action_normal = QAction(QIcon("icons/normal.png"), "Normal", self)
        action_normal.triggered.connect(lambda: self.changeMode("Normal"))
        self.toolbar.addAction(action_normal)
        
        action_add = QAction(QIcon("icons/add.png"), "Add", self)
        action_add.triggered.connect(lambda: self.changeMode("Add"))
        self.toolbar.addAction(action_add)
        
        action_remove = QAction(QIcon("icons/remove.png")   , "Remove", self)
        action_remove.triggered.connect(lambda: self.changeMode("Remove"))
        self.toolbar.addAction(action_remove)

        self.mode_label = QLabel("Mode: " + self.mode)
        self.mode_label.setAlignment(Qt.AlignRight)
        self.mode_label.setAlignment(Qt.AlignVCenter)
        self.toolbar.addWidget(self.mode_label)

        self.view = QGraphicsView()
        self.view.setParent(self)
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(self.view)

    # def addNode(self):
    #     node = random_node(
    #         self.scene.sceneRect().center(),
    #         min=100,
    #         max=400,
    #         name=f"Q{len(self.scene.items())}",
    #     )

    #     self.graph.addNode(node)
    #     self.graph.addConnection(node, self.graph.nodes[0], "Teste")

    def changeMode(self, mode: str):
        self.mode = mode
        self.mode_label.setText("Mode: " + self.mode)

    def nodeClicked(self, node: Node):
        match self.mode:
            case "Normal":
                print(node.text, node.pos(), node.center)
            case "Add":
                if self.source_node is None or self.source_node is node:
                    self.source_node = node
                else:
                    self.graph.addConnection(self.source_node.text, node.text, "Teste")
                    self.source_node = None
            case "Remove":
                self.graph.removeNode(node)
            case _:
                pass

    def connClicked(self, conn: Arrow):
        match self.mode:
            case "Remove":
                self.graph.removeConnection(conn.source_node, conn.target_node)
            case _:
                pass

    def mousePressEvent(self, event: QMouseEvent) -> None:
        match self.mode:
            case "Add":
                view_pos = self.view.mapFromGlobal(event.globalPos())
                scene_pos = QPointF(self.view.mapToScene(view_pos)) 
                
                self.graph.addNode(scene_pos, "New")

            case _:
                return super().mousePressEvent(event)
