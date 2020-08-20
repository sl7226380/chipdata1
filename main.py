import MainWindow
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow,QTableWidgetItem,QAbstractItemView,QHeaderView,QListWidgetItem
from PyQt5.QtGui import QPixmap,QIcon,QFont
from PyQt5.QtCore import QRegExp,Qt,QStringListModel,QModelIndex
import sys
import pandas as pd
import numpy as np
import xlrd

class newUI(QMainWindow,MainWindow.Ui_MainWindow):
    def __init__(self):
        super(newUI, self).__init__()
        self.setupUi(self)
        self.chipdata_headers = []
        self.initUI()
        self.mainExe()

    def initUI(self):
        #设置窗口只有最小化和关闭按钮,设置窗口的长宽为固定值
        self.setWindowFlags(Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())
        #设置表格为不能编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #设置表格单元格在横纵方向上随字体拉升
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #设置单元格字体
        self.tableWidget.setFont(QFont("微软雅黑",8))

        #设置comboBox的选项
        list_supplier=["1.晶电","2.三安","3.华灿"]
        self.comboBox.addItems(list_supplier)
        #设置默认comBox的选项时的listwidget显示值
        comboBox_selected_supplier=self.comboBox.currentText()
        data=self.dataImport(comboBox_selected_supplier)
        self.list_chiptype = data[:, 1]
        self.listWidget.addItems(self.list_chiptype)

    def mainExe(self):
        self.comboBox.activated.connect(self.comboBox_selected)
        self.listWidget.itemClicked.connect(self.listwidget_clicked)
    def dataImport(self,supplier_name):
        #导入表头并设置给tablewidget
        self.chipdata_headers=[]
        excel=xlrd.open_workbook(r"chipdata/芯片产品List V5.2 -20200604.xlsx")
        sheet=excel.sheet_by_name(supplier_name)
        for i in range(sheet.ncols):
            self.chipdata_headers.append(sheet.cell(0,i).value)
        self.tableWidget.setHorizontalHeaderLabels(self.chipdata_headers)

        #将主数据存入np array中
        chipdata=pd.read_excel(r"chipdata/芯片产品List V5.2 -20200604.xlsx",sheet_name=supplier_name,header=0)
        self.chipdata_array=np.array(chipdata)
        # print(self.chipdata_array)





        return self.chipdata_array
        # chipDataExcel=xlrd.open_workbook(r"chipdata/芯片产品List V5.2 -20200604.xlsx")
        # chipDataES=chipDataExcel.sheet_by_name("1.晶电")
        # chipData_list=[]
        # for i in range(chipDataES.nrows):
        #     line=chipDataES.row_values(i)
        #     chipData_list.append(line)
        # chipData_array=np.array(chipData_list)
        # print(chipData_array)
    def comboBox_selected(self):
        #当comboBox里的值不一样时,在listwidget里显示对应的list
        self.listWidget.clear()
        comboBox_selected_supplier=self.comboBox.currentText()
        data=self.dataImport(comboBox_selected_supplier)
        self.list_chiptype = data[:, 1]
        self.listWidget.addItems(self.list_chiptype)



    def listwidget_clicked(self,item):
        self.tableWidget.clearContents()
        listwidget_selected_chiptpye=item.text()
        # print(listwidget_selected_chiptpye)
        row_item=self.listWidget.row(item)
        print(self.listWidget.row(item))
        # 将主数据填入表中
        for i in range(self.chipdata_array.shape[1]):
            item_table = QTableWidgetItem(str(self.chipdata_array[row_item][i]))
            item_table.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(0, i, item_table)  # 需要转化为字符串


if __name__ == '__main__':
    app=QApplication(sys.argv)
    # 先QMainWindow实例化是因为Qtdesigner的类没有继承QMainWindow,单里边的方法还用到了mainwindown
    # mainwindow=QMainWindow()
    # mainUI=MainWindow.Ui_MainWindow()
    # mainUI.setupUi(mainwindow)
    mainwindow=newUI()
    mainwindow.show()
    sys.exit(app.exec())



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
