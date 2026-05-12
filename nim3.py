import streamlit as st
import random

def escolher_dificuldade():
    st.subheader("Nível de Dificuldade do Bot")
    dificuldade = st.radio(
        "Escolha o nível:",
        options=["Fácil", "Médio", "Difícil"],
        index=0,
        horizontal=True
    )
    return ["Fácil", "Médio", "Difícil"].index(dificuldade) + 1

def calcular_movimento_otimo(pilhas):
    """Calcula o movimento ideal para o Nim Misère (o último perde)."""
    nim_sum = pilhas[0] ^ pilhas[1] ^ pilhas[2]
    
    pilhas_maiores_que_1 = sum(1 for p in pilhas if p > 1)
    
    if pilhas_maiores_que_1 == 1:
        indice_pilha_grande = [i for i, p in enumerate(pilhas) if p > 1][0]
        outras_pilhas_com_1 = sum(1 for i, p in enumerate(pilhas) if p == 1 and i != indice_pilha_grande)
        alvo = 1 if outras_pilhas_com_1 % 2 == 0 else 0
        quantidade = pilhas[indice_pilha_grande] - alvo
        return indice_pilha_grande, max(1, quantidade)

    if nim_sum != 0:
        for i, p in enumerate(pilhas):
            alvo = p ^ nim_sum
            if alvo < p:
                return i, p - alvo
                
    pilhas_validas = [i for i, p in enumerate(pilhas) if p > 0]
    idx = random.choice(pilhas_validas)
    return idx, random.randint(1, pilhas[idx])

def jogada_bot(pilhas, nome_bot, dificuldade):
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
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def main():
    st.title("🎮 Jogo do Nim - O Último Perde")
    
    st.sidebar.markdown("""
    ### 📜 Regras do Jogo
    🎯 Retire bolinhas de **uma única pilha** por vez.
    👉 Retire quantas quiser daquela pilha (mínimo 1).
    ❌ **O último a retirar perde!** (Modo Misère)
    """)

    if 'pilhas' not in st.session_state:
        st.session_state.pilhas = [5, 3, 1]
    if 'jogo_iniciado' not in st.session_state:
        st.session_state.jogo_iniciado = False
    if 'moeda_sorteada' not in st.session_state:
        st.session_state.moeda_sorteada = False

    if not st.session_state.jogo_iniciado:
        st.header("⚙️ Configuração")
        colA, colB, colC = st.columns(3)
        with colA:
            p1 = st.number_input("Pilha 1:", 0, 20, 5)
        with colB:
            p2 = st.number_input("Pilha 2:", 0, 20, 3)
        with colC:
            p3 = st.number_input("Pilha 3:", 0, 20, 1)
        
        st.session_state.pilhas = [p1, p2, p3]
        st.session_state.modo = st.radio("Modo:", ["Contra o Bot", "Dois Jogadores"], horizontal=True)

        if st.session_state.modo == "Contra o Bot":
            st.session_state.nome_jogador1 = st.text_input("Seu nome:", "Jogador")
            st.session_state.nome_jogador2 = "Bot"
            st.session_state.dificuldade = escolher_dificuldade()

            st.write("---")
            st.subheader("🎲 Sorteio Inicial")
            escolha_usuario = st.radio("Escolha sua face:", ["Cara", "Coroa"], horizontal=True)
            
            if st.button("Lançar Moeda"):
                resultado = random.choice(["Cara", "Coroa"])
                st.session_state.resultado_moeda = resultado
                st.session_state.ganhou_sorteio = (escolha_usuario == resultado)
                st.session_state.moeda_sorteada = True

            if st.session_state.moeda_sorteada:
                st.info(f"Resultado: **{st.session_state.resultado_moeda}**")
                
                if st.session_state.ganhou_sorteio:
                    st.success("✨ Você ganhou o sorteio! Escolha quem começa:")
                    quem_comeca = st.radio("Iniciante:", [st.session_state.nome_jogador1, "Bot"], horizontal=True)
                    if st.button("Iniciar Partida"):
                        st.session_state.jogador_atual = 1 if quem_comeca == st.session_state.nome_jogador1 else 2
                        st.session_state.jogo_iniciado = True
                        st.rerun()
                else:
                    st.error("🤖 O Bot ganhou o sorteio!")
                    # Lógica estratégica do Bot para escolher quem começa
                    nim_sum = st.session_state.pilhas[0] ^ st.session_state.pilhas[1] ^ st.session_state.pilhas[2]
                    # No Nim Misère, nim_sum > 0 geralmente é favorável para quem começa
                    bot_comeca = nim_sum > 0 
                    
                    if bot_comeca:
                        st.write("O Bot analisou a mesa e decidiu: **Ele começa!**")
                        st.session_state.jogador_atual = 2
                    else:
                        st.write(f"O Bot analisou a mesa e decidiu: **{st.session_state.nome_jogador1} começa!**")
                        st.session_state.jogador_atual = 1
                    
                    if st.button("Ok, Vamos Jogar!"):
                        st.session_state.jogo_iniciado = True
                        st.rerun()
        else:
            # Modo 2 Jogadores
            st.session_state.nome_jogador1 = st.text_input("Nome Jogador 1:", "P1")
            st.session_state.nome_jogador2 = st.text_input("Nome Jogador 2:", "P2")
            if st.button("Iniciar Jogo"):
                st.session_state.jogador_atual = 1
                st.session_state.jogo_iniciado = True
                st.rerun()

    else:
        st.header("🎮 Partida em Andamento")
        
        # Visualização das pilhas
        cols = st.columns(3)
        for i in range(3):
            with cols[i]:
                st.subheader(f"Pilha {i+1}")
                qtd = st.session_state.pilhas[i]
                for _ in range(qtd):
                    st.write("🔴" if i == 0 else "🔵" if i == 1 else "🟢")
                st.write(f"**{qtd}** bolinhas")

        total_restante = sum(st.session_state.pilhas)
        
        if total_restante == 0:
            # Quem jogou por último retirou a última e perdeu
            perdedor_idx = 3 - st.session_state.jogador_atual
            vencedor = st.session_state.nome_jogador2 if perdedor_idx == 1 else st.session_state.nome_jogador1
            st.balloons()
            st.success(f"🏆 Fim de jogo! **{vencedor}** venceu!")
            if st.button("Novo Jogo"):
                resetar_estado()
            return

        # Turnos
        if st.session_state.modo == "Contra o Bot" and st.session_state.jogador_atual == 2:
            st.write("🤖 Bot está pensando...")
            idx, qtd = jogada_bot(st.session_state.pilhas, "Bot", st.session_state.dificuldade)
            st.session_state.pilhas[idx] -= qtd
            st.session_state.jogador_atual = 1
            st.info(f"O Bot retirou {qtd} da Pilha {idx+1}")
            st.button("Próximo Turno")
        else:
            nome = st.session_state.nome_jogador1 if st.session_state.jogador_atual == 1 else st.session_state.nome_jogador2
            st.subheader(f"Vez de: {nome}")
            
            with st.form("jogada"):
                pilhas_disponiveis = [i+1 for i, p in enumerate(st.session_state.pilhas) if p > 0]
                p_escolhida = st.selectbox("De qual pilha?", pilhas_disponiveis)
                max_retirar = st.session_state.pilhas[p_escolhida-1]
                qtd_retirar = st.number_input("Quantas bolinhas?", 1, max_retirar, 1)
                
                if st.form_submit_button("Confirmar"):
                    st.session_state.pilhas[p_escolhida-1] -= qtd_retirar
                    st.session_state.jogador_atual = 3 - st.session_state.jogador_atual
                    st.rerun()

        if st.button("Reiniciar Partida"):
            resetar_estado()

if __name__ == "__main__":
    main()