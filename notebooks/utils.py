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
    ],
    "Comportamento do condutor": [
        "Transitar na contramão",
        "Acessar a via sem observar a presença dos outros veículos",
        "Trafegar com motocicleta (ou similar) entre as faixas",
        "Mal súbito do condutor",
        "Frear bruscamente",
        "Velocidade Incompatível",
        "Reação tardia ou ineficiente do condutor",
        "Manobra de mudança de faixa",
        "Condutor deixou de manter distância do veículo da frente",
        "Ingestão de álcool pelo condutor",
        "Condutor desrespeitou a iluminação vermelha do semáforo",
        "Ausência de reação do condutor",
        "Ultrapassagem Indevida",
        "Desrespeitar a preferência no cruzamento",
        "Conversão proibida",
        "Condutor Dormindo",
        "Condutor usando celular",
        "Transitar no acostamento",
        "Estacionar ou parar em local proibido",
        "Participar de racha",
        "Transitar na calçada",
        "Deixar de acionar o farol da motocicleta (ou similar)",
        "Ingestão de substâncias psicoativas pelo condutor",
        "Retorno proibido",
        "Acesso irregular",
    ],
    "Comportamento do pedestre": [
        "Entrada inopinada do pedestre",
        "Pedestre cruzava a pista fora da faixa",
        "Ingestão de álcool e/ou substâncias psicoativas pelo pedestre",
        "Pedestre andava na pista",
        "Ingestão de álcool ou de substâncias psicoativas pelo pedestre",
    ],
    "Condição do veículo": [
        "Problema com o freio",
        "Demais falhas mecânicas ou elétricas",
        "Avarias e/ou desgaste excessivo no pneu",
        "Carga excessiva e/ou mal acondicionada",
        "Deficiência do Sistema de Iluminação/Sinalização",
        "Problema na suspensão",
        "Faróis desregulados",
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
    ],
    "Fatores ambientais": [
        "Chuva", 
        "Neblina",
        "Fumaça",
        "Demais Fenômenos da natureza",
        "Animais na Pista",
    ]
}


TIPO = {
    "Colisões": [
        "Colisão frontal",
        "Colisão transversal",
        "Colisão traseira",
        "Colisão lateral",
        "Colisão lateral mesmo sentido",
        "Colisão com objeto",
        "Colisão lateral sentido oposto"
    ],
    "Atropelamentos": [
        "Atropelamento de Pedestre",
        "Atropelamento de Animal"
    ],
    "Acidentes diversos": [
        "Tombamento",
        "Capotamento",
        "Engavetamento",
        "Queda de ocupante de veículo",
        "Saída de leito carroçável",
        "Incêndio",
        "Derramamento de carga",
        "Eventos atípicos"
    ]
}


def categorizar_causa(causa):
    for k, v in CAUSA.items():
        if causa in v:
            return k
    return causa


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

    raise ValueError("Could not compute severity")
