from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

class DescriptionLabel(QLabel):
    def __init__(self):
        text = (
            '''Este é um software desenvolvido dentro da Fundação de Amparo à Pesquisa do Estado de Goiás. '''
            '''Seu objetivo é responder comandos e perguntas do(a) usuário(a) com base em arquivos que este(a) '''
            '''importa e seleciona. Ele faz uso de modelos GPT (alteráveis em "Arquivo > Configurações > Modelo GPT") '''
            '''para acessar os dados e responder o(a) usuário(a).''')
        super().__init__(text)

        self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(True)
        self.setWordWrap(True)

class ContentsLabel(QLabel):
    def __init__(self):
        text = (
            '''Selecione abaixo a quais arquivos você gostaria que a inteligência artificial '''
            '''tivesse acesso para elaborar a resposta. Se nenhum '''
            '''arquivo for selecionado, o programa tentará decidir sozinho '''
            '''quais arquivos consultar.''')
        super().__init__(text)

        self.setWordWrap(True)