# Projeto de Automação com API - Rick and Morty

**Autor:** Samuel Lopes Gomes da Rocha  
**Tecnologias utilizadas:** Python, SQLite, Requests, Regex, SMTP

## 📌 API Utilizada
**Rick and Morty API**  
[https://rickandmortyapi.com/](https://rickandmortyapi.com/)  

API pública que fornece dados sobre personagens, localizações e episódios do universo Rick and Morty.

---

## 🔧 Funcionalidades do Projeto

### 1. Coleta de Dados
- Através da biblioteca `requests`, os dados dos personagens foram coletados de forma paginada.
- Campos coletados: `id`, `name`, `status`, `species`, `gender`, `origin`, `location`, `image`.

### 2. Armazenamento em Banco de Dados
- Criação do banco `projeto_rpa.db` utilizando `sqlite3`.
- Tabela `personagens` com todos os dados obtidos da API.

### 3. Processamento de Dados com Regex
- Identificação de personagens que possuem a letra **'s'** no nome (maiúscula ou minúscula).
- Resultado armazenado na tabela `dados_processados`.

### 4. Envio de Relatório por E-mail
- Resumo automático com número total de personagens e quantidade com a letra 's' no nome.
- Envio via `smtplib` com `SMTP_SSL` e `email.mime`.

---

## 📂 Estrutura do Projeto

```
projeto_rpa/
│
├── projeto_final_rpa.py        # Script principal com as etapas de automação
├── projeto_rpa.db              # Banco de dados SQLite com os dados coletados
└── README.md                   # Este arquivo
```

---

## 📷 Prints recomendados para demonstração

- Execução do script no terminal
- Visualização das tabelas no banco de dados
- Confirmação de e-mail enviado com sucesso

---

## ✅ Conclusão

Este projeto demonstra como integrar APIs, persistência de dados, expressões regulares e envio automatizado de relatórios, utilizando Python puro. Uma base sólida para aplicações de RPA e automações simples com dados públicos.
