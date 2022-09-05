#coding: utf8

import os
import sys
from collections import defaultdict
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import QEvent
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QMessageBox, QTreeWidgetItem
from PyQt5.QtCore import QStringListModel, QPoint
from ui import Ui_Form
from core import get_keywords

class Main(QMainWindow, Ui_Form):
    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.initModels()
        self.bindActions()

    def initModels(self):

        self.listModel = QStringListModel()
        self.listModel.setObjectName("目录树")
        self.treeView.setModel(self.listModel)

        # 打开时选择题库路径
        self.workspace = QFileDialog.getExistingDirectory(self, "选取题库根目录", "~")
        if not os.path.isdir(self.workspace):
            QMessageBox.warning(self, "FBI WARNING", "非法的目录")
            return

        self.formated_dict = self._format_filenames(self.workspace)
        self.treeList = list(self.formated_dict.keys())
        self.listModel.setStringList(self.treeList)


    def bindActions(self):
        self.treeView.doubleClicked.connect(self._treeViewDoubleClicked)
        self.treeView.clicked.connect(self._treeViewClicked)

    def _treeViewDoubleClicked(self, item):
        self._treeViewClicked(item)

    def _treeViewClicked(self, item):
        print(item.row())
        idx = item.row()
        name = self.treeList[idx]
        filename = self.formated_dict[name]
        with open(filename, 'r') as f:
            fulltext = '\n'.join(f.readlines())
            f.close()

        # 尾部追加关键词
        fulltext = self._append_keywords(fulltext)
        self.textBrowser.setMarkdown(fulltext)

    def _append_keywords(self, fulltext):
        keywords = get_keywords(fulltext)
        tail = """
---
关键词：\n"""
        tail += "; ".join([str("**"+keyword+"**") for keyword in keywords]) + "\n"
        return fulltext + "\n" + tail

    def _format_filenames(self, dir):
        dict = defaultdict()
        ls = []
        _, files = get_all_files(dir, [], ls)
        for filename in files:
            # 去除左侧 root 的路径，美化列表展示 name => fullpath
            name = str(filename).lstrip(self.workspace)
            dict[name] = filename
        return dict



def get_all_files(path, dirlist=[], filelist=[]):
    flist = os.listdir(path)
    for filename in flist:
        subpath = os.path.join(path, filename)
        if os.path.isdir(subpath):
            dirlist.append(subpath)		# 如果是文件夹，添加到文件夹列表中
            get_all_files(subpath, dirlist, filelist)	# 向子文件内递归
        if os.path.isfile(subpath):
            filelist.append(subpath)	# 如果是文件，添加到文件列表中
    return dirlist, filelist

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Main()
    win.setWindowTitle("中特助手")
    win.show()
    sys.exit(app.exec_())

