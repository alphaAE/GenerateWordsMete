from PyQt5.QtCore import pyqtSignal, Qt, QRect, QSize, QPoint
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QLayout, QPushButton, QSizePolicy, QWidget, QSpacerItem)
import sys
import csv


class FlowLayout(QLayout):
    """流式布局,使用说明
    1.声明流式布局 layout = FlowLayout
    2.将元素放入流式布局中
    3.将QGroupBox应用流式布局
    4.如果期望水平流式,将QGroupBox放入到QHBoxLayout,如果期望垂直布局,将QGroupBox放入到QVBoxLayout
    """
    heightChanged = pyqtSignal(int)

    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)

        self._item_list = []

    def __del__(self):
        while self.count():
            self.takeAt(0)

    def addItem(self, item):  # pylint: disable=invalid-name
        self._item_list.append(item)

    def addSpacing(self, size):  # pylint: disable=invalid-name
        self.addItem(QSpacerItem(size, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))

    def count(self):
        return len(self._item_list)

    def itemAt(self, index):  # pylint: disable=invalid-name
        if 0 <= index < len(self._item_list):
            return self._item_list[index]
        return None

    def takeAt(self, index):  # pylint: disable=invalid-name
        if 0 <= index < len(self._item_list):
            return self._item_list.pop(index)
        return None

    def expandingDirections(self):  # pylint: disable=invalid-name,no-self-use
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):  # pylint: disable=invalid-name,no-self-use
        return True

    def heightForWidth(self, width):  # pylint: disable=invalid-name
        height = self._do_layout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):  # pylint: disable=invalid-name
        super().setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):  # pylint: disable=invalid-name
        return self.minimumSize()

    def minimumSize(self):  # pylint: disable=invalid-name
        size = QSize()

        for item in self._item_list:
            minsize = item.minimumSize()
            extent = item.geometry().bottomRight()
            size = size.expandedTo(QSize(minsize.width(), extent.y()))

        margin = self.contentsMargins().left()
        size += QSize(2 * margin, 2 * margin)
        return size

    def _do_layout(self, rect, test_only=False):
        m = self.contentsMargins()
        effective_rect = rect.adjusted(+m.left(), +m.top(), -m.right(), -m.bottom())
        x = effective_rect.x()
        y = effective_rect.y()
        line_height = 0

        for item in self._item_list:
            wid = item.widget()

            space_x = self.spacing()
            space_y = self.spacing()
            if wid is not None:
                space_x += wid.style().layoutSpacing(
                    QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
                space_y += wid.style().layoutSpacing(
                    QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)

            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > effective_rect.right() and line_height > 0:
                x = effective_rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        new_height = y + line_height - rect.y()
        self.heightChanged.emit(new_height)
        return new_height


def list_to_csv(csv_path, save_list):
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows([i] for i in save_list)


class App(QWidget):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        # 获取显示器分辨率
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.screenheight = self.screenRect.height()
        self.screenwidth = self.screenRect.width()

        # 读取csv
        words = []
        with open("./1_words.csv", encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                words.append(row[0])
        print(words)

        self.words_checked = []
        with open("./2_words.csv", encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                self.words_checked.append(row[0])
        print(self.words_checked)

        self.setWindowTitle('count:' + str(len(words)))
        list_widget = QtWidgets.QListWidget()
        container_layout = QtWidgets.QVBoxLayout()
        group_box = QtWidgets.QGroupBox("")
        flow_layout = FlowLayout()
        group_box.setLayout(flow_layout)
        for word in words:
            btn = QPushButton(word)
            btn.setFixedHeight(60)
            btn.setFixedWidth(150)
            btn.setCheckable(True)
            if word in self.words_checked:
                btn.setChecked(True)
                btn.setStyleSheet("QPushButton{background:#10DCE8;}")
            else:
                btn.setStyleSheet("QPushButton{background:#FFA687;}")
            btn.clicked[bool].connect(self.handle_click)
            flow_layout.addWidget(btn)

        container_layout.addWidget(group_box)
        container_layout.addStretch()
        list_widget.setLayout(container_layout)

        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setGeometry(QRect(0, 0, self.screenwidth, self.screenheight - 180))
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(list_widget)

    def handle_click(self, pressed):
        source = self.sender()
        if pressed:
            source.setStyleSheet("QPushButton{background:#10DCE8;}")
            self.words_checked.append(source.text())
        else:
            source.setStyleSheet("QPushButton{background:#FFA687;}")
            self.words_checked.remove(source.text())
        list_to_csv('./2_words.csv', self.words_checked)
        print(pressed, source.text())


def main():
    app = QApplication(sys.argv)
    window = App()
    window.move(0, 0)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
