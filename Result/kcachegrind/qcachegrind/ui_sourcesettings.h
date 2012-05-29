/********************************************************************************
** Form generated from reading UI file 'sourcesettings.ui'
**
** Created: Fri May 25 12:01:58 2012
**      by: Qt User Interface Compiler version 4.8.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_SOURCESETTINGS_H
#define UI_SOURCESETTINGS_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QComboBox>
#include <QtGui/QGridLayout>
#include <QtGui/QHeaderView>
#include <QtGui/QLabel>
#include <QtGui/QLineEdit>
#include <QtGui/QPushButton>
#include <QtGui/QSpacerItem>
#include <QtGui/QTreeWidget>
#include <QtGui/QVBoxLayout>
#include <QtGui/QWidget>

QT_BEGIN_NAMESPACE

class Ui_SourceSettings
{
public:
    QGridLayout *gridLayout;
    QTreeWidget *dirList;
    QVBoxLayout *_2;
    QPushButton *addDirButton;
    QPushButton *deleteDirButton;
    QSpacerItem *Spacer5;
    QLabel *label;
    QComboBox *objectBox;
    QLabel *label_2;
    QLineEdit *dirEdit;
    QPushButton *browseDirButton;

    void setupUi(QWidget *SourceSettings)
    {
        if (SourceSettings->objectName().isEmpty())
            SourceSettings->setObjectName(QString::fromUtf8("SourceSettings"));
        SourceSettings->resize(400, 300);
        gridLayout = new QGridLayout(SourceSettings);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        gridLayout->setContentsMargins(-1, 0, 0, 0);
        dirList = new QTreeWidget(SourceSettings);
        dirList->setObjectName(QString::fromUtf8("dirList"));

        gridLayout->addWidget(dirList, 0, 0, 1, 2);

        _2 = new QVBoxLayout();
        _2->setObjectName(QString::fromUtf8("_2"));
        addDirButton = new QPushButton(SourceSettings);
        addDirButton->setObjectName(QString::fromUtf8("addDirButton"));

        _2->addWidget(addDirButton);

        deleteDirButton = new QPushButton(SourceSettings);
        deleteDirButton->setObjectName(QString::fromUtf8("deleteDirButton"));

        _2->addWidget(deleteDirButton);

        Spacer5 = new QSpacerItem(16, 49, QSizePolicy::Minimum, QSizePolicy::Expanding);

        _2->addItem(Spacer5);


        gridLayout->addLayout(_2, 0, 2, 1, 1);

        label = new QLabel(SourceSettings);
        label->setObjectName(QString::fromUtf8("label"));

        gridLayout->addWidget(label, 1, 0, 1, 1);

        objectBox = new QComboBox(SourceSettings);
        objectBox->setObjectName(QString::fromUtf8("objectBox"));

        gridLayout->addWidget(objectBox, 1, 1, 1, 2);

        label_2 = new QLabel(SourceSettings);
        label_2->setObjectName(QString::fromUtf8("label_2"));

        gridLayout->addWidget(label_2, 2, 0, 1, 1);

        dirEdit = new QLineEdit(SourceSettings);
        dirEdit->setObjectName(QString::fromUtf8("dirEdit"));

        gridLayout->addWidget(dirEdit, 2, 1, 1, 1);

        browseDirButton = new QPushButton(SourceSettings);
        browseDirButton->setObjectName(QString::fromUtf8("browseDirButton"));

        gridLayout->addWidget(browseDirButton, 2, 2, 1, 1);


        retranslateUi(SourceSettings);

        QMetaObject::connectSlotsByName(SourceSettings);
    } // setupUi

    void retranslateUi(QWidget *SourceSettings)
    {
        QTreeWidgetItem *___qtreewidgetitem = dirList->headerItem();
        ___qtreewidgetitem->setText(1, QApplication::translate("SourceSettings", "Base Directory", 0, QApplication::UnicodeUTF8));
        ___qtreewidgetitem->setText(0, QApplication::translate("SourceSettings", "ELF Object", 0, QApplication::UnicodeUTF8));
        addDirButton->setText(QApplication::translate("SourceSettings", "Add", 0, QApplication::UnicodeUTF8));
        deleteDirButton->setText(QApplication::translate("SourceSettings", "Delete", 0, QApplication::UnicodeUTF8));
        label->setText(QApplication::translate("SourceSettings", "ELF Object:", 0, QApplication::UnicodeUTF8));
        label_2->setText(QApplication::translate("SourceSettings", "Base Directory:", 0, QApplication::UnicodeUTF8));
        browseDirButton->setText(QApplication::translate("SourceSettings", "Browse...", 0, QApplication::UnicodeUTF8));
        Q_UNUSED(SourceSettings);
    } // retranslateUi

};

namespace Ui {
    class SourceSettings: public Ui_SourceSettings {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_SOURCESETTINGS_H
