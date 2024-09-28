from PyQt5.QtWidgets import QFileDialog
from qgis.PyQt.QtWidgets import QMainWindow
from qgis.core import QgsProject
from QGIS_Design_0214 import Ui_MainWindow

#PROJECT=QgsProject.instance()

#用#注释上面这句话，往后遇到PROJECT，用右侧的替代

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("312205040214 zhou tao")
        self.actionOpen_Map.triggered.connect(self.actionOpenMapTriggered)
    def actionOpenMapTriggered(self):
        map_file, ext = QFileDialog.getOpenFileName(self, '打开', '',
                                                    "QGIS Map(*.qgz);;All Files(*);;Other(*.gpkg;*.geojson;*.kml)")
        QgsProject.instance.read(map_file)
