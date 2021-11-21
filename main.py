import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QTableWidget


class AddNew(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.btn_save.clicked.connect(self.save)

    def save(self):
        query = """INSERT INTO coffee(`Название сорта`, `Степень обжарки`, `Молотый/в зернах`, 
        `Описание вкуса`, `Цена`, `Объем упаковки`) VALUES(?, ?, ?, ?, ?, ?)"""
        a = self.le_sort.text()
        b = self.le_degree.text()
        c = self.le_ground.text()
        d = self.le_taste.text()
        e = self.le_cost.text()
        f = self.le_volume.text()
        cur = self.connection.cursor()
        cur.execute(query, (a, b, c, d, e, f))
        self.connection.commit()
        self.close()

    def closeEvent(self, event):
        self.connection.close()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.btn_create_new.clicked.connect(self.create_new)
        self.select_data()

    def create_new(self):
        self.new = AddNew()
        self.new.show()

    def item_changed(self, item):
        cur = self.connection.cursor()
        self.titles = ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах',
                       'Описание вкуса', 'Цена', 'Объем упаковки']
        que = "UPDATE coffee SET\n"
        que += f"`{self.titles[item.column()]}`='{item.text()}'"
        que += "WHERE id = ?"
        cur.execute(que, (self.tableWidget.item(item.row(), 0).text(),))
        self.connection.commit()

    def select_data(self):
        query = """SELECT * FROM coffee"""
        res = self.connection.cursor().execute(query).fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def closeEvent(self, event):
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())