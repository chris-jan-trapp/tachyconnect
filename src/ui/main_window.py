# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tachy_console.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.dialect_selector = QtWidgets.QComboBox(self.centralwidget)
        self.dialect_selector.setObjectName("dialect_selector")
        self.horizontalLayout.addWidget(self.dialect_selector)
        self.command_selector = QtWidgets.QComboBox(self.centralwidget)
        self.command_selector.setObjectName("command_selector")
        self.horizontalLayout.addWidget(self.command_selector)
        self.args = QtWidgets.QLineEdit(self.centralwidget)
        self.args.setObjectName("args")
        self.horizontalLayout.addWidget(self.args)
        self.send_command = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.send_command.setObjectName("send_command")
        self.horizontalLayout.addWidget(self.send_command)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 20)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.log_viewer = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.log_viewer.setUndoRedoEnabled(False)
        self.log_viewer.setReadOnly(True)
        self.log_viewer.setObjectName("log_viewer")
        self.verticalLayout.addWidget(self.log_viewer)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuTachy = QtWidgets.QMenu(self.menubar)
        self.menuTachy.setObjectName("menuTachy")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionconnect = QtWidgets.QAction(MainWindow)
        self.actionconnect.setObjectName("actionconnect")
        self.actionidentify = QtWidgets.QAction(MainWindow)
        self.actionidentify.setObjectName("actionidentify")
        self.action_Quit = QtWidgets.QAction(MainWindow)
        self.action_Quit.setObjectName("action_Quit")
        self.actionextract_capabilities = QtWidgets.QAction(MainWindow)
        self.actionextract_capabilities.setObjectName("actionextract_capabilities")
        self.actiondump_implementation_chart = QtWidgets.QAction(MainWindow)
        self.actiondump_implementation_chart.setObjectName("actiondump_implementation_chart")
        self.menuTachy.addAction(self.actionconnect)
        self.menuTachy.addAction(self.actionidentify)
        self.menuTachy.addAction(self.actionextract_capabilities)
        self.menuTachy.addAction(self.actiondump_implementation_chart)
        self.menuTachy.addSeparator()
        self.menuTachy.addAction(self.action_Quit)
        self.menubar.addAction(self.menuTachy.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.send_command.setText(_translate("MainWindow", "send"))
        self.menuTachy.setTitle(_translate("MainWindow", "Tachy"))
        self.actionconnect.setText(_translate("MainWindow", "&connect"))
        self.actionidentify.setText(_translate("MainWindow", "&identify"))
        self.action_Quit.setText(_translate("MainWindow", "&Quit"))
        self.actionextract_capabilities.setText(_translate("MainWindow", "extract capabilities"))
        self.actiondump_implementation_chart.setText(_translate("MainWindow", "dump implementation chart"))
