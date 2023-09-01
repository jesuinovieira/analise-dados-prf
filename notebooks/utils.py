import plotly
import numpy as np
import plotly.graph_objects as go

CAUSA = {
    "Condição da via": [
        "Pista Escorregadia", 
        "Curva acentuada",
        "Acumulo de água sobre o pavimento",
        "Acumulo de óleo sobre o pavimento",
        "Acumulo de areia ou detritos sobre o pavimento",
        "Pista esburacada",
        "Afundamento ou ondulação no pavimento",
        "Acostamento em desnível",
        "Restrição de visibilidade em curvas horizontais",
        "Obstrução na via",
        "Desvio temporário",
        "Pista em desnível",
        "Restrição de visibilidade em curvas verticais",
        "Iluminação deficiente",
        "Sinalização mal posicionada",
        "Sinalização com defeito",
        "Área urbana sem a presença de local apropriado para a travessia de pedestres",
        "Redutor de velocidade em desacordo",
        "Declive acentuado",
        "Objeto estático sobre o leito carroçável",
        "Defeito na Via",
    ],
    "Comportamento do condutor: desrespeito às sinalizações": [
        "Condutor desrespeitou a iluminação vermelha do semáforo",
        "Conversão proibida",
        "Ultrapassagem Indevida",
        "Desrespeitar a preferência no cruzamento",
        "Retorno proibido",
        "Acesso irregular",
        "Transitar na contramão",
        "Transitar no acostamento",
        "Estacionar ou parar em local proibido",
        "Transitar na calçada",
    ],
    "Comportamento do condutor: direção perigosa": [
        "Acessar a via sem observar a presença dos outros veículos",
        "Trafegar com motocicleta (ou similar) entre as faixas",
        "Frear bruscamente",
        "Velocidade Incompatível",
        "Reação tardia ou ineficiente do condutor",
        "Manobra de mudança de faixa",
        "Condutor deixou de manter distância do veículo da frente",
        "Ausência de reação do condutor",
        "Condutor Dormindo",
        "Condutor usando celular",
        "Participar de racha",
        "Deixar de acionar o farol da motocicleta (ou similar)",
        "Desobediência às normas de trânsito pelo condutor",
        "Falta de Atenção à Condução",
        "Não guardar distância de segurança",
    ],
    "Comportamento do condutor: condições de saúde/consciência": [
        "Mal súbito do condutor",
        "Mal Súbito",
        "Ingestão de álcool pelo condutor",
        "Ingestão de Álcool",
        "Ingestão de substâncias psicoativas pelo condutor",
        "Ingestão de Substâncias Psicoativas",
        "Agressão Externa",
    ],
    "Comportamento do pedestre": [
        "Entrada inopinada do pedestre",
        "Pedestre cruzava a pista fora da faixa",
        "Ingestão de álcool e/ou substâncias psicoativas pelo pedestre",
        "Pedestre andava na pista",
        "Ingestão de álcool ou de substâncias psicoativas pelo pedestre",
        "Desobediência às normas de trânsito pelo pedestre",
        "Falta de Atenção do Pedestre",
    ],
    "Condição do veículo": [
        "Problema com o freio",
        "Demais falhas mecânicas ou elétricas",
        "Avarias e/ou desgaste excessivo no pneu",
        "Carga excessiva e/ou mal acondicionada",
        "Deficiência do Sistema de Iluminação/Sinalização",
        "Problema na suspensão",
        "Faróis desregulados",
        "Defeito Mecânico no Veículo",
        "Deficiência ou não Acionamento do Sistema de Iluminação/Sinalização do Veículo",
    ],
    "Infraestrutura e sinalização": [
        "Falta de elemento de contenção que evite a saída do leito carroçável",
        "Falta de acostamento",
        "Demais falhas na via",
        "Modificação proibida",
        "Faixas de trânsito com largura insuficiente",
        "Ausência de sinalização",
        "Semáforo com defeito",
        "Obras na pista",
        "Restrição de Visibilidade",
        "Sinalização da via insuficiente ou inadequada",
    ],
    "Fatores ambientais": [
        "Chuva", 
        "Neblina",
        "Fumaça",
        "Demais Fenômenos da natureza",
        "Animais na Pista",
        "Fenômenos da Natureza",
    ]
}

TIPO = {
    "Colisão": [
        "Colisão frontal",
        "Colisão transversal",
        "Colisão traseira",
        "Colisão lateral",
        "Colisão lateral mesmo sentido",
        "Colisão com objeto",
        "Colisão lateral sentido oposto"
    ],
    "Atropelamento": [
        "Atropelamento de Pedestre",
        "Atropelamento de Animal"
    ],
}

PALETTE = plotly.colors.qualitative.Alphabet * 2
PALETTE = [item for item in PALETTE if item != "#E2E2E2"]


def categorizar_causa(causa):
    for k, v in CAUSA.items():
        if causa in v:
            return k
    
    raise ValueError(f"Could not categorize accident cause: '{causa}'")


def categorizar_tipo(tipo):
    for k, v in TIPO.items():
        if tipo in v:
            return k

    return tipo


def categorizar_severidade(row):
    if row.mortos > 0:
        return 13
    if row.feridos_graves > 0:
        return 7
    if row.feridos_leves > 0:
        return 3
    if row.ilesos > 0:
        return 1
    # If none of the above fits, use classificaco_acidente
    if row.classificacao_acidente == "Com Vítimas Fatais":
        return 13
    if row.classificacao_acidente == "Com Vítimas Feridas":
        return 5
    if row.classificacao_acidente == "Sem Vítimas":
        return 1

    raise ValueError("Could not categorize severity")


def group_others(dataset, n=5):
    copy = dataset.copy()
    
    numericals = copy._get_numeric_data().columns
    categoricals = set(copy.columns) - set(numericals)

    for column in categoricals:
        counts = copy[column].value_counts()
        top_labels = counts.nlargest(n).index.tolist()
        
        copy[column] = copy[column].apply(lambda x: x if x in top_labels else "Outros")
    
    return copy


def plot_map(df, labels, dst, title):
    fig = go.Figure()

    for label in labels:
        subset = df[df.cluster == label]
        color = PALETTE[label]

        scatter = go.Scattermapbox(
            lat=subset.latitude,
            lon=subset.longitude,
            mode="markers",
            marker=dict(size=5, color=color),
            text=f"{label}",
            showlegend=True,
            name=f"Cluster {label + 1}"
        )

        fig.add_trace(scatter)

    fig.update_layout(
        title=title,
        title_x=0.95,
        title_y=0.1,
        mapbox_style="open-street-map",
        mapbox=dict(center=dict(lat=-28.25, lon=-53), zoom=5.25),
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )

    if dst:
        ratio = (1 + 5 ** 0.5) / 2
        width = 1200
        height = int(width / ratio)

        fig.write_html(f"{dst}.html")
        fig.write_image(
            f"{dst}.png",
            format="png",
            engine="kaleido",
            width=width,
            height=height
        )

    fig.show()
