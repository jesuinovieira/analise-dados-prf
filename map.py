import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ydata_profiling import ProfileReport

YEAR = "2021"
file1 = f"data/raw/{YEAR}-grouped-by-occurrence/datatran2021.csv"

df1 = pd.read_csv(file1, sep=";", encoding="iso-8859-1")
df1.describe()

dtypes1 = {
    "id": int,
    "data_inversa": "datetime64[ns]",
    "dia_semana": "category",
    "horario": "object",  # Change it to a more specific time-related type if needed
    "uf": "category",
    "br": "category",
    "km": "float64",
    "municipio": "category",
    "causa_acidente": "category",
    "tipo_acidente": "category",
    "classificacao_acidente": "category",
    "fase_dia": "category",
    "sentido_via": "category",
    "condicao_metereologica": "category",
    "tipo_pista": "category",
    "tracado_via": "category",
    "uso_solo": "category",
    "pessoas": int,
    "mortos": int,
    "feridos_leves": int,
    "feridos_graves": int,
    "ilesos": int,
    "ignorados": int,
    "feridos": int,
    "veiculos": int,
    "latitude": "float64",
    "longitude": "float64",
    "regional": "category",
    "delegacia": "category",
    "uop": "category"
}

df1 = df1[df1.uf.isin(["PR", "SC", "RS"])]

df1["km"] = df1["km"].str.replace(",", ".")
df1["latitude"] = df1["latitude"].str.replace(",", ".")
df1["longitude"] = df1["longitude"].str.replace(",", ".")

df1 = df1.astype(dtypes1)

fig = px.scatter_geo(df1, lat="latitude", lon="longitude", hover_name="id")
fig.update_layout(
    mapbox={"style": "open-street-map"},
    margin={"l": 0, "r": 0, "t": 0, "b": 0},
)

fig.show()
