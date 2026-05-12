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

def jogada_bot(total_bolinhas, max_retirada, nome_bot, dificuldade):
    if total_bolinhas <= max_retirada + 1:
        jogada = total_bolinhas - 1 if total_bolinhas > 1 else 1
        st.write(f"**{nome_bot} retira {jogada} bolinhas.**")
        return jogada

    alvo = 1
    while alvo <= total_bolinhas:
        alvo += max_retirada + 1
    jogada_otima = total_bolinhas - (alvo - (max_retirada + 1))

    jogada_otima_valida = (1 <= jogada_otima <= max_retirada)

    if jogada_otima_valida:
        if dificuldade == 1:
            usar_otima = random.random() < 0.3
        elif dificuldade == 2:
            usar_otima = random.random() < 0.6
        else:
            usar_otima = True
    else:
        usar_otima = False

    jogada = jogada_otima if usar_otima else random.randint(1, min(max_retirada, total_bolinhas))
    st.write(f"**{nome_bot} retira {jogada} bolinhas.**")
    return jogada

def resetar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def main():
    st.title("🎮 Jogo do Nim - O Último Perde")
    st.sidebar.markdown("""
    ### 📜 Regras do Jogo

    🎯 O Jogo do Nim é uma disputa de raciocínio e estratégia, jogada por duas pessoas ou por uma pessoa contra o 🤖 Bot.

    🔁 Os participantes se revezam retirando bolinhas de uma pilha comum.
    
    👉 A cada turno, é permitido retirar entre 1 e o número máximo de bolinhas definido no início.
    
    ❌ Perde quem for forçado a retirar a última bolinha.
    
    🧠 No modo contra o Bot, você escolhe o nível de dificuldade: Fácil 😄, Médio 😐 ou Difícil 😈.
    
    🎲 Um sorteio inicial (cara ou coroa) define quem começa a partida.
    """)
    if st.button("🔄 Resetar Tudo"):
        resetar_estado()

    if 'total_bolinhas' not in st.session_state:
        st.session_state.total_bolinhas = 0
    if 'max_retirada' not in st.session_state:
        st.session_state.max_retirada = 0
    if 'jogador_atual' not in st.session_state:
        st.session_state.jogador_atual = 1
    if 'nome_jogador1' not in st.session_state:
        st.session_state.nome_jogador1 = ""
    if 'nome_jogador2' not in st.session_state:
        st.session_state.nome_jogador2 = ""
    if 'modo' not in st.session_state:
        st.session_state.modo = 0
    if 'dificuldade' not in st.session_state:
        st.session_state.dificuldade = 0
    if 'jogo_iniciado' not in st.session_state:
        st.session_state.jogo_iniciado = False
    if 'vez_bot' not in st.session_state:
        st.session_state.vez_bot = False
    if 'moeda_sorteada' not in st.session_state:
        st.session_state.moeda_sorteada = False
    if 'aguardando_escolha_inicial' not in st.session_state:
        st.session_state.aguardando_escolha_inicial = False

    if not st.session_state.jogo_iniciado:
        st.header("Configuração do Jogo")

        col1, col2 = st.columns(2)
        with col1:
            st.session_state.total_bolinhas = st.number_input("Quantas bolinhas terá a pilha inicial?", min_value=2, max_value=100, value=27)
        with col2:
            st.session_state.max_retirada = st.number_input("Máximo de bolinhas por jogada:", min_value=1, max_value=10, value=4)

        st.session_state.modo = st.radio("Modo de Jogo:", options=["Um Jogador vs Bot", "Dois Jogadores"], index=0, horizontal=True)

        if st.session_state.modo == "Um Jogador vs Bot":
            st.session_state.nome_jogador1 = st.text_input("Digite seu nome:", "Jogador")
            st.session_state.nome_jogador2 = "Bot"
            st.session_state.dificuldade = escolher_dificuldade()

            st.session_state.cara_ou_coroa = st.radio(f"{st.session_state.nome_jogador1}, escolha cara ou coroa:", options=["Cara", "Coroa"], horizontal=True)
            if st.button("Jogar a moeda!"):
                st.session_state.resultado_sorteio = random.choice(["Cara", "Coroa"])
                st.session_state.moeda_sorteada = True
                st.rerun()

            if st.session_state.moeda_sorteada and not st.session_state.jogo_iniciado:
                resultado = st.session_state.resultado_sorteio
                st.subheader(f"Resultado da moeda: **{resultado}**")

                if st.session_state.cara_ou_coroa == resultado:
                    st.success("Você ganhou o sorteio!")

                    if not st.session_state.aguardando_escolha_inicial:
                        st.session_state.aguardando_escolha_inicial = True

                    iniciante = st.radio("Quem deve começar?", options=[st.session_state.nome_jogador1, st.session_state.nome_jogador2], horizontal=True, key='iniciante_escolha')

                    if st.button("Começar Jogo"):
                        st.session_state.jogador_atual = 1 if iniciante == st.session_state.nome_jogador1 else 2
                        st.session_state.vez_bot = (st.session_state.jogador_atual == 2)
                        st.session_state.jogo_iniciado = True
                        st.rerun()

                else:
                    st.warning("O Bot ganhou o sorteio!")

                    if not st.session_state.aguardando_escolha_inicial:
                        if (st.session_state.total_bolinhas - 1) % (st.session_state.max_retirada + 1) == 0:
                            st.info(f"O Bot escolhe que {st.session_state.nome_jogador1} começa.")
                            st.session_state.jogador_atual = 1
                        else:
                            st.info("O Bot escolhe começar!")
                            st.session_state.jogador_atual = 2

                        st.session_state.vez_bot = (st.session_state.jogador_atual == 2)
                        st.session_state.aguardando_escolha_inicial = True

                    if st.button("Começar Jogo"):
                        st.session_state.jogo_iniciado = True
                        st.rerun()

        else:
            st.session_state.nome_jogador1 = st.text_input("Nome do Jogador 1:", "Jogador 1")
            st.session_state.nome_jogador2 = st.text_input("Nome do Jogador 2:", "Jogador 2")

            if st.button("Iniciar Jogo"):
                st.session_state.jogador_atual = 1
                st.session_state.jogo_iniciado = True
                st.rerun()

    else:
        st.header("Partida em Andamento")

        if 'msg_ultima_jogada_bot' in st.session_state:
            st.info(st.session_state.msg_ultima_jogada_bot)
            del st.session_state.msg_ultima_jogada_bot

        bolinhas_visual = ''.join(['🔴 ' if i % 2 == 0 else '🔵 ' for i in range(st.session_state.total_bolinhas)])
        st.subheader(f"Bolinhas restantes: ")
        st.subheader(f"{bolinhas_visual}")
        st.subheader(f"{st.session_state.total_bolinhas} bolinhas!")

        if st.session_state.total_bolinhas <= 1:
            perdedor = st.session_state.nome_jogador2 if st.session_state.jogador_atual == 2 else st.session_state.nome_jogador1
            vencedor = st.session_state.nome_jogador1 if st.session_state.jogador_atual == 2 else st.session_state.nome_jogador2
            st.error(f"{perdedor} retirou a última bolinha e PERDEU!")
            st.success(f"🏆 {vencedor} venceu! Parabéns!")
            if st.button("Jogar Novamente"):
                st.session_state.jogo_iniciado = False
                resetar_estado()
                st.rerun()
            return

        if st.session_state.modo == "Um Jogador vs Bot" and st.session_state.jogador_atual == 2:
            if st.session_state.vez_bot:
                jogada = jogada_bot(
                    st.session_state.total_bolinhas,
                    st.session_state.max_retirada,
                    st.session_state.nome_jogador2,
                    st.session_state.dificuldade
                )
                st.session_state.total_bolinhas -= jogada
                st.session_state.jogador_atual = 1
                st.session_state.vez_bot = False
                st.session_state.msg_ultima_jogada_bot = f"O Bot retirou {jogada} bolinhas!"
                st.rerun()
            else:
                st.session_state.vez_bot = True
                st.rerun()

        else:
            jogador_atual_nome = st.session_state.nome_jogador1 if st.session_state.jogador_atual == 1 else st.session_state.nome_jogador2
            st.subheader(f"Vez de: {jogador_atual_nome}")

            max_permitido = min(st.session_state.max_retirada, st.session_state.total_bolinhas)
            with st.form("jogada_form"):
                jogada = st.number_input(f"{jogador_atual_nome}, quantas bolinhas deseja retirar (1-{max_permitido})?", min_value=1, max_value=max_permitido, value=1)
                submit = st.form_submit_button("Realizar Jogada")
                if submit:
                    st.session_state.total_bolinhas -= jogada
                    st.session_state.jogador_atual = 3 - st.session_state.jogador_atual
                    st.rerun()

        if st.button("Reiniciar Jogo"):
            st.session_state.jogo_iniciado = False
            resetar_estado()
            st.rerun()

if __name__ == "__main__":
    main()
