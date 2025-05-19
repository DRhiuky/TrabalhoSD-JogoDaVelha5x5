import Pyro5.api
import threading
import time
from jogo import JogoDaVelha
from config import ip_server, port_nameserver, port_objeto

def monitorar_reinicio(jogo):
    while True:
        time.sleep(1)
        if jogo.reiniciar_em and time.time() >= jogo.reiniciar_em:
            jogo.reiniciar_jogo()

def main():
    jogo = JogoDaVelha(modo="normal")
    daemon = Pyro5.server.Daemon(host=ip_server, port=port_objeto)
    uri = daemon.register(jogo)
    
    ns = Pyro5.api.locate_ns(host=ip_server, port=port_nameserver)
    ns.register("jogo.velha", uri)
    
    # Inicia thread para reiniciar o jogo quando necessário
    threading.Thread(target=monitorar_reinicio, args=(jogo,), daemon=True).start()
    
    daemon.requestLoop()

if __name__ == "__main__":
    main()