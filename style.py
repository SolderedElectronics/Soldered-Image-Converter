# GUI elements' CSS styles

comboBox = """
            QComboBox {
                border: 1px solid gray;
                border-radius: 10px;
                padding: 1px 18px 1px 3px;
                min-width: 6em;
                background-color: white;
                max-height: 30px;  /* Set a max height for the combobox */
            }

            QComboBox:editable {
                background: white;
            }

            QComboBox:!editable, QComboBox::drop-down:editable {
                background: white;
            }

            QComboBox:!editable:on, QComboBox::drop-down:editable:on {
                background: white;
            }

            QComboBox:on {
                padding-top: 3px;
                padding-left: 4px;
                background: white;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 0px;
                border-left-color: transparent;
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
                background: white;
                background-color: white;
                max-height: 30px;  /* Set a max height for the drop-down */
            }

            QComboBox::down-arrow {
                image: url("img/down_arrow.png");
                width: 16px;
                height: 16px;
                padding-right: 5px;  /* Reduced padding to prevent vertical expansion */
            }

            QComboBox QAbstractItemView {
                background: white;
                border: 1px solid gray;
                selection-background-color: lightgray;
                max-height: 150px;  /* Set a max height for the dropdown list */
            }

            QComboBox::item {
                padding: 5px;
                background: white;
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