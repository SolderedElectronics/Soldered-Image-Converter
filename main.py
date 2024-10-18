# Import the necessary libraries
import sys
import time

# Import gui libraries and elements
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QFontDatabase, QFont
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from PySide6.QtWidgets import QLabel, QApplication, QFileDialog, QMessageBox
from droplabel import DropLabel
import clipboard

# Import custom .css for styling the GUI
from style import *

# Import the version string from version.py
# No need to modify that file
from version import *

# Import all the image related functions
from image import *

# Import all boards for conversion
from boards import *

# The main window's class
class MainWindow(QtWidgets.QMainWindow):
    # Main window initialization function
    def __init__(self):
        super().__init__()
        # Let's load all the boards
        self._Inkplate10 = Inkplate10(self)
        self._Inkplate6 = Inkplate6(self)
        self._Inkplate6PLUS = Inkplate6PLUS(self)
        self._Inkplate6MOTION = Inkplate6MOTION(self)
        self.boards = [self._Inkplate10, self._Inkplate6, self._Inkplate6PLUS, self._Inkplate6MOTION]
        # Make 10 empty images for conversion
        # The user input won't be more than 10
        self.images = [ImageForConversion(num=i) for i in range(10)]
        self.num_images = 0 # There are no images loaded yet
        self.selected_image = 0 # The selected image will be the first image
        self.init_ui()

    # Initialize the user interface
    def init_ui(self):
        # First, load the QtDesigner file as the GUI
        loader = QUiLoader()
        ui_file = QFile("imageConverter.ui")
        if not ui_file.open(QFile.ReadOnly):
            print("Cannot open UI file")
            sys.exit(-1)
        self.window = loader.load(ui_file, None)
        ui_file.close()
        if self.window is None:
            print("Cannot load UI file")
            sys.exit(-1)

        # Fix fonts
        app.setStyleSheet("""
        *{
            font-family: "Source Sans Pro, Arial, Helvetica, Sans-Serif";
        }
        """)

        # Set the window title and icon
        self.window.setWindowTitle("Soldered Image Converter " + str(version))
        self.window.setWindowIcon(QtGui.QIcon('img/icon.ico'))

        # Now, get the UI elements so they can be used in code
        # Also, for some set the stylesheet and/or map them to functions

        # Stacked widget which alternates between page 0 for the startup screen
        # And page 1 for the 'image processing' screen
        self.main_stack = self.window.findChild(QtWidgets.QStackedWidget, "mainStack")

        # Make sure we're on page 0 to start with
        self.main_stack.setCurrentIndex(0)

        # Ensure the browse button is correctly set and visible
        self.browse_button = self.window.findChild(QtWidgets.QPushButton, "browseButton")
        self.browse_button.clicked.connect(self.open_file_dialog)

        # The display of which image we are currently editing
        self.filenum_label = self.window.findChild(QtWidgets.QLabel, "filenum_label")

        # Image preview qLabel
        self.previewIMG = self.window.findChild(QtWidgets.QLabel, "previewIMG")

        # Add the logo in the header
        self.header = self.window.findChild(QtWidgets.QWidget, "header")
        self.logo_path = "img/logo.png"
        self.logo_pixmap = QtGui.QPixmap(self.logo_path)
        # This is an 'unresolved reference' but is actually OK
        self.mainLogo_label = self.header.findChild(QtWidgets.QLabel, "mainLogo")
        self.mainLogo_label.setPixmap(self.logo_pixmap)
        self.mainLogo_label.setScaledContents(True)

        # Combo box for selecting the board
        self.selectBoard = self.header.findChild(QtWidgets.QComboBox, "boardSelect")
        self.selectBoard.setStyleSheet(comboBox) # Set style
        # Add items to the combo box
        for board in self.boards:
            self.selectBoard.addItem(board.name)

        # Image with steps how to use the program
        self.steps_path = "img/steps.png"
        self.steps_pixmap = QtGui.QPixmap(self.steps_path)
        self.steps = self.window.findChild(QtWidgets.QLabel, "steps")
        self.steps.setPixmap(self.steps_pixmap)

        # The place where to drop off the file to
        self.dragdrop = DropLabel(self, self.main_stack.widget(0))
        self.dragdrop.setGeometry(70, 240, 1237, 315)
        self.dragdrop_pixmap = QtGui.QPixmap("img/dragdrop.png")
        self.dragdrop.setPixmap(self.dragdrop_pixmap)

        # These are elements of page two, which will be shown after the user uploads photos
        # Image name
        self.imageName_lineEdit = self.window.findChild(QtWidgets.QLineEdit, "imageName_lineEdit")
        self.imageName_lineEdit.setStyleSheet(lineEdit)

        self.set_name = self.window.findChild(QtWidgets.QPushButton, "set_name_button")
        self.set_name.clicked.connect(self.change_name)

        # Height
        self.height_lineEdit = self.window.findChild(QtWidgets.QLineEdit, "height_lineEdit")
        self.height_lineEdit.setStyleSheet(lineEdit)

        # Width
        self.width_lineEdit = self.window.findChild(QtWidgets.QLineEdit, "width_lineEdit")
        self.width_lineEdit.setStyleSheet(lineEdit)

        # Black and white treshold
        self.bwtresh_slider = self.window.findChild(QtWidgets.QSlider, "bwtresh_slider")
        self.bwtresh_slider.setStyleSheet(slider_enabled)
        # On slider value change, do change_tresh
        self.bwtresh_slider.sliderReleased.connect(self.change_tresh)
        self.bwtresh_value = self.window.findChild(QtWidgets.QLabel, "bwtresh_value")

        # Constrain proportions checkbox
        self.constrain_check = self.window.findChild(QtWidgets.QCheckBox, "constrain_check")
        self.constrain_check.setStyleSheet(checkBox)
        self.constrain_check.stateChanged.connect(self.constrain_proportions)

        # Invert checkbox
        self.invert_check = self.window.findChild(QtWidgets.QCheckBox, "invert_check")
        self.invert_check.setStyleSheet(checkBox)
        # On click, do invert_image
        self.invert_check.stateChanged.connect(self.invert_image)

        # Resize button
        self.resize_button = self.window.findChild(QtWidgets.QPushButton, "resize_button")
        self.resize_button.clicked.connect(self.resize_image)

        # Dither kernel select combo box
        self.kernel_combo = self.window.findChild(QtWidgets.QComboBox, "kernel_combo")
        self.kernel_combo.setStyleSheet(comboBox)
        self.kernel_combo.addItem("None", userData=0)
        self.kernel_combo.addItem("Floyd-Steinberg", userData=1)
        self.kernel_combo.addItem("Jarvis", userData=2)
        self.kernel_combo.addItem("Simple2D", userData=3)
        self.kernel_combo.currentIndexChanged.connect(self.change_dither_kernel)

        # Colordepth combo box
        self.colorDepth_combo = self.window.findChild(QtWidgets.QComboBox, "colorDepth_combo")
        self.colorDepth_combo.setStyleSheet(comboBox)
        self.colorDepth_combo.currentIndexChanged.connect(self.change_color_depth)

        # Left arrow (previous image)
        self.left_arrow_path = "img/left_arrow.png"
        self.left_arrow_pixmap = QtGui.QPixmap(self.left_arrow_path)
        self.left_arrow = self.window.findChild(QtWidgets.QPushButton, "left_button")
        self.left_arrow.clicked.connect(self.prev_image)

        # Right arrow (next image)
        self.right_arrow_path = "img/right_arrow.png"
        self.right_arrow_pixmap = QtGui.QPixmap(self.right_arrow_path)
        self.right_arrow = self.window.findChild(QtWidgets.QPushButton, "right_button")
        self.right_arrow.clicked.connect(self.next_image)

        # Label
        self.current_file = self.window.findChild(QtWidgets.QLabel, "filenum_label")
        self.current_file.setText("0 / 0")

        # Info to the user that the conversion process has started
        self.converting_label = self.window.findChild(QtWidgets.QLabel, "converting_label")
        self.converting_label.setText("") # Set empty for now

        # The text edit with the resulting code
        self.resulting_code = self.window.findChild(QtWidgets.QTextEdit, "resulting_code")
        self.resulting_code.setReadOnly(True) # It's read only! But you can copy it
        self.resulting_code.clear() # Clear it

        # Copy to clipboard button
        self.copy_button = self.window.findChild(QtWidgets.QPushButton, "copy_button")
        self.copy_button.clicked.connect(self.copy_code_to_clipboard)

        # Save to .h file button
        self.save_to_header_file_button = self.window.findChild(QtWidgets.QPushButton, "save_to_header_file_button")
        self.save_to_header_file_button.clicked.connect(self.save_to_header_file)

        # Save all pictures to .h files in a folder
        self.save_all_button = self.window.findChild(QtWidgets.QPushButton, "save_all_button")
        self.save_all_button.clicked.connect(self.save_all_to_header_files)

        # Reset process
        self.reset_button = self.window.findChild(QtWidgets.QPushButton, "reset_button")
        self.reset_button.clicked.connect(self.reset_everything)

        # Great, now show the window! UI setup is complete
        self.window.show()

    # This function opens the 'Browse' file dialog
    def open_file_dialog(self):
        # Open file dialog allowing only png, bmp, and jpg files
        file_dialog = QFileDialog(self.window)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilters(["Images (*.png *.bmp *.jpg)"])
        # Run the file dialog
        if file_dialog.exec():
            self.selected_files = file_dialog.selectedFiles()

            # Check if more than 10 files are selected
            if len(self.selected_files) > 10:
                QMessageBox.critical(self.window, "Error", "You can only select up to 10 files.")
            else:
                for i, file_path in enumerate(self.selected_files):
                    # If the file path is not empty...
                    if file_path != "":
                        # Save the paths and formats of the images in memory
                        file_format = file_path[-3:].lower()
                        self.images[i].file_path = file_path
                        self.images[i].file_format = file_format
                    # Also count them
                    self.num_images +=1

                    # Print the images array to verify
                for img in self.images:
                    if img.file_path != "":
                        print(f"Path: {img.file_path}, Format: {img.file_format}")

                # Go to the next screen
                self.next_screen()

    # This function is called when files are dropped
    def handle_file_drop(self, file_paths):
        self.selected_files = file_paths
        # Now do the same if we're doing browse
        for i, file_path in enumerate(self.selected_files):
            # If the file path is not empty...
            if file_path != "":
                # Save the paths and formats of the images in memory
                file_format = file_path[-3:].lower()
                self.images[i].file_path = file_path
                self.images[i].file_format = file_format
            # Also count them
            self.num_images += 1

            # Print the images array to verify
        for img in self.images:
            if img.file_path != "":
                print(f"Path: {img.file_path}, Format: {img.file_format}")

        # Go to the next screen
        self.next_screen()
        # You can perform other actions here

    # This function goes to the next screen
    def next_screen(self):
        # Set this label's text so the user knows it's loading
        self.converting_label.setText("Processing...")
        # Let's also lock the board selection
        self.selectBoard.setEnabled(False)
        QApplication.processEvents() # Update GUI

        # Let's lock in the board
        selected_name = self.selectBoard.currentText()
        self.selected_board = None  # Initialize to None in case no match is found
        # Find the board where board.name matches the selected name
        for board in self.boards:
            if board.name == selected_name:
                self.selected_board = board
                break  # Exit the loop once the matching board is found

        # Get the combo box model
        model = self.colorDepth_combo.model()

        # Loop through each item in the combo box
        for i in range(self.colorDepth_combo.count()):
            # Get the text of the current item
            item_text = self.colorDepth_combo.itemText(i)

            # Get the QStandardItem for the current item
            item = model.item(i)

            # Check if the item is in the selected board's conversion_modes
            if item_text in self.selected_board.conversion_modes:
                # Enable the item
                item.setEnabled(True)
            else:
                # Disable the item
                item.setEnabled(False)

        # Do initial processing of the images with default settings
        for image in self.images:
            # If there is an actual image loaded:
            if image.file_path != "":
                # Do the initial default settings of processing
                image.initial_process()

        # Set the label which shows which image we're currently on
        self.filenum_label.setText(str(self.selected_image+1)+" / "+str(self.num_images))

        # Load the first image
        self.load_image(0)

    # This function loads each image into the editor part
    def load_image(self, index):
            # First, set the label that we're loading
        self.converting_label.setText("Processing...")
        QApplication.processEvents() # Make sure it's updated

        # Let's get the image
        image = self.images[index]

        # Block signals to prevent recursive calls
        self.imageName_lineEdit.blockSignals(True)
        self.colorDepth_combo.blockSignals(True)
        self.bwtresh_slider.blockSignals(True)
        self.bwtresh_value.blockSignals(True)
        self.invert_check.blockSignals(True)
        self.resize_button.blockSignals(True)
        self.constrain_check.blockSignals(True)
        self.width_lineEdit.blockSignals(True)
        self.height_lineEdit.blockSignals(True)
        self.left_arrow.blockSignals(True)
        self.right_arrow.blockSignals(True)
        self.copy_button.blockSignals(True)
        self.save_to_header_file_button.blockSignals(True)
        self.reset_button.blockSignals(True)

        # Now, in order, set all the elements values for this image
        self.imageName_lineEdit.setText(image.processed_image_name)
        self.colorDepth_combo.setCurrentIndex(image.conversion_mode)

        # Set the dithering
        self.kernel_combo.setCurrentIndex(image.ditherKernel)

        # Set the number display
        self.current_file.setText(f"{str(index+1)} / {str(self.num_images)}")

        # Set bw treshold
        self.bwtresh_slider.setValue(image.bw_tresh)
        self.bwtresh_value.setText(str(image.bw_tresh))
        # If there is a dither kernel selected, the BW Tresh slider is disabled
        if image.ditherKernel==0:
            if image.conversion_mode==0:
                self.bwtresh_slider.setEnabled(True)
                self.bwtresh_slider.setStyleSheet(slider_enabled)
            else:
                self.bwtresh_slider.setEnabled(False)
                self.bwtresh_slider.setStyleSheet(slider_disabled)
        else:
            self.bwtresh_slider.setEnabled(False)
            self.bwtresh_slider.setStyleSheet(slider_disabled)

        self.invert_check.setChecked(image.invert)
        self.constrain_check.setChecked(image.constrain)

        self.width_lineEdit.setText(str(image.width))
        self.height_lineEdit.setText(str(image.height))

        if image.constrain:
            self.height_lineEdit.setEnabled(False)
        else:
            self.height_lineEdit.setEnabled(True)

        # Process the image with the set settings
        image.process_image()

        # Send code to window
        self.resulting_code.setPlainText(image.resultString)

        # Update the preview image
        preview_path = "preview.png"
        preview_pixmap = QtGui.QPixmap(preview_path)
        preview_pixmap = preview_pixmap.scaled(self.previewIMG.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.previewIMG.setPixmap(preview_pixmap)

        # Continue signals
        self.imageName_lineEdit.blockSignals(False)
        self.colorDepth_combo.blockSignals(False)
        self.bwtresh_slider.blockSignals(False)
        self.bwtresh_value.blockSignals(False)
        self.invert_check.blockSignals(False)
        self.resize_button.blockSignals(False)
        self.constrain_check.blockSignals(False)
        self.width_lineEdit.blockSignals(False)
        self.height_lineEdit.blockSignals(False)
        self.left_arrow.blockSignals(False)
        self.right_arrow.blockSignals(False)
        self.copy_button.blockSignals(False)
        self.save_to_header_file_button.blockSignals(False)
        self.reset_button.blockSignals(False)

        # Reset the processing text
        self.converting_label.setText("")
        # Go to the next screen
        self.main_stack.setCurrentIndex(1)
        QApplication.processEvents()  # Make sure everything is updated

    # These functions happen when a parameter gets changed
    def change_name(self):
        # Set label so the user knows this takes a moment
        self.converting_label.setText("Processing...")
        QApplication.processEvents()
        # Get the new name string
        new_name = self.imageName_lineEdit.text()
        # Remove any characters not allowed in C++ variable names
        new_name = re.sub(r'[^a-zA-Z0-9_]', '', new_name)
        self.images[self.selected_image].change_name(new_name) # Change the name
        # Set it in the GUI
        self.resulting_code.setPlainText(self.images[self.selected_image].resultString)
        self.converting_label.setText("")
        QApplication.processEvents()  # Make sure everything is updated

    def change_tresh(self):
        # Let's get the value
        value = self.bwtresh_slider.value()
        # Update the display
        self.bwtresh_value.setText(str(value))
        self.images[self.selected_image].bw_tresh = value
        self.load_image(self.selected_image)

    def invert_image(self):
        invert = False
        if self.invert_check.isChecked():
            invert = True
        self.images[self.selected_image].invert = invert
        self.load_image(self.selected_image)

    def resize_image(self):
        self.images[self.selected_image].resize = True
        if self.images[self.selected_image].constrain:
            self.images[self.selected_image].width = int(self.width_lineEdit.text())
            self.images[self.selected_image].height = int(float(self.images[self.selected_image].width) / float(self.images[self.selected_image].original_ratio))
            self.height_lineEdit.setText(str(self.images[self.selected_image].height))
        else:
            self.images[self.selected_image].width = int(self.width_lineEdit.text())
            self.images[self.selected_image].height = int(self.height_lineEdit.text())
        self.load_image(self.selected_image)

    def constrain_proportions(self):
        constrain = False
        if self.constrain_check.isChecked():
            constrain = True
        self.images[self.selected_image].constrain = constrain
        #self.load_image(self.selected_image) # No need to re-load really
        # Just disable height line edit
        if constrain:
            self.height_lineEdit.setEnabled(False)
        else:
            self.height_lineEdit.setEnabled(True)

    def change_dither_kernel(self):
        selected_dither_kernel = self.kernel_combo.itemData(self.kernel_combo.currentIndex())
        self.images[self.selected_image].ditherKernel = selected_dither_kernel
        self.load_image(self.selected_image)

    def copy_code_to_clipboard(self):
        clipboard.copy(self.images[self.selected_image].resultString)
        self.converting_label.setText("Copied!")
        QApplication.processEvents()

    def save_to_header_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # Define the save file dialog
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setDefaultSuffix('h')
        file_dialog.setNameFilters(['C++ Header Files (*.h)', 'All Files (*)'])
        file_dialog.selectFile(self.images[self.selected_image].processed_image_name)

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            try:
                with open(file_path, 'w') as file:
                    file.write(self.images[self.selected_image].resultString)
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to save file: {str(e)}")

        self.converting_label.setText("Saved!")
        QApplication.processEvents()

    def save_to_header_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # Define the save file dialog
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setDefaultSuffix('h')
        file_dialog.setNameFilters(['C++ Header Files (*.h)', 'All Files (*)'])
        file_dialog.selectFile(self.images[self.selected_image].processed_image_name)

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            try:
                with open(file_path, 'w') as file:
                    file.write(self.images[self.selected_image].resultString)
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to save file: {str(e)}")

        self.converting_label.setText("Saved!")
        QApplication.processEvents()

    def save_all_to_header_files(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # Define the save folder dialog
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.Directory)
        folder_dialog.setOptions(options)

        if folder_dialog.exec():
            folder_path = folder_dialog.selectedFiles()[0]

            for x in range(self.num_images):
                file_name = self.images[x].processed_image_name
                file_content = self.images[x].resultString
                file_path = os.path.join(folder_path, file_name)

                try:
                    with open(file_path+".h", 'w') as file:
                        file.write(file_content)
                except Exception as e:
                    QMessageBox.critical(None, "Error", f"Failed to save file '{file_name}': {str(e)}")
                    return  # Exit if there is an error

            self.converting_label.setText("All files saved successfully!")
            QApplication.processEvents()

    def change_color_depth(self):
        self.images[self.selected_image].conversion_mode = self.colorDepth_combo.currentIndex()
        self.load_image(self.selected_image)

    def next_image(self):
        self.selected_image = (self.selected_image + 1) % self.num_images
        self.load_image(self.selected_image)

    def prev_image(self):
        self.selected_image = (self.selected_image - 1) % self.num_images
        self.load_image(self.selected_image)

    def reset_everything(self):
        self.images = [ImageForConversion(num=i) for i in range(10)]
        self.num_images = 0  # There are no images loaded yet
        self.selected_image = 0  # The selected image will be the first image
        self.main_stack.setCurrentIndex(0)
        self.selectBoard.setEnabled(True)

# Script execution starts here
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())

