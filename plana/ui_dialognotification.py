# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialognotification.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QSizePolicy, QWidget)

class Ui_DialogNotification(object):
    def setupUi(self, DialogNotification):
        if not DialogNotification.objectName():
            DialogNotification.setObjectName(u"DialogNotification")
        DialogNotification.resize(400, 300)
        self.buttonBox = QDialogButtonBox(DialogNotification)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.retranslateUi(DialogNotification)
        self.buttonBox.accepted.connect(DialogNotification.accept)
        self.buttonBox.rejected.connect(DialogNotification.reject)

        QMetaObject.connectSlotsByName(DialogNotification)
    # setupUi

    def retranslateUi(self, DialogNotification):
        DialogNotification.setWindowTitle(QCoreApplication.translate("DialogNotification", u"Dialog", None))
    # retranslateUi

