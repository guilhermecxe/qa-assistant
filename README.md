# QA Assistant

Este é um assistente baseado em perguntas e respostas que combina técnicas de *Retrieval Augmented-Generation* (RAG) com modelos de linguagem natural da OpenAI.

Seu principal objetivo é ser um assistente pessoal que responde perguntas ou comandos do usuário a partir de informações contidas em seus próprios arquivos.

A interface gráfica foi desenvolvida em PySide6, enquanto a inteligência por trás do assistente é impulsionada pelo pacote [rag](https://github.com/guilhermecxe/rag), criado por [Guilherme Alves](https://github.com/guilhermecxe).

## Screenshots

Configurações:
![Alt text](./screenshots/Screenshot%201.png)

Uso:
![Alt text](./screenshots/Screenshot%202.png)

Acesso ao contexto utilizado para responder:
![Alt text](./screenshots/Screenshot%203.png)

## Funcionalidades

- **Cadastro de arquivos**: Suporta o cadastro de arquivos nos formatos PDF e XLSX, que permistem na aplicação enquanto o usuário não excluí-los.
- **Perguntas baseadas em documentos**: O usuário pode fazer perguntas sobre um ou mais arquivos cadastrados, com respostas geradas diretamente a partir dos dados contidos nesses arquivos.
- **Acesso ao contexto utilizado para responder**: A aplicação possui um botão chamado "Contexto" em que, após obter uma resposta, o usuário consegue visualizar quais dados de arquivos foram utilizados como contexto para respondê-lo.
- **Configuração da chave API**: Possibilidade de registrar e alterar a chave da API da OpenAI para acessar os modelos de linguagem.
- **Seleção de modelos**: Oferece a flexibilidade de escolher diferentes modelos de linguagem (`gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo-0125`, entre outros) para ajustar o comportamento do assistente às necessidades do usuário.

## Download e execução

- Para windows: [Download](https://drive.google.com/file/d/1G2Gubb4Ft5wruRv-kiyjtUdrtdGhZKfK/view?usp=drive_link).

Após baixar a pasta da aplicação, você precisará apenas descompactá-lo, executar o arquivo `QA-Assistant.exe` e cadastrar uma chave de API da OpenAI para começar a cadastrar arquivos e fazer perguntas.

## Limitações

- **Tamanho da aplicação**: A fase de compilação do código e a geração de arquivos necessários para a execução da aplicação ainda não foi otimizada a fim de reduzir o tamanho da aplicação no disco, que hoje necessita de, aproximadamente, 700 MB.
- **Apenas perguntas e respostas**: Esta aplicação não tem a intenção de ser conversacional, isto é, nenhuma resposta sofre influência de outras perguntas ou respostas anteriores.
