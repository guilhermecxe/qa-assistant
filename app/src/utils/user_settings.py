import pickle
import os

USER_SETTINGS_PATH = 'user-settings.pkl'

DEFAULT_SETTINGS = {
    'OPENAI_API_KEY': None,
    'GPT_MODEL': None,
}

def load_user_settings() -> dict:
    if os.path.exists(USER_SETTINGS_PATH):
        with open(USER_SETTINGS_PATH, 'rb') as file:
            settings = pickle.load(file)
            return settings
    else:
        with open(USER_SETTINGS_PATH, 'wb') as file:
            pickle.dump(DEFAULT_SETTINGS, file)
        return DEFAULT_SETTINGS

def save_user_settings(openai_api_key:str=None, gpt_model:str=None):
    current_settings = load_user_settings()

    settings = {
        'OPENAI_API_KEY': openai_api_key if openai_api_key else current_settings['OPENAI_API_KEY'],
        'GPT_MODEL': gpt_model if gpt_model else current_settings['GPT_MODEL'],
    }
    with open(USER_SETTINGS_PATH, 'wb') as file:
        pickle.dump(settings, file)