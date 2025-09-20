# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_configurate.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_DialogPeriod(object):
    def setupUi(self, DialogPeriod):
        if not DialogPeriod.objectName():
            DialogPeriod.setObjectName(u"DialogPeriod")
        DialogPeriod.resize(398, 280)
        self.verticalLayoutPeriod = QVBoxLayout(DialogPeriod)
        self.verticalLayoutPeriod.setObjectName(u"verticalLayoutPeriod")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.NameHeadLabel = QLabel(DialogPeriod)
        self.NameHeadLabel.setObjectName(u"NameHeadLabel")

        self.horizontalLayout.addWidget(self.NameHeadLabel)

        self.NameLabel = QLabel(DialogPeriod)
        self.NameLabel.setObjectName(u"NameLabel")

        self.horizontalLayout.addWidget(self.NameLabel)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.BeginHeadLabel = QLabel(DialogPeriod)
        self.BeginHeadLabel.setObjectName(u"BeginHeadLabel")

        self.horizontalLayout_2.addWidget(self.BeginHeadLabel)

        self.BeginDateLabel = QLabel(DialogPeriod)
        self.BeginDateLabel.setObjectName(u"BeginDateLabel")

        self.horizontalLayout_2.addWidget(self.BeginDateLabel)

        self.BeginTimeLabel = QLabel(DialogPeriod)
        self.BeginTimeLabel.setObjectName(u"BeginTimeLabel")

        self.horizontalLayout_2.addWidget(self.BeginTimeLabel)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.DeadlineHeadLabel = QLabel(DialogPeriod)
        self.DeadlineHeadLabel.setObjectName(u"DeadlineHeadLabel")

        self.horizontalLayout_3.addWidget(self.DeadlineHeadLabel)

        self.DeadlineDateLabel = QLabel(DialogPeriod)
        self.DeadlineDateLabel.setObjectName(u"DeadlineDateLabel")

        self.horizontalLayout_3.addWidget(self.DeadlineDateLabel)

        self.DeadlineTimeLabel = QLabel(DialogPeriod)
        self.DeadlineTimeLabel.setObjectName(u"DeadlineTimeLabel")

        self.horizontalLayout_3.addWidget(self.DeadlineTimeLabel)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.DifferenceHeadLabel = QLabel(DialogPeriod)
        self.DifferenceHeadLabel.setObjectName(u"DifferenceHeadLabel")

        self.horizontalLayout_4.addWidget(self.DifferenceHeadLabel)

        self.DifferenceLabel = QLabel(DialogPeriod)
        self.DifferenceLabel.setObjectName(u"DifferenceLabel")

        self.horizontalLayout_4.addWidget(self.DifferenceLabel)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.verticalLayoutPeriod.addLayout(self.verticalLayout)

        self.line_separator = QFrame(DialogPeriod)
        self.line_separator.setObjectName(u"line_separator")
        self.line_separator.setFrameShape(QFrame.Shape.HLine)

        self.verticalLayoutPeriod.addWidget(self.line_separator)

        self.label_reminder = QLabel(DialogPeriod)
        self.label_reminder.setObjectName(u"label_reminder")
        self.label_reminder.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayoutPeriod.addWidget(self.label_reminder)

        self.dynamicFieldsLayout = QVBoxLayout()
        self.dynamicFieldsLayout.setObjectName(u"dynamicFieldsLayout")

        self.verticalLayoutPeriod.addLayout(self.dynamicFieldsLayout)

        self.tgAuthLayout = QHBoxLayout()
        self.tgAuthLayout.setObjectName(u"tgAuthLayout")
        self.checkbox_tg = QCheckBox(DialogPeriod)
        self.checkbox_tg.setObjectName(u"checkbox_tg")
        self.checkbox_tg.setEnabled(False)

        self.tgAuthLayout.addWidget(self.checkbox_tg)

        self.label_auth = QLabel(DialogPeriod)
        self.label_auth.setObjectName(u"label_auth")

        self.tgAuthLayout.addWidget(self.label_auth)

        self.btn_auth = QPushButton(DialogPeriod)
        self.btn_auth.setObjectName(u"btn_auth")
        self.btn_auth.setFlat(True)

        self.tgAuthLayout.addWidget(self.btn_auth)


        self.verticalLayoutPeriod.addLayout(self.tgAuthLayout)

        self.btn_confirm = QPushButton(DialogPeriod)
        self.btn_confirm.setObjectName(u"btn_confirm")

        self.verticalLayoutPeriod.addWidget(self.btn_confirm)


        self.retranslateUi(DialogPeriod)

        QMetaObject.connectSlotsByName(DialogPeriod)
    # setupUi

    def retranslateUi(self, DialogPeriod):
        DialogPeriod.setWindowTitle(QCoreApplication.translate("DialogPeriod", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430 \u043f\u0435\u0440\u0438\u043e\u0434\u0430", None))
        self.NameHeadLabel.setText(QCoreApplication.translate("DialogPeriod", u"\u0418\u043c\u044f:", None))
        self.NameLabel.setText("")
        self.BeginHeadLabel.setText(QCoreApplication.translate("DialogPeriod", u"\u0414\u0430\u0442\u0430 \u0441\u0442\u0430\u0440\u0442\u0430:", None))
        self.BeginDateLabel.setText("")
        self.BeginTimeLabel.setText("")
        self.DeadlineHeadLabel.setText(QCoreApplication.translate("DialogPeriod", u"\u0414\u0430\u0442\u0430 \u0434\u0435\u0434\u043b\u0430\u0439\u043d\u0430:", None))
        self.DeadlineDateLabel.setText("")
        self.DeadlineTimeLabel.setText("")
        self.DifferenceHeadLabel.setText(QCoreApplication.translate("DialogPeriod", u"\u0420\u0430\u0437\u043d\u0438\u0446\u0430:", None))
        self.DifferenceLabel.setText("")
        self.label_reminder.setText(QCoreApplication.translate("DialogPeriod", u"\u041d\u0430\u043f\u043e\u043c\u0438\u043d\u0430\u043d\u0438\u0435", None))
        self.checkbox_tg.setText(QCoreApplication.translate("DialogPeriod", u"\u041e\u0442\u043f\u0440\u0430\u0432\u043b\u044f\u0442\u044c \u0432 tg bot", None))
        self.label_auth.setStyleSheet(QCoreApplication.translate("DialogPeriod", u"color: red;", None))
        self.label_auth.setText(QCoreApplication.translate("DialogPeriod", u"\u0410\u0432\u0442\u043e\u0440\u0438\u0437\u0430\u0446\u0438\u044f: \u041d\u0435 \u043f\u0440\u043e\u0439\u0434\u0435\u043d\u0430", None))
        self.btn_auth.setStyleSheet(QCoreApplication.translate("DialogPeriod", u"text-decoration: underline; color: blue; background: none; border: none;", None))
        self.btn_auth.setText(QCoreApplication.translate("DialogPeriod", u"\u0410\u0432\u0442\u043e\u0440\u0438\u0437\u043e\u0432\u0430\u0442\u044c\u0441\u044f", None))
        self.btn_confirm.setText(QCoreApplication.translate("DialogPeriod", u"\u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435", None))
    # retranslateUi

