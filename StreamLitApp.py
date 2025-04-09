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

@st.dialog(title="json do esperimento",width="large")
def show_popup(exp):
    st.write("Aqui você pode visualizar o JSON do experimento.")
    st.json(all_experiments_jsons[exp], expanded=1)

# Caminho da pasta com os .pkl
PKL_DIR = "Results"


st.set_page_config(page_title="Comparador de Experimentos", layout="wide")
st.title("Comparador de Experimentos de Recomendação")

# Carregar arquivos
pkl_files = [f for f in os.listdir(PKL_DIR) if f.endswith(".pkl")]
if not pkl_files:
    st.warning("Nenhum arquivo .pkl encontrado na pasta 'resultados_pkl'.")
    st.stop()

# carregar experimentos 
all_experiments = {}
all_experiments_metrics = {}
all_experiments_jsons = {}
experiment_colors = {}
all_metrics_set = set()


for file in sorted(pkl_files):
    color = generate_color(file)

    with open(os.path.join(PKL_DIR, file), "rb") as f:
        data = pickle.load(f)

    raw_metrics = data.get("avg_metrics", {})
    metrics = {k.replace("avg_", ""): v for k, v in raw_metrics.items()}

    config = data.get("config", {})
    model_name = str(config.get("model_name", "desconhecido"))

    if metrics:
        all_experiments[file] = file
        all_experiments_metrics[file] = metrics
        all_metrics_set.update(metrics.keys())
        experiment_colors[file] = color
        all_experiments_jsons[file] = data

#### SIDE BAR ####

##### Filtros de experimentos  #####

filter_keys = ["dataset", "obs", "model_name"]
filter_options = {k: set() for k in filter_keys}

for exp in all_experiments_jsons:
    config = all_experiments_jsons[exp]['config']
    for key in filter_keys:
        filter_options[key].add(config.get(key, "desconhecido"))

selected_filters = {}
expander_exps = st.sidebar.expander("Filtros",False)

for key in filter_keys:
    sorted_options = sorted(filter_options[key])
    selected = expander_exps.multiselect(
        f"Filtrar por {key}",
        sorted_options,
        default=sorted_options
    )
    selected_filters[key] = selected

# Inicializa session_state uma única vez
if "selected_experiments" not in st.session_state:
    st.session_state.selected_experiments = {exp: True for exp in all_experiments}

check_all = st.sidebar.checkbox("Selecionar/Retirar todos os experimentos", value=True)
if check_all:
    for exp in all_experiments:
        st.session_state.selected_experiments[exp] = True
else:
    for exp in all_experiments:
        st.session_state.selected_experiments[exp] = False

##### EXPERIMENTOS ####

st.sidebar.header("Experimentos")
selected_experiments = {}

for exp in sorted(all_experiments):

    ### referente aos filtros de experimentos -- INICIO
    config = all_experiments_jsons[exp]['config'] 

    passed = True
    for key in filter_keys:
        value = config.get(key, "desconhecido")
        if value not in selected_filters[key]:
            passed = False
            break

    if not passed:
        if st.session_state.selected_experiments.get(exp, True):
            selected_experiments[exp] = exp
        continue
    ### referente aos filtros de experimentos -- FIM

    col1, col2, col3 = st.sidebar.columns([0.5,7.5,1.5])

    # Coluna 1 com a cor do experimento
    with col1:
        st.markdown(
            f"<div style='width: 14px; height: 14px; background-color:{experiment_colors[exp]}; border-radius: 50%; margin-top: 8px;'></div>",
            unsafe_allow_html=True
        )

    # Coluna 2 com o checkbox
    with col2:
        checked = st.checkbox(
            exp,
            value=st.session_state.selected_experiments.get(exp, True),
            key=f"cb_{exp}"
        )
        st.session_state.selected_experiments[exp] = checked
        if checked:
            selected_experiments[exp] = exp
        
    # Coluna 3 com o json
    with col3:
        if st.button("JSON", key=f"btn_{exp}"):
            show_popup(exp)
if not all_experiments:
    st.warning("Nenhum experimento foi selecionado.")
    st.stop()

## Filtro de metricas

expander_metrics = st.sidebar.expander("📐 Selecionar Métricas",False)
all_metrics = sorted(list(all_metrics_set))
dafault_metrics = ['GT_HitRate@10','HitRate@10', 'GT_NDCG@10','NDCG@10']
selected_metrics = expander_metrics.multiselect("Escolha as métricas a visualizar:", all_metrics, default=dafault_metrics)

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

for exp in selected_experiments:
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
    config_clean["runtime_seconds"] = runtime
    config_clean["runtime"] = formatted_runtime
    config_clean["recomendations"] = data['config'].get("test_run") if data['config'].get("test_run",0) > 0 else 943
    config_clean["color"] = experiment_colors.get(exp, "#000")
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
    st.dataframe(df_configs, use_container_width=True, )

### TABELA CONFIGURAÇÃO ####


### GRAFICO DE TEMPO DE EXECUÇÂO #### 

st.scatter_chart(
    data=df_configs,
    x="recomendations",
    x_label="Quantidade de Recomendacoes",
    y="runtime_seconds",
    y_label="Tempo de Execução",
    color="color")

### GRAFICO DE TEMPO DE EXECUÇÂO ####


### TABELA MÉTRICAS ####

st.subheader("📋 Tabela Comparativa de Métricas")

col1, col2 = st.columns([0.05, 0.95])  

# Criar DataFrame geral com apenas métricas selecionadas
exp_metrics_filtered = {
    exp: {metric: all_experiments_metrics[exp].get(metric, None) for metric in selected_metrics}
    for exp in selected_experiments
}
df_exp_metrics = pd.DataFrame(exp_metrics_filtered).T
df_exp_metrics = df_exp_metrics.sort_index()


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
        df_exp_metrics.style.apply(highlight_max, axis=0),
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

def plot_bar_chart_st(df_plot, title):
    st.markdown(f"### {title}")
    st.bar_chart(df_plot,stack=False,horizontal= False)

col1, col2 = st.columns(2)
st.write("asdasdasd")
st.write(df_exp_metrics[metrics_normal])

with col1:
    if metrics_normal:
        st.subheader("Sem 'GT'")
        df_normal = df_exp_metrics[metrics_normal].T
        #plot_bar_chart(df_normal, "Métricas sem GT")
        plot_bar_chart_st(df_normal, "Métricas sem GT")

with col2:
    if metrics_gt:
        st.subheader("Com 'GT'")
        df_gt = df_exp_metrics[metrics_gt].T
        plot_bar_chart(df_gt, "Métricas com GT")


### GRÁFICOS PARA MÉTRICAS ###

# Download CSV
csv = df_exp_metrics.to_csv().encode("utf-8")
st.download_button("Baixar comparação em CSV", csv, file_name="comparacao_experimentos.csv", mime="text/csv")
