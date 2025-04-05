import streamlit as st
import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

from hashlib import md5

# Função para destacar o melhor valor por coluna
def highlight_max(s):
    is_max = s == s.max()
    return ['color: gold; font-weight: bold;' if v else '' for v in is_max]

# Gerar cores fixas para cada experimento
def generate_color(name):
    return "#" + md5(name.encode()).hexdigest()[:6]

# Caminho da pasta com os .pkl
PKL_DIR = "Results"


st.set_page_config(page_title="Comparador de Experimentos", layout="wide")
st.title("Comparador de Experimentos de Recomendação")

# Carregar arquivos
pkl_files = [f for f in os.listdir(PKL_DIR) if f.endswith(".pkl")]
if not pkl_files:
    st.warning("Nenhum arquivo .pkl encontrado na pasta 'resultados_pkl'.")
    st.stop()

#### SIDE BAR ####

st.sidebar.header("Experimentos")
all_experiments = {}
all_metrics_set = set()

experiment_colors = {}

for file in sorted(pkl_files):
    color = generate_color(file)
    col1, col2 = st.sidebar.columns([0.05, 0.85])

    # Coluna 1 com a cor do experimento
    with col1:
        st.markdown(
            f"<div style='width: 14px; height: 14px; background-color:{color}; border-radius: 50%; margin-top: 8px;'></div>",
            unsafe_allow_html=True
        )
    
    # Coluna 2 com o checkbox
    with col2:
        show = st.checkbox(file, value=True, key=f"cb_{file}")
    
    if show:
        with open(os.path.join(PKL_DIR, file), "rb") as f:
            data = pickle.load(f)
        raw_metrics = data.get("avg_metrics", {})
        metrics = {k.replace("avg_", ""): v for k, v in raw_metrics.items()}
        
        if metrics:
            all_experiments[file] = metrics
            all_metrics_set.update(metrics.keys())
            experiment_colors[file] = color

if not all_experiments:
    st.warning("Nenhum experimento foi selecionado.")
    st.stop()


# Sidebar: selecionar métricas
all_metrics = sorted(list(all_metrics_set))
st.sidebar.header("📐 Selecionar Métricas")
selected_metrics = st.sidebar.multiselect("Escolha as métricas a visualizar:", all_metrics, default=all_metrics)

if not selected_metrics:
    st.warning("Nenhuma métrica foi selecionada.")
    st.stop()

# Filtrar métricas GT e não-GT
metrics_gt = [m for m in selected_metrics if "GT" in m]
metrics_normal = [m for m in selected_metrics if "GT" not in m]

#### SIDE BAR ####


### TABELA CONFIGURAÇÃO ####

st.subheader("📋 Tabela Comparativa de Configurações")

# Coleta das configurações dos experimentos visíveis
df_configs = pd.DataFrame()

col1, col2 = st.columns([0.05, 0.95])  

for exp in all_experiments:
    with open(os.path.join(PKL_DIR, exp), "rb") as f:
        data = pickle.load(f)
    config = data.get("config", {})
    config_clean = {k: str(v) for k, v in config.items()}
    # Adiciona o runtime formatado como HH:MM:SS
    runtime = data.get("runtime", None)
    if runtime is not None:
        formatted_runtime = str(timedelta(seconds=int(runtime)))
    else:
        formatted_runtime = "N/A"

    config_clean["__runtime"] = formatted_runtime
    df_configs = pd.concat([df_configs, pd.DataFrame(config_clean, index=[exp])])


# Coluna 1: Cor do experimento
with col1:
    espaco_html = "<div style='height: 35px;'></div>"
    st.markdown(espaco_html, unsafe_allow_html=True)
    cor_html = "<div style='display: flex; flex-direction: column;'>"

    for exp in df_configs.index:
        color = experiment_colors.get(exp, "#000")
        cor_html += (
            "<div style='height: 35px; display: flex; align-items: center;'>"
            f"<div style='width: 14px; height: 14px; background-color:{color}; "
            f"border-radius: 50%; margin: auto;'></div>"
            "</div>"
        )
    cor_html += "</div>"
    st.markdown(cor_html, unsafe_allow_html=True)

# Coluna 2: Tabela com configurações
with col2:
    st.dataframe(df_configs, use_container_width=True)

### TABELA CONFIGURAÇÃO ####

### TABELA MÉTRICAS ####

st.subheader("📋 Tabela Comparativa de Métricas")

col1, col2 = st.columns([0.05, 0.95])  

# Criar DataFrame geral com apenas métricas selecionadas
filtered_data = {
    exp: {metric: all_experiments[exp].get(metric, None) for metric in selected_metrics}
    for exp in all_experiments
}
df_all = pd.DataFrame(filtered_data).T
df_all = df_all.sort_index()


# Coluna 1: Cor do experimento
with col1:
    espaco_html = "<div style='height: 35px;'></div>"
    st.markdown(espaco_html, unsafe_allow_html=True)
    cor_html = "<div style='display: flex; flex-direction: column;'>"
    for exp in df_configs.index:
        color = experiment_colors.get(exp, "#000")
        cor_html += (
            "<div style='height: 35px; display: flex; align-items: center;'>"
            f"<div style='width: 14px; height: 14px; background-color:{color}; "
            f"border-radius: 50%; margin: auto;'></div>"
            "</div>"
        )
    cor_html += "</div>"
    st.markdown(cor_html, unsafe_allow_html=True)

# Coluna 2: Tabela com métricas
with col2:
    st.dataframe(
        df_all.style.apply(highlight_max, axis=0),
        use_container_width=True
    )
### TABELA MÉTRICAS ####


### GRÁFICOS PARA MÉTRICAS ###

# Função utilitária para plotar gráfico de barras
def plot_bar_chart(df_plot, title):
    fig, ax = plt.subplots(figsize=(10, len(df_plot) * 0.5))

    # Ordena as cores de acordo com as colunas (nomes dos experimentos)
    colors = [experiment_colors.get(col, "#333333") for col in df_plot.columns]

    df_plot.plot(kind="bar", ax=ax, color=colors)

    ax.set_ylabel("Valor")
    ax.set_xlabel("Métrica")
    ax.set_title(title)
    plt.xticks(rotation=45, ha="right")

    # Legenda personalizada
    ax.legend(
        title="Experimentos",
        title_fontsize="12",
        fontsize="10",
        loc="upper center",
        bbox_to_anchor=(0.5,-0.5),  
        frameon=True,            
        framealpha=0.9,
        edgecolor="gray"
    )

    st.pyplot(fig)

col1, col2 = st.columns(2)

with col1:
    if metrics_normal:
        st.subheader("Sem 'GT'")
        df_normal = df_all[metrics_normal].T
        plot_bar_chart(df_normal, "Métricas sem GT")

with col2:
    if metrics_gt:
        st.subheader("Com 'GT'")
        df_gt = df_all[metrics_gt].T
        plot_bar_chart(df_gt, "Métricas com GT")


### GRÁFICOS PARA MÉTRICAS ###

# Download CSV
csv = df_all.to_csv().encode("utf-8")
st.download_button("Baixar comparação em CSV", csv, file_name="comparacao_experimentos.csv", mime="text/csv")
