from PySide6.QtWidgets import (
    QFormLayout, QLineEdit, QDialog, QTextEdit, QPushButton)
from rag import Assistant
import rag
import os

from src.utils.user_settings import save_user_settings

class SettingsDialog(QDialog):
    def __init__(self, ai:Assistant, main_controler):
        super().__init__()
        self.setWindowTitle("Configurações")

        self.ai = ai
        self.main_controler = main_controler

        self.layout = QFormLayout()
        
        self.set_openai_api_key_edit()
        self.set_gpt_model_edit()
        self.set_chunk_size_edit()
        self.set_chunk_overlap_edit()
        self.set_max_context_chunks()
        self.set_system_instruction_edit()
        self.set_prompt_template_edit()
        self.set_save_button()

        self.setLayout(self.layout)

    def __mask_key(self, key):
        return key[:4] + '...' + key[-4:]
    
    def update_api_key(self):
        current_key = self.ai._settings.get('OPENAI_API_KEY') if self.main_controler.api_key_provided else ''
        new_key = self.openai_api_key_edit.text().strip()

        if self.__mask_key(new_key) != self.__mask_key(current_key):
            if self.ai.check_api_key(new_key):
                self.ai.update_settings(openai_api_key=new_key)
                self.openai_api_key_edit.setText(self.__mask_key(new_key))
                self.openai_api_key_edit.setStyleSheet("QLineEdit { border: 1px solid green; border-radius: 2px; padding-left: 7px; padding-bottom: 1px }")
                self.main_controler.api_key_provided = True
                self.main_controler.valid_api_key = True
                self.gpt_model_edit.setEnabled(True)
                save_user_settings(openai_api_key=new_key)
                return True
            else:
                self.openai_api_key_edit.setText(self.__mask_key(current_key)) if self.main_controler.api_key_provided else ''
                self.openai_api_key_edit.setStyleSheet("QLineEdit { border: 1px solid red; border-radius: 2px; padding-left: 7px; padding-bottom: 1px }")
                return False
        else:
            return True

    def update_model(self):
        current_model = self.ai._settings.get('GPT_MODEL')
        new_model = self.gpt_model_edit.text()

        if new_model != current_model:
            if self.ai.check_model(new_model):
                if self.ai.is_suitable_model(new_model):
                    self.ai.update_settings(gpt_model=new_model)
                    self.gpt_model_edit.setStyleSheet("QLineEdit { border: 1px solid green; border-radius: 2px; padding-left: 7px; padding-bottom: 1px }")
                    save_user_settings(gpt_model=new_model)
                    return True
                else:
                    self.gpt_model_edit.setStyleSheet("QLineEdit { border: 1px solid red; border-radius: 2px; padding-left: 7px; padding-bottom: 1px}")
                    self.gpt_model_edit.setText(current_model)
                    return False
            else:
                self.gpt_model_edit.setText(current_model)
                self.gpt_model_edit.setStyleSheet("QLineEdit { border: 1px solid red; border-radius: 2px; padding-left: 7px; padding-bottom: 1px}")
                return False
        else:
            return True

    def save(self):
        if self.update_api_key() and self.update_model():
            self.accept()

    def set_openai_api_key_edit(self):
        if self.main_controler.api_key_provided:
            openai_api_key = self.__mask_key(self.ai._settings.get('OPENAI_API_KEY'))
        else:
            openai_api_key = ''
        self.openai_api_key_edit = QLineEdit(openai_api_key)
        self.layout.addRow("Chave OpenAI:", self.openai_api_key_edit)

    def set_gpt_model_edit(self):
        self.gpt_model_edit = QLineEdit(self.ai._settings.get('GPT_MODEL'))
        self.layout.addRow("Modelo GPT:", self.gpt_model_edit)
        if not self.main_controler.api_key_provided:
            self.gpt_model_edit.setEnabled(False)

    def set_chunk_size_edit(self):
        self.chunk_size_edit = QLineEdit(str(self.ai._settings.get('CHUNK_SIZE')))
        self.chunk_size_edit.setEnabled(False)
        self.layout.addRow("Chunk size:", self.chunk_size_edit)

    def set_chunk_overlap_edit(self):
        self.chunk_overlap_edit = QLineEdit(str(self.ai._settings.get('CHUNK_OVERLAP')))
        self.chunk_overlap_edit.setEnabled(False)
        self.layout.addRow("Chunk overlap:", self.chunk_overlap_edit)

    def set_max_context_chunks(self):
        self.max_context_chunks_edit = QLineEdit(str(self.ai._settings.get('MAX_CONTEXT_CHUNKS')))
        self.max_context_chunks_edit.setEnabled(False)
        self.layout.addRow("Máximo de chunks de contexto:", self.max_context_chunks_edit)

    def set_system_instruction_edit(self):
        self.system_instruction_edit = QTextEdit()
        self.system_instruction_edit.setPlainText(self.ai._settings.get('SYSTEM_INSTRUCTION'))
        self.system_instruction_edit.setEnabled(False)
        self.layout.addRow("Instrução do modelo:", self.system_instruction_edit)

    def set_prompt_template_edit(self):
        self.prompt_template_edit = QTextEdit()
        self.prompt_template_edit.setPlainText(self.ai._settings.get('PROMPT_TEMPLATE'))
        self.prompt_template_edit.setEnabled(False)
        self.layout.addRow("Template do prompt:", self.prompt_template_edit)

    def set_save_button(self):
        self.save_button = QPushButton("Salvar")
        self.save_button.clicked.connect(self.save)
        self.layout.addWidget(self.save_button)