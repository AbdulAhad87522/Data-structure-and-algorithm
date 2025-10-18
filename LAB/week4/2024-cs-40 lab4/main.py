
import sys
import os
import time
import pandas as pd
import re
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
            
            # Clean all columns based on their content
            self.clean_all_columns()
            
            # Replace all NaN/NA values with 0
            self.df = self.df.fillna(0)
            
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
                            display_value = '0'
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

    def clean_all_columns(self):
        """
        Clean all columns in the dataframe based on their names and content
        """
        print("\n=== Starting Column Cleaning ===")
        
        for column in self.df.columns:
            column_lower = str(column).lower()
            print(f"\nProcessing column: {column}")
            
            # Check if this is a supplier name column - skip cleaning
            if any(keyword in column_lower for keyword in ['supplier', 'name', 'company', 'vendor']):
                # Check if it looks like numeric data or actual names
                sample = self.df[column].dropna().iloc[0] if not self.df[column].dropna().empty else None
                if sample and isinstance(sample, str) and not re.search(r'\d', sample):
                    print(f"  → Skipping (Supplier Name column)")
                    continue
            
            # Get a sample value to determine what kind of cleaning is needed
            sample_value = self.df[column].dropna().iloc[0] if not self.df[column].dropna().empty else None
            
            if sample_value is None:
                continue
            
            needs_cleaning = False
            
            # Check if it's already numeric
            if isinstance(sample_value, (int, float)):
                print(f"  → Already numeric, no cleaning needed")
                continue
            
            # Convert to string for pattern matching
            sample_str = str(sample_value)
            print(f"  → Sample value: {sample_str}")
            
            # Detect patterns that need cleaning
            patterns_found = []
            
            # Price pattern: US$ 30-90, $50, £45.99
            if re.search(r'[$£€¥₹]|US\$', sample_str):
                patterns_found.append("price/currency")
                needs_cleaning = True
            
            # Minimum order pattern: Min. order: 3 pieces
            if re.search(r'min\.?\s*order', sample_str, re.IGNORECASE):
                patterns_found.append("minimum order")
                needs_cleaning = True
            
            # Sold pattern: 122 sold
            if re.search(r'\d+\s*sold', sample_str, re.IGNORECASE):
                patterns_found.append("sold")
                needs_cleaning = True
            
            # Experience/time pattern: 9 yrs, 5 years, 3 months
            if re.search(r'\d+\s*(yr|year|month|day|hour)', sample_str, re.IGNORECASE):
                patterns_found.append("time/experience")
                needs_cleaning = True
            
            # Measurement pattern: 10 kg, 5 lbs, 180 cm
            if re.search(r'\d+\s*(kg|lb|cm|inch|m\b)', sample_str, re.IGNORECASE):
                patterns_found.append("measurement")
                needs_cleaning = True
            
            # Pieces pattern: 3 pieces, 100 pcs
            if re.search(r'\d+\s*(piece|pcs|pc)', sample_str, re.IGNORECASE):
                patterns_found.append("pieces")
                needs_cleaning = True
            
            if needs_cleaning:
                print(f"  → Patterns detected: {', '.join(patterns_found)}")
                print(f"  → Applying cleaning...")
                self.df[column] = self.df[column].apply(self.extract_number)
                print(f"  → Cleaning complete")
            else:
                print(f"  → No cleaning needed")

    def extract_number(self, value):
        """
        Extract numeric value from various formats:
        - "US$ 30-90" -> 30
        - "$50.99" -> 50.99
        - "Min. order: 3 pieces" -> 3
        - "122 sold" -> 122
        - "9 yrs" -> 9
        - "5 years" -> 5
        - "10 kg" -> 10
        - "N/A" -> 0
        """
        # If already numeric, return as is
        if pd.isna(value):
            return 0
        
        if isinstance(value, (int, float)):
            return value
        
        # Convert to string
        value_str = str(value).strip()
        
        # Check for N/A or similar values
        if value_str.upper() in ['N/A', 'NA', 'NULL', 'NONE', '-', '', 'NAN']:
            return 0
        
        # Remove common prefixes and text
        # Handle "Min. order: 3 pieces" format
        value_str = re.sub(r'min\.?\s*order\s*:', '', value_str, flags=re.IGNORECASE)
        
        # Remove currency symbols
        value_str = re.sub(r'US\$|[$£€¥₹]', '', value_str)
        
        # Remove text suffixes with word boundaries
        value_str = re.sub(r'\b(yr|years?|months?|days?|hours?|mins?|minutes?|secs?|seconds?)\b', '', value_str, flags=re.IGNORECASE)
        value_str = re.sub(r'\b(sold|pieces?|pcs?|pc)\b', '', value_str, flags=re.IGNORECASE)
        value_str = re.sub(r'\b(kg|kgs?|lb|lbs?|pounds?|cm|meter|meters?|m|inch|inches)\b', '', value_str, flags=re.IGNORECASE)
        
        # Remove extra spaces and colons
        value_str = re.sub(r'[:\s]+', ' ', value_str).strip()
        
        # Find all numbers (including decimals)
        numbers = re.findall(r'\d+\.?\d*', value_str)
        
        if numbers:
            # Return the first number as float
            try:
                return float(numbers[0])
            except ValueError:
                return 0
        else:
            # No number found
            return 0

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
                    display_value = '0'
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
        
        # Get the original column data from dataframe
        column_data = self.df[selected_column].copy()
        is_numeric = False
        
        # Check if this is a linear-time algorithm that requires integers
        linear_time_algos = ["Counting Sort", "Radix Sort", "Bucket Sort"]
        
        # Try to convert to numeric
        try:
            numeric_data = pd.to_numeric(column_data, errors='coerce')
            
            # Check if we have any valid numeric values
            non_nan_count = numeric_data.notna().sum()
            
            if non_nan_count > 0:  # At least some values are numeric
                is_numeric = True
                
                # For linear time algorithms, check if data can be converted to integers
                if algorithm in linear_time_algos:
                    try:
                        # Check for negative values in Radix Sort
                        if algorithm == "Radix Sort" and (numeric_data.dropna() < 0).any():
                            QMessageBox.warning(self, "Warning", 
                                "Radix Sort only works with non-negative integers!\n"
                                "Please select a different algorithm or column.")
                            return
                        
                        # Convert to integers, replacing NaN with 0
                        column_data = numeric_data.fillna(0).astype(int).tolist()
                        
                    except (ValueError, OverflowError):
                        QMessageBox.warning(self, "Warning", 
                            f"{algorithm} requires integer data!\n"
                            f"The selected column contains values that cannot be converted to integers.\n"
                            "Please select a different algorithm or column.")
                        return
                else:
                    # For other algorithms, use numeric values (can be float)
                    # Replace NaN with 0
                    column_data = numeric_data.fillna(0).tolist()
            else:
                # No valid numeric values found
                is_numeric = False
                
        except Exception as e:
            print(f"Error during numeric conversion: {e}")
            is_numeric = False
        
        # If not numeric, treat as strings
        if not is_numeric:
            if algorithm in linear_time_algos:
                QMessageBox.warning(self, "Warning", 
                    f"{algorithm} requires numeric (integer) data!\n"
                    "Please select a column with numeric values.")
                return
            # Convert to strings, replacing NaN with empty string
            column_data = column_data.fillna("").astype(str).tolist()
        
        # Start timing
        start_time = time.time()
        
        try:
            # Call appropriate algorithm
            if algorithm == "Insertion Sort":
                sorted_indices = insertion(column_data)
            elif algorithm == "Bubble Sort":
                sorted_indices = bubblesort(column_data)
            elif algorithm == "Selection Sort":
                sorted_indices = selectionsort(column_data)
            elif algorithm == "Merge Sort":
                sorted_indices = mergesort(column_data)
            elif algorithm == "Quick Sort":
                sorted_indices = quicksort(column_data)
            elif algorithm == "Counting Sort":
                sorted_indices = countingsort(column_data)
            elif algorithm == "Radix Sort":
                sorted_indices = radixsort(column_data)
            elif algorithm == "Bucket Sort":
                sorted_indices = bucketsort(column_data)
            else:
                QMessageBox.warning(self, "Warning", f"{algorithm} not recognized!")
                return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error during {algorithm}:\n{str(e)}")
            print(f"Sorting error: {e}")
            import traceback
            traceback.print_exc()
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


# Sorting Algorithms
def bubblesort(arr):
    """Bubble Sort - Returns indices in ascending order"""
    indexed_arr = [(value, idx) for idx, value in enumerate(arr)]
    n = len(indexed_arr)
    
    for i in range(n - 1):
        for j in range(n - i - 1):
            if indexed_arr[j][0] > indexed_arr[j + 1][0]:
                indexed_arr[j], indexed_arr[j + 1] = indexed_arr[j + 1], indexed_arr[j]
    
    return [idx for value, idx in indexed_arr]


def merge(indexed_arr, st, mid, end):
    temp = []
    i = st 
    j = mid + 1
    
    while i <= mid and j <= end:
        if indexed_arr[i][0] <= indexed_arr[j][0]:
            temp.append(indexed_arr[i])
            i = i + 1
        else:
            temp.append(indexed_arr[j])
            j = j + 1
    
    while i <= mid:
        temp.append(indexed_arr[i])
        i = i + 1
                
    while j <= end:
        temp.append(indexed_arr[j])
        j = j + 1
    
    for i in range(len(temp)):
        indexed_arr[i + st] = temp[i]

    
def mergesort_helper(indexed_arr, st, end):
    if st < end:
        mid = st + (end - st) // 2
        mergesort_helper(indexed_arr, st, mid)
        mergesort_helper(indexed_arr, mid + 1, end)
        merge(indexed_arr, st, mid, end)


def mergesort(arr):
    """Merge Sort - Returns indices in ascending order"""
    indexed_arr = [(value, idx) for idx, value in enumerate(arr)]
    mergesort_helper(indexed_arr, 0, len(indexed_arr) - 1)
    return [idx for value, idx in indexed_arr]


def insertion(arr):
    """Insertion Sort - Returns indices in ascending order"""
    indexed_arr = [(value, idx) for idx, value in enumerate(arr)]
    n = len(indexed_arr)
    
    for i in range(1, n):
        key = indexed_arr[i]
        j = i - 1
        while j >= 0 and key[0] < indexed_arr[j][0]:
            indexed_arr[j + 1] = indexed_arr[j]
            j = j - 1
        indexed_arr[j + 1] = key
    
    return [idx for value, idx in indexed_arr]


def selectionsort(arr):
    """Selection Sort - Returns indices in ascending order"""
    indexed_array = [(value, idx) for idx, value in enumerate(arr)]
    n = len(indexed_array)
    
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if indexed_array[j][0] < indexed_array[min_idx][0]:
                min_idx = j
        if min_idx != i:
            indexed_array[min_idx], indexed_array[i] = indexed_array[i], indexed_array[min_idx]
    
    return [idx for value, idx in indexed_array]


def partition(indexed_array, q, r):
    """Partition for ascending order"""
    x = indexed_array[r][0]
    i = q - 1
    
    for j in range(q, r):
        if indexed_array[j][0] <= x:
            i = i + 1
            indexed_array[i], indexed_array[j] = indexed_array[j], indexed_array[i]
    
    indexed_array[i + 1], indexed_array[r] = indexed_array[r], indexed_array[i + 1]
    return i + 1


def quicksort_helper(indexed_array, q, r):
    if q < r:
        p = partition(indexed_array, q, r)
        quicksort_helper(indexed_array, q, p - 1)
        quicksort_helper(indexed_array, p + 1, r)


def quicksort(arr):
    """Quick Sort - Returns indices in ascending order"""
    indexed_array = [(value, idx) for idx, value in enumerate(arr)]
    n = len(indexed_array)
    
    if n > 0:
        quicksort_helper(indexed_array, 0, n - 1)
    
    return [idx for value, idx in indexed_array]


def countingsort(arr):
    """Counting Sort - Returns indices in ascending order"""
    if len(arr) == 0:
        return []
    
    try:
        indexed_array = [(int(value), idx) for idx, value in enumerate(arr)]
    except (ValueError, TypeError) as e:
        raise ValueError(f"Counting Sort requires integer values: {e}")
    
    min_val = min(val for val, _ in indexed_array)
    max_val = max(val for val, _ in indexed_array)
    
    range_size = max_val - min_val + 1
    count = [0] * range_size
    output = [None] * len(indexed_array)
    
    for value, idx in indexed_array:
        count[value - min_val] += 1
    
    for i in range(1, range_size):
        count[i] += count[i - 1]
    
    for i in range(len(indexed_array) - 1, -1, -1):
        value, idx = indexed_array[i]
        output[count[value - min_val] - 1] = (value, idx)
        count[value - min_val] -= 1
    
    return [idx for value, idx in output]


