import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QVBoxLayout, QMenu, QAction, QDialog, QApplication
from qgis.PyQt.QtWidgets import QMainWindow
from qgis._core import QgsLayerTreeModel, QgsVectorLayer, QgsRasterLayer, QgsMapLayer, QgsLayerTreeNode, \
    QgsVectorLayerCache
from qgis._gui import QgsMapCanvas, QgsLayerTreeMapCanvasBridge, QgsLayerTreeView, QgsAttributeTableView, QgsGui, \
    QgsAttributeTableModel, QgsAttributeTableFilterModel
from qgis.core import QgsProject
from qgis.PyQt.QtCore import QObject, pyqtSignal
from QGIS_Design_0214 import Ui_MainWindow
#PROJECT=QgsProject.instance()

#用#注释上面这句话，往后遇到PROJECT，用右侧的替代

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

        #默认菜单（选中）
        self.defaultMenu = QMenu()
        self.defaultMenu.addAction(self.action_zoom_to_layer)
        self.defaultMenu.addAction(self.action_move_to_top)
        self.defaultMenu.addAction(self.action_move_to_bottom)
        self.defaultMenu.addAction(self.action_remove_layer)

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





