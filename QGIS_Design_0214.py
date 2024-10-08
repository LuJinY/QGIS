# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QGIS_Design_0214.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuMap = QtWidgets.QMenu(self.menubar)
        self.menuMap.setObjectName("menuMap")
        self.menuData = QtWidgets.QMenu(self.menubar)
        self.menuData.setObjectName("menuData")
        self.menuNavigate = QtWidgets.QMenu(self.menubar)
        self.menuNavigate.setObjectName("menuNavigate")
        self.menuAnalysic = QtWidgets.QMenu(self.menubar)
        self.menuAnalysic.setObjectName("menuAnalysic")
        self.menuSetting = QtWidgets.QMenu(self.menubar)
        self.menuSetting.setObjectName("menuSetting")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.actionOpenMap = QtWidgets.QAction(MainWindow)
        self.actionOpenMap.setObjectName("actionOpenMap")
        self.actionOpenVector = QtWidgets.QAction(MainWindow)
        self.actionOpenVector.setObjectName("actionOpenVector")
        self.actionOpenRaster = QtWidgets.QAction(MainWindow)
        self.actionOpenRaster.setObjectName("actionOpenRaster")
        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtWidgets.QAction(MainWindow)
        self.actionRedo.setObjectName("actionRedo")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionEditVector = QtWidgets.QAction(MainWindow)
        self.actionEditVector.setCheckable(True)
        self.actionEditVector.setObjectName("actionEditVector")
        self.actionSelectFeature = QtWidgets.QAction(MainWindow)
        self.actionSelectFeature.setCheckable(True)
        self.actionSelectFeature.setObjectName("actionSelectFeature")
        self.actionDelectFeature = QtWidgets.QAction(MainWindow)
        self.actionDelectFeature.setCheckable(False)
        self.actionDelectFeature.setObjectName("actionDelectFeature")
        self.actionDeleteFeature = QtWidgets.QAction(MainWindow)
        self.actionDeleteFeature.setObjectName("actionDeleteFeature")
        self.menuMap.addAction(self.actionOpenMap)
        self.menuMap.addAction(self.actionExit)
        self.menuData.addAction(self.actionOpenVector)
        self.menuData.addAction(self.actionOpenRaster)
        self.menuEdit.addAction(self.actionEditVector)
        self.menuEdit.addAction(self.actionSelectFeature)
        self.menuEdit.addAction(self.actionDeleteFeature)
        self.menubar.addAction(self.menuMap.menuAction())
        self.menubar.addAction(self.menuData.menuAction())
        self.menubar.addAction(self.menuNavigate.menuAction())
        self.menubar.addAction(self.menuAnalysic.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuMap.setTitle(_translate("MainWindow", "Map"))
        self.menuData.setTitle(_translate("MainWindow", "Data"))
        self.menuNavigate.setTitle(_translate("MainWindow", "Navigate"))
        self.menuAnalysic.setTitle(_translate("MainWindow", "Analysic"))
        self.menuSetting.setTitle(_translate("MainWindow", "Setting"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionOpenMap.setText(_translate("MainWindow", "Open Map"))
        self.actionOpenVector.setText(_translate("MainWindow", "OpenVector"))
        self.actionOpenRaster.setText(_translate("MainWindow", "OpenRaster"))
        self.actionUndo.setText(_translate("MainWindow", "Undo"))
        self.actionRedo.setText(_translate("MainWindow", "Redo"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionEditVector.setText(_translate("MainWindow", "EditVector"))
        self.actionSelectFeature.setText(_translate("MainWindow", "SelectFeature"))
        self.actionDelectFeature.setText(_translate("MainWindow", "DelectFeature"))
        self.actionDeleteFeature.setText(_translate("MainWindow", "DeleteFeature"))
