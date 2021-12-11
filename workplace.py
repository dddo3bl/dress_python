# from _typeshed import NoneType
from logging import NullHandler
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from PyQt5.uic import loadUiType
from os import path
import mysql.connector
import qdarkstyle
import calendar


FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__) , "workplace.ui"))

class Main(QMainWindow , FORM_CLASS):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUI()
        self.Handel_DB_connection()
        self.Handel_butons()
        self.handel_combo_box()


    

    def handel_combo_box(self):
        month = [1,2,3,4,5,6,7,8,9,10,11,12]
        for i in month:
            self.month.addItem(str(i))


    def InitUI(self):
        self.setWindowTitle("المعمل")


# connect to database 
    def Handel_DB_connection(self):
        self.db = mysql.connector.connect(
        host = 'mysql-52374-0.cloudclusters.net',
        user = 'do3bl',
        passwd = '123456789',
        database = 'dress',
        port = '16397'
        )
        self.cur = self.db.cursor()
        print('connection done')

    def handel_combo_box(self):
        self.cur.execute(''' SELECT * FROM employees WHERE dept_id = 2''')
        worker = self.cur.fetchall()
        print(worker)
        for row in worker:
            self.worker.addItem(str(row[0]) + " - " + row[1])
# to handel all butons when clicked in the system
# and eche butons has a method activat when clicked on the buton
    def Handel_butons(self):
        self.refresh.clicked.connect(self.show_clint)
        self.refresh_2.clicked.connect(self.non_taked)
        self.acciptwork.clicked.connect(self.show_worker)
        self.showmontbtn.clicked.connect(self.showmonthreport)


    def show_worker(self):
        work_data = str(self.worker.currentText()[:2])
        workplacenum = self.workplacenum.text()
        self.cur.execute(''' UPDATE workplace SET takeed = 1, worker_id = %s where workplace_id = %s ''',(work_data,workplacenum))
        self.db.commit()
        
        

    def non_taked(self):
        self.tableWidget.setRowCount(0);
        self.cur.execute(''' SELECT workplace.workplace_id, clintsize.clint_id, clintsize.clint_name, clintsize.hight, clintsize.chist_whdth, clintsize.bttn, clintsize.lower_part, clintsize.cholder, clintsize.hand_length, clintsize.hand_whdth, clintsize.muscle, clintsize.nick, fabrics.fabric_name, fabrics.fabric_id, workplace.date_order, workplace.metr_num, dress_type.dress_id from workplace, clintsize, fabrics, dress_type,clint_order WHERE workplace.clintid = clintsize.clint_id AND workplace.fabric_id = fabrics.fabric_id AND workplace.dress_id = dress_type.dress_id AND workplace.order_clint = clint_order.clint_orderid AND workplace.takeed = 0 AND clint_order.is_bayed = 1''')
        result = self.cur.fetchall()
        print(result)
        for row, form in enumerate(result):
            for column, item in enumerate(form):
                self.tableWidget.setItem(row,column,QTableWidgetItem(str(item)))
                column += 1
            row_postion = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_postion)

    def show_clint(self):
        clint_id = self.clint_id.text()
        self.tableWidget_2.setRowCount(0)
        if clint_id == "":
            QMessageBox.warning(
                self, 'erorr', 'ادخل رقم العميل', QMessageBox.Yes)
        else:
            self.cur.execute(''' SELECT workplace.workplace_id, workplace.clintid ,workplace.order_clint, workplace.date_order, workplace.takeed from workplace WHERE workplace.order_clint = %s''',[clint_id])
            result = self.cur.fetchall()
            if len(result) == 0:
                QMessageBox.warning(
                self, 'erorr', 'لا يوجد سجلات للعميل  ', QMessageBox.Yes)
            else :
                for row, form in enumerate(result):
                    for column, item in enumerate(form):
                        self.tableWidget_2.setItem(row,column,QTableWidgetItem(str(item)))
                        column += 1
                    row_postion = self.tableWidget_2.rowCount()
                    self.tableWidget_2.insertRow(row_postion)
                self.tableWidget_2.removeRow(row-1)


    def showmonthreport(self):
        index = self.month.currentText()
        mydate = calendar.month_name[int(index)]
        self.cur.execute(''' select workplace.workplace_id, workplace.clintid, clintsize.clint_name, workplace.fabric_id, workplace.date_order, workplace.worker_id ,employees.employee_name, clint_order.bayed from workplace,clintsize,employees,clint_order where workplace.clintid = clintsize.clint_id and workplace.worker_id = employees.employee_id AND workplace.order_clint = clint_order.clint_orderid AND monthname(date_order) = %s AND takeed = 1''',[mydate])
        result = self.cur.fetchall()
        if len(result) == 0:
            QMessageBox.warning(
                self, 'erorr', 'لا يوجد سجلات لهذا الشهر  ', QMessageBox.Yes)
        else:
            self.tableWidget_3.insertRow(0)
            for row, form in enumerate(result):
                for column, item in enumerate(form):
                    self.tableWidget_3.setItem(row,column,QTableWidgetItem(str(item)))
                    column += 1
                row_postion = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_postion)
            self.tableWidget_3.removeRow(row-1)
            
            



def main():
    app = QApplication(sys.argv)
    window = Main()

    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window.show()
    app.exec_()

if __name__=='__main__':
    main()

