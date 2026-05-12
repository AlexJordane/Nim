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
    """
    Calcula o movimento ideal para o Nim convencional (o último ganha).
    O objetivo é deixar a soma XOR (Nim-sum) das pilhas igual a zero.
    """
    # A Soma de Nim é a base da estratégia vencedora
    nim_sum = pilhas[0] ^ pilhas[1] ^ pilhas[2]
    
    # Se a soma não for zero, existe um movimento que a torna zero
    if nim_sum != 0:
        for i, p in enumerate(pilhas):
            alvo = p ^ nim_sum
            if alvo < p:
                return i, p - alvo
                
    # Se a soma já for zero ou não houver jogada matemática óbvia,
    # o Bot escolhe um movimento aleatório entre as pilhas disponíveis.
    pilhas_validas = [i for i, p in enumerate(pilhas) if p > 0]
    if not pilhas_validas:
        return 0, 0
        
    idx = random.choice(pilhas_validas)
    return idx, random.randint(1, pilhas[idx])

def jogada_bot(pilhas, nome_bot, dificuldade):
    """Gerencia a decisão do Bot baseada na dificuldade escolhida."""
    if dificuldade == 1:
        usar_otimo = random.random() < 0.2  # 20% de precisão
    elif dificuldade == 2:
        usar_otimo = random.random() < 0.6  # 60% de precisão
    else:
        usar_otimo = True  # 100% de precisão

    if usar_otimo:
        idx, qtd = calcular_movimento_otimo(pilhas)
    else:
        pilhas_validas = [i for i, p in enumerate(pilhas) if p > 0]
        idx = random.choice(pilhas_validas)
        qtd = random.randint(1, pilhas[idx])

    return idx, qtd

def resetar_estado():
    """Limpa a memória da sessão para uma nova partida."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def main():
    st.title("🎮 Jogo do Nim - O Último Ganha")
    st.sidebar.markdown("""
    ### 📜 Regras do Jogo

    🎯 O Jogo do Nim é uma disputa de estratégia para duas pessoas ou contra o 🤖 Bot.

    🔁 Participantes se revezam retirando bolinhas de **uma das três pilhas**.
    
    👉 No seu turno, você pode retirar quantas bolinhas quiser de uma única pilha (no mínimo uma).
    
    🏆 **Vence quem retirar a última bolinha do tabuleiro!**
    
    🎲 Um sorteio inicial define quem começa a partida.
    """)

    # Inicialização das variáveis de controle
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
        st.session_state.modo = st.radio("Modo de Jogo:", ["Contra o Bot", "Dois Jogadores"], horizontal=True)

        if st.session_state.modo == "Contra o Bot":
            st.session_state.nome_jogador1 = st.text_input("Seu nome:", "Pessoa Jogadora")
            st.session_state.nome_jogador2 = "Bot"
            st.session_state.dificuldade = escolher_dificuldade()

            st.write("---")
            st.subheader("🎲 Sorteio da Moeda")
            escolha_usuario = st.radio("Escolha sua face:", ["Cara", "Coroa"], horizontal=True)
            
            if st.button("Lançar Moeda"):
                resultado = random.choice(["Cara", "Coroa"])
                st.session_state.resultado_moeda = resultado
                st.session_state.ganhou_sorteio = (escolha_usuario == resultado)
                st.session_state.moeda_sorteada = True

            if st.session_state.moeda_sorteada:
                st.info(f"O resultado foi: **{st.session_state.resultado_moeda}**")
                
                if st.session_state.ganhou_sorteio:
                    st.success("✨ Você ganhou o sorteio! Quem deve dar o primeiro passo?")
                    quem_comeca = st.radio("Iniciante:", [st.session_state.nome_jogador1, "Bot"], horizontal=True)
                    if st.button("Iniciar Partida"):
                        st.session_state.jogador_atual = 1 if quem_comeca == st.session_state.nome_jogador1 else 2
                        st.session_state.jogo_iniciado = True
                        st.rerun()
                else:
                    st.error("🤖 O Bot ganhou o sorteio!")
                    nim_sum = st.session_state.pilhas[0] ^ st.session_state.pilhas[1] ^ st.session_state.pilhas[2]
                    
                    # No Nim "Último Ganha", começar em uma posição com nim_sum > 0 é vantajoso.
                    if nim_sum > 0:
                        st.write("O Bot analisou o tabuleiro e decidiu começar!")
                        st.session_state.jogador_atual = 2
                    else:
                        st.write(f"O Bot analisou o tabuleiro e convidou {st.session_state.nome_jogador1} para começar!")
                        st.session_state.jogador_atual = 1
                    
                    if st.button("Tudo pronto! Vamos jogar"):
                        st.session_state.jogo_iniciado = True
                        st.rerun()
        else:
            st.session_state.nome_jogador1 = st.text_input("Nome de quem joga primeiro:", "Pessoa 1")
            st.session_state.nome_jogador2 = st.text_input("Nome de quem joga depois:", "Pessoa 2")
            if st.button("Começar Diversão"):
                st.session_state.jogador_atual = 1
                st.session_state.jogo_iniciado = True
                st.rerun()

    else:
        st.header("🎮 Partida em Andamento")
        
        # Exibição visual das pilhas em colunas
        cols = st.columns(3)
        icones = ["🔴", "🔵", "🟢"]
        for i in range(3):
            with cols[i]:
                st.subheader(f"Pilha {i+1}")
                qtd = st.session_state.pilhas[i]
                # Mostra as bolinhas visualmente
                st.write((icones[i] + " ") * qtd if qtd > 0 else "*(Vazia)*")
                st.write(f"Contagem: **{qtd}**")

        total_restante = sum(st.session_state.pilhas)
        
        if total_restante == 0:
            # Como o jogador_atual é alternado logo após a jogada, 
            # o vencedor é quem fez o movimento anterior.
            vencedor_idx = 3 - st.session_state.jogador_atual
            vencedor_nome = st.session_state.nome_jogador1 if vencedor_idx == 1 else st.session_state.nome_jogador2
            
            st.balloons()
            st.success(f"🏆 Parabéns! **{vencedor_nome}** retirou a última bolinha e venceu a partida!")
            if st.button("Jogar Novamente"):
                resetar_estado()
            return

        # Gerenciamento de Turnos
        if st.session_state.modo == "Contra o Bot" and st.session_state.jogador_atual == 2:
            st.write("🤖 O Bot está calculando o próximo passo...")
            idx, qtd = jogada_bot(st.session_state.pilhas, "Bot", st.session_state.dificuldade)
            st.session_state.pilhas[idx] -= qtd
            st.session_state.jogador_atual = 1
            st.info(f"O Bot retirou {qtd} bolinha(s) da Pilha {idx+1}")
            st.button("Continuar")
        else:
            atual_nome = st.session_state.nome_jogador1 if st.session_state.jogador_atual == 1 else st.session_state.nome_jogador2
            st.subheader(f"Vez de: {atual_nome}")
            
            with st.form("formulario_jogada"):
                opcoes_pilha = [i+1 for i, p in enumerate(st.session_state.pilhas) if p > 0]
                escolha = st.selectbox("Selecione a pilha:", opcoes_pilha)
                limite = st.session_state.pilhas[escolha-1]
                quantidade = st.number_input("Quantas bolinhas deseja retirar?", 1, limite, 1)
                
                if st.form_submit_button("Confirmar Jogada"):
                    st.session_state.pilhas[escolha-1] -= quantidade
                    st.session_state.jogador_atual = 3 - st.session_state.jogador_atual
                    st.rerun()

        if st.button("Encerrar e Reiniciar"):
            resetar_estado()

if __name__ == "__main__":
    main()