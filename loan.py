####################################
#      贷款利率计算 练习
#      作者   最爱点灯的星星
#      Ver1.0
#      目前没有加入异常处理，只能实现等额本息
######################################

import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets

uiFile = "loan.ui"
Ui_MyMainWindow, QtBaseClass = uic.loadUiType(uiFile)


class MyApp(QtWidgets.QMainWindow, Ui_MyMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MyMainWindow.__init__(self)
        self.setupUi(self)
        self.butt_calc.clicked.connect(self.loan_Compute)

    def loan_Compute(self):
        self.outlist.clear()

        loan_Num = int(self.loannum.text())  #借款总金额
        Annual_interest_rate = (self.rate.value())/100  #年化利率 不用输%号
        stage = self.period.value()      #借款期数 (按月为单位！)

        for ii in range(1,stage + 1):
            if(ii == 1):
                monthly_all = loan_Num * (Annual_interest_rate / 12) * pow((1 + (Annual_interest_rate / 12)), stage) / (
                            pow((1 + (Annual_interest_rate / 12)), stage) - 1) # 月均还款(本金+利息)
                repay_rate_all = stage * loan_Num * (Annual_interest_rate / 12) * pow((1 + (Annual_interest_rate / 12)),
                                 stage) / (pow((1 + (Annual_interest_rate / 12)), stage) - 1) - loan_Num # 还款利息总和
                repay_rate_1 = loan_Num * (Annual_interest_rate / 12) # 还款利息
                surplus_rate = repay_rate_all - repay_rate_1  # 剩余利息
                surplus_loan_num = loan_Num - (monthly_all - repay_rate_1) # 剩余本金
                outstr = "1: 利息 %.3f  本金 %.3f 还款总额（本金+利息） %.3f " % ( repay_rate_1, monthly_all - repay_rate_1, monthly_all)
            else:
                repay_rate_n_1 = (loan_Num * (Annual_interest_rate/12) - monthly_all)*pow((1 + (Annual_interest_rate/12)),(ii - 1)) + monthly_all
                surplus_loan_num = monthly_all - repay_rate_n_1
                outstr = "{} : 利息 {} 本金 {} 还款总额（本金+利息）{}".format(ii, repay_rate_n_1, surplus_loan_num, monthly_all)

            self.outlist.addItem(outstr)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Main_window = MyApp()
    Main_window.show()
    sys.exit(app.exec_())