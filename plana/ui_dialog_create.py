# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_create.ui'
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
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QCheckBox, QDateEdit,
    QDialog, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTextEdit, QTimeEdit,
    QVBoxLayout, QWidget)

class Ui_DialogCreate(object):
    def setupUi(self, DialogCreate):
        if not DialogCreate.objectName():
            DialogCreate.setObjectName(u"DialogCreate")
        DialogCreate.resize(1025, 978)
        self.verticalLayoutDialog = QVBoxLayout(DialogCreate)
        self.verticalLayoutDialog.setObjectName(u"verticalLayoutDialog")
        self.NotificationNameLineEdit = QLineEdit(DialogCreate)
        self.NotificationNameLineEdit.setObjectName(u"NotificationNameLineEdit")

        self.verticalLayoutDialog.addWidget(self.NotificationNameLineEdit)

        self.NotificationDescriptionTextEdit = QTextEdit(DialogCreate)
        self.NotificationDescriptionTextEdit.setObjectName(u"NotificationDescriptionTextEdit")

        self.verticalLayoutDialog.addWidget(self.NotificationDescriptionTextEdit)

        self.line_exeption = QLineEdit(DialogCreate)
        self.line_exeption.setObjectName(u"line_exeption")
        self.line_exeption.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_exeption.sizePolicy().hasHeightForWidth())
        self.line_exeption.setSizePolicy(sizePolicy)
        self.line_exeption.setMaximumSize(QSize(16777215, 20))

        self.verticalLayoutDialog.addWidget(self.line_exeption)

        self.DatePickCheckBox = QCheckBox(DialogCreate)
        self.DatePickCheckBox.setObjectName(u"DatePickCheckBox")

        self.verticalLayoutDialog.addWidget(self.DatePickCheckBox)

        self.DateLayout = QVBoxLayout()
        self.DateLayout.setObjectName(u"DateLayout")
        self.BeginDateLayout = QVBoxLayout()
        self.BeginDateLayout.setObjectName(u"BeginDateLayout")
        self.BeginLabel = QLabel(DialogCreate)
        self.BeginLabel.setObjectName(u"BeginLabel")

        self.BeginDateLayout.addWidget(self.BeginLabel)

        self.BeginDateOptionsLayout = QHBoxLayout()
        self.BeginDateOptionsLayout.setObjectName(u"BeginDateOptionsLayout")
        self.BeginDateEdit = QDateEdit(DialogCreate)
        self.BeginDateEdit.setObjectName(u"BeginDateEdit")
        self.BeginDateEdit.setCalendarPopup(False)

        self.BeginDateOptionsLayout.addWidget(self.BeginDateEdit)

        self.BeginTimeEdit = QTimeEdit(DialogCreate)
        self.BeginTimeEdit.setObjectName(u"BeginTimeEdit")
        self.BeginTimeEdit.setCalendarPopup(False)

        self.BeginDateOptionsLayout.addWidget(self.BeginTimeEdit)


        self.BeginDateLayout.addLayout(self.BeginDateOptionsLayout)

        self.BeginDateCalendar = QCalendarWidget(DialogCreate)
        self.BeginDateCalendar.setObjectName(u"BeginDateCalendar")

        self.BeginDateLayout.addWidget(self.BeginDateCalendar)


        self.DateLayout.addLayout(self.BeginDateLayout)

        self.DeadlineDateLayout = QVBoxLayout()
        self.DeadlineDateLayout.setObjectName(u"DeadlineDateLayout")
        self.DeadLineLabel = QLabel(DialogCreate)
        self.DeadLineLabel.setObjectName(u"DeadLineLabel")

        self.DeadlineDateLayout.addWidget(self.DeadLineLabel)

        self.DeadlineDateOptionsLayout = QHBoxLayout()
        self.DeadlineDateOptionsLayout.setObjectName(u"DeadlineDateOptionsLayout")
        self.DeadlineDateEdit = QDateEdit(DialogCreate)
        self.DeadlineDateEdit.setObjectName(u"DeadlineDateEdit")
        self.DeadlineDateEdit.setCalendarPopup(False)

        self.DeadlineDateOptionsLayout.addWidget(self.DeadlineDateEdit)

        self.DeadlineTimeEdit = QTimeEdit(DialogCreate)
        self.DeadlineTimeEdit.setObjectName(u"DeadlineTimeEdit")
        self.DeadlineTimeEdit.setCalendarPopup(False)

        self.DeadlineDateOptionsLayout.addWidget(self.DeadlineTimeEdit)


        self.DeadlineDateLayout.addLayout(self.DeadlineDateOptionsLayout)

        self.DeadlineDateCalendar = QCalendarWidget(DialogCreate)
        self.DeadlineDateCalendar.setObjectName(u"DeadlineDateCalendar")

        self.DeadlineDateLayout.addWidget(self.DeadlineDateCalendar)


        self.DateLayout.addLayout(self.DeadlineDateLayout)


        self.verticalLayoutDialog.addLayout(self.DateLayout)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.setObjectName(u"buttonsLayout")
        self.OkCreationPushButton = QPushButton(DialogCreate)
        self.OkCreationPushButton.setObjectName(u"OkCreationPushButton")

        self.buttonsLayout.addWidget(self.OkCreationPushButton)

        self.CancelCreationPushButton = QPushButton(DialogCreate)
        self.CancelCreationPushButton.setObjectName(u"CancelCreationPushButton")

        self.buttonsLayout.addWidget(self.CancelCreationPushButton)


        self.verticalLayoutDialog.addLayout(self.buttonsLayout)


        self.retranslateUi(DialogCreate)

        QMetaObject.connectSlotsByName(DialogCreate)
    # setupUi

    def retranslateUi(self, DialogCreate):
        DialogCreate.setWindowTitle(QCoreApplication.translate("DialogCreate", u"\u0421\u043e\u0437\u0434\u0430\u043d\u0438\u0435 \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u044f", None))
        self.NotificationNameLineEdit.setPlaceholderText(QCoreApplication.translate("DialogCreate", u"\u0418\u043c\u044f \u043d\u0430\u043f\u043e\u043c\u0438\u043d\u0430\u043d\u0438\u044f", None))
        self.NotificationDescriptionTextEdit.setPlaceholderText(QCoreApplication.translate("DialogCreate", u"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435", None))
        self.DatePickCheckBox.setText(QCoreApplication.translate("DialogCreate", u"\u0423\u043a\u0430\u0437\u0430\u0442\u044c \u0432\u0440\u0435\u043c\u044f", None))
        self.BeginLabel.setText(QCoreApplication.translate("DialogCreate", u"\u0414\u0430\u0442\u0430 \u043d\u0430\u0447\u0430\u043b\u0430:", None))
        self.DeadLineLabel.setText(QCoreApplication.translate("DialogCreate", u"\u0414\u0430\u0442\u0430 \u0434\u0435\u0434\u043b\u0430\u0439\u043d\u0430:", None))
        self.OkCreationPushButton.setText(QCoreApplication.translate("DialogCreate", u"OK", None))
        self.CancelCreationPushButton.setText(QCoreApplication.translate("DialogCreate", u"X", None))
    # retranslateUi

