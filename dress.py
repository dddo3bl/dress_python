from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from PyQt5.uic import loadUiType
import os
from os import path
import mysql.connector
import time
import qdarkstyle


FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "dress.ui"))
FORM_CLASS2, _ = loadUiType(path.join(path.dirname(__file__), "login.ui"))


class Login(QMainWindow, FORM_CLASS2):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.login.clicked.connect(self.hundal_login)
        self.window2 = None

    def hundal_login(self):
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='',
            database='dress',

        )
        self.cur = self.db.cursor()

        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        # sql = ''' SELECT * FROM users '''
        self.cur.execute(''' SELECT * FROM users ''')
        data = self.cur.fetchall()
        for row in data:
            if row[1] == username and row[2] == int(password):
                self.window2 = Main()
                self.close()
                self.window2.show()
            else:
                self.label.setText("يرجى التأكد من اسم المستخدم وكلمة المرور")


class Main(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUI()
        self.Handel_DB_connection()
        self.Handel_butons()
        self.handel_combo_box()

    def handel_combo_box(self):
        self.cur.execute(''' SELECT * FROM dress_type ''')
        data1 = self.cur.fetchall()
        for row in data1:
            self.dress_type.addItem(str(row[0]) + ' - ' + row[1])

        

    def InitUI(self):
        # changes in the run time
        # print("done")
        self.setWindowTitle("الرجل الانيق للثياب")
        self.tabWidget.tabBar().setVisible(False)

# connect to database
    def Handel_DB_connection(self):
        self.db = mysql.connector.connect(
            host='mysql-52374-0.cloudclusters.net',
            user='do3bl',
            passwd='123456789',
            database='dress',
            port = '16397'
        )
        self.cur = self.db.cursor()
        print('connection done')

# to handel all butons when clicked in the system
# and eche butons has a method activat when clicked on the buton
    def Handel_butons(self):
        self.save_newclint.clicked.connect(self.new_clint)
        self.pushButton_3.clicked.connect(self.order_newdress)
        self.search_clint.clicked.connect(self.search_for_clint)
        self.order_new_drees.clicked.connect(self.order_newdress)
        self.price_of_clint.clicked.connect(self.show_total)
        self.update_clint_size.clicked.connect(self.update_sizes)
        self.add_new_fabric.clicked.connect(self.add_fabric)
        self.updata_existing_fabric.clicked.connect(self.update_fabric)
        self.add_user.clicked.connect(self.create_user)
        self.modfiy_user.clicked.connect(self.update_user)

# to show all failds when search
    def search_for_clint(self):
        # when search abdut some clint and don't know if he exist
        if self.listWidget.row(self.listWidget.currentItem()) == 0:
            sql = '''  SELECT * FROM clintsize WHERE clint_id = %s  '''
            clint_number = self.lineEdit.text()
            self.cur.execute(sql, [(clint_number)])
            data = self.cur.fetchone()

            self.lineEdit_3.setText(data[1])
            self.lineEdit_4.setText(str(data[2]))
            self.lineEdit_5.setText(str(data[3]))
            self.lineEdit_6.setText(str(data[6]))
            self.lineEdit_7.setText(str(data[4]))
            self.lineEdit_8.setText(str(data[9]))
            self.lineEdit_9.setText(str(data[5]))
            self.lineEdit_10.setText(str(data[10]))
            self.lineEdit_11.setText(str(data[8]))
            self.lineEdit_12.setText(str(data[11]))
            self.lineEdit_13.setText(str(data[7]))
    # if the clint is alrady exist
        if self.listWidget.row(self.listWidget.currentItem()) == 1:
            sql = '''  SELECT * FROM clintsize WHERE clint_id = %s  '''
            clint_number = self.lineEdit.text()
            self.cur.execute(sql, [(clint_number)])
            data = self.cur.fetchall()

            for row in data:
                self.lineEdit_14.setText(str(row[0]))
                self.lineEdit_15.setText(row[1])
                self.lineEdit_16.setText(str(row[2]))
                self.lineEdit_17.setText(str(row[3]))
                self.lineEdit_18.setText(str(row[6]))
                self.lineEdit_19.setText(str(row[4]))
                self.lineEdit_20.setText(str(row[9]))
                self.lineEdit_21.setText(str(row[5]))
                self.lineEdit_22.setText(str(row[10]))
                self.lineEdit_23.setText(str(row[8]))
                self.lineEdit_24.setText(str(row[11]))
                self.lineEdit_25.setText(str(row[7]))

        if self.listWidget.row(self.listWidget.currentItem()) == 2:
            sql = ''' SELECT * FROM fabrics WHERE fabric_id = %s'''
            fabric_id = self.lineEdit.text()
            self.cur.execute(sql, [(fabric_id)])
            data = self.cur.fetchone()
            self.lineEdit_28.setText(str(data[0]))
            self.lineEdit_29.setText(str(data[4]))
            self.lineEdit_30.setText(data[1])
            self.lineEdit_31.setText(str(data[5]))
            self.lineEdit_32.setText(str(data[2]))
            self.lineEdit_33.setText(str(data[6]))
            self.lineEdit_34.setText(str(data[3]))
            self.lineEdit_35.setText(data[7])
            self.lineEdit_36.setText(str(data[8]))
            self.lineEdit_37.setText(str(data[9]))

    def order_newdress(self):

        sql = '''  SELECT * FROM clintsize WHERE clint_id = %s  '''
        clint_number = self.lineEdit.text()
        self.cur.execute(sql, [(clint_number)])
        data = self.cur.fetchall()

        metr = 0
        clint_id = self.lineEdit_14.text()
        clint_name = self.lineEdit_15.text()
        clinr_phone = self.lineEdit_16.text()
        hight = self.lineEdit_17.text()
        chist_hight = self.lineEdit_18.text()
        bttn = self.lineEdit_19.text()
        under = self.lineEdit_20.text()
        cholder = self.lineEdit_21.text()
        hand_lengt = self.lineEdit_22.text()
        hand_hight = self.lineEdit_23.text()
        muscle = self.lineEdit_24.text()
        nick = self.lineEdit_25.text()
        bayed = self.lineEdit_27.text()
        dress_type = self.dress_type.currentIndex()
        # worker_selected = self.worker.currentIndex()
        if dress_type == 0 or clint_name == "" or clinr_phone == "" or hight == "" or chist_hight == "" or bttn == "" or under == "" or cholder == "" or hand_lengt == "" or hand_hight == "" or muscle == "" or nick == "":
            QMessageBox.warning(
                self, 'erorr', 'ادخل رقم القماش', QMessageBox.Yes)
        else:
            if float(bttn) <= 30:
                metr = float(hight) * 2
            elif float(bttn) >= 30:
                metr = float(hight) * 3

            fabric_id = self.lineEdit_26.text()
            all_fabric = ''' SELECT * FROM fabrics WHERE fabric_id = %s '''
            self.cur.execute(all_fabric, [(fabric_id)])
            fabric_data = self.cur.fetchone()

            # print(fabric_data)
            fabric_id = fabric_data[0]
            fabric_m_price = fabric_data[4]
            used_metrs = fabric_data[8]
            all_metrs = fabric_data[9]
            if used_metrs >= all_metrs/2:
                fabric_m_price = 60
            elif used_metrs >= all_metrs:
                fabric_m_price = 50
            elif used_metrs >= all_metrs/4:
                fabric_m_price = 70

            convert_sentmeter_to_meter = metr/100
            all_metrs_ubdate = convert_sentmeter_to_meter + used_metrs
            x = time.strftime('%Y-%m-%d %H:%M:%S')
            hand_made_amount = 50
            company = 50
            price = convert_sentmeter_to_meter * fabric_m_price * .17 + \
                convert_sentmeter_to_meter * fabric_m_price + hand_made_amount + company

            # to get dress information to save in database
            self.cur.execute(
                ''' SELECT * FROM dress_type WHERE dress_id = %s ''', [dress_type])
            dresss = self.cur.fetchone()
            dress_id = dresss[0]

            

            
            self.cur.execute(''' INSERT INTO clint_order 
                            (clint_name , clint_id, fabricid, total_price, bayed, dress_id, order_time) VALUES (%s, %s, %s ,%s, %s, %s, %s) ''',
                             (clint_name, clint_id, fabric_id, price, bayed, dress_id,x))
            lastrow = self.cur.lastrowid
            self.cur.execute(''' INSERT INTO  workplace 
                        (clintid,  metr_num, fabric_id, date_order, dress_id,order_clint)
                        VALUES(%s, %s, %s, %s, %s,%s) ''',
                             (clint_id, metr, fabric_id, x, dress_id, lastrow))
            self.cur.execute(
                ''' UPDATE fabrics SET used_m = %s  WHERE fabric_id = %s ''', (all_metrs_ubdate, fabric_id))
            self.db.commit()

    def show_total(self):
        metr = 0
        hight = self.lineEdit_17.text()
        bttn = self.lineEdit_19.text()
        fabric_id = self.lineEdit_26.text()
        if float(bttn) <= 30:
            metr = float(hight) * 2
        elif float(bttn) >= 30:
            metr = float(hight) * 3

        if fabric_id == "":
            QMessageBox.warning(
                self, 'erorr', 'ادخل رقم القماش', QMessageBox.Yes)
        else:
            # get price of wounted fabric
            all_fabric = ''' SELECT * FROM fabrics WHERE fabric_id = %s '''
            self.cur.execute(all_fabric, [(fabric_id)])

            fabric_data = self.cur.fetchone()
            used_metrs = fabric_data[8]  # used metrs in the data base
            all_metrs = fabric_data[9]  # all metrs in all roll
            fabric_m_price = fabric_data[4]  # price of 1 metr
            # it has been saved in sentmeter and should be saved in meter
            convert_sentmeter_to_meter = metr/100
            # after saved in meter it have to sum with fabric meter price
            price = convert_sentmeter_to_meter * fabric_m_price
            if used_metrs >= all_metrs/2:
                fabric_m_price = 50
            elif used_metrs >= all_metrs:
                fabric_m_price = 60
            elif used_metrs >= all_metrs/4:
                fabric_m_price = 70
            x = time.strftime('%Y-%m-%d %H:%M:%S')
            hand_made_amount = 50
            company = 50
            price = convert_sentmeter_to_meter * fabric_m_price * .17 + \
                convert_sentmeter_to_meter * fabric_m_price + hand_made_amount + company
            self.lcdNumber.display(price)

    def update_sizes(self):
        # to update clint size
        clintid = self.lineEdit.text()
        clinr_phone = self.lineEdit_16.text()
        hight = self.lineEdit_17.text()
        chist_hight = self.lineEdit_18.text()
        bttn = self.lineEdit_19.text()
        under = self.lineEdit_20.text()
        cholder = self.lineEdit_21.text()
        hand_lengt = self.lineEdit_22.text()
        hand_hight = self.lineEdit_23.text()
        muscle = self.lineEdit_24.text()
        nick = self.lineEdit_25.text()

        self.cur.execute(''' UPDATE clintsize SET clint_phone = %s , hight = %s , bttn = %s , cholder = %s , chist_whdth = %s , nick = %s , hand_whdth = %s , lower_part = %s , hand_length = %s , muscle = %s WHERE clint_id = %s ''',
                         (clinr_phone, hight, bttn, cholder, chist_hight, nick, hand_hight, under, hand_lengt, muscle, clintid))
        self.db.commit()
        self.statusbar.showMessage("تم تعديل البيانات بنجاح")


# for new clint


    def new_clint(self):
        clint_name = self.lineEdit_3.text()
        clint_phone = self.lineEdit_4.text()
        hight = self.lineEdit_5.text()
        chist_hight = self.lineEdit_6.text()
        bttn = self.lineEdit_7.text()
        lawer_part = self.lineEdit_8.text()
        cholder = self.lineEdit_9.text()
        hand_length = self.lineEdit_10.text()
        hand_whdth = self.lineEdit_11.text()
        muscel = self.lineEdit_12.text()
        nick = self.lineEdit_13.text()
        if clint_name == "" or hight == "" or clint_phone == "" or chist_hight == "" or bttn == "" or lawer_part == "" or cholder == "" or hand_length == "" or hand_whdth == "" or nick == "" or muscel == "":
            QMessageBox.warning(
                self, 'erorr', 'تأكد من ان كل الخانات ممتلئة', QMessageBox.Yes)
        else:
            self.cur.execute(''' INSERT INTO clintsize(clint_name, clint_phone, hight, bttn, cholder, chist_whdth, nick, hand_whdth, lower_part, hand_length, muscle) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)  ''',
                             (clint_name, clint_phone, hight, bttn, cholder, chist_hight, nick, hand_whdth, lawer_part, hand_length, muscel))
            self.db.commit()

# add new fabric
    def add_fabric(self):
        fabric_id = self.lineEdit_28.text()
        fabric_meter_price = self.lineEdit_29.text()
        fabric_name = self.lineEdit_30.text()
        fabric_roll_prise = self.lineEdit_31.text()
        fabric_roll_num = self.lineEdit_32.text()
        fabric_all_roll_price = self.lineEdit_33.text()
        fabric_metr_in_roll = self.lineEdit_34.text()
        fabric_color = self.lineEdit_35.text()
        used_meter = self.lineEdit_36.text()
        all_meter_in_all_rolls = self.lineEdit_37.text()

        if fabric_id == "" or fabric_name == "" or fabric_all_roll_price == "" or fabric_meter_price == "" or fabric_roll_prise == "" or fabric_roll_num == "" or fabric_metr_in_roll == "" or fabric_color == "" or used_meter == "" or all_meter_in_all_rolls == "":
            QMessageBox.warning(
                self, 'erorr', 'تأكد من ان كل الخانات ممتلئة', QMessageBox.Yes)
        else:
            self.cur.execute(''' INSERT INTO fabrics (fabric_name, fabric_roll, m_in_roll, price_per_m, price_per_roll, total_price_rolls, color, used_m, all_metrs, tax_amount) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 17) ''',
                             (fabric_name, fabric_roll_num, fabric_metr_in_roll, fabric_meter_price, fabric_roll_prise, fabric_all_roll_price, fabric_color, used_meter, all_meter_in_all_rolls))
            self.db.commit()
    
    def update_fabric(self):
        fabric_id = self.lineEdit_28.text()
        fabric_meter_price = self.lineEdit_29.text()
        fabric_name = self.lineEdit_30.text()
        fabric_roll_prise = self.lineEdit_31.text()
        fabric_roll_num = self.lineEdit_32.text()
        fabric_all_roll_price = self.lineEdit_33.text()
        fabric_metr_in_roll = self.lineEdit_34.text()
        fabric_color = self.lineEdit_35.text()
        used_meter = self.lineEdit_36.text()
        all_meter_in_all_rolls = self.lineEdit_37.text()
        if fabric_id == "" or fabric_name == "" or fabric_all_roll_price == "" or fabric_meter_price == "" or fabric_roll_prise == "" or fabric_roll_num == "" or fabric_metr_in_roll == "" or fabric_color == "" or used_meter == "" or all_meter_in_all_rolls == "":
            QMessageBox.warning(
                self, 'erorr', 'تأكد من ان كل الخانات ممتلئة', QMessageBox.Yes)
        else:
            self.cur.execute(''' UPDATE fabrics 
            SET fabric_name = %s , fabric_roll = %s , m_in_roll = %s , price_per_m = %s , price_per_roll = %s , total_price_rolls = %s , color = %s , used_m = %s , all_metrs = %s 
            WHERE fabric_id = %s ''', (fabric_name, fabric_roll_num, fabric_metr_in_roll, fabric_meter_price, fabric_roll_prise, fabric_all_roll_price, fabric_color, used_meter, all_meter_in_all_rolls, fabric_id))
            self.db.commit()


# create new user


    def create_user(self):
        name = self.lineEdit_44.text()
        password1 = self.lineEdit_45.text()
        password2 = self.lineEdit_46.text()
        if password1 == password2 and len(password1) > 8:
            self.cur.execute('''
            INSERT INTO users (user_name, password) VALUES (%s, %s)
            ''', (name, password1))
            self.db.commit()
            self.statusbar.showMessage("تم اضافة المستخدم بنجاح")
        else:
            QMessageBox.warning(
                self, 'erorr', 'تأكد من كلمة المرور واكثر من 8 حروف', QMessageBox.Yes)

# update user information
    def update_user(self):
        username = self.lineEdit_42.text()
        old_pass = self.lineEdit_47.text()
        new_pass1 = self.lineEdit_48.text()
        new_pass2 = self.lineEdit_49.text()

        self.cur.execute(''' 
        SELECT * FROM users WHERE user_name = %s
         ''', [username])
        data = self.cur.fetchone()

        if data[1] == username and data[2] == int(old_pass):
            if new_pass1 == new_pass2 and len(new_pass1) > 8:
                self.cur.execute(''' 
                UPDATE users SET password = %s WHERE user_name = %s AND password = %s
                 ''', (new_pass1, data[1], int(old_pass)))
                self.db.commit()
                self.statusbar.showMessage("تم تعديل كلمة سر المستخدم بنجاح")

            else:
                QMessageBox.warning(
                    self, 'erorr', 'تأكد من كلمة المرور واكثر من 8 حروف', QMessageBox.Yes)


def main():
    app = QApplication(sys.argv)
    # window = Main()
    window = Login()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
