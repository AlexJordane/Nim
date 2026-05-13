import streamlit as st
import random

def escolher_dificuldade():
    """Interface para seleção do nível de desafio do Bot."""
    st.subheader("Nível de Dificuldade do Bot")
    dificuldade = st.radio(
        "Escolha o nível:",
        options=["Fácil", "Médio", "Difícil"],
        index=0,
        horizontal=True
    )
    return ["Fácil", "Médio", "Difícil"].index(dificuldade) + 1

def calcular_movimento_otimo(pilhas):
    """Calcula o movimento ideal para o Nim convencional (o último ganha)."""
    nim_sum = pilhas[0] ^ pilhas[1] ^ pilhas[2]
    
    if nim_sum != 0:
        for i, p in enumerate(pilhas):
            alvo = p ^ nim_sum
            if alvo < p:
                return i, p - alvo
                
    pilhas_validas = [i for i, p in enumerate(pilhas) if p > 0]
    if not pilhas_validas:
        return 0, 0
        
    idx = random.choice(pilhas_validas)
    return idx, random.randint(1, pilhas[idx])

def jogada_bot(pilhas, nome_bot, dificuldade):
    """Gerencia a decisão do Bot baseada na dificuldade."""
    if dificuldade == 1:
        usar_otimo = random.random() < 0.2
    elif dificuldade == 2:
        usar_otimo = random.random() < 0.6
    else:
        usar_otimo = True

    if usar_otimo:
        idx, qtd = calcular_movimento_otimo(pilhas)
    else:
        pilhas_validas = [i for i, p in enumerate(pilhas) if p > 0]
        idx = random.choice(pilhas_validas)
        qtd = random.randint(1, pilhas[idx])

    return idx, qtd

def resetar_estado():
    """Reinicia o jogo."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def main():
    st.title("🎮 Jogo do Nim - O Último Ganha")
    
    if 'pilhas' not in st.session_state:
        st.session_state.pilhas = [5, 3, 1]
    if 'jogo_iniciado' not in st.session_state:
        st.session_state.jogo_iniciado = False
    if 'moeda_sorteada' not in st.session_state:
        st.session_state.moeda_sorteada = False

    if not st.session_state.jogo_iniciado:
        st.header("⚙️ Configuração")
        colA, colB, colC = st.columns(3)
        with colA: p1 = st.number_input("Pilha 1:", 0, 20, 5)
        with colB: p2 = st.number_input("Pilha 2:", 0, 20, 3)
        with colC: p3 = st.number_input("Pilha 3:", 0, 20, 1)
        
        st.session_state.pilhas = [p1, p2, p3]
        st.session_state.modo = st.radio("Modo:", ["Contra o Bot", "Dois Jogadores"], horizontal=True)

        if st.session_state.modo == "Contra o Bot":
            st.session_state.nome_jogador1 = st.text_input("Seu nome:", "Jogador")
            st.session_state.nome_jogador2 = "Bot"
            st.session_state.dificuldade = escolher_dificuldade()

            st.subheader("🎲 Sorteio")
            escolha = st.radio("Sua face:", ["Cara", "Coroa"], horizontal=True)
            if st.button("Lançar Moeda"):
                res = random.choice(["Cara", "Coroa"])
                st.session_state.resultado_moeda = res
                st.session_state.ganhou_sorteio = (escolha == res)
                st.session_state.moeda_sorteada = True

            if st.session_state.moeda_sorteada:
                st.info(f"Resultado: {st.session_state.resultado_moeda}")
                if st.session_state.ganhou_sorteio:
                    st.success("Você ganhou! Escolha quem começa:")
                    quem = st.radio("Iniciante:", [st.session_state.nome_jogador1, "Bot"], horizontal=True)
                    if st.button("Iniciar"):
                        st.session_state.jogador_atual = 1 if quem == st.session_state.nome_jogador1 else 2
                        st.session_state.jogo_iniciado = True
                        st.rerun()
                else:
                    st.error("Bot ganhou!")
                    st.session_state.jogador_atual = 2
                    if st.button("Começar"):
                        st.session_state.jogo_iniciado = True
                        st.rerun()
        else:
            if st.button("Iniciar Jogo"):
                st.session_state.jogador_atual = 1
                st.session_state.jogo_iniciado = True
                st.rerun()
    else:
        st.header("🎮 Partida em Andamento")
        cols = st.columns(3)
        icones = ["🔴", "🔵", "🟢"]
        for i in range(3):
            with cols[i]:
                st.subheader(f"Pilha {i+1}")
                qtd = st.session_state.pilhas[i]
                st.write((icones[i] + " ") * qtd if qtd > 0 else "*(Vazia)*")
                st.write(f"Contagem: **{qtd}**")

        if sum(st.session_state.pilhas) == 0:
            vencedor = st.session_state.nome_jogador1 if st.session_state.jogador_atual == 2 else st.session_state.nome_jogador2
            st.balloons()
            st.success(f"🏆 {vencedor} venceu!")
            if st.button("Reiniciar"): resetar_estado()
            return

        if st.session_state.modo == "Contra o Bot" and st.session_state.jogador_atual == 2:
            st.write("🤖 Bot pensando...")
            idx, qtd = jogada_bot(st.session_state.pilhas, "Bot", st.session_state.dificuldade)
            st.session_state.pilhas[idx] -= qtd
            st.session_state.jogador_atual = 1
            st.rerun()
        else:
            nome = st.session_state.nome_jogador1 if st.session_state.jogador_atual == 1 else st.session_state.nome_jogador2
            st.subheader(f"Vez de: {nome}")
            
            with st.form("jogada"):
                # Permitimos selecionar qualquer pilha, mesmo vazia, para validar depois
                escolha = st.selectbox("Selecione a pilha:", [1, 2, 3])
                # Removemos o limite do number_input para permitir a digitação livre
                quantidade = st.number_input("Quantas bolinhas?", min_value=1, step=1)
                
                confirmar = st.form_submit_button("Confirmar Jogada")
                
                if confirmar:
                    pilha_index = escolha - 1
                    disponivel = st.session_state.pilhas[pilha_index]
                    
                    if quantidade > disponivel:
                        st.error(f"⚠️ Jogada inválida! Você tentou retirar {quantidade} bolinhas, mas a Pilha {escolha} só tem {disponivel}.")
                    else:
                        st.session_state.pilhas[pilha_index] -= quantidade
                        st.session_state.jogador_atual = 3 - st.session_state.jogador_atual
                        st.rerun()

        if st.button("Sair"): resetar_estado()

if __name__ == "__main__":
    main()