import streamlit as st
import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
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
dafault_metrics = ['GT_HitRate@10','HitRate@10', 'GT_NDCG@10','NDCG@10','GT_Hallucination','GT_NDCG@10_safe','GT_HitRate@10_safe']
selected_metrics = expander_metrics.multiselect("Escolha as métricas a visualizar:", all_metrics, default=dafault_metrics)

if not selected_metrics:
    st.warning("Nenhuma métrica foi selecionada.")
    st.stop()

# Filtrar métricas GT e não-GT
metrics_gt = [m for m in selected_metrics if "GT" in m and "Hallucination" not in m and "safe" not in m]
metrics_normal = [m for m in selected_metrics if "GT" not in m and "safe" not in m]
metrics_hallucination = [m for m in selected_metrics if "Hallucination" in m]
metrics_safe = [m for m in selected_metrics if "safe" in m]

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
df_configs_sorted = df_configs.sort_values("runtime_seconds", ascending=False).reset_index()
df_configs_sorted = df_configs_sorted.rename(columns={"index": "experimento"})
# Converte para minutos
df_configs_sorted["runtime_minutes"] = df_configs_sorted["runtime_seconds"] / 60
# Adiciona coluna formatada com ' mins'
df_configs_sorted["runtime_text"] = df_configs_sorted["runtime_minutes"].map(lambda x: f"{x:.2f} mins")

# Usa o nome do experimento como categoria no eixo Y
#df_configs_sorted["experimento"] = df_configs_sorted.index.astype(str)



# Altura proporcional
chart_height = 100 * len(df_configs_sorted)

bars = alt.Chart(df_configs_sorted).mark_bar(
    yOffset=5,
    cornerRadiusEnd=5,
    height=20  # espessura da barra
).encode(
    y=alt.Y(
        "experimento:N",
        scale=alt.Scale(padding=0),
        axis=alt.Axis(
            bandPosition=0,
            grid=True,
            domain=False,
            ticks=False,
            labelAlign="left",
            labelBaseline="middle",
            labelPadding=-5,
            labelOffset=-15,
            labelFontSize=18,
            title=None,
            labelLimit=0
        )
    ),
    x=alt.X(
        "runtime_minutes:Q",
        axis=alt.Axis(grid=False),
        title="Tempo de Execução (min)"
    ),
    color=alt.Color(
        "experimento:N",
        scale=alt.Scale(range=df_configs_sorted["color"].tolist()),
        legend=None
    ),
    tooltip=[
        alt.Tooltip("experimento:N", title="Experimento"),
        alt.Tooltip("runtime_minutes:Q", title="Tempo (min)", format=".2f")
    ],
).properties(height=chart_height)

# Texto com valores
text = alt.Chart(df_configs_sorted).mark_text(
    align="left",
    baseline="middle",
    dx=3,   # deslocamento à direita da barra
    dy=5,   # deslocamento para baixo
    fontSize=16,
    color="white",
).encode(
    y=alt.Y("experimento:N"),
    x=alt.X("runtime_minutes:Q"),
    text=alt.Text("runtime_text:N")
)

# Combina os dois
chart = (bars + text).properties(height=chart_height)

st.altair_chart(chart, use_container_width=True)


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

def plot_bar_chart_vega(df_plot, title):
    st.markdown(f"### {title}")
    
    # Derrete o DataFrame: transforma colunas de métricas em linhas
    df_long = df_plot.drop(columns=["cor"]).reset_index().melt(
        id_vars=["index"], var_name="Métrica", value_name="Valor"
    )

    # Renomeia a coluna 'index' para 'experimento'
    df_long = df_long.rename(columns={"index": "experimento"})

    # Limpa os nomes das métricas para exibição
    df_long["Métrica_Limpa"] = (
        df_long["Métrica"]
        .str.replace(r"^GT_", "", regex=True)
        .str.replace(r"_safe$", "", regex=True)
    )

    # Lista com os nomes e cores dos experimentos
    experimentos = df_long["experimento"].unique().tolist()
    cores = df_plot["cor"].values.tolist()

    chart = alt.Chart(df_long).mark_bar(cornerRadiusEnd=5).encode(
        #x=alt.X("Métrica:N", title="Métricas"),
        x=alt.X("Métrica_Limpa:N", title=None, axis=alt.Axis(
                                                    labelFontSize=16,
                                                    labelAngle=0,
                                                    )),
        y=alt.Y("Valor:Q", title=None, scale=alt.Scale(domain=[0, 1])),
        xOffset=alt.XOffset("experimento:N", title="Experimentos"),
        color=alt.Color(
            "experimento:N",
            scale=alt.Scale(domain=experimentos, range=cores),
            legend=None
        ),
        tooltip=[
            alt.Tooltip("experimento:N", title="Experimento"),
            alt.Tooltip("Métrica:N", title="Métrica"),
            alt.Tooltip("Valor:Q", title="Valor", format=".3f"),
        ],
    )

    st.altair_chart(chart, use_container_width=True)

def plot_bar_chart_vega_halluci(df_plot, title):
    st.markdown(f"### {title}")
    
    # Derrete o DataFrame: transforma colunas de métricas em linhas
    df_long = df_plot.drop(columns=["cor"]).reset_index().melt(
        id_vars=["index"], var_name="Métrica", value_name="Valor"
    )

    # Renomeia a coluna 'index' para 'experimento'
    df_long = df_long.rename(columns={"index": "experimento"})

    # Lista com os nomes e cores dos experimentos
    experimentos = df_long["experimento"].unique().tolist()
    cores = df_plot["cor"].values.tolist()

    # Altura proporcional ao número de experimentos
    chart_height = 100 * len(experimentos)

    chart = alt.Chart(df_long).mark_bar(
        yOffset=5,
        cornerRadiusEnd=5,
        height=20  # controla a espessura da barra
    ).encode(
        y=alt.Y(
            "experimento:N",
            scale=alt.Scale(padding=0),
            axis=alt.Axis(
                bandPosition=0,
                grid=True,
                domain=False,
                ticks=False,
                labelAlign="left",
                labelBaseline="middle",
                labelPadding=-5,
                labelOffset=-15,
                labelFontSize=18,
                title=None,
                labelLimit=0
            )
        ),
        x=alt.X(
            "Valor:Q",
            scale=alt.Scale(domain=[0, 1]),
            axis=alt.Axis(grid=False),
            title=None
        ),
        color=alt.Color(
            "experimento:N",
            scale=alt.Scale(domain=experimentos, range=cores),
            legend=None
        ),
        tooltip=[
            alt.Tooltip("experimento:N", title="Experimento"),
            alt.Tooltip("Valor:Q", title="Valor"),
        ],
    ).properties(height=chart_height)

    st.altair_chart(chart, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    if metrics_gt:
        df_gt = df_exp_metrics[metrics_gt]
        df_gt["cor"] = df_gt.index.map(lambda exp: experiment_colors.get(exp, "#000"))
        plot_bar_chart_vega(df_gt, "Métricas com GT")



    if metrics_hallucination:
        df_hallucination = df_exp_metrics[metrics_hallucination]
        df_hallucination["cor"] = df_hallucination.index.map(lambda exp: experiment_colors.get(exp, "#000"))
        plot_bar_chart_vega_halluci(df_hallucination, "Alucinação")

with col2:

    if metrics_safe:
        df_safe = df_exp_metrics[metrics_safe]
        df_safe["cor"] = df_safe.index.map(lambda exp: experiment_colors.get(exp, "#000"))
        plot_bar_chart_vega(df_safe, "Métricas sem alucinação")

    if metrics_normal:
        df_normal = df_exp_metrics[metrics_normal]
        df_normal["cor"] = df_normal.index.map(lambda exp: experiment_colors.get(exp, "#000"))
        plot_bar_chart_vega(df_normal, "Métricas sem GT")

### GRÁFICOS PARA MÉTRICAS ###

# Download CSV
csv = df_exp_metrics.to_csv().encode("utf-8")
st.download_button("Baixar comparação em CSV", csv, file_name="comparacao_experimentos.csv", mime="text/csv")
