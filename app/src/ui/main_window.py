from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import (QLabel, QPushButton, QVBoxLayout, QMainWindow,
    QWidget, QTextEdit, QFileDialog, QSizePolicy, QMessageBox, QSpacerItem)
from PySide6.QtCore import Qt

from src.ui.dialogs.settings_dialog import SettingsDialog
from src.ui.dialogs.loading_dialog import LoadingDialog
from src.ui.dialogs.context_dialog import ContextDialog

from src.ui.widget_managers.status_manager import StatusManager
from src.ui.widget_managers.table_manager import TableManager
from src.ui.widget_managers.question_manager import QuestionManager

from src.controllers.main_controller import MainController

from src.ui.widgets.table_widget import TableWidget
from src.ui.widgets.labels import DescriptionLabel, ContentsLabel
from src.ui.widgets.horizontal_line import HorizontalLine

from src.ui.layouts.main_layout import MainLayout

from src.ui.widgets.text_edits import QuestionTextEdit, AnswearTextEdit

def calc_price(question, context, answear):
    aprox_input_tokens = (len(question) + len(context)) / 4
    aprox_output_tokens = len(answear) / 4
    dolars = (aprox_input_tokens/1000) * 0.00015 + (aprox_output_tokens/1000) * 0.00060
    reais = dolars*6
    print(f'Custo aproximado: U$ {dolars} (R$ {reais})')

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.controller = MainController(self)

        # Window settings
        geometry = self.screen().availableGeometry()
        self.setMinimumSize(geometry.width() * 0.7, geometry.height() * 0.7)
        self.setWindowTitle('Assistente FAPEG')
        self.setFont(QFont('Segoe UI', 10))

        # Layouts
        self.main_layout = MainLayout()
        self.assistent_layout = QVBoxLayout()
        self.files_layout = QVBoxLayout()

        self.main_layout.addLayout(self.assistent_layout)
        self.main_layout.addItem(QSpacerItem(10, 0))
        self.main_layout.addLayout(self.files_layout)

        self.main_layout.setStretch(0, 6)
        self.main_layout.setStretch(2, 4)

        # Central Widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_layout)

        # Buttons
        self.ask_button = QPushButton('Perguntar')
        self.show_context_dialog_button = QPushButton('Ver contexto')
        self.add_file_button = QPushButton('Adicionar novo arquivo')
        self.delete_files_button = QPushButton('Remover arquivos selecionados')

        self.ask_button.setMinimumSize(200, 30)
        self.ask_button.setMaximumWidth(200)
        self.add_file_button.setMinimumSize(200, 30)
        self.add_file_button.setMaximumWidth(200)
        self.delete_files_button.setMinimumSize(200, 30)
        self.delete_files_button.setMaximumWidth(200)

        self.ask_button.clicked.connect(self.ask)
        self.add_file_button.clicked.connect(self.add_file)
        self.delete_files_button.clicked.connect(self.delete_files)
        self.show_context_dialog_button.clicked.connect(self.show_context_dialog)

        # Table creation
        table = TableWidget()

        # Widgets
        question = QuestionTextEdit()
        self.answear = AnswearTextEdit()

        self.assistent_layout.addWidget(DescriptionLabel())
        self.assistent_layout.addItem(QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.assistent_layout.addWidget(HorizontalLine())
        self.assistent_layout.addWidget(QLabel('Insira sua pergunta ou comando abaixo:'))
        self.assistent_layout.addWidget(question)
        self.assistent_layout.addWidget(self.ask_button, alignment=Qt.AlignCenter)
        self.assistent_layout.addWidget(QLabel('Resposta:'))
        self.assistent_layout.addWidget(self.answear)
        self.assistent_layout.addWidget(self.show_context_dialog_button)

        self.files_layout.addWidget(ContentsLabel())
        self.files_layout.addWidget(table)
        self.files_layout.addWidget(self.add_file_button, alignment=Qt.AlignCenter)
        self.files_layout.addWidget(self.delete_files_button, alignment=Qt.AlignCenter)

        # Menu bar
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu('Arquivo')

        settings_action = QAction('Configurações', self)
        settings_action.triggered.connect(self.show_settings_dialog)
        self.file_menu.addAction(settings_action)

        # Status Bar
        status = self.statusBar()

        # Managers
        self.table_manager = TableManager(table)
        self.status_manager = StatusManager(status)  
        self.question_manager = QuestionManager(question)

        self.populate_table()

    def clear_status(self):
        self.status_manager.clear()

    def update_status(self, type_, message, time_out=5000):
        self.status_manager.update(type_, message, time_out)

    def show_message_box(self, message_type, message, buttons=None):
        if not buttons:
            buttons = QMessageBox.Ok

        match message_type:
            case 'Confirmação':
                message_box = QMessageBox()
                message_box.setWindowTitle(message_type)
                message_box.setText(message)
                message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                message_box.button(QMessageBox.Yes).setText("Sim")
                message_box.button(QMessageBox.No).setText("Não")
                return message_box.exec()
            case _:
                return QMessageBox.critical(self, message_type, message, buttons)

    def show_settings_dialog(self):
        try:
            dialog = SettingsDialog(self.controller.ai, self.controller)
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to open settings dialog: {e}')

    def show_context_dialog(self):
        context = self.controller.ai.last_context
        if context:
            self.context_text = context
            dialog = ContextDialog(self.controller.ai.last_question, '\n\n'.join(doc.page_content for doc in context))
            calc_price(self.question_text, self.context_text, self.answear_text)
            dialog.exec()
        else:
            self.show_message_box('Erro', 'Parece que você ainda não fez uma pergunta ou deu um comando para gerar um contexto.', QMessageBox.Ok)

    def show_loading_dialog(self, message):
        self.loading_dialog = LoadingDialog(message)
        self.loading_dialog.show()
        self.setEnabled(False)

    def close_loading_dialog(self):
        self.loading_dialog.close()
        self.setEnabled(True)

    def handle_answear(self, answear):
        self.answear.setMarkdown(answear)
        self.close_loading_dialog()
        self.answear_text = answear

    def ask(self):
        if not self.controller.api_key_provided:
            self.show_message_box('Erro', 'Para utilizar este programa você precisa cadastrar uma "Chave OpenAI" em "Arquivo > Configurações"')
            return
        if not self.controller.valid_api_key:
            self.show_message_box('Erro', 'Sua "Chave OpenAI" não é válida, tente alterá-la em "Arquivo > Configurações"')
            return
        if self.table_manager.empty():
            self.show_message_box('Erro', 'Você precisa adicionar ao menos um arquivo para fazer uma pergunta ou dar um comando.', QMessageBox.Ok)
            return
        # question_manager.py
        question = self.question_manager.get_question()
        self.question_text = question
        if not question:
            self.show_message_box('Erro', 'Parece que você não inseriu uma pergunta ainda.', QMessageBox.Ok)
            return

        # table manager
        contents = self.table_manager.selected_data()

        self.show_loading_dialog('Lendo o(s) documento(s) e elaborando resposta.')
        self.controller.ask(question, contents, self.handle_answear)

    def handle_file_addition(self):
        self.populate_table()
        self.close_loading_dialog()

    def add_file(self):
        if not self.controller.api_key_provided:
            self.show_message_box('Erro', 'Para utilizar este programa você precisa cadastrar uma "Chave OpenAI" em "Arquivo > Configurações"')
            return
        if not self.controller.valid_api_key:
            self.show_message_box('Erro', 'Sua "Chave OpenAI" não é válida, tente alterá-la em "Arquivo > Configurações"')
            return
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecione o arquivo", "",
            "Arquivos PDF (*.pdf);;Arquivos Excel (*.xlsx)")
        
        if not file_path:
            return
        
        if not self.table_manager.file_path_present(file_path):
            if self.controller.allowed_file_size(file_path):
                self.show_loading_dialog('Lendo o documento e salvando as informações.')
                self.controller.add_file(file_path, self.handle_file_addition)
            else:
                file_size = int(round(self.controller.get_file_size(file_path)/1024, 0))
                extension = file_path.split('.')[-1]
                max_size = int(round(self.controller.get_allowed_size(extension)/1024, 0))
                self.show_message_box('Erro', f'O arquivo que você tentou inserir é muito grande ({file_size} MB), o máximo é {max_size} MB.', QMessageBox.Ok)
        else:
            self.show_message_box('Erro', 'Este arquivo já está presente.', QMessageBox.Ok)

    def handle_files_removal(self):
        self.populate_table()
        self.close_loading_dialog()

    def delete_files(self):
        selected_paths = self.table_manager.selected_data()
        if selected_paths:
            result = self.show_message_box('Confirmação', 'Tem certeza que deseja remover os arquivos selecionados?', QMessageBox.Yes | QMessageBox.No)

            if result == QMessageBox.Yes:
                self.show_loading_dialog('Removendo arquivos.')
                self.controller.remove_files(selected_paths, self.handle_files_removal)

    def populate_table(self):
        available_contents = self.controller.get_available_contents()
        self.table_manager.populate(available_contents)