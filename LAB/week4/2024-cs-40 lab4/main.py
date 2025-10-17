import sys
import os
import time
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem, 
                             QMessageBox, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QFileDialog)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Store the dataframe
        self.df = None
        
        # Connect menu action to load CSV
        self.ui.actionfile.triggered.connect(self.load_csv_data)
        self.ui.actionload_csv.triggered.connect(self.load_csv_data)
        
        # Connect sorting buttons
        self.setup_connections()
        
    def setup_connections(self):
        # Connect sorting buttons
        self.ui.bubblesort.clicked.connect(lambda: self.sort_data("Bubble Sort"))
        self.ui.insertionsort.clicked.connect(lambda: self.sort_data("Insertion Sort"))
        self.ui.selectionsort.clicked.connect(lambda: self.sort_data("Selection Sort"))
        self.ui.mergesort.clicked.connect(lambda: self.sort_data("Merge Sort"))
        self.ui.quicksort.clicked.connect(lambda: self.sort_data("Quick Sort"))
        self.ui.countingsort.clicked.connect(lambda: self.sort_data("Counting Sort"))
        self.ui.radixsort.clicked.connect(lambda: self.sort_data("Radix Sort"))
        self.ui.bucketsort.clicked.connect(lambda: self.sort_data("Bucket Sort"))
        
    def load_csv_data(self):
        try:
            # Open file dialog to select CSV file
            file_path, _ = QFileDialog.getOpenFileName(
                self, 
                "Open CSV File", 
                "", 
                "CSV Files (*.csv);;All Files (*)"
            )
            
            if not file_path:
                return  # User cancelled
                
            print(f"Loading file: {file_path}")
            
            # Load CSV file with error handling
            try:
                self.df = pd.read_csv(file_path)
                print(f"CSV loaded successfully. Shape: {self.df.shape}")
                print(f"Columns: {self.df.columns.tolist()}")
                print(f"First few rows:\n{self.df.head()}")
            except pd.errors.EmptyDataError:
                QMessageBox.critical(self, "Error", "The CSV file is empty!")
                return
            except pd.errors.ParserError as e:
                QMessageBox.critical(self, "Error", f"Error parsing CSV file: {str(e)}")
                return
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error reading CSV: {str(e)}")
                return
            
            # Check if dataframe is empty
            if self.df.empty:
                QMessageBox.warning(self, "Warning", "The CSV file contains no data!")
                return
            
            # Clear the table widget completely
            self.ui.tableWidget.setRowCount(0)
            self.ui.tableWidget.setColumnCount(0)
            self.ui.tableWidget.clear()
            
            # Set up the table dimensions
            num_rows = len(self.df)
            num_cols = len(self.df.columns)
            
            print(f"Setting table to {num_rows} rows and {num_cols} columns")
            
            self.ui.tableWidget.setRowCount(num_rows)
            self.ui.tableWidget.setColumnCount(num_cols)
            
            # Set column headers
            self.ui.tableWidget.setHorizontalHeaderLabels([str(col) for col in self.df.columns])
            
            # Populate table with data
            for row in range(num_rows):
                for col in range(num_cols):
                    try:
                        # Get the value
                        value = self.df.iloc[row, col]
                        
                        # Handle different data types
                        if pd.isna(value):
                            display_value = 'N/A'
                        else:
                            display_value = str(value)
                        
                        # Create table item
                        item = QTableWidgetItem(display_value)
                        self.ui.tableWidget.setItem(row, col, item)
                        
                    except Exception as e:
                        print(f"Error at row {row}, col {col}: {e}")
                        item = QTableWidgetItem("Error")
                        self.ui.tableWidget.setItem(row, col, item)
            
            print(f"Table populated with {num_rows} rows")
            
            # Update combo box with column names
            self.ui.comboBox.clear()
            self.ui.comboBox.addItems([str(col) for col in self.df.columns])
            
            # Update stats
            self.ui.lineEdit_2.setText(str(num_rows))
            self.ui.statusbar.showMessage(f"Loaded {num_rows} records from {os.path.basename(file_path)}")
            
            # Resize columns to fit content
            self.ui.tableWidget.resizeColumnsToContents()
            
            # Also adjust row heights
            self.ui.tableWidget.resizeRowsToContents()
            
            QMessageBox.information(self, "Success", f"Loaded {num_rows} records with {num_cols} columns successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load CSV: {str(e)}")
            print(f"Error details: {e}")
            import traceback
            traceback.print_exc()

    def update_table_display(self):
        """Refresh the table widget with current DataFrame data"""
        # Disable sorting temporarily while updating
        self.ui.tableWidget.setSortingEnabled(False)
        
        # Clear the table
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)
        
        # Set dimensions
        num_rows = len(self.df)
        num_cols = len(self.df.columns)
        
        self.ui.tableWidget.setRowCount(num_rows)
        self.ui.tableWidget.setColumnCount(num_cols)
        
        # Set headers
        self.ui.tableWidget.setHorizontalHeaderLabels([str(col) for col in self.df.columns])
        
        # Populate with data
        for row in range(num_rows):
            for col in range(num_cols):
                value = self.df.iloc[row, col]
                
                if pd.isna(value):
                    display_value = 'N/A'
                else:
                    display_value = str(value)
                
                item = QTableWidgetItem(display_value)
                self.ui.tableWidget.setItem(row, col, item)
        
        # Resize columns
        self.ui.tableWidget.resizeColumnsToContents()
        
        # Re-enable sorting
        self.ui.tableWidget.setSortingEnabled(True)
        
    def sort_data(self, algorithm):
        if self.df is None:
            QMessageBox.warning(self, "Warning", "Please load CSV data first!")
            return
            
        selected_column = self.ui.comboBox.currentText()
        if not selected_column:
            QMessageBox.warning(self, "Warning", "Please select a column first!")
            return
        
        column_data = self.df[selected_column].tolist()
        is_numeric = False
        
        # Validate numeric data
        try:
            # Try converting to numeric
            numeric_data = pd.to_numeric(self.df[selected_column], errors='coerce')
            # Check if all values were successfully converted (not NaN)
            if not numeric_data.isna().all():
                column_data = numeric_data.tolist()
                is_numeric = True
        except:
            pass  # Keep this pass here, it's fine
        
        # If not numeric, treat as strings
        if not is_numeric:
            column_data = [str(x) if not pd.isna(x) else "" for x in column_data]
        
        # Start timing
        start_time = time.time()
        
        # Call appropriate algorithm
        if algorithm == "Insertion Sort":
            sorted_indices = insertion(column_data)
        elif algorithm == "Bubble Sort":
            sorted_indices = bubblesort(column_data)
            # ← REMOVE the return here!
        elif algorithm == "Selection Sort":
            QMessageBox.warning(self, "Warning", f"{algorithm} not implemented yet!")
            return
        elif algorithm == "Merge Sort":
            QMessageBox.warning(self, "Warning", f"{algorithm} not implemented yet!")
            return
        elif algorithm == "Quick Sort":
            QMessageBox.warning(self, "Warning", f"{algorithm} not implemented yet!")
            return
        elif algorithm == "Counting Sort":
            QMessageBox.warning(self, "Warning", f"{algorithm} not implemented yet!")
            return
        elif algorithm == "Radix Sort":
            QMessageBox.warning(self, "Warning", f"{algorithm} not implemented yet!")
            return
        elif algorithm == "Bucket Sort":
            QMessageBox.warning(self, "Warning", f"{algorithm} not implemented yet!")
            return
        else:
            QMessageBox.warning(self, "Warning", f"{algorithm} not recognized!")
            return
        
        # End timing
        end_time = time.time()
        total = end_time - start_time
        
        # Update DataFrame with sorted order
        self.df = self.df.iloc[sorted_indices].reset_index(drop=True)
        
        # Update display
        self.update_table_display()
        
        # Update time field
        self.ui.lineEdit_3.setText(f"{total:.6f} seconds")
        
        # Show success message
        QMessageBox.information(self, "Success", f"{algorithm} completed in {total:.6f} seconds!")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        
        # Central widget with layout
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Main vertical layout
        main_layout = QVBoxLayout(self.centralwidget)
        
        # Top section layout
        top_layout = QHBoxLayout()
        
        # URL section
        url_layout = QVBoxLayout()
        self.label = QtWidgets.QLabel("Enter the URL:")
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setPlaceholderText("Enter website URL here...")
        url_layout.addWidget(self.label)
        url_layout.addWidget(self.lineEdit)
        top_layout.addLayout(url_layout)
        
        # Stats section
        stats_layout = QVBoxLayout()
        self.label_2 = QtWidgets.QLabel("Total data scraped:")
        self.lineEdit_2 = QtWidgets.QLineEdit()
        self.lineEdit_2.setReadOnly(True)
        stats_layout.addWidget(self.label_2)
        stats_layout.addWidget(self.lineEdit_2)
        top_layout.addLayout(stats_layout)
        
        # Time section
        time_layout = QVBoxLayout()
        self.label_3 = QtWidgets.QLabel("Total time taken:")
        self.lineEdit_3 = QtWidgets.QLineEdit()
        self.lineEdit_3.setReadOnly(True)
        time_layout.addWidget(self.label_3)
        time_layout.addWidget(self.lineEdit_3)
        top_layout.addLayout(time_layout)
        
        # Add stretch to push elements to the left
        top_layout.addStretch()
        
        main_layout.addLayout(top_layout)
        
        # Middle section (Table and Controls)
        middle_layout = QHBoxLayout()
        
        # Left controls panel
        left_panel = QVBoxLayout()
        
        # Column selection
        self.groupBox_2 = QtWidgets.QGroupBox("Select Columns")
        group_layout = QVBoxLayout(self.groupBox_2)
        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.setMinimumHeight(30)
        group_layout.addWidget(self.comboBox)
        left_panel.addWidget(self.groupBox_2)
        
        # Algorithms
        self.groupBox = QtWidgets.QGroupBox("Algorithms")
        algorithms_layout = QVBoxLayout(self.groupBox)
        
        self.bubblesort = QtWidgets.QPushButton("Bubble Sort")
        self.insertionsort = QtWidgets.QPushButton("Insertion Sort")
        self.selectionsort = QtWidgets.QPushButton("Selection Sort")
        self.mergesort = QtWidgets.QPushButton("Merge Sort")
        self.quicksort = QtWidgets.QPushButton("Quick Sort")
        self.countingsort = QtWidgets.QPushButton("Counting Sort")
        self.radixsort = QtWidgets.QPushButton("Radix Sort")
        self.bucketsort = QtWidgets.QPushButton("Bucket Sort")
        
        # Set fixed height for buttons for consistency
        buttons = [self.bubblesort, self.insertionsort, self.selectionsort, self.mergesort, 
                  self.quicksort, self.countingsort, self.radixsort, self.bucketsort]
        for button in buttons:
            button.setMinimumHeight(35)
            algorithms_layout.addWidget(button)
        
        left_panel.addWidget(self.groupBox)
        left_panel.addStretch()
        
        # Add left panel to middle layout with fixed width
        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left_panel)
        left_widget.setMaximumWidth(250)
        middle_layout.addWidget(left_widget)
        
        # Table
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        
        # Enable sorting by clicking headers
        self.tableWidget.setSortingEnabled(True)
        
        middle_layout.addWidget(self.tableWidget)
        
        main_layout.addLayout(middle_layout)
        
        # Set main layout
        MainWindow.setCentralWidget(self.centralwidget)
        
        # Menu bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 21))
        self.menufile = QtWidgets.QMenu("File", self.menubar)
        MainWindow.setMenuBar(self.menubar)
        
        # Actions
        self.actionfile = QtWidgets.QAction("Load CSV", MainWindow)
        self.actionload_csv = QtWidgets.QAction("Load CSV", MainWindow)
        self.menufile.addAction(self.actionfile)
        self.menufile.addAction(self.actionload_csv)
        self.menubar.addAction(self.menufile.menuAction())
        
        # Status bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ready to load CSV file")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Data Structure Project - Product Management"))
        
        # Set tooltips for better UX
        self.lineEdit.setToolTip(_translate("MainWindow", "Enter the URL to scrape data from"))
        self.lineEdit_2.setToolTip(_translate("MainWindow", "Total number of records loaded"))
        self.lineEdit_3.setToolTip(_translate("MainWindow", "Time taken for the last operation"))
        self.comboBox.setToolTip(_translate("MainWindow", "Select column for sorting operations"))
        
        # Algorithm buttons tooltips
        self.bubblesort.setToolTip(_translate("MainWindow", "Bubble Sort - O(n²)"))
        self.insertionsort.setToolTip(_translate("MainWindow", "Insertion Sort - O(n²)"))
        self.selectionsort.setToolTip(_translate("MainWindow", "Selection Sort - O(n²)"))
        self.mergesort.setToolTip(_translate("MainWindow", "Merge Sort - O(n log n)"))
        self.quicksort.setToolTip(_translate("MainWindow", "Quick Sort - O(n log n)"))
        self.countingsort.setToolTip(_translate("MainWindow", "Counting Sort - O(n+k)"))
        self.radixsort.setToolTip(_translate("MainWindow", "Radix Sort - O(nk)"))
        self.bucketsort.setToolTip(_translate("MainWindow", "Bucket Sort - O(n+k)"))


# Sorting Algorithms - Add your implementations here
def bubblesort(arr):
    """
    Bubble Sort - Returns indices in descending order (largest to smallest)
    """
    # Create indexed array: [(value, original_index), ...]
    indexed_arr = [(value, idx) for idx, value in enumerate(arr)]
    n = len(indexed_arr)
    
    # Bubble sort on indexed array
    for i in range(n - 1):
        for j in range(n - i - 1):
            # Compare by value (first element of tuple)
            if indexed_arr[j][0] > indexed_arr[j + 1][0]:  # Descending order
                # Swap
                indexed_arr[j], indexed_arr[j + 1] = indexed_arr[j + 1], indexed_arr[j]
    
    # Return only the indices in sorted order
    return [idx for value, idx in indexed_arr]

def insertion(arr):
    """
    Insertion Sort - Returns indices in descending order (largest to smallest)
    """
    indexed_arr = [(value, idx) for idx, value in enumerate(arr)]

    n = len(indexed_arr)
    for i in range(1, n):
        key = indexed_arr[i]
        j = i - 1
        while j >= 0 and key[0] > indexed_arr[j][0]:  # Use > for descending
            indexed_arr[j + 1] = indexed_arr[j]
            j = j - 1  # ← Must be indented inside the while loop
        indexed_arr[j + 1] = key
    
    return [idx for value, idx in indexed_arr]

# Add your other sorting algorithms here following the same pattern
# def insertionsort(arr):
#     # Your implementation
#     pass

# def selectionsort(arr):
#     # Your implementation
#     pass

# ... etc


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Data Structure Project")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("CS200")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())