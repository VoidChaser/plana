# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'welcome.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_WelcomeWindow(object):
    def setupUi(self, WelcomeWindow):
        if not WelcomeWindow.objectName():
            WelcomeWindow.setObjectName(u"WelcomeWindow")
        WelcomeWindow.resize(400, 200)
        self.verticalLayout = QVBoxLayout(WelcomeWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacerTop = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacerTop)

        self.labelGreeting = QLabel(WelcomeWindow)
        self.labelGreeting.setObjectName(u"labelGreeting")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.labelGreeting.setFont(font)
        self.labelGreeting.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.labelGreeting)

        self.verticalSpacerMiddle = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacerMiddle)

        self.btnAuth = QPushButton(WelcomeWindow)
        self.btnAuth.setObjectName(u"btnAuth")
        self.btnAuth.setMinimumSize(QSize(0, 40))

        self.verticalLayout.addWidget(self.btnAuth)

        self.btnSkip = QPushButton(WelcomeWindow)
        self.btnSkip.setObjectName(u"btnSkip")
        self.btnSkip.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout.addWidget(self.btnSkip)

        self.verticalSpacerBottom = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacerBottom)


        self.retranslateUi(WelcomeWindow)

        QMetaObject.connectSlotsByName(WelcomeWindow)
    # setupUi

    def retranslateUi(self, WelcomeWindow):
        WelcomeWindow.setWindowTitle(QCoreApplication.translate("WelcomeWindow", u"\u041f\u0440\u0438\u0432\u0435\u0442\u0441\u0442\u0432\u0438\u0435", None))
        self.labelGreeting.setText(QCoreApplication.translate("WelcomeWindow", u"\u041f\u0440\u0438\u0432\u0435\u0442, \u044d\u0442\u043e \u043f\u043b\u0430\u043d\u0435\u0440", None))
        self.btnAuth.setText(QCoreApplication.translate("WelcomeWindow", u"\u0410\u0432\u0442\u043e\u0440\u0438\u0437\u043e\u0432\u0430\u0442\u044c\u0441\u044f \u0447\u0435\u0440\u0435\u0437 Telegram", None))
        self.btnSkip.setText(QCoreApplication.translate("WelcomeWindow", u"\u041f\u0440\u043e\u043f\u0443\u0441\u0442\u0438\u0442\u044c \u0430\u0432\u0442\u043e\u0440\u0438\u0437\u0430\u0446\u0438\u044e", None))
    # retranslateUi

