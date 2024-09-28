from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QVBoxLayout
from qgis.PyQt.QtWidgets import QMainWindow
from qgis._core import QgsLayerTreeModel
from qgis._gui import QgsMapCanvas, QgsLayerTreeMapCanvasBridge, QgsLayerTreeView
from qgis.core import QgsProject
from QGIS_Design_0214 import Ui_MainWindow
#PROJECT=QgsProject.instance()

#用#注释上面这句话，往后遇到PROJECT，用右侧的替代

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        #初始化界面
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("312205040214 zhou tao")

        #绑定槽函数OpenMap
        self.actionOpen_Map.triggered.connect(self.actionOpenMapTriggered)

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



    #响应槽函数OpenMao
    def actionOpenMapTriggered(self):
        map_file, ext = QFileDialog.getOpenFileName(self, '打开', '',
                                                    "QGIS Map(*.qgz);;All Files(*);;Other(*.gpkg;*.geojson;*.kml)")
        QgsProject.instance().read(map_file)

