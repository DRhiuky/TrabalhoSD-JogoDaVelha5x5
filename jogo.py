import os
from datetime import datetime
import Pyro5.api
import uuid
import time
import random

@Pyro5.api.expose
class JogoDaVelha:
    def __init__(self, modo="normal"):
        self.tabuleiro = [[" " for _ in range(5)] for _ in range(5)]
        self.jogadores = {}
        self.ordem = []
        self.simbolos = {}
        self.turno = 0
        self.vencedor = None
        self.modo = modo
        self.callbacks = {}
        self.reiniciar_em = None
        self.log_file = "log_jogo.txt"
        with open(self.log_file, "w") as f:
            f.write(f"=== LOG DE JOGADAS ===\nIniciado em {datetime.now()}\n\n")

        print("✅ Servidor registrado com sucesso no NameServer!")
        print("🎮 Aguardando conexões dos clientes para iniciar o jogo...")

    def registrar_jogador(self, nome):
        if self.vencedor is not None:
            return -2
        if self.modo == "teste":
            return -3
        if len(self.jogadores) >= 3:
            return -1

        jogador_id = str(uuid.uuid4())
        self.jogadores[jogador_id] = nome
        self.ordem.append(jogador_id)

        for s in ["X", "O", "V"]:
            if s not in self.simbolos.values():
                self.simbolos[jogador_id] = s
                break

        print(f"🔗 Jogador conectado: {nome} ({self.simbolos[jogador_id]})")
        if len(self.jogadores) == 3:
            random.shuffle(self.ordem)
            print("🔀 Ordem de turnos sorteada!")
            print("✅ Todos os jogadores conectados! Aguardando confirmação de atividade...")
        return jogador_id

    def registrar_callback(self, jogador_id, callback_uri):
        self.callbacks[jogador_id] = callback_uri

    def obter_tabuleiro(self):
        return self.tabuleiro

    def jogador_da_vez(self):
        if not self.ordem:
            return None
        return self.ordem[self.turno % len(self.ordem)]

    def get_vencedor(self):
        return self.vencedor

    def get_simbolo(self, jogador_id):
        return self.simbolos.get(jogador_id, "?")

    def jogar(self, jogador_id, linha, coluna):
        if self.vencedor:
            return "Jogo encerrado. Vitória de " + self.vencedor

        if jogador_id != self.jogador_da_vez():
            return "Não é sua vez."

        if not (0 <= linha < 5 and 0 <= coluna < 5):
            return "Jogada fora dos limites."

        if self.tabuleiro[linha][coluna] != " ":
            return "Posição ocupada."

        simbolo = self.simbolos[jogador_id]
        self.tabuleiro[linha][coluna] = simbolo
        self.registrar_log(jogador_id, linha, coluna, simbolo)

        if self.verificar_vitoria(simbolo):
            self.vencedor = self.jogadores[jogador_id]
            print(f"🏁 Jogo finalizado! Vencedor: {self.vencedor} ({simbolo})")
            self.reiniciar_em = time.time() + 5
            return f"{simbolo} venceu!"

        if self.verificar_empate():
            print("🤝 Jogo finalizado com empate.")
            self.vencedor = "Empate"
            self.reiniciar_em = time.time() + 5
            return "Empate!"

        self.turno += 1
        return "OK"

    def verificar_vitoria(self, jogador):
        for linha in self.tabuleiro:
            for i in range(3):
                if linha[i] == linha[i+1] == linha[i+2] == jogador:
                    return True
        for col in range(5):
            for i in range(3):
                if self.tabuleiro[i][col] == self.tabuleiro[i+1][col] == self.tabuleiro[i+2][col] == jogador:
                    return True
        for i in range(3):
            for j in range(3):
                if (self.tabuleiro[i][j] == self.tabuleiro[i+1][j+1] == self.tabuleiro[i+2][j+2] == jogador or
                    self.tabuleiro[i][j+2] == self.tabuleiro[i+1][j+1] == self.tabuleiro[i+2][j] == jogador):
                    return True
        return False

    def verificar_empate(self):
        return all(cell != " " for row in self.tabuleiro for cell in row)

    def jogo_ativo(self):
        if self.reiniciar_em and time.time() >= self.reiniciar_em:
            self.reiniciar_jogo()
            return False

        if len(self.jogadores) < 3 or self.vencedor is not None:
            return False

        inativos = []
        for jogador_id in list(self.jogadores.keys()):
            uri = self.callbacks.get(jogador_id)
            if not uri:
                inativos.append(jogador_id)
                continue
            try:
                proxy = Pyro5.api.Proxy(uri)
                if proxy.ping() != "ok":
                    inativos.append(jogador_id)
            except:
                inativos.append(jogador_id)

        if not hasattr(self, "_jogo_liberado") and len(inativos) == 0:
            self._jogo_liberado = True
            print("🚀 Todos os jogadores confirmados! Jogo iniciado.")

        if inativos:
            for jid in inativos:
                nome = self.jogadores.get(jid, f"Jogador")
                print(f"❌ Jogador desconectado: {nome}")
                self.jogadores.pop(jid, None)
                self.callbacks.pop(jid, None)
                self.simbolos.pop(jid, None)
                if jid in self.ordem:
                    self.ordem.remove(jid)
            if self.vencedor is None and len(self.jogadores) < 3:
                print("💥 Jogo encerrado por desconexão de jogador.")
                self.vencedor = "Ninguém (desconexão)"
                self.reiniciar_em = time.time() + 5
            return False

        return True

    def registrar_log(self, jogador_id, linha, coluna, simbolo):
        nome = self.jogadores.get(jogador_id, f"Jogador")
        with open(self.log_file, "a") as f:
            f.write(f"Turno {self.turno + 1}: {nome} ({simbolo}) -> Linha {linha}, Coluna {coluna}\n")

    def reiniciar_jogo(self):
        print("🔄 Reiniciando servidor para nova rodada...\n")
        self.tabuleiro = [[" " for _ in range(5)] for _ in range(5)]
        self.jogadores.clear()
        self.ordem.clear()
        self.simbolos.clear()
        self.callbacks.clear()
        self.turno = 0
        self.vencedor = None
        self.reiniciar_em = None
        if hasattr(self, "_jogo_liberado"):
            del self._jogo_liberado
        print("🎮 Aguardando conexões dos clientes para iniciar o jogo...")