# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from funcs import *
from scapy.all import *
from threading import Thread
import datetime
import socket


class Ui_capturing_window():
    def __init__(self, mac, start_window):
        self.chosen_mac = mac
        self.capturing_status = True
        self.ip_protocols = {num:name[8:] for name,num in vars(socket).items() if name.startswith("IPPROTO")}
        self.window_to_reshow = start_window


    def setupUi(self, MainWindow):
        self.my_window = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(676, 545)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Packets_table = QtWidgets.QTableWidget(self.centralwidget)
        self.Packets_table.setObjectName("Packets")
        self.Packets_table.setColumnCount(5)
        self.Packets_table.setRowCount(0)
        self.Packets_table.setColumnWidth(0,200) ###########################
        self.Packets_table.itemSelectionChanged.connect(self.selected_change)

        item = QtWidgets.QTableWidgetItem()
        self.Packets_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.Packets_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.Packets_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.Packets_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.Packets_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.Packets_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.Packets_table.setHorizontalHeaderItem(6, item)
        self.verticalLayout.addWidget(self.Packets_table)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)

        self.pack_details = QtWidgets.QTextBrowser(self.centralwidget)
        self.pack_details.setObjectName("pack_hex")
        self.verticalLayout.addWidget(self.pack_details)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 676, 21))
        self.menubar.setObjectName("menubar")
        self.menuCapture = QtWidgets.QMenu(self.menubar)
        self.menuCapture.setObjectName("menuCapture")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionClear.triggered.connect(self.clear_c)


        self.actionStart = QtWidgets.QAction(MainWindow)
        self.actionStart.setObjectName("actionStart")
        self.actionStart.triggered.connect(self.start_c)


        self.actionStop = QtWidgets.QAction(MainWindow)
        self.actionStop.setObjectName("actionStop")
        self.actionStop.triggered.connect(self.stop_c)


        self.menuCapture.addAction(self.actionStart)
        self.menuCapture.addAction(self.actionStop)
        self.menuCapture.addAction(self.actionClear)

        self.menubar.addAction(self.menuCapture.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "capturing window"))

        item = self.Packets_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Time"))
        item = self.Packets_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Source"))
        item = self.Packets_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Destination"))
        item = self.Packets_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Protocol"))
        item = self.Packets_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Length"))

        self.menuCapture.setTitle(_translate("MainWindow", "Capture"))
        self.actionClear.setText(_translate("MainWindow", "Clear"))
        self.actionStart.setText(_translate("MainWindow", "Start"))
        self.actionStop.setText(_translate("MainWindow", "Stop"))


    def reshow(self):
        self.window_to_reshow.show()


    def back_c(self):
        self.reshow()
        self.my_window.close()

    def start_c(self):
        if self.chosen_mac is None:
            self.back_c()
        self.capturing_status = True
        sniffer = Thread(target=self.threaded_sniff_target)
        sniffer.daemon = True
        sniffer.start()


    def stop_c(self):
        self.capturing_status = False

    def sniffed_packet(self,p):
        if IP in p:
            if self.chosen_mac in [mac_for_ip(p[IP].src), mac_for_ip(p[IP].dst)]:
                rowPosition = self.Packets_table.rowCount()
                self.Packets_table.insertRow(rowPosition)
                self.Packets_table.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(str(datetime.datetime.fromtimestamp(p.time))))
                self.Packets_table.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(p[IP].src))
                self.Packets_table.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(p[IP].dst))
                self.Packets_table.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(self.ip_protocols[int(p[IP].proto)]))
                self.Packets_table.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(str(p[IP].len)))



    def threaded_sniff_target(self):
        self.pckts = sniff(prn=self.sniffed_packet, stop_filter=lambda packet : not self.capturing_status)

    def selected_change(self):
        index = self.Packets_table.currentRow()
        p = self.pckts[index]
        b = p.show
        #p.show()
        try:
            e = str(b).index("<Raw")
        except:
            e = -1
        self.pack_details.setText((("\n" + "-"*150 + "\n").join(str(b)[28: e].split("|"))).replace(" ","\n"))

    def clear_c(self):
        self.Packets_table.setRowCount(0)
        #self.pack_raw.setText("")
        self.pack_details.setText("")




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_capturing_window("64:5a:04:b4:6a:1c")
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

