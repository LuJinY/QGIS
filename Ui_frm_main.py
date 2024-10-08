import os
import traceback
from tarfile import data_filter

from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QVBoxLayout, QMenu, QAction, QDialog, QApplication, QMessageBox
from PyQt5.uic.Compiler.qtproxies import QtWidgets
from pygments.lexer import default
from qgis.PyQt.QtWidgets import QMainWindow
from qgis._core import QgsLayerTreeModel, QgsVectorLayer, QgsRasterLayer, QgsMapLayer, QgsLayerTreeNode, \
    QgsVectorLayerCache, QgsLayerTree, QgsLayerTreeGroup
from qgis._gui import QgsMapCanvas, QgsLayerTreeMapCanvasBridge, QgsLayerTreeView, QgsAttributeTableView, QgsGui, \
    QgsAttributeTableModel, QgsAttributeTableFilterModel, QgsLayerTreeViewMenuProvider, QgsLayerTreeViewDefaultActions, \
    QgsMapToolIdentifyFeature
from qgis.core import QgsProject, QgsMapLayerType
from qgis.PyQt.QtCore import QObject, pyqtSignal
from QGIS_Design_0214 import Ui_MainWindow
#PROJECT=QgsProject.instance()


class AttributeDialog(QDialog):
    def __init__(self, mainWindows,layer):
        super(AttributeDialog,self).__init__(mainWindows)
        self.mainWindows = mainWindows
        self.mapCanvas=self.mainWindows.mapCanvas
        self.layer:QgsVectorLayer=layer
        self.setWindowTitle(self.layer.name()+"属性表:")
        vl=QHBoxLayout(self)
        self.tableView= QgsAttributeTableView(self)
        self.resize(400,400)
        vl.addWidget(self.tableView)
        self.openAttributeDialog()
        QgsGui.editorWidgetRegistry().initEditors(self.mapCanvas)

    def openAttributeDialog(self):
        self.layerCache=QgsVectorLayerCache(self.layer,10000)
        self.tableModel=QgsAttributeTableModel(self.layerCache)
        self.tableModel.loadLayer()
        self.tableFilterModel= QgsAttributeTableFilterModel(self.mapCanvas, self.tableModel, parent=self.tableModel)
        self.tableFilterModel.setFilterMode(QgsAttributeTableFilterModel.ShowAll) #显示问题
        self.tableView.setModel(self.tableFilterModel)

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        #初始化界面
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("312205040214 zhou tao")

        #绑定槽函数OpenMap
        self.actionOpenMap.triggered.connect(self.actionOpenMapTriggered)

        #设置画布
        self.mapCanvas = QgsMapCanvas(self)
        hl = QHBoxLayout(self.frame)
        hl.setContentsMargins(0, 0, 0, 0)  # 设置周围间距
        hl.addWidget(self.mapCanvas)
        #关联画布,建立图层树与地图画布的桥接
        self.layerTreeBridge = QgsLayerTreeMapCanvasBridge(QgsProject.instance().layerTreeRoot(), self.mapCanvas, self)

        #初始化图层树
        v1 = QVBoxLayout(self.dockWidgetContents)
        self.layerTreeView = QgsLayerTreeView(self)
        v1.addWidget(self.layerTreeView)

        #设置图层树风格
        self.model = QgsLayerTreeModel(QgsProject.instance().layerTreeRoot(), self)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeRename)  # 允许图层节点重命名
        self.model.setFlag(QgsLayerTreeModel.AllowNodeReorder)  # 允许图层拖拽排序
        self.model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)  # 允许改变图层节点可视性
        self.model.setFlag(QgsLayerTreeModel.ShowLegendAsTree)  # 展示图例
        self.model.setAutoCollapseLegendNodes(10)  # 当节点数大于等于10时自动折叠
        self.layerTreeView.setModel(self.model)

        #槽函数actionOpenVector和actionOpenRaster
        self.actionOpenVector.triggered.connect(self.actionOpenVectorTriggered)
        self.actionOpenRaster.triggered.connect(self.actionOpenRasterTriggered)

        #选中图层时的默认Action
        self.default_action = self.layerTreeView.defaultActions()
        self.action_zoom_to_layer = self.default_action.actionZoomToLayer(self.mapCanvas)
        self.action_move_to_top = self.default_action.actionMoveToTop()
        self.action_move_to_bottom = self.default_action.actionMoveToBottom()
        self.action_remove_layer = self.default_action.actionRemoveGroupOrLayer()

        #默认菜单(未选中)
        self.otherMenu = QMenu()
        self.otherMenu.addAction(self.actionOpenMap)
        self.otherMenu.addAction(self.actionOpenVector)
        self.otherMenu.addAction(self.actionOpenRaster)
        self.otherMenu.addAction('展开所有图层', self.layerTreeView.expandAllNodes)
        self.otherMenu.addAction('折叠所有图层', self.layerTreeView.collapseAllNodes)

        #默认菜单（选中）
        self.defaultMenu = QMenu()
        self.defaultMenu.addAction(self.action_zoom_to_layer)
        self.defaultMenu.addAction(self.action_move_to_top)
        self.defaultMenu.addAction(self.action_move_to_bottom)
        self.defaultMenu.addAction(self.action_remove_layer)
        self.actions: QgsLayerTreeViewDefaultActions = self.layerTreeView.defaultActions()

        #菜单关联
        self.layerTreeView.customContextMenuRequested.connect(self.showContextMenu)
        self.layerTreeView.setContextMenuPolicy(Qt.CustomContextMenu)

        #设置不同的右键菜单
        self.vectorMenu = QMenu()
        self.actionShowAttributeDialog = QAction("打开属性表", self.layerTreeView)
        self.vectorMenu.addAction(self.action_zoom_to_layer)
        self.vectorMenu.addAction(self.action_move_to_top)
        self.vectorMenu.addAction(self.action_move_to_bottom)
        self.vectorMenu.addAction(self.action_remove_layer)
        self.vectorMenu.addAction(self.actionShowAttributeDialog)
        self.actionShowAttributeDialog.triggered.connect(self.openAttributeTableTriggered)

        #退出设置
        self.actionExit.triggered.connect(self.actionExitTriggered)

        #拖拽设置
        self.setAcceptDrops(True)

        self.actionEditVector.setEnabled(False)
        self.editTempLayer: QgsVectorLayer = None  # 初始编辑图层为None

        #鼠标触发事件
        self.layerTreeView.clicked.connect(self.layerClicked)

        #编辑、选择、删除要素
        self.actionEditVector.triggered.connect(self.actionEditVectorTriggered)
        self.actionSelectFeature.triggered.connect(self.actionSelectFeatureTriggered)
        self.actionDeleteFeature.triggered.connect(self.actionDeleteFeatureTriggered)


    #响应actionOpenMap
    def actionOpenMapTriggered(self):
        map_file, ext = QFileDialog.getOpenFileName(self, '打开', '',
                                                    "QGIS Map(*.qgz);;All Files(*);;Other(*.gpkg;*.geojson;*.kml)")
        QgsProject.instance().read(map_file)

    #响应actionOpenVector
    def actionOpenVectorTriggered(self):
        data_file, ext = QFileDialog.getOpenFileName(self, 'Open Vector','.',"QGIS Vector(*.shp)")
        vectorLayer = QgsVectorLayer(data_file,os.path.basename(data_file))
        QgsProject.instance().addMapLayer(vectorLayer)

    #响应actionOpenRaster
    def actionOpenRasterTriggered(self):
        data_file,ext= QFileDialog.getOpenFileName(self,'Open Rasters'  "QGlS Raster(* tif")
        rasterLayer=QgsRasterLayer(data_file,os.path.basename(data_file))
        QgsProject.instance().addMapLayer(rasterLayer)

    #响应showContextMenu
    def showContextMenu(self,index):
        selected_nodes:list[QgsLayerTreeNode] = self.layerTreeView.selectedLayerNodes()
        selected_layers:list[QgsMapLayer] = self.layerTreeView.selectedLayers()
        if len(selected_nodes)==0:
            self.otherMenu.exec(QCursor.pos())
        else:
            pass
        if len(selected_layers)==1:
            current_layer = selected_layers[0]
            if isinstance(current_layer, QgsVectorLayer):
                self.vectorMenu.exec(QCursor.pos())
            elif isinstance(current_layer, QgsRasterLayer):
                self.defaultMenu.exec(QCursor.pos())
        else:
            pass

    #响应——openAttributeTable
    def openAttributeTableTriggered(self):
        self.layer=self.layerTreeView.currentLayer()
        ad=AttributeDialog(self,self.layer)
        ad.show()

    #响应——actionExit
    def actionExitTriggered(self):
        print("Exiting QGIS开发...")
        QApplication.quit()
        print("Succeed")

    #判断拖拽的数据
    def dragEnterEvent(self, fileData):
        if fileData.mimeData().hasUrls():
            fileData.accept()
        else:
            fileData.ignore()

    #处理拖拽数据,需要拖拽至菜单栏Data位置，否则程序崩溃
    def dropEvent(self, fileData):
        mimeData: QMimeData = fileData.mimeData()
        filePathList = [u.path()[1:] for u in mimeData.urls()]
        for filePath in filePathList:
            filePath: str = filePath.replace("/", "//")
            if filePath.split(".")[-1] in ["tif", "TIF", "tiff", "TIFF", "GTIFF", "png", "jpg", "pdf"]:
                data_file=filePath
                rasterLayer = QgsRasterLayer(data_file, os.path.basename(data_file))
                QgsProject.instance().addMapLayer(rasterLayer)
            elif filePath.split(".")[-1] in ["shp", "SHP", "gpkg", "geojson", "kml"]:
                data_file=filePath
                vectorLayer = QgsVectorLayer(data_file, os.path.basename(data_file))
                QgsProject.instance().addMapLayer(vectorLayer)
            elif filePath == "":
                pass
            else:
                QMessageBox.about(self, '警告', f'{filePath}为不支持的文件类型，目前支持栅格影像和shp矢量')

    #处理图层点击事件，并选择启用或禁用
    def layerClicked(self):
        curLayer: QgsMapLayer = self.layerTreeView.currentLayer()
        if curLayer and type(curLayer) == QgsVectorLayer and not curLayer.readOnly():
            self.actionEditVector.setEnabled(True)
        else:
            self.actionEditVector.setEnabled(False)

    #响应——EditVector
    def actionEditVectorTriggered(self):
        if self.actionEditVector.isChecked():
            self.editTempLayer: QgsVectorLayer = self.layerTreeView.currentLayer()
            self.editTempLayer.startEditing()
        else:
            saveShpEdit = QMessageBox.question(self, '保存编辑', "确定要将编辑内容保存到内存吗？",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if saveShpEdit == QMessageBox.Yes:
                self.editTempLayer.commitChanges()
            else:
                self.editTempLayer.rollBack()

            self.mapCanvas.refresh()
            self.editTempLayer = None

    #处理在地图上选择的特征，并在控制台输出结果
    def selectToolIdentified(self, feature):
        print(feature.id())
        layerTemp: QgsVectorLayer = self.layerTreeView.currentLayer()
        if layerTemp.type() == QgsMapLayerType.VectorLayer:
            if feature.id() in layerTemp.selectedFeatureIds():
                layerTemp.deselect(feature.id())
            else:
                layerTemp.removeSelection()
                layerTemp.select(feature.id())

    #响应——SelectFeature
    def actionSelectFeatureTriggered(self):
        if self.actionSelectFeature.isChecked():
            if self.mapCanvas.mapTool():
                self.mapCanvas.unsetMapTool(self.mapCanvas.mapTool())
            self.selectTool = QgsMapToolIdentifyFeature(self.mapCanvas)
            self.selectTool.setCursor(Qt.ArrowCursor)
            self.selectTool.featureIdentified.connect(self.selectToolIdentified)
            layers = self.mapCanvas.layers()
            if layers:
                self.selectTool.setLayer(self.layerTreeView.currentLayer())
            self.mapCanvas.setMapTool(self.selectTool)
        else:
            if self.mapCanvas.mapTool():
                self.mapCanvas.unsetMapTool(self.mapCanvas.mapTool())

    #响应——DeleteFeature
    def actionDeleteFeatureTriggered(self):
        if self.editTempLayer == None:
            QMessageBox.information(self, '警告', '您没有编辑中矢量')
            return
        if len(self.editTempLayer.selectedFeatureIds()) == 0:
            QMessageBox.information(self, '删除选中矢量', '您没有选择任何矢量')
        else:
            self.editTempLayer.deleteSelectedFeatures()