/********************************************************************************
** Form generated from reading UI file 'colorsettings.ui'
**
** Created: Fri May 25 12:01:58 2012
**      by: Qt User Interface Compiler version 4.8.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_COLORSETTINGS_H
#define UI_COLORSETTINGS_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QGridLayout>
#include <QtGui/QHeaderView>
#include <QtGui/QLabel>
#include <QtGui/QPushButton>
#include <QtGui/QSpacerItem>
#include <QtGui/QTreeWidget>
#include <QtGui/QWidget>
#include "qtcolorbutton.h"

QT_BEGIN_NAMESPACE

class Ui_ColorSettings
{
public:
    QGridLayout *gridLayout;
    QTreeWidget *colorList;
    QLabel *label_2;
    QtColorButton *colorButton;
    QSpacerItem *horizontalSpacer;
    QPushButton *resetButton;

    void setupUi(QWidget *ColorSettings)
    {
        if (ColorSettings->objectName().isEmpty())
            ColorSettings->setObjectName(QString::fromUtf8("ColorSettings"));
        ColorSettings->resize(400, 300);
        gridLayout = new QGridLayout(ColorSettings);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        gridLayout->setContentsMargins(-1, 0, 0, 0);
        colorList = new QTreeWidget(ColorSettings);
        colorList->setObjectName(QString::fromUtf8("colorList"));

        gridLayout->addWidget(colorList, 0, 0, 1, 4);

        label_2 = new QLabel(ColorSettings);
        label_2->setObjectName(QString::fromUtf8("label_2"));

        gridLayout->addWidget(label_2, 1, 0, 1, 1);

        colorButton = new QtColorButton(ColorSettings);
        colorButton->setObjectName(QString::fromUtf8("colorButton"));
        QSizePolicy sizePolicy(QSizePolicy::Minimum, QSizePolicy::Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(colorButton->sizePolicy().hasHeightForWidth());
        colorButton->setSizePolicy(sizePolicy);

        gridLayout->addWidget(colorButton, 1, 1, 1, 1);

        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout->addItem(horizontalSpacer, 1, 2, 1, 1);

        resetButton = new QPushButton(ColorSettings);
        resetButton->setObjectName(QString::fromUtf8("resetButton"));

        gridLayout->addWidget(resetButton, 1, 3, 1, 1);


        retranslateUi(ColorSettings);

        QMetaObject::connectSlotsByName(ColorSettings);
    } // setupUi

    void retranslateUi(QWidget *ColorSettings)
    {
        QTreeWidgetItem *___qtreewidgetitem = colorList->headerItem();
        ___qtreewidgetitem->setText(2, QApplication::translate("ColorSettings", "Name", 0, QApplication::UnicodeUTF8));
        ___qtreewidgetitem->setText(1, QApplication::translate("ColorSettings", "Color", 0, QApplication::UnicodeUTF8));
        ___qtreewidgetitem->setText(0, QApplication::translate("ColorSettings", "Type", 0, QApplication::UnicodeUTF8));
        label_2->setText(QApplication::translate("ColorSettings", "Color:", 0, QApplication::UnicodeUTF8));
        colorButton->setText(QString());
        resetButton->setText(QApplication::translate("ColorSettings", "Reset", 0, QApplication::UnicodeUTF8));
        Q_UNUSED(ColorSettings);
    } // retranslateUi

};

namespace Ui {
    class ColorSettings: public Ui_ColorSettings {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_COLORSETTINGS_H
