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
                # Try different encodings
                try:
                    self.df = pd.read_csv(file_path, encoding='utf-8')
                except UnicodeDecodeError:
                    try:
                        self.df = pd.read_csv(file_path, encoding='latin-1')
                    except:
                        self.df = pd.read_csv(file_path, encoding='ISO-8859-1')
                
                print(f"CSV loaded successfully. Shape: {self.df.shape}")
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
            
            # Clean price columns - Extract first number from formats like "US$ 30-90"
            self.clean_price_columns()
            
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

    def clean_price_columns(self):
        """
        Clean specific columns based on their exact names
        """
        print("\n=== Starting Column-Specific Cleaning ===")
        
        for column in self.df.columns:
            print(f"\nProcessing column: {column}")
            
            # Apply cleaning based on exact column name
            if column == "Price":
                print(f"  → Cleaning Price column (removing US$ and currency symbols)")
                self.df[column] = self.df[column].apply(lambda x: self.extract_number_price(x))
            
            elif column == "Minimum Orders":
                print(f"  → Cleaning Minimum Orders column (removing 'Min. order:')")
                self.df[column] = self.df[column].apply(lambda x: self.extract_number_min_orders(x))
            
            elif column == "Total Sold":
                print(f"  → Cleaning Total Sold column (removing 'sold' from end)")
                self.df[column] = self.df[column].apply(lambda x: self.extract_number_sold(x))
            
            elif column == "Supplier's Experience":
                print(f"  → Cleaning Supplier's Experience column (removing 'yr' from end)")
                self.df[column] = self.df[column].apply(lambda x: self.extract_number_experience(x))
            
            else:
                print(f"  → No cleaning needed (not a target column)")


    def extract_number_price(self, value):
        """
        Extract number from Price column - removes US$ and other currency symbols
        Examples: "US$ 30-90" -> 30, "$50.99" -> 50.99
        """
        # If already numeric, return as is
        if pd.isna(value):
            return 0
        
        if isinstance(value, (int, float)):
            return value
        
        # Convert to string
        value_str = str(value).strip()
        
        # Check for N/A or similar values
        if value_str.upper() in ['N/A', 'NA', 'NULL', 'NONE', '-', '']:
            return 0
        
        # Remove currency symbols: US$, $, £, €, ¥, ₹
        value_str = re.sub(r'US\$|[$£€¥₹]', '', value_str)
        
        # Remove spaces
        value_str = re.sub(r'\s+', '', value_str)
        
        # Find all numbers (including decimals)
        numbers = re.findall(r'\d+\.?\d*', value_str)
        
        if numbers:
            try:
                return float(numbers[0])
            except ValueError:
                return 0
        else:
            return 0


    def extract_number_min_orders(self, value):
        """
        Extract number from Minimum Orders column - removes "Min. order:" from start
        Examples: "Min. order: 3 pieces" -> 3
        """
        # If already numeric, return as is
        if pd.isna(value):
            return 0
        
        if isinstance(value, (int, float)):
            return value
        
        # Convert to string
        value_str = str(value).strip()
        
        # Check for N/A or similar values
        if value_str.upper() in ['N/A', 'NA', 'NULL', 'NONE', '-', '']:
            return 0
        
        # Remove "Min. order:" from the beginning (case-insensitive)
        value_str = re.sub(r'^min\.?\s*order\s*:\s*', '', value_str, flags=re.IGNORECASE)
        
        # Find all numbers (including decimals)
        numbers = re.findall(r'\d+\.?\d*', value_str)
        
        if numbers:
            try:
                return float(numbers[0])
            except ValueError:
                return 0
        else:
            return 0


    def extract_number_sold(self, value):
        """
        Extract number from Total Sold column - removes "sold" from end
        Examples: "122 sold" -> 122
        """
        # If already numeric, return as is
        if pd.isna(value):
            return 0
        
        if isinstance(value, (int, float)):
            return value
        
        # Convert to string
        value_str = str(value).strip()
        
        # Check for N/A or similar values
        if value_str.upper() in ['N/A', 'NA', 'NULL', 'NONE', '-', '']:
            return 0
        
        # Remove "sold" from the end (case-insensitive)
        value_str = re.sub(r'\s*sold\s*$', '', value_str, flags=re.IGNORECASE)
        
        # Find all numbers (including decimals)
        numbers = re.findall(r'\d+\.?\d*', value_str)
        
        if numbers:
            try:
                return float(numbers[0])
            except ValueError:
                return 0
        else:
            return 0


    def extract_number_experience(self, value):
        """
        Extract number from Supplier's Experience column - removes "yr" or "yrs" from end
        Examples: "9 yrs" -> 9, "5 yr" -> 5
        """
        # If already numeric, return as is
        if pd.isna(value):
            return 0
        
        if isinstance(value, (int, float)):
            return value
        
        # Convert to string
        value_str = str(value).strip()
        
        # Check for N/A or similar values
        if value_str.upper() in ['N/A', 'NA', 'NULL', 'NONE', '-', '']:
            return 0
        
        # Remove "yr" or "yrs" from the end (case-insensitive)
        value_str = re.sub(r'\s*yrs?\s*$', '', value_str, flags=re.IGNORECASE)
        
        # Find all numbers (including decimals)
        numbers = re.findall(r'\d+\.?\d*', value_str)
        
        if numbers:
            try:
                return float(numbers[0])
            except ValueError:
                return 0
        else:
            return 0
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
                    # Replace NaN with a very large negative number so they sort to the end
                    column_data = numeric_data.fillna(float('-inf')).tolist()
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
        
        # Show success message
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



def merge(indexed_arr, st, mid, end):
    temp = []
    i = st 
    j = mid + 1
    
    # Compare in descending order (larger values first)
    while i <= mid and j <= end:
        if indexed_arr[i][0] <= indexed_arr[j][0]:  # >= for descending
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
    """
    Merge Sort - Returns indices in descending order (largest to smallest)
    """
    indexed_arr = [(value, idx) for idx, value in enumerate(arr)]
    
    mergesort_helper(indexed_arr, 0, len(indexed_arr) - 1)
    
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
        while j >= 0 and key[0] < indexed_arr[j][0]:  # Use > for descending
            indexed_arr[j + 1] = indexed_arr[j]
            j = j - 1  # ← Must be indented inside the while loop
        indexed_arr[j + 1] = key
    
    return [idx for value, idx in indexed_arr]

def selectionsort(arr):
    indexed_arrray = [(value,idx) for idx , value in enumerate(arr)]
    n = len(indexed_arrray)
    for i in range(n-1):
        min_idx = i
        for j in range(i+1 , n):
            if(indexed_arrray[j][0] < indexed_arrray[min_idx][0]):
                min_idx = j
        if min_idx != i:
            indexed_arrray[min_idx] , indexed_arrray[i] = indexed_arrray[i] , indexed_arrray[min_idx]
    return [idx for value, idx in indexed_arrray]


def partition(indexed_array, q, r):
    """Partition for ascending order"""
    x = indexed_array[r][0]  # Pivot value
    i = q - 1
    
    for j in range(q, r):
        if indexed_array[j][0] <= x:  # <= for ascending order
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
    """
    Quick Sort - Returns indices in ascending order (smallest to largest)
    """
    indexed_array = [(value, idx) for idx, value in enumerate(arr)]
    n = len(indexed_array)
    
    if n > 0:
        quicksort_helper(indexed_array, 0, n - 1)
    
    return [idx for value, idx in indexed_array]


def countingsort(arr):
    """
    Counting Sort - Returns indices in ascending order (smallest to largest)
    Works with integers only
    """
    if len(arr) == 0:
        return []
    
    # Ensure all values are integers
    try:
        indexed_array = [(int(value), idx) for idx, value in enumerate(arr)]
    except (ValueError, TypeError) as e:
        raise ValueError(f"Counting Sort requires integer values: {e}")
    
    # Find min and max values
    min_val = min(val for val, _ in indexed_array)
    max_val = max(val for val, _ in indexed_array)
    
    range_size = max_val - min_val + 1
    count = [0] * range_size
    output = [None] * len(indexed_array)
    
    # Count occurrences
    for value, idx in indexed_array:
        count[value - min_val] += 1
    
    # Cumulative count (for ascending order, iterate forwards)
    for i in range(1, range_size):
        count[i] += count[i - 1]
    
    # Build output array (iterate backwards to maintain stability)
    for i in range(len(indexed_array) - 1, -1, -1):
        value, idx = indexed_array[i]
        output[count[value - min_val] - 1] = (value, idx)
        count[value - min_val] -= 1
    
    return [idx for value, idx in output]

def counting_sort_by_digit(indexed_array, exp):
    """Helper function for radix sort - sorts by a specific digit"""
    n = len(indexed_array)
    output = [None] * n
    count = [0] * 10
    
    # Count occurrences of each digit
    for i in range(n):
        digit = (indexed_array[i][0] // exp) % 10
        count[digit] += 1
    
    # Cumulative count
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    # Build output array (iterate backwards for stability)
    for i in range(n - 1, -1, -1):
        digit = (indexed_array[i][0] // exp) % 10
        output[count[digit] - 1] = indexed_array[i]
        count[digit] -= 1
    
    # Copy back to original array
    for i in range(n):
        indexed_array[i] = output[i]


def radixsort(arr):
    """
    Radix Sort - Returns indices in ascending order (smallest to largest)
    Only works with non-negative integers
    """
    if len(arr) == 0:
        return []
    
    # Check for negative values
    if any(x < 0 for x in arr):
        raise ValueError("Radix sort only supports non-negative integers")
    
    indexed_array = [(value, idx) for idx, value in enumerate(arr)]
    max_val = max(val for val, _ in indexed_array)
    
    # Sort by each digit, starting from least significant
    exp = 1
    while (max_val // exp) > 0:
        counting_sort_by_digit(indexed_array, exp)
        exp *= 10
    
    return [idx for value, idx in indexed_array]


def insertionSort(indexed_array):
    """Helper insertion sort for buckets (ascending)"""
    for i in range(1, len(indexed_array)):
        key = indexed_array[i]
        j = i - 1
        while j >= 0 and indexed_array[j][0] > key[0]:
            indexed_array[j + 1] = indexed_array[j]
            j -= 1
        indexed_array[j + 1] = key


def bucketsort(arr):
    """
    Bucket Sort - Returns indices in ascending order (smallest to largest)
    """
    n = len(arr)
    if n == 0:
        return []
    
    indexed_array = [(value, idx) for idx, value in enumerate(arr)]
    
    min_val = min(val for val, _ in indexed_array)
    max_val = max(val for val, _ in indexed_array)
    
    # If all values are the same, return as-is
    if min_val == max_val:
        return [idx for _, idx in indexed_array]
    
    # Create buckets
    buckets = [[] for _ in range(n)]
    range_val = max_val - min_val
    
    # Distribute elements into buckets
    for value, idx in indexed_array:
        bucket_idx = int((value - min_val) / range_val * (n - 1))
        buckets[bucket_idx].append((value, idx))
    
    # Sort each bucket
    for bucket in buckets:
        insertionSort(bucket)
    
    # Collect from all buckets in order (ascending)
    result = []
    for bucket in buckets:
        result.extend(bucket)
    
    return [idx for value, idx in result]

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