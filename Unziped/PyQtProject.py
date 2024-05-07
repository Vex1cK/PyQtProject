# -*- coding: utf-8 -*-
"""Кодировка файла, и импортирование нужных модулей:"""
import sys
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from PyQt5.QtCore import Qt, QVariant, QTimer
from PyQt5 import QtCore, QtWidgets, QtGui

"""Ниже записаны 6 констант, первые 4 из них это
названия столбцов в таблицах которые присутствуют на графическом интерфейсе,
также они используются программмой для поиска, редактирования и удаления элементов
из таблиц, т.к. в базе данных названия столбцов идентичны.

Следующие 2 константы используются программой в процессе добавления 
элементов в таблицы."""
COLUMN_LABLES1 = ['itemId', 'shopId', 'shopName', 'goodId', 'titleGood', 'price']
COLUMN_LABLES2 = ['idGood', 'typeIdGood', 'typeName', 'titleGood']
COLUMN_LABLES3 = ['idShop', 'shopName', 'shopLink']
COLUMN_LABLES4 = ['idType', 'typeName']
COLUMN_LABLES_ONLY_CHOICE = ['typeName', 'shopName', 'titleGood']
ADD_WINDOW_WIDGETS_COORDS = [(40, 70), (170, 200), (300, 330), (430, 460)]
'2 класса ошибок:'


class Upd(ValueError):
    pass

class Error(ValueError):
    pass

class Ui_Dialog(object):
    """ui форма для диалогового окна которое появляется
    в процессе добавления элементов в таблицу
    (ui форма это шаблон граф. интерфейса т.е. все кнопки
    таблицы и т.д. которые не имеют никакого функционала.)"""

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(527, 664)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(140, 610, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

class Ui_MainWindow(object):
    """Также ui форма для основного граф. интерфейса."""

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(928, 804)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 921, 771))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.LineEdit1 = QtWidgets.QLineEdit(self.tab)
        self.LineEdit1.setGeometry(QtCore.QRect(410, 20, 471, 31))
        self.LineEdit1.setObjectName("LineEdit1")
        self.TableWidget1 = QtWidgets.QTableWidget(self.tab)
        self.TableWidget1.setGeometry(QtCore.QRect(10, 170, 871, 571))
        self.TableWidget1.setObjectName("TableWidget1")
        self.TableWidget1.setColumnCount(0)
        self.TableWidget1.setRowCount(0)
        self.Lable1 = QtWidgets.QLabel(self.tab)
        self.Lable1.setGeometry(QtCore.QRect(10, 20, 111, 31))
        self.Lable1.setObjectName("Lable1")
        self.BtnChangeItem1 = QtWidgets.QPushButton(self.tab)
        self.BtnChangeItem1.setGeometry(QtCore.QRect(540, 120, 211, 41))
        self.BtnChangeItem1.setObjectName("BtnChangeItem1")
        self.BtnDeleteStr1 = QtWidgets.QPushButton(self.tab)
        self.BtnDeleteStr1.setGeometry(QtCore.QRect(60, 120, 181, 41))
        self.BtnDeleteStr1.setObjectName("BtnDeleteStr1")
        self.ComboBox1 = QtWidgets.QComboBox(self.tab)
        self.ComboBox1.setGeometry(QtCore.QRect(120, 20, 281, 31))
        self.ComboBox1.setObjectName("ComboBox1")
        self.LabelNoSearch1 = QtWidgets.QLabel(self.tab)
        self.LabelNoSearch1.setGeometry(QtCore.QRect(410, 0, 471, 16))
        self.LabelNoSearch1.setText("")
        self.LabelNoSearch1.setObjectName("LabelNoSearch1")
        self.btnUpdate1 = QtWidgets.QPushButton(self.tab)
        self.btnUpdate1.setGeometry(QtCore.QRect(830, 70, 71, 91))
        self.btnUpdate1.setObjectName("btnUpdate1")
        self.BtnSave1 = QtWidgets.QPushButton(self.tab)
        self.BtnSave1.setGeometry(QtCore.QRect(330, 70, 121, 41))
        self.BtnSave1.setObjectName("BtnSave1")
        self.BtnAdd1 = QtWidgets.QPushButton(self.tab)
        self.BtnAdd1.setGeometry(QtCore.QRect(330, 120, 121, 41))
        self.BtnAdd1.setObjectName("BtnAdd1")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.TableWidget2 = QtWidgets.QTableWidget(self.tab_2)
        self.TableWidget2.setGeometry(QtCore.QRect(10, 170, 871, 571))
        self.TableWidget2.setObjectName("TableWidget2")
        self.TableWidget2.setColumnCount(0)
        self.TableWidget2.setRowCount(0)
        self.Lable2 = QtWidgets.QLabel(self.tab_2)
        self.Lable2.setGeometry(QtCore.QRect(10, 20, 111, 31))
        self.Lable2.setObjectName("Lable2")
        self.BtnChangeItem2 = QtWidgets.QPushButton(self.tab_2)
        self.BtnChangeItem2.setGeometry(QtCore.QRect(540, 120, 211, 41))
        self.BtnChangeItem2.setObjectName("BtnChangeItem2")
        self.BtnDeleteStr2 = QtWidgets.QPushButton(self.tab_2)
        self.BtnDeleteStr2.setGeometry(QtCore.QRect(60, 120, 181, 41))
        self.BtnDeleteStr2.setObjectName("BtnDeleteStr2")
        self.LineEdit2 = QtWidgets.QLineEdit(self.tab_2)
        self.LineEdit2.setGeometry(QtCore.QRect(410, 20, 471, 31))
        self.LineEdit2.setObjectName("LineEdit2")
        self.ComboBox2 = QtWidgets.QComboBox(self.tab_2)
        self.ComboBox2.setGeometry(QtCore.QRect(120, 20, 281, 31))
        self.ComboBox2.setObjectName("ComboBox2")
        self.LabelNoSearch2 = QtWidgets.QLabel(self.tab_2)
        self.LabelNoSearch2.setGeometry(QtCore.QRect(410, 0, 471, 16))
        self.LabelNoSearch2.setText("")
        self.LabelNoSearch2.setObjectName("LabelNoSearch2")
        self.btnUpdate2 = QtWidgets.QPushButton(self.tab_2)
        self.btnUpdate2.setGeometry(QtCore.QRect(830, 70, 71, 91))
        self.btnUpdate2.setObjectName("btnUpdate2")
        self.BtnSave2 = QtWidgets.QPushButton(self.tab_2)
        self.BtnSave2.setGeometry(QtCore.QRect(330, 70, 121, 41))
        self.BtnSave2.setObjectName("BtnSave2")
        self.BtnAdd2 = QtWidgets.QPushButton(self.tab_2)
        self.BtnAdd2.setGeometry(QtCore.QRect(330, 120, 121, 41))
        self.BtnAdd2.setObjectName("BtnAdd2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.TableWidget3 = QtWidgets.QTableWidget(self.tab_3)
        self.TableWidget3.setGeometry(QtCore.QRect(10, 170, 871, 571))
        self.TableWidget3.setObjectName("TableWidget3")
        self.TableWidget3.setColumnCount(0)
        self.TableWidget3.setRowCount(0)
        self.BtnChangeItem3 = QtWidgets.QPushButton(self.tab_3)
        self.BtnChangeItem3.setGeometry(QtCore.QRect(540, 120, 211, 41))
        self.BtnChangeItem3.setObjectName("BtnChangeItem3")
        self.BtnDeleteStr3 = QtWidgets.QPushButton(self.tab_3)
        self.BtnDeleteStr3.setGeometry(QtCore.QRect(60, 120, 181, 41))
        self.BtnDeleteStr3.setObjectName("BtnDeleteStr3")
        self.LineEdit3 = QtWidgets.QLineEdit(self.tab_3)
        self.LineEdit3.setGeometry(QtCore.QRect(410, 20, 471, 31))
        self.LineEdit3.setObjectName("LineEdit3")
        self.btnUpdate3 = QtWidgets.QPushButton(self.tab_3)
        self.btnUpdate3.setGeometry(QtCore.QRect(830, 70, 71, 91))
        self.btnUpdate3.setObjectName("btnUpdate3")
        self.Lable3 = QtWidgets.QLabel(self.tab_3)
        self.Lable3.setGeometry(QtCore.QRect(10, 20, 111, 31))
        self.Lable3.setObjectName("Lable3")
        self.ComboBox3 = QtWidgets.QComboBox(self.tab_3)
        self.ComboBox3.setGeometry(QtCore.QRect(120, 20, 281, 31))
        self.ComboBox3.setObjectName("ComboBox3")
        self.LabelNoSearch3 = QtWidgets.QLabel(self.tab_3)
        self.LabelNoSearch3.setGeometry(QtCore.QRect(410, 0, 471, 16))
        self.LabelNoSearch3.setText("")
        self.LabelNoSearch3.setObjectName("LabelNoSearch3")
        self.BtnSave3 = QtWidgets.QPushButton(self.tab_3)
        self.BtnSave3.setGeometry(QtCore.QRect(330, 70, 121, 41))
        self.BtnSave3.setObjectName("BtnSave3")
        self.BtnAdd3 = QtWidgets.QPushButton(self.tab_3)
        self.BtnAdd3.setGeometry(QtCore.QRect(330, 120, 121, 41))
        self.BtnAdd3.setObjectName("BtnAdd3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.TableWidget4 = QtWidgets.QTableWidget(self.tab_4)
        self.TableWidget4.setGeometry(QtCore.QRect(10, 170, 871, 571))
        self.TableWidget4.setObjectName("TableWidget4")
        self.TableWidget4.setColumnCount(0)
        self.TableWidget4.setRowCount(0)
        self.BtnChangeItem4 = QtWidgets.QPushButton(self.tab_4)
        self.BtnChangeItem4.setGeometry(QtCore.QRect(540, 120, 211, 41))
        self.BtnChangeItem4.setObjectName("BtnChangeItem4")
        self.BtnDeleteStr4 = QtWidgets.QPushButton(self.tab_4)
        self.BtnDeleteStr4.setGeometry(QtCore.QRect(60, 120, 181, 41))
        self.BtnDeleteStr4.setObjectName("BtnDeleteStr4")
        self.LineEdit4 = QtWidgets.QLineEdit(self.tab_4)
        self.LineEdit4.setGeometry(QtCore.QRect(410, 20, 471, 31))
        self.LineEdit4.setObjectName("LineEdit4")
        self.btnUpdate4 = QtWidgets.QPushButton(self.tab_4)
        self.btnUpdate4.setGeometry(QtCore.QRect(830, 70, 71, 91))
        self.btnUpdate4.setObjectName("btnUpdate4")
        self.Lable4 = QtWidgets.QLabel(self.tab_4)
        self.Lable4.setGeometry(QtCore.QRect(10, 20, 111, 31))
        self.Lable4.setObjectName("Lable4")
        self.ComboBox4 = QtWidgets.QComboBox(self.tab_4)
        self.ComboBox4.setGeometry(QtCore.QRect(120, 20, 281, 31))
        self.ComboBox4.setObjectName("ComboBox4")
        self.LabelNoSearch4 = QtWidgets.QLabel(self.tab_4)
        self.LabelNoSearch4.setGeometry(QtCore.QRect(410, 0, 471, 16))
        self.LabelNoSearch4.setText("")
        self.LabelNoSearch4.setObjectName("LabelNoSearch4")
        self.BtnSave4 = QtWidgets.QPushButton(self.tab_4)
        self.BtnSave4.setGeometry(QtCore.QRect(330, 70, 121, 41))
        self.BtnSave4.setObjectName("BtnSave4")
        self.BtnAdd4 = QtWidgets.QPushButton(self.tab_4)
        self.BtnAdd4.setGeometry(QtCore.QRect(330, 120, 121, 41))
        self.BtnAdd4.setObjectName("BtnAdd4")
        self.tabWidget.addTab(self.tab_4, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 928, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Lable1.setText(_translate("MainWindow",
                                       "<html><head/><body><p><span style=\" font-size:16pt;\">Поиск по:</span></p></body></html>"))
        self.BtnChangeItem1.setText(_translate("MainWindow", "Редактировать выбранный элемент"))
        self.BtnDeleteStr1.setText(_translate("MainWindow", "Удалить выбранную строку"))
        self.btnUpdate1.setText(_translate("MainWindow", "Обновить"))
        self.BtnSave1.setText(_translate("MainWindow", "Сохранить"))
        self.BtnAdd1.setText(_translate("MainWindow", "Добавить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Price list"))
        self.Lable2.setText(_translate("MainWindow",
                                       "<html><head/><body><p><span style=\" font-size:16pt;\">Поиск по:</span></p></body></html>"))
        self.BtnChangeItem2.setText(_translate("MainWindow", "Редактировать выбранный элемент"))
        self.BtnDeleteStr2.setText(_translate("MainWindow", "Удалить выбранную строку"))
        self.btnUpdate2.setText(_translate("MainWindow", "Обновить"))
        self.BtnSave2.setText(_translate("MainWindow", "Сохранить"))
        self.BtnAdd2.setText(_translate("MainWindow", "Добавить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Goods"))
        self.BtnChangeItem3.setText(_translate("MainWindow", "Редактировать выбранный элемент"))
        self.BtnDeleteStr3.setText(_translate("MainWindow", "Удалить выбранную строку"))
        self.btnUpdate3.setText(_translate("MainWindow", "Обновить"))
        self.Lable3.setText(_translate("MainWindow",
                                       "<html><head/><body><p><span style=\" font-size:16pt;\">Поиск по:</span></p></body></html>"))
        self.BtnSave3.setText(_translate("MainWindow", "Сохранить"))
        self.BtnAdd3.setText(_translate("MainWindow", "Добавить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Shops"))
        self.BtnChangeItem4.setText(_translate("MainWindow", "Редактировать выбранный элемент"))
        self.BtnDeleteStr4.setText(_translate("MainWindow", "Удалить выбранную строку"))
        self.btnUpdate4.setText(_translate("MainWindow", "Обновить"))
        self.Lable4.setText(_translate("MainWindow",
                                       "<html><head/><body><p><span style=\" font-size:16pt;\">Поиск по:</span></p></body></html>"))
        self.BtnSave4.setText(_translate("MainWindow", "Сохранить"))
        self.BtnAdd4.setText(_translate("MainWindow", "Добавить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Types of goods"))

class MainWindow(QMainWindow, Ui_MainWindow):
    """Класс в котором реализован весь функционал за исключением еще
    одного класса описывающим диалоговое окно"""

    def __init__(self):
        """Создание объекта"""
        super().__init__()  # __init__ из класса QMainWindow
        self.setupUi(self)  # setupUi из класса Ui_MainWindow
        self.setWindows()

    def setWindows(self):
        # Поключение к базе данных и создание "курсора"
        self.db = sqlite3.connect('DataBase.sqlite')
        self.cur = self.db.cursor()

        """ "Установка" всех окон по-очереди, в данных методах
        проиходит коннект кнопок к их функциям, первичное заполнение таблицы
        и т.д."""

        # Комментарии присутствуют только в методе window1, т.к. в остальных методах всё идентично
        self.window1()
        self.window2()
        self.window3()
        self.window4()
        self.finalSet()

        self.isSave = True
        # Данная переменная хранит информацию о сохранённости всех данных в базе данных
        # Изначально всё уже сохранено, т.к. ничего не изменяется

    def window1(self):
        self.searchStr1 = """SELECT itemId, shopId, shopName, goodId, titleGood, price
FROM PriceList
INNER JOIN goods ON idGood = goodId
INNER JOIN shops ON idShop = shopId"""
        # Это поиск по базе данных без доп. условий, он всегда одинаковый

        result1 = self.cur.execute(self.searchStr1).fetchall()  # Запрос к базе
        quantColumns = len(result1[0])  # кол-во столбцов
        quantRows = len(result1)  # кол-во строк

        self.TableWidget1.setColumnCount(quantColumns)
        self.TableWidget1.setRowCount(quantRows)
        # Установка кол-ва сток и столбцов

        self.TableWidget1.setHorizontalHeaderLabels(COLUMN_LABLES1)
        self.TableWidget1.setVerticalHeaderLabels(['' for _ in range(1, len(result1) + 1)])
        # Установка названий столбцов и строк

        for cLable1 in COLUMN_LABLES1:
            self.ComboBox1.addItem(cLable1)

        # Заполнение таблицы:
        for i in range(quantRows):
            for j in range(quantColumns):
                item = QTableWidgetItem()
                item.setData(Qt.EditRole, QVariant(result1[i][j]))
                item.setFlags(QtCore.Qt.ItemIsEnabled)

                self.TableWidget1.setItem(i, j, item)

        self.TableWidget1.resizeRowsToContents()
        self.TableWidget1.resizeColumnsToContents()
        # Установка ширины и высоты ячеек, строк и столбцов по размеру содержанию

        self.TableWidget1.cellClicked.connect(self.table1Click)  # Клик по ячейке, коннект к методу

        self.btnUpdate1.clicked.connect(self.fastUpd1)  # Кнопка "Обновить"
        self.BtnDeleteStr1.clicked.connect(self.deleteStr1)  # кнопка "Удалить"
        self.BtnChangeItem1.clicked.connect(self.itemUpdate1)  # кнопка "Редактировать"
        self.BtnSave1.clicked.connect(self.save)  # кнопка "сохранить"
        self.BtnAdd1.clicked.connect(self.add1)  # кнопка "добавить"

    def window2(self):
        self.searchStr2 = """SELECT idGood, typeIdGood, typeName, titleGood
FROM goods
INNER JOIN typesOfGoods ON idType = typeIdGood"""
        result2 = self.cur.execute(self.searchStr2).fetchall()
        quantColumns = len(result2[0])
        quantRows = len(result2)

        self.TableWidget2.setColumnCount(quantColumns)
        self.TableWidget2.setRowCount(quantRows)

        self.TableWidget2.setHorizontalHeaderLabels(COLUMN_LABLES2)
        self.TableWidget2.setVerticalHeaderLabels(map(lambda x: str(x), range(1, len(result2) + 1)))

        for cLable2 in COLUMN_LABLES2:
            self.ComboBox2.addItem(cLable2)

        for i in range(quantRows):
            for j in range(quantColumns):
                item = QTableWidgetItem()
                item.setData(Qt.EditRole, QVariant(result2[i][j]))
                item.setFlags(QtCore.Qt.ItemIsEnabled)

                self.TableWidget2.setItem(i, j, item)

        self.TableWidget2.resizeRowsToContents()
        self.TableWidget2.resizeColumnsToContents()

        self.TableWidget2.cellClicked.connect(self.table2Click)

        self.btnUpdate2.clicked.connect(self.fastUpd2)
        self.BtnDeleteStr2.clicked.connect(self.deleteStr2)
        self.BtnChangeItem2.clicked.connect(self.itemUpdate2)
        self.BtnSave2.clicked.connect(self.save)
        self.BtnAdd2.clicked.connect(self.add2)

    def window3(self):
        result3 = self.cur.execute("SELECT * FROM shops").fetchall()
        quantColumns = len(result3[0])
        quantRows = len(result3)

        self.TableWidget3.setColumnCount(quantColumns)
        self.TableWidget3.setRowCount(quantRows)

        self.TableWidget3.setHorizontalHeaderLabels(COLUMN_LABLES3)
        self.TableWidget3.setVerticalHeaderLabels(map(lambda x: str(x), range(1, len(result3) + 1)))

        for cLable3 in COLUMN_LABLES3:
            self.ComboBox3.addItem(cLable3)

        for i in range(quantRows):
            for j in range(quantColumns):
                item = QTableWidgetItem()
                item.setData(Qt.EditRole, QVariant(result3[i][j]))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                """Такое создание item позволяет сортировке
                сортировать числа как числа, а не как строки."""

                self.TableWidget3.setItem(i, j, item)

        self.TableWidget3.resizeRowsToContents()
        self.TableWidget3.resizeColumnsToContents()

        self.TableWidget3.cellClicked.connect(self.table3Click)

        self.btnUpdate3.clicked.connect(self.fastUpd3)
        self.BtnDeleteStr3.clicked.connect(self.deleteStr3)
        self.BtnChangeItem3.clicked.connect(self.itemUpdate3)
        self.BtnSave3.clicked.connect(self.save)
        self.BtnAdd3.clicked.connect(self.add3)

    def window4(self):
        result4 = self.cur.execute("SELECT * FROM typesOfGoods").fetchall()
        quantColumns = len(result4[0])
        quantRows = len(result4)

        self.TableWidget4.setColumnCount(quantColumns)
        self.TableWidget4.setRowCount(quantRows)

        self.TableWidget4.setHorizontalHeaderLabels(COLUMN_LABLES4)
        self.TableWidget4.setVerticalHeaderLabels(map(lambda x: str(x), range(1, len(result4) + 1)))

        for cLable4 in COLUMN_LABLES4:
            self.ComboBox4.addItem(cLable4)

        for i in range(quantRows):
            for j in range(quantColumns):
                item = QTableWidgetItem()
                item.setData(Qt.EditRole, QVariant(result4[i][j]))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                """Такое создание item позволяет сортировке
                сортировать числа как числа, а не как строки."""

                self.TableWidget4.setItem(i, j, item)

        self.TableWidget4.resizeRowsToContents()
        self.TableWidget4.resizeColumnsToContents()

        self.TableWidget4.cellClicked.connect(self.table4Click)

        self.btnUpdate4.clicked.connect(self.fastUpd4)
        self.BtnDeleteStr4.clicked.connect(self.deleteStr4)
        self.BtnChangeItem4.clicked.connect(self.itemUpdate4)
        self.BtnSave4.clicked.connect(self.save)
        self.BtnAdd4.clicked.connect(self.add4)

    def finalSet(self):
        # Создание и запуск таймера
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.search)
        self.timer1.start(100)  # Обновление раз в 0.1 секунду

        self.last1 = ('itemId', '')
        self.last2 = ('idGood', '')
        self.last3 = ('idShop', '')
        self.last4 = ('idType', '')
        """Эти четыре переменные хранят информацию об последнем поиске
        это нужно потому что таймер делает авто-обновление таблицы в соответствии
        с новым запросом, а если он не изменился, то не тратить время зря и не
        обновлять таблицы попусту. Чтобы это отслеживать и нужны эти четыре переменные.
        (каждой таблице своя переменная)"""

        self.item1 = False
        self.item2 = False
        self.item3 = False
        self.item4 = False
        """В этих переменных хранится информация о последней нажатой ячейке
        (каждой таблице своя переменная)"""

    def search(self):
        # По-порядку обновление (поиск) по каждой из 4х таблиц
        # Я также оставил комментарии только в методе search1 т.к. они идентичны
        self.search1()
        self.search2()
        self.search3()
        self.search4()

    def search1(self, fast=None):
        conditionColumn = self.ComboBox1.currentText()  # Выбраных столбец, по которому происходит поиск
        conditionText = self.LineEdit1.text().lower()  # Подстрока, или стока по которой происходит поиск
        conditionText = conditionText.replace('\\', '\\\\').replace(
            '%', '\%'
        ).replace(
            '_', '\_'
        ).replace(
            '[', '\['
        )  # Такое преобразование нужно чтобы была возможность в подстроку указывать спец. символы
        if self.last1 != (conditionColumn, conditionText) or fast == 'fast':
            # Если условия поиска изменились, или была нажата кнопка "Обновить"

            if conditionColumn in ('shopName', 'titleGood'):
                # Если поиск происходит по столбцам с текстовым форматом. (не int)
                result = self.cur.execute(self.searchStr1 +  # Поиск
                                          f'\nWHERE {conditionColumn} LIKE' +
                                          f' "%{conditionText}%" ESCAPE "\\"').fetchall()
            else:  # Поиск по столбцам формат которых только числа (int)
                if conditionText:
                    # Если поле для подстроки НЕ пустое, то ищем с условием
                    result = self.cur.execute(self.searchStr1 +
                                              f'\nWHERE {conditionColumn} LIKE' +
                                              f' "{conditionText}" ESCAPE "\\"').fetchall()
                else:
                    # Иначе - ищем без условия:
                    result = self.cur.execute(self.searchStr1).fetchall()

            quantRows = len(result)  # кол-во найденых строк
            self.TableWidget1.setRowCount(quantRows)  # Установка кол-ва строк
            self.TableWidget1.setVerticalHeaderLabels(['' for _ in range(1, len(result) + 1)])
            # Установка имён для этих строк

            self.itemsToNull(1)  # обнуление последней нажатой ячейки.

            if result:  # Если что-либо найдено, обновляем таблицу:
                for i in range(quantRows):
                    for j in range(len(result[0])):
                        item = QTableWidgetItem()
                        item.setData(Qt.EditRole, QVariant(result[i][j]))
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.TableWidget1.setItem(i, j, item)

                self.LabelNoSearch1.setText('')

            else:
                # Иначе - пишем что ничего не найдено:
                self.LabelNoSearch1.setText('Ничего не найдено!')

            self.last1 = (conditionColumn, conditionText)  # обновление переменной о последнем поиске

    def search2(self, fast=None):
        conditionColumn = self.ComboBox2.currentText()
        conditionText = self.LineEdit2.text().lower()
        conditionText = conditionText.replace('\\', '\\\\').replace(
            '%', '\%'
        ).replace(
            '_', '\_'
        ).replace(
            '[', '\['
        )
        if self.last2 != (conditionColumn, conditionText) or fast == 'fast':
            if conditionColumn in ('titleGood', 'typeName'):
                result = self.cur.execute(self.searchStr2 +
                                          f'\nWHERE {conditionColumn} LIKE "%{conditionText}%" ESCAPE "\\"').fetchall()
            else:
                if conditionText:
                    result = self.cur.execute(self.searchStr2 +
                                              f'\nWHERE {conditionColumn} LIKE "{conditionText}" ESCAPE "\\"').fetchall()
                else:
                    result = self.cur.execute(self.searchStr2).fetchall()

            quantRows = len(result)
            self.TableWidget2.setRowCount(quantRows)
            self.TableWidget2.setVerticalHeaderLabels(['' for _ in range(1, len(result) + 1)])

            self.itemsToNull(2)

            if result:
                for i in range(quantRows):
                    for j in range(len(result[0])):
                        item = QTableWidgetItem()
                        item.setData(Qt.EditRole, QVariant(result[i][j]))
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.TableWidget2.setItem(i, j, item)

                self.LabelNoSearch2.setText('')

            else:
                self.LabelNoSearch2.setText('Ничего не найдено!')

            self.last2 = (conditionColumn, conditionText)

    def search3(self, fast=None):
        conditionColumn = self.ComboBox3.currentText()
        conditionText = self.LineEdit3.text().lower()
        conditionText = conditionText.replace('\\', '\\\\').replace(
            '%', '\%'
        ).replace(
            '_', '\_'
        ).replace(
            '[', '\['
        )
        if self.last3 != (conditionColumn, conditionText) or fast == 'fast':
            if conditionColumn == 'shopName' or 'shopLink':
                result = self.cur.execute("SELECT * FROM shops\n\t\t" +
                                          f'WHERE {conditionColumn} LIKE "%{conditionText}%" ESCAPE "\\"').fetchall()
            else:
                if conditionText:
                    result = self.cur.execute(f"SELECT * FROM shops\n\t\t" +
                                              f'WHERE {conditionColumn} LIKE "{conditionText}" ESCAPE "\\"').fetchall()
                else:
                    result = self.cur.execute(f"SELECT * FROM shops").fetchall()

            quantRows = len(result)
            self.TableWidget3.setRowCount(quantRows)
            self.TableWidget3.setVerticalHeaderLabels(['' for _ in range(1, len(result) + 1)])

            self.itemsToNull(3)

            if result:
                for i in range(quantRows):
                    for j in range(3):
                        item = QTableWidgetItem()
                        item.setData(Qt.EditRole, QVariant(result[i][j]))
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.TableWidget3.setItem(i, j, item)

                self.LabelNoSearch3.setText('')

            else:
                self.LabelNoSearch3.setText('Ничего не найдено!')

            self.last3 = (conditionColumn, conditionText)

    def search4(self, fast=None):
        conditionColumn = self.ComboBox4.currentText()
        conditionText = self.LineEdit4.text().lower()
        conditionText = conditionText.replace('\\', '\\\\').replace(
            '%', '\%'
        ).replace(
            '_', '\_'
        ).replace(
            '[', '\['
        )
        if self.last4 != (conditionColumn, conditionText) or fast == 'fast':
            if conditionColumn == 'typeName':
                result = self.cur.execute("SELECT * FROM typesOfGoods\n\t\t" +
                                          f'WHERE {conditionColumn} LIKE "%{conditionText}%" ESCAPE "\\"').fetchall()
            else:
                if conditionText:
                    result = self.cur.execute(f"SELECT * FROM typesOfGoods\n\t\t" +
                                              f'WHERE {conditionColumn} LIKE "{conditionText}" ESCAPE "\\"').fetchall()
                else:
                    result = self.cur.execute(f"SELECT * FROM typesOfGoods").fetchall()

            quantRows = len(result)
            self.TableWidget4.setRowCount(quantRows)
            self.TableWidget4.setVerticalHeaderLabels(['' for _ in range(1, len(result) + 1)])

            self.itemsToNull(4)

            if result:
                for i in range(quantRows):
                    for j in range(2):
                        item = QTableWidgetItem()
                        item.setData(Qt.EditRole, QVariant(result[i][j]))
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.TableWidget4.setItem(i, j, item)

                self.LabelNoSearch4.setText('')

            else:
                self.LabelNoSearch4.setText('Ничего не найдено!')

            self.last4 = (conditionColumn, conditionText)

    def fastUpd1(self):
        # Этот и следующие 3 метода - функция кнопки "обновить"
        # Они запускаю цикл обновления содержания таблицы в независимости от того,
        # был ли произведён поиск отличный от последнего
        self.search1(fast='fast')

    def fastUpd2(self):
        self.search2(fast='fast')

    def fastUpd3(self):
        self.search3(fast='fast')

    def fastUpd4(self):
        self.search4(fast='fast')

    def itemsToNull(self, id):
        # Обнуление последней нажатой ячейки.
        if id == 1:
            if self.item1:
                try:
                    self.item1.setBackground(QtGui.QBrush(QtGui.QColor('white')))
                except RuntimeError:
                    pass
            self.item1 = None
        elif id == 2:
            if self.item2:
                try:
                    self.item2.setBackground(QtGui.QBrush(QtGui.QColor('white')))
                except RuntimeError:
                    pass
            self.item2 = None
        elif id == 3:
            if self.item3:
                try:
                    self.item3.setBackground(QtGui.QBrush(QtGui.QColor('white')))
                except RuntimeError:
                    pass
            self.item3 = None
        elif id == 4:
            if self.item4:
                try:
                    self.item4.setBackground(QtGui.QBrush(QtGui.QColor('white')))
                except RuntimeError:
                    pass
            self.item4 = None

    def table1Click(self):
        # Клик по табличке, выделение нажатой ячейки и запись её в переменную
        self.x1 = self.TableWidget1.currentRow()
        self.y1 = self.TableWidget1.currentColumn()
        if self.item1:
            self.item1.setBackground(QtGui.QBrush(QtGui.QColor('white')))
        self.item1 = self.TableWidget1.item(self.x1, self.y1)
        self.item1.setBackground(QtGui.QBrush(QtGui.QColor('lightGreen')))

    def table2Click(self):
        self.x2 = self.TableWidget2.currentRow()
        self.y2 = self.TableWidget2.currentColumn()
        if self.item2:
            self.item2.setBackground(QtGui.QBrush(QtGui.QColor('white')))
        self.item2 = self.TableWidget2.item(self.x2, self.y2)
        self.item2.setBackground(QtGui.QBrush(QtGui.QColor('lightGreen')))

    def table3Click(self):
        self.x3 = self.TableWidget3.currentRow()
        self.y3 = self.TableWidget3.currentColumn()
        if self.item3:
            self.item3.setBackground(QtGui.QBrush(QtGui.QColor('white')))
        self.item3 = self.TableWidget3.item(self.x3, self.y3)
        self.item3.setBackground(QtGui.QBrush(QtGui.QColor('lightGreen')))

    def table4Click(self):
        self.x4 = self.TableWidget4.currentRow()
        self.y4 = self.TableWidget4.currentColumn()
        if self.item4:
            self.item4.setBackground(QtGui.QBrush(QtGui.QColor('white')))
        self.item4 = self.TableWidget4.item(self.x4, self.y4)
        self.item4.setBackground(QtGui.QBrush(QtGui.QColor('lightGreen')))

    def errorMessage(self, title):
        # Вызов окна с оповещением об какой-либо ошибке
        QMessageBox.critical(self, 'Error', title, QMessageBox.Ok)

    def deleteStr1(self):
        # Также, комментарии пишу только сюда, следующие 3 метода идентичны.
        if self.item1:  # Если есть хоть 1 нажатый элемент
            itemId = self.TableWidget1.item(self.x1, 0).text()
            # Значение первого столба элемента в той же строке что и последний нажатый

            valid = QMessageBox.question(
                self,
                'Подтверждение действия',
                f"Вы действительно хотите удалить строку с itemId {itemId}?",
                QMessageBox.Yes,
                QMessageBox.No
            )  # Запрашиваем подтверждение

            if valid == QMessageBox.Yes:  # Если есть согласие:
                self.cur.execute("DELETE FROM PriceList\n" +
                                 f'WHERE itemId = {itemId}')  # Удаление

                self.cur.execute('UPDATE SQLITE_SEQUENCE SET SEQ = 0 WHERE NAME = "PriceList"')
                # Обнуление счетскика автоикрементора

                self.fastUpd1()
                self.isSave = False
                self.itemsToNull(1)
        else:
            # Иначе - ошибка:
            self.errorMessage('Ошибка!\nНе выбран ни один элемент!')

    def deleteStr2(self):
        if self.item2:
            id = self.TableWidget2.item(self.x2, 0).text()

            valid = QMessageBox.question(
                self,
                'Подтверждение действия',
                f"Вы действительно хотите удалить строку с idGood {id}?",
                QMessageBox.Yes,
                QMessageBox.No
            )

            if valid == QMessageBox.Yes:
                self.cur.execute("DELETE FROM goods\n" +
                                 f'WHERE idGood = {id}')
                self.cur.execute('UPDATE SQLITE_SEQUENCE SET SEQ = 0 WHERE NAME = "goods"')
                self.fastUpd2()
                self.isSave = False
                self.itemsToNull(2)
        else:
            self.errorMessage('Ошибка!\nНе выбран ни один элемент!')

    def deleteStr3(self):
        if self.item3:
            id = self.TableWidget3.item(self.x3, 0).text()

            valid = QMessageBox.question(
                self,
                'Подтверждение действия',
                f"Вы действительно хотите удалить строку с idShop {id}?",
                QMessageBox.Yes,
                QMessageBox.No
            )

            if valid == QMessageBox.Yes:
                self.cur.execute("DELETE FROM shops\n" +
                                 f'WHERE idShop = {id}')
                self.cur.execute('UPDATE SQLITE_SEQUENCE SET SEQ = 0 WHERE NAME = "shops"')
                self.fastUpd3()
                self.isSave = False
                self.itemsToNull(3)
        else:
            self.errorMessage('Ошибка!\nНе выбран ни один элемент!')

    def deleteStr4(self):
        if self.item4:
            id = self.TableWidget4.item(self.x4, 0).text()

            valid = QMessageBox.question(
                self,
                'Подтверждение действия',
                f"Вы действительно хотите удалить строку с idType {id}?",
                QMessageBox.Yes,
                QMessageBox.No
            )

            if valid == QMessageBox.Yes:
                self.cur.execute("DELETE FROM typesOfGoods\n" +
                                 f'WHERE idType = {id}')
                self.cur.execute('UPDATE SQLITE_SEQUENCE SET SEQ = 0 WHERE NAME = "typesOfGoods"')
                self.fastUpd4()
                self.isSave = False
                self.itemsToNull(4)
        else:
            self.errorMessage('Ошибка!\nНе выбран ни один элемент!')

    def itemUpdate1(self):
        # Комментарии пишу толко сюда, остальные 3 метода идентичны.
        if self.item1:  # Есть ли нажатая ячейка.
            column = COLUMN_LABLES1[self.y1]  # Столбец нажатой ячейки
            if column == 'itemId':  # Нередактируемые столбцы
                self.errorMessage('Данное поле редактировать нельзя!')
                self.itemsToNull(1)
                return 0
            if column == 'shopId' or column == 'shopName':  # Для зависимых столбцов я сделал comboBox
                # Для независимых от других таблиц столбцов просто LineEdit
                items = self.cur.execute("""SELECT shopName FROM shops""").fetchall()
                items = [i[0] for i in items]

                title, okPressed = QInputDialog.getItem(self, 'Внесение изменений',
                                                        'Выберите новое значение:', items, 0, False)

                title = self.cur.execute("SELECT idShop FROM shops\n" +
                                         f'WHERE shopName = "{title}"').fetchone()[0]
                column = 'shopId'
            elif column == 'goodId' or column == 'titleGood':
                items = self.cur.execute("""SELECT titleGood FROM goods""").fetchall()
                items = [i[0] for i in items]

                title, okPressed = QInputDialog.getItem(self, 'Внесение изменений',
                                                        'Выберите новое значение:', items, 0, False)

                title = self.cur.execute("SELECT idGood FROM goods\n" +
                                         f'WHERE titleGood = "{title}"').fetchone()[0]
                column = 'goodId'
            else:
                title, okPressed = QInputDialog.getText(self, 'Внесение изменений', 'Введите новое значение:')
            # Получение подтверждения и нового значения для ячейки

            if okPressed:
                try:
                    title = int(title)  # проверка на корректность введённых данных
                    try:
                        """Если всё хорошо поднимается ошибка Upd, после чего мы попадаем
                        в блок except и производится редактирование ячейки.
                        Если есть какая-либо ошибка, поднимается ошибка Error
                        и в except'е открывается диалоговое окно оповещающее об ошибке"""
                        raise Upd()
                    except Upd:
                        # Редактирование ячейки:
                        self.cur.execute('UPDATE PriceList\n' +
                                         f'SET {column} = "{title}"' +
                                         f'WHERE itemId = "{self.TableWidget1.item(self.x1, 0).text()}"')
                        self.fastUpd1()
                        self.isSave = False
                    except Error as titl:
                        # Диалоговое окно с ошибкой:
                        self.errorMessage(str(titl))
                except ValueError:
                    # Ичена - ошибка:
                    self.errorMessage('Ошибка!\nНеверный формат значения!')
        else:
            # Иначе - ошибка:
            self.errorMessage('Ошибка!\nНе выбран ни один элемент!')

    def itemUpdate2(self):
        if self.item2:
            column = COLUMN_LABLES2[self.y2]
            if column == 'idGood':
                self.errorMessage('Данное поле редактировать нельзя!')
                self.itemsToNull(1)
                return 0
            if column == 'typeName' or column == 'typeIdGood':
                items = self.cur.execute("SELECT typeName FROM typesOfGoods").fetchall()
                items = [i[0] for i in items]

                title, okPressed = QInputDialog.getItem(self, 'Внесение изменений',
                                                        'Выберите новое значение:', items, 0, False)

                title = self.cur.execute("SELECT idType FROM typesOfGoods\n" +
                                         f'WHERE typeName = "{title}"').fetchone()[0]
                column = 'typeIdGood'
            else:
                title, okPressed = QInputDialog.getText(self, 'Внесение изменений', 'Введите новое значение:')

            if okPressed:
                if column != 'titleGood':  # Условие на столбец с типом данных int
                    try:
                        title = int(title)
                        self.cur.execute('UPDATE goods\n' +
                                         f'SET {column} = "{title}"' +
                                         f'WHERE idGood = "{self.TableWidget2.item(self.x2, 0).text()}"')
                        self.isSave = False
                    except ValueError:
                        self.errorMessage('Ошибка!\nНеверный формат значения!')

                else:
                    self.cur.execute('UPDATE goods\n' +
                                     f'SET {column} = "{title}"' +
                                     f'WHERE idGood = "{self.TableWidget2.item(self.x2, 0).text()}"')
                    self.isSave = False  # Разместил 2 раза т.к. после except'a переменная изменится если
                self.fastUpd2()  # <- она будет изменяться здесь, а это ошибка
                self.itemsToNull(2)
            else:
                self.errorMessage('Ошибка!\nНе выбран ни один элемент!')


    def itemUpdate3(self):
        if self.item3:
            column = COLUMN_LABLES3[self.y3]
            if column == 'idShop':
                self.errorMessage('Данное поле редактировать нельзя!')
                self.itemsToNull(1)
                return 0
            title, okPressed = QInputDialog.getText(self, 'Внесение изменений', 'Введите новое значение:')

            if okPressed:
                self.cur.execute('UPDATE shops\n' +
                                 f'SET {column} = "{title}"' +
                                 f'WHERE idShop = "{self.TableWidget3.item(self.x3, 0).text()}"')
                self.isSave = False
                self.fastUpd3()
                self.itemsToNull(3)
        else:
            self.errorMessage('Ошибка!\nНе выбран ни один элемент!')


    def itemUpdate4(self):
        if self.item4:
            column = COLUMN_LABLES4[self.y4]
            if column == 'idType':
                self.errorMessage('Данное поле редактировать нельзя!')
                self.itemsToNull(1)
                return 0
            title, okPressed = QInputDialog.getText(self, 'Внесение изменений', 'Введите новое значение:')

            if okPressed:
                self.cur.execute('UPDATE typesOfGoods\n' +
                                 f'SET {column} = "{title}"' +
                                 f'WHERE idType = "{self.TableWidget4.item(self.x4, 0).text()}"')
                self.isSave = False
                self.fastUpd4()
                self.itemsToNull(4)
        else:
            self.errorMessage('Ошибка!\nНе выбран ни один элемент!')


    def save(self, fast=None):
        # Сохранение базы данных
        if not fast:
            valid = QMessageBox.question(
                self,
                'Подтверждение действия',
                "Вы действительно хотите сохранить изменения?",
                QMessageBox.Yes,
                QMessageBox.No
            )
        else:
            valid = None

        if valid == QMessageBox.Yes or fast:
            self.db.commit()
            self.isSave = True


    def closeEvent(self, event):  # Переопределить closeEvent
        # Проверка на сохранённость данных, подтверждение о сохранении
        # При попытке закрыть окно*
        if not self.isSave:
            reply = QMessageBox.question(
                self, 'Сохранение',
                "У вас имеются несохранённые данные.\nСохранить изменения?",
                QMessageBox.Yes,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.save(fast=True)
                event.accept()
            elif reply == QMessageBox.No:
                event.accept()
            elif reply == QMessageBox.Cancel:
                event.ignore()
        else:
            event.accept()


    def mousePressEvent(self, event):
        # Если нажать мышкой по пустому месту (не по таблице)
        # Все ранее нажатые ячейки анулируются.
        for i in range(1, 5):
            self.itemsToNull(i)


    def add1(self):
        # След. 3 метода идентичны
        # Вызов диалогового окна, куда передаются названия столбцов
        self.addWindow(COLUMN_LABLES1, [0, 2, 4, 5])
        self.tableAdd = 1  # В какую таблицу происходит добавление


    def add2(self):
        self.addWindow(COLUMN_LABLES2, [0, 2, 3])
        self.tableAdd = 2


    def add3(self):
        self.addWindow(COLUMN_LABLES3, [0, 1, 2])
        self.tableAdd = 3


    def add4(self):
        self.addWindow(COLUMN_LABLES4, [0, 1])
        self.tableAdd = 4


    def addWindow(self, lables, ids):
        self.windowAdd = WindowAdd([lables[i] for i in ids], self.db)
        # Вызов самого диалогового окна

        self.timerAdd = QTimer()
        self.timerAdd.timeout.connect(self.getItemsFromAddWindow)
        self.timerAdd.start(250)
        # Запуск таймера, который раз в 0.25 сек. проверяет была ли нажата кнопка ok либо cancel


    def getItemsFromAddWindow(self):
        # Заходит в if после нажатия кнопки ok либо cancel в диалоговом окне добавления
        if not self.windowAdd.okPressed == 'NONE':
            self.timerAdd.stop()  # Остановка таймера

            if self.windowAdd.okPressed:  # Если была нажата кнопка ok
                self.addItems = self.windowAdd.items  # Запись полученных данных в переменную

                # Вызов одного из методов, в зависимости от того, в какую таблицу происходит добавление
                if self.tableAdd == 1:
                    self.addToTable1()
                elif self.tableAdd == 2:
                    self.addToTable2()
                elif self.tableAdd == 3:
                    self.addToTable3()
                elif self.tableAdd == 4:
                    self.addToTable4()

            self.windowAdd.close()  # закрытие диалогового окна


    def addToTable1(self):
        # Комментарии пишу только сюда, след. 3 метода идентичны
        if self.addItems[0] == 'По Умолчанию (на 1 больше предыдущего)':
            # Проверка на введение первого поля
            columns = '(shopId,goodId,price)'  # Столбцы в которые произведётся запись данных
            values = f'({self.addItems[1]},{self.addItems[2]}'  # сами данные, соответственно столбцам
        else:
            columns = '(itemId,shopId,goodId,price)'
            try:
                # Проверка на корректносить введения значения первого столбца (id'шника)
                idsh = int(self.addItems[0])
                result = self.cur.execute("SELECT itemId FROM PriceList").fetchall()
                result = [i[0] for i in result]
                if idsh not in result:
                    values = f'({idsh},{self.addItems[1]},{self.addItems[2]}'
                else:
                    raise ValueError()
            except ValueError:
                # Если нет - ошибка:
                self.errorMessage('Некорректно введено значение поля itemId!')
                return 0
        try:
            # Проверка на коректность введения (в данном случае) столбца price
            values += f',{int(self.addItems[3])})'
            self.cur.execute("INSERT INTO PriceList" + columns + " VALUES" + values)
            self.fastUpd1()
            self.isSave = False
        except ValueError:
            self.errorMessage('Некорректно введено значение поля price!')


    def addToTable2(self):
        if self.addItems[0] == 'По Умолчанию (на 1 больше предыдущего)':
            columns = '(typeIdGood,titleGood)'
            values = f'({self.addItems[1]},"{self.addItems[2]}")'
        else:
            columns = '(idGood,typeIdGood,titleGood)'
            try:
                idsh = int(self.addItems[0])
                result = self.cur.execute("SELECT idGood FROM goods").fetchall()
                result = [i[0] for i in result]
                if idsh not in result:
                    values = f'({idsh},{self.addItems[1]},"{self.addItems[2]}")'
                else:
                    raise ValueError()
            except ValueError:
                self.errorMessage('Некорректно введено значение поля idGood!')
                return 0
        self.cur.execute("INSERT INTO goods" + columns + " VALUES" + values)
        self.fastUpd2()
        self.isSave = False


    def addToTable3(self):
        if self.addItems[0] == 'По Умолчанию (на 1 больше предыдущего)':
            columns = '(shopName,shopLink)'
            values = f'("{self.addItems[1]}","{self.addItems[2]}")'
        else:
            columns = '(idShop,shopName,shopLink)'
            try:
                idsh = int(self.addItems[0])
                result = self.cur.execute("SELECT idShop FROM shops").fetchall()
                result = [i[0] for i in result]
                if idsh not in result:
                    values = f'({idsh},"{self.addItems[1]}","{self.addItems[2]}")'
                else:
                    raise ValueError()
            except ValueError:
                self.errorMessage('Некорректно введено значение поля idShop!')
                return 0
        self.cur.execute("INSERT INTO shops" + columns + " VALUES" + values)
        self.fastUpd3()
        self.isSave = False


    def addToTable4(self):
        if self.addItems[0] == 'По Умолчанию (на 1 больше предыдущего)':
            columns = '(typeName)'
            values = f'("{self.addItems[1]}")'
        else:
            columns = '(idType,typeName)'
            try:
                idsh = int(self.addItems[0])
                result = self.cur.execute("SELECT idType FROM typesOfGoods").fetchall()
                result = [i[0] for i in result]
                if idsh not in result:
                    values = f'({idsh},"{self.addItems[1]}")'
                else:
                    raise ValueError()
            except ValueError:
                self.errorMessage('Некорректно введено значение поля idType!')
                return 0
        self.cur.execute("INSERT INTO typesOfGoods" + columns + " VALUES" + values)
        self.fastUpd4()
        self.isSave = False

class WindowAdd(Ui_Dialog, QtWidgets.QWidget):
    """Класс диалогового окна добавления элементов в таблицу."""

    def __init__(self, namesOfColumns, bd):
        super().__init__()
        self.setupUi(self)
        self.names = namesOfColumns  # названия столбцов
        self.cur = bd.cursor()  # курсор для поиска по базе
        self.widgets = []  # виджеты ввода информации
        self.okPressed = 'NONE'  # нажата ли одна из кнопок (ok, cancel)

        self.setWindowTitle('Добавление элемента в таблицу')
        # название окна

        for i in range(len(namesOfColumns)):
            nameColumn = self.names[i]

            # label с названием столбца, значение которого необходио ввести
            label = QtWidgets.QLabel(self)
            label.resize(481, 31)
            label.setText(nameColumn)
            label.move(20, ADD_WINDOW_WIDGETS_COORDS[i][0])

            if (nameColumn == COLUMN_LABLES_ONLY_CHOICE[0] and namesOfColumns[0] == 'idGood') or \
                    (nameColumn in COLUMN_LABLES_ONLY_CHOICE[1:] and \
                     namesOfColumns[0] == 'itemId'):
                """Если столбец зависит от другой таблицы, то создаётся comboBox
                с Возможными элементами"""
                comboBox = QtWidgets.QComboBox(self)
                comboBox.resize(481, 41)
                comboBox.move(20, ADD_WINDOW_WIDGETS_COORDS[i][1])

                if nameColumn == COLUMN_LABLES_ONLY_CHOICE[0]:
                    search = """SELECT typeName FROM typesOfGoods"""
                elif nameColumn == COLUMN_LABLES_ONLY_CHOICE[1]:
                    search = """SELECT shopName FROM shops"""
                else:
                    search = """SELECT titleGood FROM goods"""

                for item in self.cur.execute(search).fetchall():
                    comboBox.addItem(str(item[0]))
                    # Заполнение comboBox'а

                self.widgets.append(comboBox)
            else:
                # Если столбец не зависим, то создаётся LineEdit
                lineEdit = QtWidgets.QLineEdit(self)
                lineEdit.resize(481, 41)
                lineEdit.move(20, ADD_WINDOW_WIDGETS_COORDS[i][1])
                if i == 0:
                    lineEdit.setText('По Умолчанию (на 1 больше предыдущего)')
                self.widgets.append(lineEdit)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        # Коннект кнопок
        self.show()

    def reject(self):
        # Нажатие кнопки cancel
        self.items = []  # Данные полученные из виджетов для ввода (ничего)
        self.okPressed = False

    def accept(self):
        # Нажатие кнопки ok
        self.items = []  # Данные полученные из виджетов для ввода
        for i in self.widgets:
            """В этом цикле извлекается полученная информация из виджетов
            и заносится в список"""
            if i.__class__ is QtWidgets.QLineEdit:
                self.items.append(i.text())
            elif i.__class__ is QtWidgets.QComboBox:
                if i == self.widgets[2]:
                    item = self.cur.execute('SELECT idGood FROM goods\n' +
                                            f'WHERE titleGood = "{i.currentText()}"').fetchall()
                    self.items.append(item[0][0])
                elif i == self.widgets[1]:
                    typess = self.cur.execute("SELECT typeName FROM typesOfGoods").fetchall()
                    types = [i[0] for i in typess]
                    if i.currentText() in types:
                        item = self.cur.execute('SELECT idType FROM typesOfGoods\n' +
                                                f'WHERE typeName = "{i.currentText()}"').fetchall()
                    else:
                        item = self.cur.execute('SELECT idShop FROM shops\n' +
                                                f'WHERE shopName = "{i.currentText()}"').fetchall()
                    self.items.append(item[0][0])

        self.okPressed = True


def main():
    # Стандартная конструкция создания и вывода на экран графического интерфейка
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
