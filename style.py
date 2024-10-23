# GUI elements' CSS styles

comboBox = """
QComboBox {
  background: #FFFFFF;
  padding: 2px 18px 2px 3px;
  selection-background-color: #D0D0D0;
  selection-color: #000000;
  border: 1px solid gray;
  border-radius: 10px;
}

QComboBox:editable {
  background: #FFFFFF;
}

QComboBox:!editable,
QComboBox::drop-down:editable,
QComboBox:!editable:on,
QComboBox::drop-down:editable:on {
  background: #FFFFFF;
}

QComboBox::drop-down {
  subcontrol-origin: padding;
  subcontrol-position: top right;
  border-left: none;
  width: 20px; /* Adjust the width if needed */
  image: url("img/down_arrow.png");
}

QComboBox::down-arrow {
  image: url("img/down_arrow.png");
  width: 12px; /* Adjust the arrow size if needed */
  height: 12px;
}

QComboBox QAbstractItemView {
  background: #FFFFFF;
  border: none;
}
            """

lineEdit = """
            QLineEdit {
                border: 1px solid gray;
                border-radius: 10px;
                padding: 1px 18px 1px 3px;
                min-width: 6em;
                background-color: white;
                font-size:15px;
            }
            """

checkBox = """
            QCheckBox {
                padding-right: 25px; /* Space to push the checkbox to the right */
                text-align: left;
            }
            
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px; /* Rounded edges */
                border: 1px solid #5A5A5A; /* Border color */
                background-color: white; /* Background color */
            }
            
            QCheckBox::indicator:checked {
                background-color: #5A5A5A; /* Background color when checked */
                border: 1px solid #5A5A5A; /* Border color when checked */
            }
            
            QCheckBox::indicator:unchecked {
                background-color: white; /* Background color when unchecked */
            }
            """

slider_enabled = """
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #d6d6d6;
                margin: 2px 0;
                border-radius: 4px;
            }
            
            QSlider::handle:horizontal {
                background: #23B9D6;
                border: 1px solid #23B9D6;
                width: 18px;
                height: 18px;
                border-radius: 9px;
                margin: -5px 0;
            }
            
            QSlider::sub-page:horizontal {
                background: #23B9D6;
                border: 1px solid #23B9D6;
                height: 8px;
                border-radius: 4px;
            }
            
            QSlider::add-page:horizontal {
                background: #d6d6d6;
                border: 1px solid #d6d6d6;
                height: 8px;
                border-radius: 4px;
            }
            """

slider_disabled = """
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #d6d6d6;
                margin: 2px 0;
                border-radius: 4px;
            }

            QSlider::handle:horizontal {
                background: #D9D9D9;
                border: 1px solid #D9D9D9;
                width: 18px;
                height: 18px;
                border-radius: 9px;
                margin: -5px 0;
            }

            QSlider::sub-page:horizontal {
                background: #D9D9D9;
                border: 1px solid #D9D9D9;
                height: 8px;
                border-radius: 4px;
            }

            QSlider::add-page:horizontal {
                background: #d6d6d6;
                border: 1px solid #d6d6d6;
                height: 8px;
                border-radius: 4px;
            }
            """