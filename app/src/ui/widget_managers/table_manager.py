from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QTableView, QAbstractItemView
from PySide6.QtCore import QTimer
import os

class TableManager():
    def __init__(self, table:QTableWidget):
        self.table = table
        self.file_paths = []

    def populate(self, data):
        self.table.clearContents()

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Arquivo', 'Formato', 'Local'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)
        self.table.setRowCount(len(data))

        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.MultiSelection)

        rows = [
            (os.path.basename(row), row.split('.')[-1].upper(), row)
            for row in data]
        
        self.file_paths = []

        sorted_rows = sorted(rows, key=lambda row: row[2])

        for i, (file, type_, path) in enumerate(sorted_rows):
            item_file = QTableWidgetItem(file)
            item_type = QTableWidgetItem(type_)
            item_path = QTableWidgetItem(path)
            self.table.setItem(i, 0, item_file)
            self.table.setItem(i, 1, item_type)
            self.table.setItem(i, 2, item_path)
            self.file_paths.append(item_path.text())

    def selected_data(self):
        selected_indexes = self.table.selectedIndexes()
        files_path = set()
        if selected_indexes:
            for index in selected_indexes:
                path = self.table.item(index.row(), 2).text()
                files_path.add(path)
        return list(files_path)
    
    def file_path_present(self, file_path):
        return file_path in self.file_paths

    def empty(self):
        return len(self.file_paths) == 0