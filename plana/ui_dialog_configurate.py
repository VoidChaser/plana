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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpinBox, QVBoxLayout, QWidget)

class Ui_DialogPeriod(object):
    def setupUi(self, DialogPeriod):
        if not DialogPeriod.objectName():
            DialogPeriod.setObjectName(u"DialogPeriod")
        DialogPeriod.resize(398, 258)
        self.verticalLayoutPeriod = QVBoxLayout(DialogPeriod)
        self.verticalLayoutPeriod.setObjectName(u"verticalLayoutPeriod")
        self.label_name = QLabel(DialogPeriod)
        self.label_name.setObjectName(u"label_name")

        self.verticalLayoutPeriod.addWidget(self.label_name)

        self.label_start = QLabel(DialogPeriod)
        self.label_start.setObjectName(u"label_start")

        self.verticalLayoutPeriod.addWidget(self.label_start)

        self.label_deadline = QLabel(DialogPeriod)
        self.label_deadline.setObjectName(u"label_deadline")

        self.verticalLayoutPeriod.addWidget(self.label_deadline)

        self.label_diff = QLabel(DialogPeriod)
        self.label_diff.setObjectName(u"label_diff")

        self.verticalLayoutPeriod.addWidget(self.label_diff)

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
        self.fieldExample = QHBoxLayout()
        self.fieldExample.setObjectName(u"fieldExample")
        self.combo_period = QComboBox(DialogPeriod)
        self.combo_period.addItem("")
        self.combo_period.addItem("")
        self.combo_period.addItem("")
        self.combo_period.addItem("")
        self.combo_period.setObjectName(u"combo_period")

        self.fieldExample.addWidget(self.combo_period)

        self.spin_value = QSpinBox(DialogPeriod)
        self.spin_value.setObjectName(u"spin_value")

        self.fieldExample.addWidget(self.spin_value)


        self.dynamicFieldsLayout.addLayout(self.fieldExample)

        self.btn_add_field = QPushButton(DialogPeriod)
        self.btn_add_field.setObjectName(u"btn_add_field")

        self.dynamicFieldsLayout.addWidget(self.btn_add_field)


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
        self.label_name.setText(QCoreApplication.translate("DialogPeriod", u"\u0418\u043c\u044f: [ ]", None))
        self.label_start.setText(QCoreApplication.translate("DialogPeriod", u"\u0414\u0430\u0442\u0430 \u0441\u0442\u0430\u0440\u0442\u0430: [ ]", None))
        self.label_deadline.setText(QCoreApplication.translate("DialogPeriod", u"\u0414\u0430\u0442\u0430 \u0434\u0435\u0434\u043b\u0430\u0439\u043d\u0430: [ ]", None))
        self.label_diff.setText(QCoreApplication.translate("DialogPeriod", u"\u0420\u0430\u0437\u043d\u0438\u0446\u0430: 0 \u0434\u043d\u0435\u0439 0 \u0447\u0430\u0441\u043e\u0432 0 \u043c\u0438\u043d\u0443\u0442", None))
        self.label_reminder.setText(QCoreApplication.translate("DialogPeriod", u"\u041d\u0430\u043f\u043e\u043c\u0438\u043d\u0430\u043d\u0438\u0435", None))
        self.combo_period.setItemText(0, QCoreApplication.translate("DialogPeriod", u"\u0413\u043e\u0434", None))
        self.combo_period.setItemText(1, QCoreApplication.translate("DialogPeriod", u"\u041c\u0435\u0441\u044f\u0446", None))
        self.combo_period.setItemText(2, QCoreApplication.translate("DialogPeriod", u"\u0414\u0435\u043d\u044c", None))
        self.combo_period.setItemText(3, QCoreApplication.translate("DialogPeriod", u"\u041c\u0438\u043d\u0443\u0442\u0430", None))

        self.btn_add_field.setText(QCoreApplication.translate("DialogPeriod", u"+", None))
        self.checkbox_tg.setText(QCoreApplication.translate("DialogPeriod", u"\u041e\u0442\u043f\u0440\u0430\u0432\u043b\u044f\u0442\u044c \u0432 tg bot", None))
        self.label_auth.setStyleSheet(QCoreApplication.translate("DialogPeriod", u"color: red;", None))
        self.label_auth.setText(QCoreApplication.translate("DialogPeriod", u"\u0410\u0432\u0442\u043e\u0440\u0438\u0437\u0430\u0446\u0438\u044f: \u041d\u0435 \u043f\u0440\u043e\u0439\u0434\u0435\u043d\u0430", None))
        self.btn_auth.setStyleSheet(QCoreApplication.translate("DialogPeriod", u"text-decoration: underline; color: blue; background: none; border: none;", None))
        self.btn_auth.setText(QCoreApplication.translate("DialogPeriod", u"\u0410\u0432\u0442\u043e\u0440\u0438\u0437\u043e\u0432\u0430\u0442\u044c\u0441\u044f", None))
        self.btn_confirm.setText(QCoreApplication.translate("DialogPeriod", u"\u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435", None))
    # retranslateUi

