# app_realtime_final_cloud.py
import pandas as pd
import streamlit as st
import time

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(page_title="Ranking em Tempo Real", layout="wide")
st.title("🏆 Ranking em Tempo Real")

# =========================
# CSS ANIMAÇÕES
# =========================
st.markdown("""
<style>
@keyframes pulse {
  0% { box-shadow: 0 0 15px gold; transform: translateY(0px); }
  50% { box-shadow: 0 0 35px gold; transform: translateY(-10px); }
  100% { box-shadow: 0 0 15px gold; transform: translateY(0px); }
}
.pulse {
  animation: pulse 2s infinite;
}

.highlight {
  background-color: #ffeaa7;
  padding: 10px;
  border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# FUNÇÃO PARA CARREGAR DADOS
# =========================
@st.cache_data(ttl=10)
def carregar_dados():
    url = "https://docs.google.com/spreadsheets/d/1hHHm1Wu6KIECV7BHOpA20i9gLwbz6eQp5D6td9LUxHw/gviz/tq?tqx=out:csv"
    df = pd.read_csv(url)

    required_cols = ["Nome", "Pontuacao", "Foto"]
    if not all(col in df.columns for col in required_cols):
        st.error(f"Colunas incorretas. Precisamos de: {required_cols}")
        st.stop()

    df = df.sort_values(by="Pontuacao", ascending=False).reset_index(drop=True)
    df["Ranking"] = df.index + 1

    return df

# =========================
# BUSCA
# =========================
busca = st.text_input("🔍 Buscar participante")

# =========================
# AUTO REFRESH
# =========================
placeholder = st.empty()

while True:
    with placeholder.container():

        # Ranking completo (NUNCA alterar)
        df_full = carregar_dados()

        # DataFrame filtrado (apenas para exibição)
        if busca:
            df_filtrado = df_full[df_full["Nome"].str.contains(busca, case=False, na=False)]
        else:
            df_filtrado = df_full

        # =========================
        # LAYOUT
        # =========================
        col_esq, col_dir = st.columns([1, 1])

        # =========================
        # TOP 3 GLOBAL
        # =========================
        with col_esq:
            st.subheader("🥇 Top 3")

            top3 = df_full.head(3)

            medalha_cores = ["#FFD700", "#C0C0C0", "#CD7F32"]
            sizes = [160, 120, 100]
            medalhas = ["🥇", "🥈", "🥉"]

            podium_cols = st.columns(3)

            for i, (_, row) in enumerate(top3.iterrows()):
                with podium_cols[i]:
                    classe_pulso = "pulse" if i == 0 else ""

                    st.markdown(
                        f"""
                        <div style="display:flex; justify-content:center;">
                            <div class="{classe_pulso}" style="
                                background-color: {medalha_cores[i]};
                                width: 170px;
                                height: 180px;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                border-radius: 10px;
                                margin-bottom: 10px;
                            ">
                                <img src="{row['Foto']}" width="{sizes[i]}" style="border-radius: 50%;">
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(f"### {medalhas[i]}")
                    st.markdown(f"**#{row['Ranking']} {row['Nome']}**")
                    st.write(f"⭐ {row['Pontuacao']} pontos")

        # =========================
        # RANKING GERAL (COM DESTAQUE NA BUSCA)
        # =========================
        with col_dir:
            st.subheader("📋 Ranking Geral")

            for _, row in df_filtrado.iterrows():

                destaque = ""
                if busca and busca.lower() in row["Nome"].lower():
                    destaque = "highlight"

                c1, c2, c3 = st.columns([1, 3, 1])

                with c1:
                    st.image(row["Foto"], width=60)

                with c2:
                    st.markdown(
                        f'<div class="{destaque}"><b>#{row["Ranking"]} - {row["Nome"]}</b></div>',
                        unsafe_allow_html=True
                    )

                with c3:
                    st.write(f"⭐ {row['Pontuacao']}")

                st.divider()

        # =========================
        # GRÁFICO
        # =========================
        st.subheader("📊 Pontuação dos Participantes")
        st.bar_chart(df_full.set_index("Nome")["Pontuacao"])

    time.sleep(5)
