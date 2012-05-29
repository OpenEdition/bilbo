/********************************************************************************
** Form generated from reading UI file 'generalsettings.ui'
**
** Created: Fri May 25 12:01:58 2012
**      by: Qt User Interface Compiler version 4.8.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_GENERALSETTINGS_H
#define UI_GENERALSETTINGS_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QGridLayout>
#include <QtGui/QHeaderView>
#include <QtGui/QLabel>
#include <QtGui/QLineEdit>
#include <QtGui/QSpacerItem>
#include <QtGui/QWidget>

QT_BEGIN_NAMESPACE

class Ui_GeneralSettings
{
public:
    QGridLayout *gridLayout;
    QLabel *TextLabel4_3;
    QLineEdit *precisionEdit;
    QLabel *TextLabel4_3_2;
    QLineEdit *contextEdit;
    QLabel *TextLabel5;
    QLineEdit *maxListEdit;
    QSpacerItem *verticalSpacer_2;
    QLabel *TextLabel3;
    QSpacerItem *Spacer6_2_2_3;
    QLabel *TextLabel2_2;
    QLineEdit *symbolCount;
    QSpacerItem *Spacer6_2_2_2;
    QLabel *TextLabel2;
    QLineEdit *symbolLength;
    QSpacerItem *verticalSpacer;

    void setupUi(QWidget *GeneralSettings)
    {
        if (GeneralSettings->objectName().isEmpty())
            GeneralSettings->setObjectName(QString::fromUtf8("GeneralSettings"));
        GeneralSettings->resize(274, 260);
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::MinimumExpanding);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(GeneralSettings->sizePolicy().hasHeightForWidth());
        GeneralSettings->setSizePolicy(sizePolicy);
        gridLayout = new QGridLayout(GeneralSettings);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        gridLayout->setContentsMargins(-1, 0, 0, 0);
        TextLabel4_3 = new QLabel(GeneralSettings);
        TextLabel4_3->setObjectName(QString::fromUtf8("TextLabel4_3"));
        TextLabel4_3->setWordWrap(false);

        gridLayout->addWidget(TextLabel4_3, 0, 0, 1, 3);

        precisionEdit = new QLineEdit(GeneralSettings);
        precisionEdit->setObjectName(QString::fromUtf8("precisionEdit"));
        QSizePolicy sizePolicy1(QSizePolicy::Expanding, QSizePolicy::Fixed);
        sizePolicy1.setHorizontalStretch(2);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(precisionEdit->sizePolicy().hasHeightForWidth());
        precisionEdit->setSizePolicy(sizePolicy1);

        gridLayout->addWidget(precisionEdit, 0, 3, 1, 1);

        TextLabel4_3_2 = new QLabel(GeneralSettings);
        TextLabel4_3_2->setObjectName(QString::fromUtf8("TextLabel4_3_2"));
        TextLabel4_3_2->setWordWrap(false);

        gridLayout->addWidget(TextLabel4_3_2, 1, 0, 1, 3);

        contextEdit = new QLineEdit(GeneralSettings);
        contextEdit->setObjectName(QString::fromUtf8("contextEdit"));
        QSizePolicy sizePolicy2(QSizePolicy::Expanding, QSizePolicy::Fixed);
        sizePolicy2.setHorizontalStretch(0);
        sizePolicy2.setVerticalStretch(0);
        sizePolicy2.setHeightForWidth(contextEdit->sizePolicy().hasHeightForWidth());
        contextEdit->setSizePolicy(sizePolicy2);

        gridLayout->addWidget(contextEdit, 1, 3, 1, 1);

        TextLabel5 = new QLabel(GeneralSettings);
        TextLabel5->setObjectName(QString::fromUtf8("TextLabel5"));
        TextLabel5->setWordWrap(false);

        gridLayout->addWidget(TextLabel5, 2, 0, 1, 3);

        maxListEdit = new QLineEdit(GeneralSettings);
        maxListEdit->setObjectName(QString::fromUtf8("maxListEdit"));

        gridLayout->addWidget(maxListEdit, 2, 3, 1, 1);

        verticalSpacer_2 = new QSpacerItem(20, 10, QSizePolicy::Minimum, QSizePolicy::Fixed);

        gridLayout->addItem(verticalSpacer_2, 3, 1, 1, 1);

        TextLabel3 = new QLabel(GeneralSettings);
        TextLabel3->setObjectName(QString::fromUtf8("TextLabel3"));
        QSizePolicy sizePolicy3(QSizePolicy::Preferred, QSizePolicy::Fixed);
        sizePolicy3.setHorizontalStretch(0);
        sizePolicy3.setVerticalStretch(0);
        sizePolicy3.setHeightForWidth(TextLabel3->sizePolicy().hasHeightForWidth());
        TextLabel3->setSizePolicy(sizePolicy3);
        TextLabel3->setAlignment(Qt::AlignBottom|Qt::AlignLeading|Qt::AlignLeft);

        gridLayout->addWidget(TextLabel3, 4, 0, 1, 4);

        Spacer6_2_2_3 = new QSpacerItem(16, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout->addItem(Spacer6_2_2_3, 5, 0, 1, 1);

        TextLabel2_2 = new QLabel(GeneralSettings);
        TextLabel2_2->setObjectName(QString::fromUtf8("TextLabel2_2"));
        TextLabel2_2->setWordWrap(false);

        gridLayout->addWidget(TextLabel2_2, 5, 1, 1, 2);

        symbolCount = new QLineEdit(GeneralSettings);
        symbolCount->setObjectName(QString::fromUtf8("symbolCount"));
        sizePolicy2.setHeightForWidth(symbolCount->sizePolicy().hasHeightForWidth());
        symbolCount->setSizePolicy(sizePolicy2);

        gridLayout->addWidget(symbolCount, 5, 3, 1, 1);

        Spacer6_2_2_2 = new QSpacerItem(16, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout->addItem(Spacer6_2_2_2, 6, 0, 1, 1);

        TextLabel2 = new QLabel(GeneralSettings);
        TextLabel2->setObjectName(QString::fromUtf8("TextLabel2"));
        TextLabel2->setWordWrap(false);

        gridLayout->addWidget(TextLabel2, 6, 1, 1, 2);

        symbolLength = new QLineEdit(GeneralSettings);
        symbolLength->setObjectName(QString::fromUtf8("symbolLength"));
        sizePolicy2.setHeightForWidth(symbolLength->sizePolicy().hasHeightForWidth());
        symbolLength->setSizePolicy(sizePolicy2);

        gridLayout->addWidget(symbolLength, 6, 3, 1, 1);

        verticalSpacer = new QSpacerItem(20, 65, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout->addItem(verticalSpacer, 7, 2, 1, 1);


        retranslateUi(GeneralSettings);

        QMetaObject::connectSlotsByName(GeneralSettings);
    } // setupUi

    void retranslateUi(QWidget *GeneralSettings)
    {
        TextLabel4_3->setText(QApplication::translate("GeneralSettings", "Precision of percentage values:", 0, QApplication::UnicodeUTF8));
        TextLabel4_3_2->setText(QApplication::translate("GeneralSettings", "Context lines in annotations:", 0, QApplication::UnicodeUTF8));
        TextLabel5->setText(QApplication::translate("GeneralSettings", "Maximum number of items in lists:", 0, QApplication::UnicodeUTF8));
        TextLabel3->setText(QApplication::translate("GeneralSettings", "Symbols in tooltips and context menus truncated", 0, QApplication::UnicodeUTF8));
        TextLabel2_2->setText(QApplication::translate("GeneralSettings", "with more entries than:", 0, QApplication::UnicodeUTF8));
        TextLabel2->setText(QApplication::translate("GeneralSettings", "with more characters than:", 0, QApplication::UnicodeUTF8));
        Q_UNUSED(GeneralSettings);
    } // retranslateUi

};

namespace Ui {
    class GeneralSettings: public Ui_GeneralSettings {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_GENERALSETTINGS_H
