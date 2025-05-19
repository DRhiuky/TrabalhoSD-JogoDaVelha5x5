from jogo import JogoDaVelha

def exibir_tabuleiro(tabuleiro):
    print("\n  " + "   ".join(str(i) for i in range(5)))
    print(" +" + "---+" * 5)
    for i, linha in enumerate(tabuleiro):
        print(f"{i}| " + " | ".join(linha) + " |")
        print(" +" + "---+" * 5)

def main():
    jogo = JogoDaVelha(modo="teste")
    print("\nTeste concluído.")
    exibir_tabuleiro(jogo.obter_tabuleiro())

    if jogo.vencedor:
        print(f"\nVencedor: {jogo.vencedor}")
    elif jogo.verificar_empate():
        print("\nO jogo terminou em empate.")
    else:
        print("\nO jogo não terminou completamente.")

if __name__ == "__main__":
    main()
