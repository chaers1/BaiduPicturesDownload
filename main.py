"""软件运行窗口界面，需要用到pyqt5的属性和创建的窗口这两中方法"""
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QUrl, QTextStream
from Image_capture import Core
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from baiduchengxu import Ui_mainWindow  # 这是一个一键生成的gui的类


class worker(QThread):
    signal = pyqtSignal(str)

    def __init__(self, name, sdtas, sdta, drive_letter, names, parent=None):
        super(worker, self).__init__(parent)
        self.core = Core(name, sdtas, sdta, drive_letter, names)

    def __del__(self):
        self.wait()

    def run(self):
        restlt = self.core.tian_pian()
        self.signal.emit(restlt)


class Mainwindow(QMainWindow):  # 继承的类QMainWindow是一个继承的窗口类，第二个就是设计窗口的类
    def __init__(self):
        # 初始化构造函数
        super().__init__()

        # 导入创建好的界面类并创建实例
        self.ui = Ui_mainWindow()

        # 构造出设计好的显示屏
        self.ui.setupUi(self)

        # 设置窗口固定大小
        self.setFixedSize(self.width(), self.height())

        # 创建图片爬取模块实例
        self.co = Core()

        # 程序运行结果展示设置
        self.yunxing = self.ui.xiazaixinxizhanshi
        self.yunxing.setReadOnly(True)
        # 新线程
        self.mythread = None
        # 设置图片搜索栏
        self.ui.tupiansousuo.setPlaceholderText('请输入关键词.....')  # 对于pyqt组件的设定最好放在构造函数内，不然不会显示
        self.ui.cipan.setToolTip("请输入想要存储文件到本地的磁盘位置\n"
                                 "例如：'D'E'F'请根据个人电脑的情况进行输入")
        self.ui.cipan.setPlaceholderText("输入本地磁盘..")
        self.ui.wenjianming.setToolTip("创建图片的保存本地的文件名\n"
                                       "也可以与关键词保持一致")
        self.ui.wenjianming.setPlaceholderText("创建文件名......")
        self.ui.xiazaixinxizhanshi.setPlaceholderText("下载信息展示\n"
                                                      "运行后请等待下载结果........")

        # 程序超链接设置
        self.lianjie1 = self.ui.lianjie_1
        self.lianjie2 = self.ui.lianjie_2
        self.lianjie3 = self.ui.lianjie_3
        self.lianjie1.setOpenExternalLinks(True)
        self.lianjie2.setOpenExternalLinks(True)
        self.lianjie3.setOpenExternalLinks(True)
        # 运行槽函数
        self.ui.baiduyixia.clicked.connect(self.functions)

    # 设定用户输入槽函数和槽函数对应的组件
    def functions(self):
        self.ui.baiduyixia.setText("请等待....")  # 点击后显示下载中请等待
        self.ui.baiduyixia.setEnabled(True)  # 用户使用时必须等待上一次操作完成才可以操作
        self.co.name = self.ui.tupiansousuo.toPlainText()  # 获取关键词文本
        if self.co.name == "":
            QMessageBox.warning(self, '错误', '信息不能为空')
            return self.ui.baiduyixia.setText("百度一下")

        self.co.sdtas = int(self.ui.kaishi.text())  # 获取下载起始页
        if self.co.sdtas < 1:
            QMessageBox.warning(self, "提示", "起始页需要大于0从1开始")  # 对起始页进行判断，如果起始页小于零就弹出提示
            return self.ui.baiduyixia.setText("百度一下")

        self.co.sdta = int(self.ui.zhongzhi.text())  # 获取终止页数
        if self.co.sdta < self.co.sdtas:
            QMessageBox.warning(self, "提示", "网站的每一页图片为30张，所以终止页数一定要大于起始页数")  # 对终止页进行判断，小于起始页就会弹出提示
            return self.ui.baiduyixia.setText("百度一下")

        self.co.drive_letter = self.ui.cipan.toPlainText()  # 获取磁盘存储文本信息
        self.co.names = self.ui.wenjianming.toPlainText()  # 获取本地文件名
        QMessageBox.information(self, "信息确认",
                                f"      您输入的信息是\n"
                                f"类型：{self.co.name}\n"
                                f"页数{self.co.sdta - self.co.sdtas}\n"
                                f"存储磁盘{self.co.drive_letter}\n"
                                f"子文件名：{self.co.names}")  # 对用户的输入信息进行最后的确认
        self.mythread = worker(self.co.name, self.co.sdtas, self.co.sdta, self.co.drive_letter,
                               self.co.names)  # 向新线程中传递参数
        self.mythread.signal.connect(self.update_text_edit)
        self.mythread.start()  # 启动新线程

    def update_text_edit(self):
        sys.stdout = QTextStream(self.yunxing.document())
        sys.stdout.setCodec("utf-8")
        sys.stdout.setFieldAlignment(QTextStream.AlignRight)


    # pyqt中超链接链接信号槽的设定
    def lianjie(self):
        QDesktopServices.openUrl(QUrl(self.lianjie1))
        QDesktopServices.openUrl(QUrl(self.lianjie2))
        QDesktopServices.openUrl(QUrl(self.lianjie3))


if __name__ == "__main__":
    try:
        app = QApplication([])  # 创建一个应用实例
        app.setWindowIcon(QtGui.QIcon("bearwn.webp"))  # 程序图标
        window = Mainwindow()  # 创建窗口实例
        window.show()  # 运行程序
        app.exec_()  # 对程序进行监听
    except Exception as e:
        print(e)
# if __name__ == "__main__":
#     app = QApplication([])  # 创建一个应用实例
#     app.setWindowIcon(QtGui.QIcon("bearwn.webp"))  # 程序图标
#     window = Mainwindow()  # 创建窗口实例
#     window.show()  # 运行程序
#     app.exec_()  # 对程序进行监听

