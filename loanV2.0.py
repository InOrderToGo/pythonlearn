####################################
#      贷款利率计算（实现等额本金 等额本息）仅仅作为练习  不作为实际使用工具！
#      作者   最爱点灯的星星
#      版本   Ver2.0
#      目前没有加入异常处理
#      修改表头，增加 月还款 总利息，总利息+本金 显示
#      2018.09.10
######################################

import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QRadioButton, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem
import math
import time

# g_selectrB = 0  # 0 等额本息 1 等额本金

uiFile = "loan2.0.ui"
Ui_MyMainWindow, QtBaseClass = uic.loadUiType(uiFile)

class MyApp(QtWidgets.QMainWindow, Ui_MyMainWindow):
    # static private count
    # g_selectrB = 0  # 0 等额本息 1 等额本金  放在这loan_Compute print("=====%d" % (g_selectrB)) 失败 ？？
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MyMainWindow.__init__(self)
        self.setupUi(self)
        self.butt_calc.clicked.connect(self.loan_Compute)
        self.rB_debx.setChecked(True);
        # self.rB_debx.toggle()
        # self.rB_debx.toggled.connect(self.seledebx)
        # self.rB_debj.toggle()
        # self.rB_debj.toggled.connect(self.seledebj)
        # ls = ['期数', '利息', '本金', '还款总额（本金+利息）']
        # self.outlist.addItems(ls)
        self.initablewid()

    def initablewid(self):
        self.tW_wid.setColumnCount(6)
        # self.tW_wid.setRowCount(2)
        ls = ['期数', '期初余额', '利息', '本金', '还款总额（本金+利息）', '期末余额']
        print(ls[0])
        self.tW_wid.setHorizontalHeaderLabels(ls)
        self.tW_wid.setColumnWidth(0,80)# 列宽
        self.tW_wid.setColumnWidth(4, 150)  # 列宽
        self.tW_wid.setRowHeight(0,20)#行高
        # self.tW_wid.verticalHeader().setVisible(False)#隐藏垂直表头
        # self.tW_wid.horizontalHeader().setVisible(False)#隐藏水平表头


    # @classmethod
    def seledebx(self, value):
        pass
        # g_selectrB = 0
        # print("seledebx--------%d" % (g_selectrB))

    # @classmethod
    def seledebj(self, value):
        pass
        # g_selectrB = 1
        # print("seledebj+++++++%d" % (g_selectrB))

    # @classmethod  不能加 加了后self.outlist.clear() 不能运行
    def loan_Compute(self):
        self.outlist.clear()
        rowPosition = self.tW_wid.rowCount()
        print("total row = %d" % (rowPosition))
        for rP in range(0, rowPosition)[::-1]:
            self.tW_wid.removeRow(rP)
            print('remove %d row...' % (rP))
            # time.sleep(5)
        self.tW_wid.clearContents()

        loan_Num = int(self.loannum.text())  #借款总金额
        Annual_interest_rate = (self.rate.value())/100  #年化利率 不用输%号
        stage = self.period.value()      #借款期数 (按月为单位！)

        if self.rB_debx.isChecked():  #等额本息
            sum_rate = []  # 月利息列表
            # sum_rate_total = (stage + 1) * loan_Num * (Annual_interest_rate / 12) / 2 # 利息总和
            for ii in range(1,stage + 1):
                if(ii == 1):
                    monthly_all = loan_Num * (Annual_interest_rate / 12) * pow((1 + (Annual_interest_rate / 12)), stage) / (
                                pow((1 + (Annual_interest_rate / 12)), stage) - 1) # 月均还款(本金+利息)
                    repay_rate_all = stage * loan_Num * (Annual_interest_rate / 12) * pow((1 + (Annual_interest_rate / 12)),
                                     stage) / (pow((1 + (Annual_interest_rate / 12)), stage) - 1) - loan_Num # 还款利息总和
                    repay_rate_1 = loan_Num * (Annual_interest_rate / 12) # 还款利息
                    surplus_rate = repay_rate_all - repay_rate_1  # 剩余利息
                    surplus_loan_num = loan_Num - (monthly_all - repay_rate_1) # 剩余本金
                    sum_rate.append(repay_rate_1)
                    # outstr = "%d: 利息 %.3f  本金 %.3f 还款总额（本金+利息） %.3f " % (ii, repay_rate_1, monthly_all - repay_rate_1, monthly_all)
                    rowPosition = self.tW_wid.rowCount()
                    print("==========%d" % (rowPosition))
                    self.tW_wid.insertRow(rowPosition)
                    self.tW_wid.setItem(rowPosition, 0, QTableWidgetItem(str(ii)))
                    outstr = "%.3f" % (repay_rate_1)
                    self.tW_wid.setItem(rowPosition, 2, QTableWidgetItem(outstr))
                    outstr = "%.3f" % (monthly_all - repay_rate_1)
                    self.tW_wid.setItem(rowPosition, 3, QTableWidgetItem(outstr))
                    outstr = "%.3f" % (monthly_all)
                    self.tW_wid.setItem(rowPosition, 4, QTableWidgetItem(outstr))
                    outstr = "%.3f" % (loan_Num)   #期初
                    self.tW_wid.setItem(rowPosition, 1, QTableWidgetItem(outstr))
                    outstr = "%.3f" % (surplus_loan_num) #期末
                    self.tW_wid.setItem(rowPosition, 5, QTableWidgetItem(outstr))

                else:
                    qichu = surplus_loan_num
                    repay_rate_n_1 = (loan_Num * (Annual_interest_rate/12) - monthly_all)*pow((1 + (Annual_interest_rate/12)),(ii - 1)) + monthly_all
                    repay_loan_num = monthly_all - repay_rate_n_1
                    surplus_loan_num -= repay_loan_num
                    sum_rate.append(repay_rate_n_1)
                    # outstr = "%d: 利息 %.3f  本金 %.3f 还款总额（本金+利息） %.3f " % (ii,  repay_rate_n_1, repay_loan_num, monthly_all)
                    rowPosition = self.tW_wid.rowCount()
                    self.tW_wid.insertRow(rowPosition)
                    self.tW_wid.setItem(rowPosition, 0, QTableWidgetItem(str(ii)))
                    outstr = "%.3f" % (repay_rate_n_1)
                    self.tW_wid.setItem(rowPosition, 2, QTableWidgetItem(outstr))
                    outstr = "%.3f" % (repay_loan_num)
                    self.tW_wid.setItem(rowPosition, 3, QTableWidgetItem(outstr))
                    outstr = "%.3f" % (monthly_all)
                    self.tW_wid.setItem(rowPosition, 4, QTableWidgetItem(outstr))
                    outstr = "%.3f" % (qichu) #期初
                    self.tW_wid.setItem(rowPosition, 1, QTableWidgetItem(outstr))
                    outstr = "%.3f" % (surplus_loan_num) #期末
                    self.tW_wid.setItem(rowPosition, 5, QTableWidgetItem(outstr))

                # self.outlist.addItem(outstr)

            sum_rate_total = math.fsum(sum_rate)  #利息总和
            outstr = "利息总和 %.3f" % (sum_rate_total)  #
            self.outlist.addItem(outstr)
            sum_loan_rate = sum_rate_total + loan_Num
            outstr = "本息总计 %.3f" % (sum_loan_rate)  #
            self.outlist.addItem(outstr)

        if self.rB_debj.isChecked():  #等额本金
            sum_rate = []  # 月利息列表
            sum_rate1 = (stage + 1) * loan_Num * (Annual_interest_rate / 12) / 2 # 利息总和
            # print(sum_rate1)
            # print("总额（本金+利息）%.3f  总利息 %.3f " % (loan_Num + sum_rate1, sum_rate1))
            # 每月应还本金
            repay_loan_num = loan_Num / stage
            surplus_loan_num = loan_Num
            for jj in range(1, stage + 1):
                qichu = surplus_loan_num
                repay_rate_n_1 = (loan_Num - repay_loan_num * (jj - 1)) * (Annual_interest_rate / 12)  # 每月应还利息
                sum_rate.append(repay_rate_n_1)
                monthly_all = repay_loan_num + repay_rate_n_1
                outstr = "%d: 利息 %.3f  本金 %.3f 还款总额（本金+利息） %.3f " % (jj, repay_rate_n_1, repay_loan_num, monthly_all)
                count_sum_rate = math.fsum(sum_rate)
                # self.outlist.addItem(outstr)
                surplus_loan_num -= repay_loan_num

                rowPosition = self.tW_wid.rowCount()
                self.tW_wid.insertRow(rowPosition)
                self.tW_wid.setItem(rowPosition, 0, QTableWidgetItem(str(jj)))
                outstr = "%.3f" % (repay_rate_n_1)
                self.tW_wid.setItem(rowPosition, 2, QTableWidgetItem(outstr))
                outstr = "%.3f" % (repay_loan_num)
                self.tW_wid.setItem(rowPosition, 3, QTableWidgetItem(outstr))
                outstr = "%.3f" % (monthly_all)
                self.tW_wid.setItem(rowPosition, 4, QTableWidgetItem(outstr))
                outstr = "%.3f" % (qichu)  # 期初
                self.tW_wid.setItem(rowPosition, 1, QTableWidgetItem(outstr))
                outstr = "%.3f" % (surplus_loan_num)  # 期末
                self.tW_wid.setItem(rowPosition, 5, QTableWidgetItem(outstr))

            outstr = "利息总和(方法1) %.3f" % (count_sum_rate)  #
            self.outlist.addItem(outstr)
            outstr = "利息总和(方法2) %.3f" % (sum_rate1)  #
            self.outlist.addItem(outstr)
            sum_loan_rate = count_sum_rate + loan_Num
            outstr = "本息总计 %.3f" % (sum_loan_rate)  #
            self.outlist.addItem(outstr)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Main_window = MyApp()
    Main_window.show()
    sys.exit(app.exec_())
    print("..............................")