# from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QGraphicsSceneMouseEvent
import numpy as np
import random
from math import sin, cos, pi
from typing import TypedDict
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

ALLOWED_KEYS = {
    Qt.Key_Backspace,
    Qt.Key_Delete,
    Qt.Key_Left,
    Qt.Key_Right,
    Qt.Key_Up,
    Qt.Key_Down,
    Qt.Key_Shift
}


def random_node(center: QPointF, min: int = 100, max: int = 800, name: str = "") -> QPointF:
    angle = random.uniform(0, 2) * pi
    dist = random.randint(min, max)

    node = Node(
        center=center + QPointF(cos(angle) * dist, -sin(angle) * dist),
        text=name
    )

    return node


class EditableText(QGraphicsTextItem):
    def __init__(self, text: str, center: QPointF = QPointF(0, 0), max_length: int = 30):
        super().__init__(text)
        self.setFlags(QGraphicsItem.ItemIsFocusable)

        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.setDefaultTextColor(Qt.white)

        self.center = center
        self.max_length = max_length

        self.ReajustSize()

        self.keyReleaseEvent(lambda event: event.ignore())

    def keyReleaseEvent(self, _):
        self.ReajustSize()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            event.ignore()
            return

        if len(self.toPlainText()) >= self.max_length and event.key() not in ALLOWED_KEYS:
            event.ignore()
            return

        super().keyPressEvent(event)

    def ReajustSize(self):
        self.adjustSize()
        self.setPos(self.center - QPointF(self.textWidth() / 2,
                                          self.boundingRect().height() / 2))

        if self.parentItem():
            self.parentItem().resizeBorder(self.boundingRect().width() * 1.2)
            self.parentItem().text = self.toPlainText()


class Node(QGraphicsItem):
    def __init__(self, center: QPointF, text: str):
        super().__init__()

        self.setFlags(QGraphicsItem.ItemIsMovable |
                      QGraphicsItem.ItemIsSelectable |
                      QGraphicsItem.ItemIsFocusable |
                      QGraphicsItem.ItemSendsGeometryChanges)

        pen = QPen(Qt.white, 3)

        self.center = center
        self.text = text
        self.translocation = QPointF(0, 0)
        self.diameter = 50

        self.border = QGraphicsEllipseItem(0, 0, 0, 0)
        self.border.setParentItem(self)
        self.border.setPen(pen)

        self.text_child = EditableText(self.text, center)
        self.text_child.setParentItem(self)

        self.resizeBorder()

    def boundingRect(self):
        return self.childrenBoundingRect()

    def paint(self, *args):
        pass

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.translocation = value
            print("Scene Pos: " + str(self.scenePos().x()) + " " + str(self.scenePos().y()))
            print("Local Pos: " + str(self.pos().x()) + " " + str(self.pos().y()))
            # print(value)
            
            if self.parentItem():
                self.parentItem().updateConnection(self)

        return value

    def getText(self):
        return self.text_child.toPlainText()

    def resizeBorder(self, diameter: float = 50):
        diameter = max(diameter, 50)

        self.border.setRect(0, 0, diameter, diameter)
        self.border.setPos(self.center - QPointF(diameter / 2, diameter / 2))

        self.diameter = diameter

        if self.parentItem():
            self.parentItem().updateConnection(self)
    
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.parentItem().sendEventUpwards("NodePress", self)
        
        return super().mousePressEvent(event)


class Arrow(QGraphicsLineItem):
    def __init__(self, source: Node, target: Node, data: str):
        super().__init__()

        self.source_node = source
        self.target_node = target
        
        self.source, self.target, self.angle = self.calculateLine(
            source, target)
        self.data = data

        self.head = QGraphicsPolygonItem(self.drawHead())
        self.head.setParentItem(self)

        self.text = QGraphicsTextItem(data)
        self.text.setParentItem(self)

        pen = QPen(Qt.white, 3)
        self.setPen(pen)

        self.head.setPen(pen)
        self.head.setBrush(QBrush(Qt.white))

        self.updateLine(source, target, data)

    def drawHead(self, size=7):
        rotation_matrix = np.array([
            [cos(self.angle), sin(self.angle)],
            [-sin(self.angle), cos(self.angle)]
        ])

        points = np.array([
            [0, 0],
            [-size*2, size],
            [-size*2, -size],
        ])

        triangle = QPolygonF()
        for point in points:
            point = rotation_matrix @ point
            triangle.append(QPointF(point[0], point[1]))

        return triangle

    def calculateLine(self, source_node: Node, target_node: Node):
        source_center = source_node.center + source_node.translocation
        target_center = target_node.center + target_node.translocation

        # In radians
        angle = QLineF(source_center, target_center).angle() / 180 * pi

        xs = cos(angle) * source_node.diameter / 2
        ys = -sin(angle) * source_node.diameter / 2

        xt = cos(angle + pi) * target_node.diameter / 2
        yt = -sin(angle + pi) * target_node.diameter / 2

        source_pos = source_center + QPointF(xs, ys)
        target_pos = target_center + QPointF(xt, yt)

        return source_pos, target_pos, angle

    def updateLine(self, source: Node, target: Node, data: str = ''):
        self.source, self.target, self.angle = self.calculateLine(
            source, target)
        self.data = data if len(data) > 0 else self.data

        degrees = -self.angle * 180 / pi
        text_width = self.text.boundingRect().width() / 2
        transform = QTransform()

        # It must come before the translation
        if -degrees > 90 and -degrees < 270:
            transform.scale(-1, -1)

        transform.translate(-cos(self.angle) * text_width,
                            sin(self.angle) * text_width)

        self.text.setRotation(degrees)
        self.text.setTransform(transform)
        self.text.setPos(self.target - (self.target - self.source) / 2)
        self.text.setPlainText(self.data)

        self.head.setPos(self.target)
        self.head.setPolygon(self.drawHead())

        self.setLine(QLineF(self.source, self.target))

    def paintEvent(self, event):
        painter = QPainter()
        painter.pen = QPen(Qt.white, 3)
        painter.drawPolygon(self.head)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.parentItem().sendEventUpwards("ConnPress", self)
        return super().mousePressEvent(event)


class NodeConnection(TypedDict):
    source_node: Node
    target_node: Node
    data: str
    line: Arrow


class GraphHandler(QGraphicsWidget):
    def __init__(self, nodes: list[Node] = []):
        super().__init__()

        self.mode = "Normal"
        self.nodes: list[Node] = []
        self.connections: list[NodeConnection] = []

        for node in nodes:
            self.addNode(node)

    def addNode(self, node: Node):
        node.setParentItem(self)
        self.nodes.append(node)

    def removeNode(self, node: Node):
        self.nodes.remove(node)
        node.setParentItem(None)

        conns = self.getConnections(node) + self.getConnections(node, target=True)
        for conn in conns:
            self.removeConnection(conn['source_node'], conn['target_node'])

        node.hide()
        self.update()

    def addConnection(self, source_node: Node, target_node: Node, data: str):
        connections = self.getConnections(source_node)

        # Update data
        for conn in connections:
            if conn['target_node'] is target_node:
                conn['data'] = data
                return

        line = Arrow(source_node, target_node, data)

        line.setParentItem(self)

        # Add new connection
        self.connections.append(
            NodeConnection(
                source_node=source_node,
                target_node=target_node,
                data=data,
                line=line
            )
        )

    def getConnections(self, node: Node, target: bool = False) -> list[NodeConnection]:
        connection = []

        key = 'target_node' if target else 'source_node'

        for conn in self.connections:
            if conn[key] == node:
                connection.append(conn)
        return connection

    def removeConnection(self, source_node: Node, target_node: Node):
        connections = self.getConnections(source_node)

        # Ignore if no connections
        if len(connections) == 0:
            return

        for conn in connections:
            if conn['target_node'] == target_node:
                line = conn['line']
                line.setParentItem(None)
                line.hide()

                self.connections.remove(conn)
                return

    def updateConnection(self, node: Node, data: str = ''):
        connections = self.getConnections(
            node) + self.getConnections(node, target=True)

        for conn in connections:
            conn['line'].updateLine(
                conn['source_node'], conn['target_node'], data)
            
    def sendEventUpwards(self, type: str, sender = None):
        match (type):
            case "NodePress":
                self.parent().nodeClicked(sender)
            case "ConnPress":
                self.parent().connClicked(sender)
            case _:
                pass