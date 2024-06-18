from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, QPointF, QRect, QSizeF
from PySide6.QtWidgets import *


class EditableText(QGraphicsTextItem):
    def __init__(self, text: str, center: QPointF = QPointF(0, 0), parent: QGraphicsItem = None):
        super().__init__(text)
        self.setFlags(QGraphicsItem.ItemIsSelectable |
                      QGraphicsItem.ItemIsMovable |
                      QGraphicsItem.ItemIsFocusable)

        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.setDefaultTextColor(Qt.white)

        self.center = center
        self.parente = parent

        self.ReajustSize()

        self.keyReleaseEvent(
            lambda event: event.ignore())

    def keyReleaseEvent(self, _):
        self.ReajustSize()

    def ReajustSize(self):
        self.adjustSize()
        self.setPos(self.center - QPointF(self.textWidth() / 2,
                                          self.boundingRect().height() / 2))

        self.parente.ResizeBorder(self.boundingRect().width() * 1.2)


class Node(QGraphicsItemGroup):
    def __init__(self, center: QPointF, text: str):
        super().__init__()

        self.setHandlesChildEvents(False)
        pen = QPen(Qt.white, 3)

        self.center = center

        self.border = QGraphicsEllipseItem(0, 0, 0, 0)
        self.ResizeBorder()
        self.border.setPen(pen)

        self.text_child = EditableText(text, center, self)

        self.addToGroup(self.border)
        self.addToGroup(self.text_child)

    def ResizeBorder(self, diameter: float = 50):
        diameter = max(diameter, 50)

        self.border.setRect(0, 0, diameter, diameter)
        self.border.setPos(self.center - QPointF(diameter / 2, diameter / 2))
