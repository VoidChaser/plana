# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(764, 658)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_time = QLabel(self.centralwidget)
        self.label_time.setObjectName(u"label_time")
        self.label_time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_time)

        self.table_tasks = QTableWidget(self.centralwidget)
        if (self.table_tasks.columnCount() < 8):
            self.table_tasks.setColumnCount(8)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.AppointmentNew))
        font = QFont()
        font.setFamilies([u"Sitka"])
        font.setPointSize(14)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem.setFont(font);
        __qtablewidgetitem.setIcon(icon);
        self.table_tasks.setHorizontalHeaderItem(0, __qtablewidgetitem)
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentNew))
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem1.setFont(font);
        __qtablewidgetitem1.setIcon(icon1);
        self.table_tasks.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MailMessageNew))
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem2.setFont(font);
        __qtablewidgetitem2.setIcon(icon2);
        self.table_tasks.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoPrevious))
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem3.setFont(font);
        __qtablewidgetitem3.setIcon(icon3);
        self.table_tasks.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpenRecent))
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem4.setFont(font);
        __qtablewidgetitem4.setIcon(icon4);
        self.table_tasks.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        icon5 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoNext))
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem5.setFont(font);
        __qtablewidgetitem5.setIcon(icon5);
        self.table_tasks.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem6.setFont(font);
        __qtablewidgetitem6.setIcon(icon4);
        self.table_tasks.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        icon6 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStop))
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem7.setFont(font);
        __qtablewidgetitem7.setIcon(icon6);
        self.table_tasks.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        self.table_tasks.setObjectName(u"table_tasks")
        font1 = QFont()
        font1.setFamilies([u"Sitka"])
        font1.setPointSize(12)
        self.table_tasks.setFont(font1)
        self.table_tasks.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.table_tasks.setAutoFillBackground(False)
        self.table_tasks.setAlternatingRowColors(False)
        self.table_tasks.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_tasks.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_tasks.setShowGrid(True)
        self.table_tasks.horizontalHeader().setCascadingSectionResizes(False)
        self.table_tasks.horizontalHeader().setHighlightSections(True)
        self.table_tasks.horizontalHeader().setStretchLastSection(True)
        self.table_tasks.verticalHeader().setVisible(True)
        self.table_tasks.verticalHeader().setCascadingSectionResizes(False)
        self.table_tasks.verticalHeader().setDefaultSectionSize(34)
        self.table_tasks.verticalHeader().setHighlightSections(False)
        self.table_tasks.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.table_tasks)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setObjectName(u"bottomLayout")
        self.bottomLayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.btn_settings = QPushButton(self.centralwidget)
        self.btn_settings.setObjectName(u"btn_settings")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_settings.sizePolicy().hasHeightForWidth())
        self.btn_settings.setSizePolicy(sizePolicy1)
        self.btn_settings.setMaximumSize(QSize(100, 100))

        self.bottomLayout.addWidget(self.btn_settings)

        self.btn_delete = QPushButton(self.centralwidget)
        self.btn_delete.setObjectName(u"btn_delete")
        sizePolicy1.setHeightForWidth(self.btn_delete.sizePolicy().hasHeightForWidth())
        self.btn_delete.setSizePolicy(sizePolicy1)
        self.btn_delete.setMaximumSize(QSize(100, 100))

        self.bottomLayout.addWidget(self.btn_delete)

        self.btn_add = QPushButton(self.centralwidget)
        self.btn_add.setObjectName(u"btn_add")
        sizePolicy1.setHeightForWidth(self.btn_add.sizePolicy().hasHeightForWidth())
        self.btn_add.setSizePolicy(sizePolicy1)
        self.btn_add.setMaximumSize(QSize(100, 100))

        self.bottomLayout.addWidget(self.btn_add)


        self.verticalLayout.addLayout(self.bottomLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 764, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_time.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt;\">00:00:00</span></p></body></html>", None))
        ___qtablewidgetitem = self.table_tasks.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u041d\u043e\u043c\u0435\u0440", None));
        ___qtablewidgetitem1 = self.table_tasks.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435", None));
        ___qtablewidgetitem2 = self.table_tasks.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435", None));
        ___qtablewidgetitem3 = self.table_tasks.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u0414\u0430\u0442\u0430 \u043d\u0430\u0447\u0430\u043b\u0430", None));
        ___qtablewidgetitem4 = self.table_tasks.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0440\u0435\u043c\u044f \u043d\u0430\u0447\u0430\u043b\u0430", None));
        ___qtablewidgetitem5 = self.table_tasks.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"\u0414\u0430\u0442\u0430 \u0434\u0435\u0434\u043b\u0430\u0439\u043d\u0430", None));
        ___qtablewidgetitem6 = self.table_tasks.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0440\u0435\u043c\u044f \u0434\u0435\u0434\u043b\u0430\u0439\u043d\u0430", None));
        ___qtablewidgetitem7 = self.table_tasks.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435", None));
        self.btn_settings.setText(QCoreApplication.translate("MainWindow", u"!", None))
        self.btn_delete.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.btn_add.setText(QCoreApplication.translate("MainWindow", u"+", None))
    # retranslateUi

