import Pyro5.api
import Pyro5.server
import os
import time
import threading
from config import ip_server, port_nameserver

@Pyro5.api.expose
class ClienteCallback:
    def ping(self):
        return "ok"

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_tabuleiro(tabuleiro):
    print("\n  " + "   ".join(str(i) for i in range(5)))
    print(" +" + "---+" * 5)
    for i, linha in enumerate(tabuleiro):
        print(f"{i}| " + " | ".join(linha) + " |")
        print(" +" + "---+" * 5)

def exibir_jogador(simbolo, nome):
    print(f"Você é o jogador {simbolo} ({nome})")

# Inicia daemon separado para o callback do cliente
daemon = Pyro5.server.Daemon()
threading.Thread(target=daemon.requestLoop, daemon=True).start()

# Conecta ao servidor Pyro
ns = Pyro5.api.locate_ns(host=ip_server, port=port_nameserver)
uri = ns.lookup("jogo.velha")
jogo = Pyro5.api.Proxy(uri)

# Registro do jogador
nome = input("Digite seu nome: ")
jogador_id = jogo.registrar_jogador(nome)

if jogador_id == -1:
    print("Número máximo de jogadores já conectado. Tente novamente mais tarde.")
    exit()
elif jogador_id == -2:
    print("O jogo já terminou. Aguarde o próximo.")
    exit()
elif jogador_id == -3:
    print("Servidor está em modo de teste. Jogadas automáticas em execução.")
    exit()

# Recupera símbolo do jogador
simbolo = jogo.get_simbolo(jogador_id)
print(f"Você está conectado como: {nome} ({simbolo})\nID do jogador: {jogador_id}")

# Cria e registra callback do cliente
callback = ClienteCallback()
callback_uri = daemon.register(callback)
jogo.registrar_callback(jogador_id, callback_uri)

# Espera até os 3 jogadores estarem conectados e ativos
exibir_jogador(simbolo, nome)
print("Aguardando os 3 jogadores se conectarem...")
while not jogo.jogo_ativo():
    time.sleep(2)
    limpar()
    exibir_jogador(simbolo, nome)
    print("Aguardando os 3 jogadores se conectarem...")

# Loop principal do jogo
fim = False
while not fim:
    if not jogo.jogo_ativo():
        break

    vez = jogo.jogador_da_vez()
    while vez != jogador_id and not jogo.get_vencedor():
        if not jogo.jogo_ativo():
            break
        limpar()
        exibir_jogador(simbolo, nome)
        simbolo_vez = jogo.get_simbolo(vez)
        print(f"Jogador da vez: {simbolo_vez}")
        exibir_tabuleiro(jogo.obter_tabuleiro())
        print("⏳ Aguardando sua vez...")
        time.sleep(2)
        vez = jogo.jogador_da_vez()

    if jogo.get_vencedor() or not jogo.jogo_ativo():
        fim = True
        break

    limpar()
    print(f"🟢 Sua vez! Você está conectado como: {nome} ({simbolo})")
    exibir_tabuleiro(jogo.obter_tabuleiro())

    try:
        linha = int(input("Linha (0-4): "))
        coluna = int(input("Coluna (0-4): "))
    except ValueError:
        print("Digite números válidos.")
        time.sleep(2)
        continue

    resposta = jogo.jogar(jogador_id, linha, coluna)
    limpar()
    exibir_tabuleiro(jogo.obter_tabuleiro())
    print(resposta)
    time.sleep(2)

    if "venceu" in resposta or "Empate" in resposta or not jogo.jogo_ativo():
        fim = True
        break

# Espera o jogo reiniciar no servidor (verifica se ainda ativo)
time.sleep(0.5)
while jogo.jogo_ativo():
    time.sleep(1)

# Resultado final
limpar()
exibir_jogador(simbolo, nome)
exibir_tabuleiro(jogo.obter_tabuleiro())
vencedor = jogo.get_vencedor()

if vencedor:
    print(f"\n🏆 Vencedor: {vencedor}")
else:
    print("\n🤝 O jogo terminou em empate ou foi encerrado por desconexão.")

print("\n🎮 Fim de jogo.")