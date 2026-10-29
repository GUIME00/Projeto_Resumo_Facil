# Resumo Fácil — aplicação de NLP

Aplicação web em português que resume textos usando sumarização extrativa com TF-IDF.

## Requisitos
- Python 3.10 ou superior
- Internet para instalar as bibliotecas na primeira execução

## Como executar no Windows

1. Extraia o arquivo ZIP para uma pasta.
2. Abra o Prompt de Comando ou o terminal do VS Code nessa pasta.
3. (Opcional, recomendado) Crie um ambiente virtual:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

4. Instale as dependências:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Inicie a aplicação:

   ```bash
   python -m streamlit run app.py
   ```

6. O Streamlit abrirá a aplicação no navegador. Se não abrir automaticamente, acesse o endereço local mostrado no terminal (normalmente http://localhost:8501).

## Como usar
- Cole um texto em português (idealmente com várias frases).
- Escolha Curto, Médio ou Longo.
- Clique em **Gerar resumo**.
- Baixe o resultado em `.txt`, se quiser.

## Como funciona
O programa divide o texto em frases, transforma as frases em vetores TF-IDF, calcula uma pontuação de relevância e seleciona as frases mais bem pontuadas, preservando a ordem original.

É um resumidor **extrativo**, não um modelo generativo. Ele seleciona frases do texto original e não cria novas frases. Por isso, a qualidade depende da estrutura e do tamanho do texto. Sempre revise o resultado.

## Solução de problemas
- Se `streamlit` não for reconhecido, use `python -m streamlit run app.py`.
- Se ocorrer erro ao importar `streamlit`, verifique se não existe um arquivo chamado `streamlit.py` na pasta do projeto. Se existir, renomeie-o e apague a pasta `__pycache__` relacionada.
- Se `pip` falhar, tente `python -m pip install --upgrade pip` e depois instale as dependências novamente.
