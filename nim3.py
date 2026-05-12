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
    
    # Contar quantas pilhas têm mais de 1 bolinha
    pilhas_maiores_que_1 = sum(1 for p in pilhas if p > 1)
    
    # Estratégia Misère: Quando resta apenas uma pilha > 1,
    # devemos deixar um número ÍMPAR de pilhas de tamanho 1.
    if pilhas_maiores_que_1 == 1:
        indice_pilha_grande = [i for i, p in enumerate(pilhas) if p > 1][0]
        outras_pilhas_com_1 = sum(1 for i, p in enumerate(pilhas) if p == 1 and i != indice_pilha_grande)
        
        # Se as outras pilhas com 1 forem par (0 ou 2), deixamos 1 na grande (total ímpar)
        # Se as outras pilhas com 1 forem ímpar (1), limpamos a grande (total ímpar)
        alvo = 1 if outras_pilhas_com_1 % 2 == 0 else 0
        quantidade = pilhas[indice_pilha_grande] - alvo
        return indice_pilha_grande, quantidade

    # Estratégia Normal (XOR sum) enquanto houver várias pilhas grandes
    if nim_sum != 0:
        for i, p in enumerate(pilhas):
            alvo = p ^ nim_sum
            if alvo < p:
                return i, p - alvo
                
    # Se não houver movimento ótimo (ou nim_sum já for 0), faz uma jogada aleatória
    pilhas_validas = [i for i, p in enumerate(pilhas) if p > 0]
    idx = random.choice(pilhas_validas)
    return idx, random.randint(1, pilhas[idx])

def jogada_bot(pilhas, nome_bot, dificuldade):
    # Definir se o bot vai jogar "sério" ou aleatório com base na dificuldade
    if dificuldade == 1:
        usar_otimo = random.random() < 0.2  # 20% inteligente
    elif dificuldade == 2:
        usar_otimo = random.random() < 0.6  # 60% inteligente
    else:
        usar_otimo = True  # 100% inteligente

    if usar_otimo:
        idx, qtd = calcular_movimento_otimo(pilhas)
    else:
        pilhas_validas = [i for i, p in enumerate(pilhas) if p > 0]
        idx = random.choice(pilhas_validas)
        qtd = random.randint(1, pilhas[idx])

    st.write(f"**{nome_bot} retira {qtd} bolinha(s) da Pilha {idx + 1}.**")
    return idx, qtd

def resetar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def main():
    st.title("🎮 Jogo do Nim - Versão 3 Pilhas")
    st.sidebar.markdown("""
    ### 📜 Novas Regras
    👉 Escolha **uma das três pilhas** no seu turno.
    👉 Retire **quantas bolinhas quiser** (pelo menos uma) daquela pilha.
    ❌ Perde quem for forçado a retirar a última bolinha do jogo.
    """)

    if st.button("🔄 Resetar Tudo"):
        resetar_estado()

    # Inicialização do estado
    if 'pilhas' not in st.session_state:
        st.session_state.pilhas = [5, 3, 1]
    if 'jogador_atual' not in st.session_state:
        st.session_state.jogador_atual = 1
    if 'jogo_iniciado' not in st.session_state:
        st.session_state.jogo_iniciado = False
    if 'moeda_sorteada' not in st.session_state:
        st.session_state.moeda_sorteada = False

    if not st.session_state.jogo_iniciado:
        st.header("Configuração das Pilhas")
        colA, colB, colC = st.columns(3)
        with colA:
            p1 = st.number_input("Pilha 1 (Esquerda):", 0, 20, 5)
        with colB:
            p2 = st.number_input("Pilha 2 (Meio):", 0, 20, 3)
        with colC:
            p3 = st.number_input("Pilha 3 (Direita):", 0, 20, 1)
        
        st.session_state.pilhas = [p1, p2, p3]

        # Visualização prévia
        st.write("---")
        v_col1, v_col2, v_col3 = st.columns(3)
        for i, col in enumerate([v_col1, v_col2, v_col3]):
            with col:
                st.markdown(f"**Pilha {i+1}**")
                for _ in range(st.session_state.pilhas[i]):
                    st.write("🔴" if i % 2 == 0 else "🔵")

        st.session_state.modo = st.radio("Modo de Jogo:", options=["Contra o Bot", "Dois Jogadores"], horizontal=True)

        if st.session_state.modo == "Contra o Bot":
            st.session_state.nome_jogador1 = st.text_input("Seu nome:", "Jogador")
            st.session_state.nome_jogador2 = "Bot"
            st.session_state.dificuldade = escolher_dificuldade()
            
            if st.button("Iniciar Sorteio"):
                st.session_state.resultado_sorteio = random.choice([1, 2])
                st.session_state.moeda_sorteada = True
        else:
            st.session_state.nome_jogador1 = st.text_input("Nome Jogador 1:", "P1")
            st.session_state.nome_jogador2 = st.text_input("Nome Jogador 2:", "P2")
            if st.button("Iniciar Jogo"):
                st.session_state.jogador_atual = 1
                st.session_state.jogo_iniciado = True
                st.rerun()

        if st.session_state.moeda_sorteada and not st.session_state.jogo_iniciado:
            vencedor_sorteio = st.session_state.nome_jogador1 if st.session_state.resultado_sorteio == 1 else "Bot"
            st.info(f"O sorteio definiu que **{vencedor_sorteio}** escolhe quem começa!")
            
            # Se o bot ganha o sorteio, ele sempre escolhe o estado vencedor
            if vencedor_sorteio == "Bot":
                nim_sum = st.session_state.pilhas[0] ^ st.session_state.pilhas[1] ^ st.session_state.pilhas[2]
                if nim_sum == 0: # Estado perdedor para quem começa, bot manda jogador começar
                    st.session_state.jogador_atual = 1
                else: # Bot começa para garantir o nim_sum = 0 para o jogador
                    st.session_state.jogador_atual = 2
                if st.button("Começar!"):
                    st.session_state.jogo_iniciado = True
                    st.rerun()
            else:
                escolha = st.radio("Quem começa?", [st.session_state.nome_jogador1, "Bot"])
                if st.button("Confirmar e Iniciar"):
                    st.session_state.jogador_atual = 1 if escolha == st.session_state.nome_jogador1 else 2
                    st.session_state.jogo_iniciado = True
                    st.rerun()

    else:
        st.header("Partida em Andamento")
        
        # Visualização das bolinhas
        cols = st.columns(3)
        for i in range(3):
            with cols[i]:
                st.subheader(f"Pilha {i+1}")
                qtd = st.session_state.pilhas[i]
                for _ in range(qtd):
                    st.write("🔴" if i % 2 == 0 else "🔵")
                st.write(f"({qtd} bolinhas)")

        # Checar fim de jogo
        total_restante = sum(st.session_state.pilhas)
        if total_restante == 0:
            # Quem fez a última jogada perdeu
            perdedor_idx = 3 - st.session_state.jogador_atual # Inverteu na última rodada
            perdedor_nome = st.session_state.nome_jogador1 if perdedor_idx == 1 else st.session_state.nome_jogador2
            vencedor_nome = st.session_state.nome_jogador2 if perdedor_idx == 1 else st.session_state.nome_jogador1
            
            st.error(f"❌ {perdedor_nome} retirou a última bolinha e PERDEU!")
            st.success(f"🏆 {vencedor_nome} é o grande vencedor!")
            if st.button("Jogar Novamente"):
                resetar_estado()
            return

        # Turnos
        if st.session_state.modo == "Contra o Bot" and st.session_state.jogador_atual == 2:
            st.write("🤖 **Bot pensando...**")
            idx, qtd = jogada_bot(st.session_state.pilhas, "Bot", st.session_state.dificuldade)
            st.session_state.pilhas[idx] -= qtd
            st.session_state.jogador_atual = 1
            st.button("Continuar")
        else:
            nome = st.session_state.nome_jogador1 if st.session_state.jogador_atual == 1 else st.session_state.nome_jogador2
            st.subheader(f"Vez de: {nome}")
            
            with st.form("jogada_form"):
                col_p, col_q = st.columns(2)
                with col_p:
                    # Só mostra pilhas que ainda têm bolinhas
                    opcoes_pilhas = [i+1 for i, p in enumerate(st.session_state.pilhas) if p > 0]
                    escolha_pilha = st.selectbox("Escolha a Pilha:", options=opcoes_pilhas)
                with col_q:
                    max_p = st.session_state.pilhas[escolha_pilha-1]
                    quantidade = st.number_input("Quanto retirar?", 1, max_p, 1)
                
                if st.form_submit_button("Confirmar Jogada"):
                    st.session_state.pilhas[escolha_pilha-1] -= quantidade
                    st.session_state.jogador_atual = 3 - st.session_state.jogador_atual
                    st.rerun()

        if st.button("Reiniciar Jogo"):
            resetar_estado()

if __name__ == "__main__":
    main()