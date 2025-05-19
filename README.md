# Jogo da Velha Distribuído com RMI (Pyro5)

Este projeto implementa um jogo da velha 5x5 para **3 jogadores remotos**, utilizando a técnica de **Invocação de Métodos Remotos (RMI)** com a biblioteca **Pyro5** em Python.

## Tecnologias Utilizadas

- Python 3.12
- [Pyro5](https://pyro5.readthedocs.io) – Remote Method Invocation para objetos Python
- Terminal/Console
- Arquitetura Cliente-Servidor com comunicação via TCP/IP

## Regras do Jogo

- Tabuleiro de **5x5**
- 3 jogadores: **X**, **O** e **V**
- Vence quem formar 3 símbolos iguais em linha, coluna ou diagonal
- O jogo detecta **empate** ou **desconexões**
- No fim, o servidor reinicia automaticamente para uma nova rodada

## Estrutura do Projeto

```
projeto/
├── cliente.py           # Lógica do cliente com interface terminal
├── servidor.py          # Lógica do servidor e controle do jogo
├── jogo.py              # Objeto remoto Pyro com regras do jogo
├── config.py            # Organiza Endereços Ip e portas
├── log_jogo.txt         # Log das jogadas criado em tempo real
├── teste.py (opcional)  # Testa sequencia de jogadas no script jogadas
└── jogadas.txt (opcional)  # Script de jogadas para modo de teste
```

## Como Executar

### 1. Verifique se o Python está instalado
No terminal, execute:

```powershell
python --version
```

Se não estiver, baixe em: https://www.python.org/downloads  
**Marcar a opção "Add Python to PATH" durante a instalação.**

---

### 2. Crie e ative o ambiente virtual

No diretório do projeto, execute:

```powershell
python -m venv venv
```

Ative o ambiente virtual:

- No **CMD**:
  ```cmd
  venv\Scripts\activate
  ```

- No **PowerShell**:
  ```powershell
  .\venv\bin\Activate.ps1
  ```

> Se receber um erro de permissão, execute:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```
> E tente ativar novamente.

---

### 3. Instale o Pyro5

Com o ambiente virtual ativado:

```bash
pip install Pyro5
```

---

### 4. Inicie o NameServer do Pyro5

Em um terminal separado (com o `venv` ativado):

```bash
python -m Pyro5.nameserver
```

---

### 5. Inicie o servidor

Em outro terminal (com o `venv` ativado):

```bash
python servidor.py
```

---

### 6. Inicie 3 clientes (cada um em um terminal separado)

```bash
python cliente.py
```

Cada cliente deverá informar um nome. O símbolo (**X**, **O** ou **V**) será atribuído com base na ordem de entrada.

---

## Reinício automático

- O servidor reinicia automaticamente após cada partida
- Os clientes podem se reconectar a qualquer momento
- Se algum jogador desconectar, a partida atual é encerrada

---

### Arquivo `config.py`: Gerenciamento de IPs e Portas

O arquivo `config.py` centraliza a configuração de IPs e portas para facilitar o uso do projeto em diferentes ambientes.

### Exemplos de uso

| Situação                             | Valor de `ip_server`               |
|-------------------------------------|------------------------------------|
| Cliente e servidor na mesma máquina | `"localhost"` ou `"127.0.0.1"`     |
| Cliente e servidor na mesma rede    | IP da máquina do servidor (ex: `"192.168.1.25"`) |
| Cliente remoto via internet         | IP público com redirecionamento de portas |

---

## Extras

- O arquivo `log_jogo.txt` registra todas as jogadas em tempo real
- O modo de teste com `python teste.py` pode ser usado para simulações automáticas com `jogadas.txt`.
