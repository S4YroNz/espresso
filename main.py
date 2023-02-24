import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QLabel, \
    QMessageBox
import sqlite3 as sql


class Example(QWidget):
    def __init__(self):
        self.right_status = True
        super().__init__()
        self.initUI()

    def initUI(self):
        sc_width = 750
        sc_height = 300
        self.setGeometry(500, 300, sc_width, sc_height)
        self.setWindowTitle('Эспрессо')
        self.con = sql.connect("coffee.sqlite")

        self.table = QTableWidget(self)

        self.table.resize(sc_width - 20, sc_height - 110)
        self.table.move(10, 10)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки'])
        self.load_by_id()

    def load_by_id(self):
        cur = self.con.cursor()
        res = cur.execute(f"""SELECT * FROM coffee""").fetchall()
        self.table.setRowCount(len(res))
        for i in range(len(res)):
            for j in range(7):
                self.table.setItem(i, j, QTableWidgetItem(str(res[i][j])))

    def change(self):
        if QMessageBox.question(self, 'python', f'Изменить данные с id = {self.get_id()}?',
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
            return

        cur = self.con.cursor()

        res = cur.execute(f"""SELECT * FROM films
                    WHERE id = ?""", (self.get_id(),)).fetchall()[0]

        cur.execute("""DELETE  FROM films
        WHERE id = ?""", (self.get_id(),))

        cur.execute("""INSERT INTO films VALUES(?,?,?,?,?)""",
                    (res[0], res[1][::-1], res[2] + 1000, res[3], res[4] * 2))
        self.con.commit()
        self.load_by_id()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
