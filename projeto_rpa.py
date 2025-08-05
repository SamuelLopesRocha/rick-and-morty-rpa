import requests
import sqlite3
import re
import smtplib
from email.mime.text import MIMEText

# === ETAPA 1: Coleta de Dados da API ===
def coletar_personagens():
    url = 'https://rickandmortyapi.com/api/character'
    personagens = []

    while url:
        resposta = requests.get(url)
        if resposta.status_code != 200:
            print(f"Erro ao acessar a API: {resposta.status_code}")
            break

        dados = resposta.json()
        for item in dados['results']:
            personagem = {
                'id': item['id'],
                'name': item['name'],
                'status': item['status'],
                'species': item['species'],
                'gender': item['gender'],
                'origin': item['origin']['name'],
                'location': item['location']['name'],
                'image': item['image']
            }
            personagens.append(personagem)

        url = dados['info']['next']

    return personagens

# === ETAPA 2: Armazenar em banco SQLite ===
def salvar_em_banco(personagens):
    conn = sqlite3.connect('projeto_rpa.db')
    cursor = conn.cursor()

    # Tabela de personagens
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personagens (
            id INTEGER PRIMARY KEY,
            name TEXT,
            status TEXT,
            species TEXT,
            gender TEXT,
            origin TEXT,
            location TEXT,
            image TEXT
        )
    ''')

    for p in personagens:
        cursor.execute('''
            INSERT OR REPLACE INTO personagens (id, name, status, species, gender, origin, location, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (p['id'], p['name'], p['status'], p['species'], p['gender'], p['origin'], p['location'], p['image']))

    conn.commit()
    conn.close()

# === ETAPA 3: Processamento com expressões regulares ===
def processar_dados():
    conn = sqlite3.connect('projeto_rpa.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dados_processados (
            id INTEGER PRIMARY KEY,
            name TEXT,
            possui_nome_com_s TEXT
        )
    ''')

    cursor.execute('SELECT id, name FROM personagens')
    for linha in cursor.fetchall():
        id_, nome = linha
        possui_s = 'sim' if re.search(r'\bs', nome, re.IGNORECASE) else 'não'
        cursor.execute('''
            INSERT OR REPLACE INTO dados_processados (id, name, possui_nome_com_s)
            VALUES (?, ?, ?)
        ''', (id_, nome, possui_s))

    conn.commit()
    conn.close()

# === ETAPA 4: Envio de relatório por e-mail ===
def enviar_email():
    conn = sqlite3.connect('projeto_rpa.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM personagens')
    total_personagens = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM dados_processados WHERE possui_nome_com_s = "sim"')
    com_s = cursor.fetchone()[0]

    texto_email = f"""
    Relatório do Projeto RPA - Samuel Lopes Gomes da Rocha

    Total de personagens coletados: 826
    Personagens com 's' no nome: {com_s}

    Dados armazenados em: projeto_rpa.db  
    """

    conn.close()

    msg = MIMEText(texto_email)
    msg['Subject'] = 'Relatório do Projeto RPA - Samuel Lopes Gomes da Rocha'
    msg['From'] = 'samuellopesgomes02@gmail.com'
    msg['To'] = 'samuellopesgomes07@gmail.com'

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('samuellopesgomes02@gmail.com', 'ohpd rgki ekqk gtos')
            smtp.send_message(msg)
        print("E-mail enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

# === EXECUÇÃO PRINCIPAL ===
if __name__ == "__main__":
    print("Coletando dados da API...")
    dados = coletar_personagens()
    print(f"{len(dados)} personagens coletados.")

    print("Salvando no banco de dados...")
    salvar_em_banco(dados)

    print("Processando dados com regex...")
    processar_dados()

    print("Enviando relatório por e-mail...")
    enviar_email()
