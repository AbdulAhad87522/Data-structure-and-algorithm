import sys
import os

# Force UTF-8 encoding for console output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
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
        self.original_df = None  # Store original data for reset
        
        # Connect menu action to load CSV
        self.ui.actionfile.triggered.connect(self.load_csv_data)
        self.ui.actionload_csv.triggered.connect(self.load_csv_data)
        
        # Connect sorting buttons
        self.setup_connections()
        
        # Connect URL line edit to scraping function
        self.ui.lineEdit.returnPressed.connect(self.scrape_url)
        
        # Connect search functionality
        self.ui.search_button.clicked.connect(self.search_data)
        self.ui.reset_button.clicked.connect(self.reset_search)
        
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
    
    def scrape_url(self):
        """
        Scrape data from the URL entered by the user
        This function is called when user presses Enter in the URL field
        """
        url = self.ui.lineEdit.text().strip()
        
        if not url:
            QMessageBox.warning(self, "Warning", "Please enter a URL!")
            return
        
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            QMessageBox.warning(self, "Warning", "Please enter a valid URL starting with http:// or https://")
            return
        
        try:
            # Show progress message
            self.ui.statusbar.showMessage(f"Scraping data from {url}...")
            QApplication.processEvents()  # Update UI
            
            # Start timing
            start_time = time.time()
            
            # Call your scraping function here
            # Replace this with your actual scraping code
            scraped_data = self.scrape_data_from_url(url)
            
            # End timing
            end_time = time.time()
            total_time = end_time - start_time
            
            if scraped_data is not None and not scraped_data.empty:
                # Store the scraped data
                self.df = scraped_data
                
                # Clean the data
                self.clean_price_columns()
                
                # Store cleaned data as original for reset
                self.original_df = self.df.copy()
                
                # Display the data
                self.display_dataframe()
                
                # Update stats
                num_rows = len(self.df)
                self.ui.lineEdit_2.setText(str(num_rows))
                self.ui.lineEdit_3.setText(f"{total_time:.6f} seconds")
                
                # Update combo box with column names
                self.ui.comboBox.clear()
                self.ui.comboBox.addItems([str(col) for col in self.df.columns])
                
                # Update secondary combo box
                self.ui.comboBox_2.clear()
                self.ui.comboBox_2.addItem("None (Single Column Sort)")
                self.ui.comboBox_2.addItems([str(col) for col in self.df.columns])
                
                # Update search combo box
                self.ui.search_combo.clear()
                self.ui.search_combo.addItems([str(col) for col in self.df.columns])
                
                # Show success message
                self.ui.statusbar.showMessage(f"Successfully scraped {num_rows} records in {total_time:.2f} seconds")
                QMessageBox.information(self, "Success", 
                    f"Scraped {num_rows} records successfully!\nTime taken: {total_time:.2f} seconds")
            else:
                self.ui.statusbar.showMessage("No data found")
                QMessageBox.warning(self, "Warning", "No data was scraped from the URL!")
                
        except Exception as e:
            self.ui.statusbar.showMessage("Scraping failed")
            QMessageBox.critical(self, "Error", f"Failed to scrape data:\n{str(e)}")
            print(f"Scraping error: {e}")
            import traceback
            traceback.print_exc()
    
    def scrape_data_from_url(self, url):
        """
        Scrape data from Alibaba using Selenium and BeautifulSoup
        
        Parameters:
        - url: The base URL to scrape from (can be modified for pagination)
        
        Returns:
        - pandas DataFrame with the scraped data
        """
        try:
            import undetected_chromedriver as uc
            from bs4 import BeautifulSoup as bs
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
        except ImportError as e:
            QMessageBox.critical(self, "Import Error", 
                f"Required libraries not found:\n{str(e)}\n\n"
                "Please install:\n"
                "pip install undetected-chromedriver\n"
                "pip install beautifulsoup4\n"
                "pip install selenium")
            return None
        
        names = []
        prices = []
        minimunorders = []
        total_sold = []
        suppliers = []
        suppliers_type = []
        suppliers_location = []
        suppliers_name = []
        
        driver = None
        
        try:
            # Initialize Chrome driver
            driver = uc.Chrome()
            
            # Scrape multiple pages (1 to 20)
            for i in range(1, 20):
                # Update status bar with current page
                self.ui.statusbar.showMessage(f"Scraping page {i} of 19...")
                QApplication.processEvents()  # Update UI
                
                page_url = f"https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&from=pcHomeContent&has4Tab=true&keywords=shoes&originKeywords=shoes&tab=all&&page={i}&spm=undefined.pagination.0"
                
                driver.get(page_url)
                
                # Wait for products to load
                WebDriverWait(driver, 25).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "fy26-product-card-content"))
                )
                
                # Parse the page
                soup = bs(driver.page_source, 'html.parser')
                products = soup.find_all('div', class_="fy26-product-card-content")
                
                for product in products:
                    try:
                        name = product.find('h2', class_='searchx-product-e-title')
                        final_name = name.text.strip() if name else 'N/A'
                        
                        price = product.find('div', class_="searchx-product-price-price-main")
                        final_price = price.text.strip() if price else 'N/A'
                        
                        minimun = product.find('div', class_="searchx-moq")
                        final_minimum = minimun.text.strip() if minimun else 'N/A'
                        
                        sold = product.find('div', class_='searchx-sold-order')
                        total = sold.text.strip() if sold else 'N/A'
                        
                        supplier_div = product.find('div', class_='searchx-product-area supplier-area-layout')
                        if supplier_div:
                            supplier_spans = supplier_div.find_all('span')
                            supplier = supplier_div.text.strip()
                            supplier_name = supplier_spans[0].text.strip() if len(supplier_spans) > 0 else 'N/A'
                            supplier_type = supplier_spans[1].text.strip() if len(supplier_spans) > 1 else 'N/A'
                            supplier_location = supplier_spans[2].text.strip() if len(supplier_spans) > 2 else 'N/A'
                        else:
                            supplier = 'N/A'
                            supplier_name = 'N/A'
                            supplier_type = 'N/A'
                            supplier_location = 'N/A'
                        
                        names.append(final_name)
                        prices.append(final_price)
                        minimunorders.append(final_minimum)
                        total_sold.append(total)
                        suppliers.append(supplier_name)
                        suppliers_type.append(supplier_type)
                        suppliers_location.append(supplier_location)
                        suppliers_name.append(supplier)
                        
                        print(f"Total of {len(names)} scraped in {i} iterations")
                        
                    except Exception as e:
                        print(f"Error scraping product: {e}")
                        continue
            
            # Create DataFrame
            df = pd.DataFrame({
                "Names": names,
                "Price": prices,
                "Minimum Orders": minimunorders,
                "Total Sold": total_sold,
                "Supplier Name": suppliers_name,   
                "Supplier's Experience": suppliers,
                "Supplier Country": suppliers_type,
                "Supplier Rating": suppliers_location
            })
            
            print(f"Total products scraped: {len(names)}")
            
            return df
            
        except Exception as e:
            print(f"Error during scraping: {e}")
            import traceback
            traceback.print_exc()
            return None
            
        finally:
            if driver:
                driver.quit()
    
    def display_dataframe(self):
        """Display the current DataFrame in the table widget"""
        if self.df is None or self.df.empty:
            return
        
        # Clear the table widget completely
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)
        self.ui.tableWidget.clear()
        
        # Set up the table dimensions
        num_rows = len(self.df)
        num_cols = len(self.df.columns)
        
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
        
        # Resize columns to fit content
        self.ui.tableWidget.resizeColumnsToContents()
        
        # Also adjust row heights
        self.ui.tableWidget.resizeRowsToContents()
        
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
            
            # Clean price columns
            self.clean_price_columns()
            
            # Store cleaned data as original for reset
            self.original_df = self.df.copy()
            
            # Display the data
            self.display_dataframe()
            
            # Update stats
            num_rows = len(self.df)
            num_cols = len(self.df.columns)
            
            # Update combo box with column names
            self.ui.comboBox.clear()
            self.ui.comboBox.addItems([str(col) for col in self.df.columns])
            
            # Update secondary combo box
            self.ui.comboBox_2.clear()
            self.ui.comboBox_2.addItem("None (Single Column Sort)")
            self.ui.comboBox_2.addItems([str(col) for col in self.df.columns])
            
            # Update search combo box
            self.ui.search_combo.clear()
            self.ui.search_combo.addItems([str(col) for col in self.df.columns])
            
            # Update secondary combo box
            self.ui.comboBox_2.clear()
            self.ui.comboBox_2.addItem("None (Single Column Sort)")
            self.ui.comboBox_2.addItems([str(col) for col in self.df.columns])
            
            # Update stats
            self.ui.lineEdit_2.setText(str(num_rows))
            self.ui.statusbar.showMessage(f"Loaded {num_rows} records from {os.path.basename(file_path)}")
            
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
                print(f"  > Cleaning Price column (removing US$ and currency symbols)")
                self.df[column] = self.df[column].apply(lambda x: self.extract_number_price(x))
            
            elif column == "Minimum Orders":
                print(f"  > Cleaning Minimum Orders column (removing 'Min. order:')")
                self.df[column] = self.df[column].apply(lambda x: self.extract_number_min_orders(x))
            
            elif column == "Total Sold":
                print(f"  > Cleaning Total Sold column (removing 'sold' from end)")
                self.df[column] = self.df[column].apply(lambda x: self.extract_number_sold(x))
            
            elif column == "Supplier's Experience":
                print(f"  > Cleaning Supplier's Experience column (removing 'yr' from end)")
                self.df[column] = self.df[column].apply(lambda x: self.extract_number_experience(x))
            
            else:
                print(f"  > No cleaning needed (not a target column)")


    def extract_number_price(self, value):
        """Extract number from Price column"""
        if pd.isna(value):
            return 0
        
        if isinstance(value, (int, float)):
            return value
        
        value_str = str(value).strip()
        
        if value_str.upper() in ['N/A', 'NA', 'NULL', 'NONE', '-', '']:
            return 0
        
        value_str = re.sub(r'US\$|[$£€¥₹]', '', value_str)
        value_str = re.sub(r'\s+', '', value_str)
        
        numbers = re.findall(r'\d+\.?\d*', value_str)
        
        if numbers:
            try:
                return float(numbers[0])
            except ValueError:
                return 0
        else:
            return 0


    def extract_number_min_orders(self, value):
        """Extract number from Minimum Orders column"""
        if pd.isna(value):
            return 0
        
        if isinstance(value, (int, float)):
            return value
        
        value_str = str(value).strip()
        
        if value_str.upper() in ['N/A', 'NA', 'NULL', 'NONE', '-', '']:
            return 0
        
        value_str = re.sub(r'^min\.?\s*order\s*:\s*', '', value_str, flags=re.IGNORECASE)
        
        numbers = re.findall(r'\d+\.?\d*', value_str)
        
        if numbers:
            try:
                return float(numbers[0])
            except ValueError:
                return 0
        else:
            return 0


    def extract_number_sold(self, value):
        """Extract number from Total Sold column"""
        if pd.isna(value):
            return 0
        
        if isinstance(value, (int, float)):
            return value
        
        value_str = str(value).strip()
        
        if value_str.upper() in ['N/A', 'NA', 'NULL', 'NONE', '-', '']:
            return 0
        
        value_str = re.sub(r'\s*sold\s*$', '', value_str, flags=re.IGNORECASE)
        
        numbers = re.findall(r'\d+\.?\d*', value_str)
        
        if numbers:
            try:
                return float(numbers[0])
            except ValueError:
                return 0
        else:
            return 0


    def extract_number_experience(self, value):
        """Extract number from Supplier's Experience column"""
        if pd.isna(value):
            return 0
        
        if isinstance(value, (int, float)):
            return value
        
        value_str = str(value).strip()
        
        if value_str.upper() in ['N/A', 'NA', 'NULL', 'NONE', '-', '']:
            return 0
        
        value_str = re.sub(r'\s*yrs?\s*$', '', value_str, flags=re.IGNORECASE)
        
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
            QMessageBox.warning(self, "Warning", "Please select a primary column first!")
            return
        
        # Check if secondary column is selected
        secondary_column = self.ui.comboBox_2.currentText()
        use_secondary = secondary_column and secondary_column != "None (Single Column Sort)"
        
        if use_secondary and secondary_column == selected_column:
            QMessageBox.warning(self, "Warning", "Primary and secondary columns cannot be the same!")
            return
        
        # Determine if we're doing single or dual column sort
        if use_secondary:
            self.sort_two_columns(algorithm, selected_column, secondary_column)
        else:
            self.sort_single_column(algorithm, selected_column)
    
    def sort_single_column(self, algorithm, selected_column):
        """Sort by a single column"""
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
        QMessageBox.information(self, "Success", 
            f"{algorithm} completed in {total:.6f} seconds!\nSorted by: {selected_column}")
    
    def sort_two_columns(self, algorithm, primary_column, secondary_column):
        """Sort by two columns - primary first, then secondary as tiebreaker"""
        
        print(f"\n=== TWO-COLUMN SORT ===")
        print(f"Algorithm: {algorithm}")
        print(f"Primary: {primary_column}, Secondary: {secondary_column}")
        
        # Check if linear-time algorithms are used (they don't support multi-column well)
        linear_time_algos = ["Counting Sort", "Radix Sort", "Bucket Sort"]
        if algorithm in linear_time_algos:
            QMessageBox.warning(self, "Warning", 
                f"{algorithm} doesn't support efficient two-column sorting!\n"
                "Please use comparison-based algorithms like Merge Sort or Quick Sort.")
            return
        
        # Get both columns
        primary_data = self.df[primary_column].copy()
        secondary_data = self.df[secondary_column].copy()
        
        # Convert to numeric if possible
        try:
            primary_numeric = pd.to_numeric(primary_data, errors='coerce')
            if primary_numeric.notna().sum() > 0:
                primary_data = primary_numeric.fillna(float('-inf'))
                print(f"Primary column is numeric")
            else:
                primary_data = primary_data.fillna("").astype(str)
                print(f"Primary column is string")
        except:
            primary_data = primary_data.fillna("").astype(str)
            print(f"Primary column is string (exception)")
        
        try:
            secondary_numeric = pd.to_numeric(secondary_data, errors='coerce')
            if secondary_numeric.notna().sum() > 0:
                secondary_data = secondary_numeric.fillna(float('-inf'))
                print(f"Secondary column is numeric")
            else:
                secondary_data = secondary_data.fillna("").astype(str)
                print(f"Secondary column is string")
        except:
            secondary_data = secondary_data.fillna("").astype(str)
            print(f"Secondary column is string (exception)")
        
        # Create combined data: list of tuples (primary_value, secondary_value, original_index)
        combined_data = [(primary_data.iloc[i], secondary_data.iloc[i], i) 
                        for i in range(len(primary_data))]
        
        # Show sample data
        print(f"Sample data (first 3 rows):")
        for i in range(min(3, len(combined_data))):
            print(f"  Row {i}: Primary={combined_data[i][0]}, Secondary={combined_data[i][1]}")
        
        # Start timing
        start_time = time.time()
        
        try:
            # Call appropriate algorithm for two-column sorting
            if algorithm == "Insertion Sort":
                sorted_indices = insertion_two_columns(combined_data)
            elif algorithm == "Bubble Sort":
                sorted_indices = bubblesort_two_columns(combined_data)
            elif algorithm == "Selection Sort":
                sorted_indices = selectionsort_two_columns(combined_data)
            elif algorithm == "Merge Sort":
                sorted_indices = mergesort_two_columns(combined_data)
            elif algorithm == "Quick Sort":
                sorted_indices = quicksort_two_columns(combined_data)
            else:
                QMessageBox.warning(self, "Warning", f"{algorithm} not supported for two-column sorting!")
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
        
        print(f"Sorting completed in {total:.6f} seconds")
        print(f"First 3 sorted indices: {sorted_indices[:3]}")
        
        # Update DataFrame with sorted order
        self.df = self.df.iloc[sorted_indices].reset_index(drop=True)
        
        # Update display
        self.update_table_display()
        
        # Update time field
        self.ui.lineEdit_3.setText(f"{total:.6f} seconds")
        
        # Show success message
        QMessageBox.information(self, "Success", 
            f"{algorithm} completed in {total:.6f} seconds!\n"
            f"Sorted by: {primary_column} (primary), {secondary_column} (secondary)")
    
    def search_data(self):
        """Search for a value in the selected column"""
        if self.df is None:
            QMessageBox.warning(self, "Warning", "Please load data first!")
            return
        
        # Get search parameters
        search_column = self.ui.search_combo.currentText()
        search_value = self.ui.search_input.text().strip()
        
        if not search_column:
            QMessageBox.warning(self, "Warning", "Please select a column to search in!")
            return
        
        if not search_value:
            QMessageBox.warning(self, "Warning", "Please enter a search value!")
            return
        
        try:
            # Get the column data
            column_data = self.original_df[search_column].copy()
            
            # Try to convert search value to numeric if column is numeric
            try:
                numeric_col = pd.to_numeric(column_data, errors='coerce')
                if numeric_col.notna().sum() > 0:
                    # Column is numeric, try to convert search value
                    try:
                        search_value_numeric = float(search_value)
                        # Search for exact match or close match
                        mask = column_data == search_value_numeric
                    except ValueError:
                        # Search value is not numeric, convert column to string
                        mask = column_data.astype(str).str.contains(search_value, case=False, na=False)
                else:
                    # Column is not numeric, do string search
                    mask = column_data.astype(str).str.contains(search_value, case=False, na=False)
            except:
                # Default to string search
                mask = column_data.astype(str).str.contains(search_value, case=False, na=False)
            
            # Filter the dataframe
            filtered_df = self.original_df[mask].copy()
            
            if filtered_df.empty:
                QMessageBox.information(self, "No Results", 
                    f"No records found containing '{search_value}' in column '{search_column}'")
                return
            
            # Update the displayed dataframe
            self.df = filtered_df
            self.update_table_display()
            
            # Update stats
            num_results = len(filtered_df)
            self.ui.lineEdit_2.setText(f"{num_results} (filtered)")
            self.ui.statusbar.showMessage(f"Found {num_results} records matching '{search_value}' in '{search_column}'")
            
            QMessageBox.information(self, "Search Results", 
                f"Found {num_results} matching records!\n"
                f"Use 'Reset Search' button to view all data again.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Search error: {str(e)}")
            print(f"Search error: {e}")
            import traceback
            traceback.print_exc()
    
    def reset_search(self):
        """Reset the search and display all data"""
        if self.original_df is None:
            QMessageBox.warning(self, "Warning", "No data loaded!")
            return
        
        # Restore original dataframe
        self.df = self.original_df.copy()
        self.update_table_display()
        
        # Update stats
        num_rows = len(self.df)
        self.ui.lineEdit_2.setText(str(num_rows))
        self.ui.statusbar.showMessage(f"Showing all {num_rows} records")
        
        # Clear search input
        self.ui.search_input.clear()
        
        QMessageBox.information(self, "Reset", "Displaying all data")


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
        self.lineEdit.setPlaceholderText("Enter website URL here and press Enter...")
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
        self.groupBox_2 = QtWidgets.QGroupBox("Select Columns for Sorting")
        group_layout = QVBoxLayout(self.groupBox_2)
        
        # Primary column label and combo box
        primary_label = QtWidgets.QLabel("Primary Column:")
        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.setMinimumHeight(30)
        group_layout.addWidget(primary_label)
        group_layout.addWidget(self.comboBox)
        
        # Secondary column label and combo box
        secondary_label = QtWidgets.QLabel("Secondary Column (Optional):")
        self.comboBox_2 = QtWidgets.QComboBox()
        self.comboBox_2.setMinimumHeight(30)
        self.comboBox_2.addItem("None (Single Column Sort)")  # Default option
        group_layout.addWidget(secondary_label)
        group_layout.addWidget(self.comboBox_2)
        
        left_panel.addWidget(self.groupBox_2)
        
        # Search section
        self.groupBox_3 = QtWidgets.QGroupBox("Search Data")
        search_layout = QVBoxLayout(self.groupBox_3)
        
        # Search column selection
        search_col_label = QtWidgets.QLabel("Search in Column:")
        self.search_combo = QtWidgets.QComboBox()
        self.search_combo.setMinimumHeight(30)
        search_layout.addWidget(search_col_label)
        search_layout.addWidget(self.search_combo)
        
        # Search input
        search_input_label = QtWidgets.QLabel("Search Value:")
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Enter value to search...")
        self.search_input.setMinimumHeight(30)
        search_layout.addWidget(search_input_label)
        search_layout.addWidget(self.search_input)
        
        # Search buttons
        search_buttons_layout = QHBoxLayout()
        self.search_button = QtWidgets.QPushButton("Search")
        self.search_button.setMinimumHeight(35)
        self.reset_button = QtWidgets.QPushButton("Reset")
        self.reset_button.setMinimumHeight(35)
        search_buttons_layout.addWidget(self.search_button)
        search_buttons_layout.addWidget(self.reset_button)
        search_layout.addLayout(search_buttons_layout)
        
        left_panel.addWidget(self.groupBox_3)
        
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
        self.statusbar.showMessage("Ready to load CSV file or scrape URL")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Data Structure Project - Product Management"))
        
        # Set tooltips for better UX
        self.lineEdit.setToolTip(_translate("MainWindow", "Enter the URL to scrape data from and press Enter"))
        self.lineEdit_2.setToolTip(_translate("MainWindow", "Total number of records loaded"))
        self.lineEdit_3.setToolTip(_translate("MainWindow", "Time taken for the last operation"))
        self.comboBox.setToolTip(_translate("MainWindow", "Select primary column for sorting"))
        self.comboBox_2.setToolTip(_translate("MainWindow", "Select secondary column for sorting (optional)"))
        self.search_combo.setToolTip(_translate("MainWindow", "Select column to search in"))
        self.search_input.setToolTip(_translate("MainWindow", "Enter value to search for"))
        self.search_button.setToolTip(_translate("MainWindow", "Search for matching records"))
        self.reset_button.setToolTip(_translate("MainWindow", "Show all records again"))
        
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
    indexed_arr = [(value, idx) for idx, value in enumerate(arr)]
    mergesort_helper(indexed_arr, 0, len(indexed_arr) - 1)
    return [idx for value, idx in indexed_arr]


def insertion(arr):
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
    indexed_array = [(value, idx) for idx, value in enumerate(arr)]
    n = len(indexed_array)
    
    if n > 0:
        quicksort_helper(indexed_array, 0, n - 1)
    
    return [idx for value, idx in indexed_array]


def countingsort(arr):
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


def counting_sort_by_digit(indexed_array, exp):
    n = len(indexed_array)
    output = [None] * n
    count = [0] * 10
    
    for i in range(n):
        digit = (indexed_array[i][0] // exp) % 10
        count[digit] += 1
    
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    for i in range(n - 1, -1, -1):
        digit = (indexed_array[i][0] // exp) % 10
        output[count[digit] - 1] = indexed_array[i]
        count[digit] -= 1
    
    for i in range(n):
        indexed_array[i] = output[i]


def radixsort(arr):
    if len(arr) == 0:
        return []
    
    if any(x < 0 for x in arr):
        raise ValueError("Radix sort only supports non-negative integers")
    
    indexed_array = [(value, idx) for idx, value in enumerate(arr)]
    max_val = max(val for val, _ in indexed_array)
    
    exp = 1
    while (max_val // exp) > 0:
        counting_sort_by_digit(indexed_array, exp)
        exp *= 10
    
    return [idx for value, idx in indexed_array]


def insertionSort(indexed_array):
    for i in range(1, len(indexed_array)):
        key = indexed_array[i]
        j = i - 1
        while j >= 0 and indexed_array[j][0] > key[0]:
            indexed_array[j + 1] = indexed_array[j]
            j -= 1
        indexed_array[j + 1] = key


def bucketsort(arr):
    n = len(arr)
    if n == 0:
        return []
    
    indexed_array = [(value, idx) for idx, value in enumerate(arr)]
    
    min_val = min(val for val, _ in indexed_array)
    max_val = max(val for val, _ in indexed_array)
    
    if min_val == max_val:
        return [idx for _, idx in indexed_array]
    
    buckets = [[] for _ in range(n)]
    range_val = max_val - min_val
    
    for value, idx in indexed_array:
        bucket_idx = int((value - min_val) / range_val * (n - 1))
        buckets[bucket_idx].append((value, idx))
    
    for bucket in buckets:
        insertionSort(bucket)
    
    result = []
    for bucket in buckets:
        result.extend(bucket)
    
    return [idx for value, idx in result]


# ========== TWO-COLUMN SORTING ALGORITHMS ==========

def compare_two_values(a, b):
    """
    Compare two tuples (primary, secondary)
    Returns: True if a <= b (for ascending order)
    """
    # Compare primary values first
    if a[0] != b[0]:
        return a[0] < b[0]
    # If primary values are equal, compare secondary
    return a[1] <= b[1]


def bubblesort_two_columns(arr):
    """Bubble Sort for two columns"""
    n = len(arr)
    
    for i in range(n - 1):
        for j in range(n - i - 1):
            # Compare: if arr[j] > arr[j+1], swap
            if not compare_two_values(arr[j][:2], arr[j + 1][:2]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    
    return [item[2] for item in arr]


def insertion_two_columns(arr):
    """Insertion Sort for two columns"""
    n = len(arr)
    
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        # Move elements that are greater than key
        while j >= 0 and not compare_two_values(arr[j][:2], key[:2]):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    
    return [item[2] for item in arr]


def selectionsort_two_columns(arr):
    """Selection Sort for two columns"""
    n = len(arr)
    
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            # Find minimum element
            if compare_two_values(arr[j][:2], arr[min_idx][:2]) and arr[j][:2] != arr[min_idx][:2]:
                min_idx = j
        if min_idx != i:
            arr[min_idx], arr[i] = arr[i], arr[min_idx]
    
    return [item[2] for item in arr]


def merge_two_columns(arr, st, mid, end):
    """Merge function for two-column merge sort"""
    temp = []
    i = st
    j = mid + 1
    
    while i <= mid and j <= end:
        # Compare (primary, secondary) tuples
        if compare_two_values(arr[i][:2], arr[j][:2]):
            temp.append(arr[i])
            i += 1
        else:
            temp.append(arr[j])
            j += 1
    
    while i <= mid:
        temp.append(arr[i])
        i += 1
    
    while j <= end:
        temp.append(arr[j])
        j += 1
    
    for i in range(len(temp)):
        arr[i + st] = temp[i]


def mergesort_two_columns_helper(arr, st, end):
    """Merge sort helper for two columns"""
    if st < end:
        mid = st + (end - st) // 2
        mergesort_two_columns_helper(arr, st, mid)
        mergesort_two_columns_helper(arr, mid + 1, end)
        merge_two_columns(arr, st, mid, end)


def mergesort_two_columns(arr):
    """Merge Sort for two columns"""
    if len(arr) > 0:
        mergesort_two_columns_helper(arr, 0, len(arr) - 1)
    return [item[2] for item in arr]


def partition_two_columns(arr, q, r):
    """Partition function for two-column quick sort"""
    pivot = arr[r]
    i = q - 1
    
    for j in range(q, r):
        # Compare with pivot
        if compare_two_values(arr[j][:2], pivot[:2]):
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[r] = arr[r], arr[i + 1]
    return i + 1


def quicksort_two_columns_helper(arr, q, r):
    """Quick sort helper for two columns"""
    if q < r:
        p = partition_two_columns(arr, q, r)
        quicksort_two_columns_helper(arr, q, p - 1)
        quicksort_two_columns_helper(arr, p + 1, r)


def quicksort_two_columns(arr):
    """Quick Sort for two columns"""
    n = len(arr)
    if n > 0:
        quicksort_two_columns_helper(arr, 0, n - 1)
    return [item[2] for item in arr]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setApplicationName("Data Structure Project")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("CS200")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())