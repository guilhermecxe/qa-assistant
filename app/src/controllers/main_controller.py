import os
import openai
from rag import Assistant

from src.threads.ask_thread import AskWorkerThread
from src.threads.add_file_thread import AddFileWorkerThread
from src.threads.remove_files_thread import RemoveFilesWorkerThread
from src.utils.user_settings import load_user_settings

class MainController:
    def __init__(self, main_window):
        self.main_window = main_window

        self.user_settings = load_user_settings()
        print(self.user_settings)

        try:
            self.ai = Assistant(openai_api_key=self.user_settings['OPENAI_API_KEY'], gpt_model=self.user_settings['GPT_MODEL'])
            self.api_key_provided = True
            if self.ai.check_api_key(self.user_settings['OPENAI_API_KEY']):
                self.valid_api_key = True
            else:
                self.valid_api_key = False
        except (openai.OpenAIError, ValueError):
            self.ai = Assistant('key holder', gpt_model=self.user_settings['GPT_MODEL'])
            self.api_key_provided = False
            self.valid_api_key = False
        print('Valid API KEY:', self.valid_api_key)

    def ask(self, question, contents, answear_handler):
        self.worker = AskWorkerThread(self.ai, question, contents)
        self.worker.result_ready.connect(answear_handler)
        self.worker.start()

    def get_available_contents(self):
        return self.ai.get_available_contents()
    
    def get_file_size(self, file_path):
        '''In KB'''
        return os.path.getsize(file_path)/1024

    def get_allowed_size(self, extension=None):
        if extension:
            return self.ai.get_contents_max_size()[extension]
        else:
            return self.ai.get_contents_max_size()

    def allowed_file_size(self, file_path):
        size = self.get_file_size(file_path)
        extension = file_path.split('.')[-1]
        return size <= self.get_allowed_size(extension)

    def add_file(self, file_path, handler):
        self.worker = AddFileWorkerThread(self.ai, file_path)
        self.worker.result_ready.connect(handler)
        self.worker.start()

    def remove_files(self, files_path, handler):
        self.worker = RemoveFilesWorkerThread(self.ai, files_path)
        self.worker.result_ready.connect(handler)
        self.worker.start()