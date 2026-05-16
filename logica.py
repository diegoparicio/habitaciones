import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import os

# -----------------------------
# 1. CARGA DE DATOS
# -----------------------------
BASE_DIR = os.path.dirname(__file__)

df = pd.read_csv(
    os.path.join(BASE_DIR, "dataset_inquilinos.csv"),
    index_col="id_inquilino"
)

df.columns = [
'horario', 'bioritmo', 'nivel_educativo', 'leer', 'animacion', 
'cine', 'mascotas', 'cocinar', 'deporte', 'dieta', 'fumador',
'visitas', 'orden', 'musica_tipo', 'musica_alta', 'plan_perfecto', 'instrumento'
]

# Limpieza de datos: convertir a string y eliminar espacios en blanco
df = df.astype(str).apply(lambda x: x.str.strip())

# -----------------------------
# 2. ENCODER (GLOBAL)
# -----------------------------
encoder = OneHotEncoder(
    sparse_output=False,
    handle_unknown="ignore"
)

# -----------------------------
# 3. FUNCIÓN PRINCIPAL
# -----------------------------
def inquilinos_compatibles(id_inquilinos, topn):

    # validar IDs
    for id_inquilino in id_inquilinos:
        if id_inquilino not in df.index:
            return "Al menos uno de los inquilinos no encontrado"

    # -----------------------------
    # ENCODING (AQUÍ NO EN STARTUP)
    # -----------------------------
    df_encoded = encoder.fit_transform(df)

    # -----------------------------
    # MATRIZ SIMILITUD (AQUÍ TAMBIÉN)
    # -----------------------------
    matriz_s = np.dot(df_encoded, df_encoded.T)

    df_similaridad = pd.DataFrame(
        matriz_s,
        index=df.index,
        columns=df.index
    )

    # -----------------------------
    # CÁLCULO DE SIMILITUD
    # -----------------------------
    filas_inquilinos = df_similaridad.loc[id_inquilinos]

    similitud_promedio = filas_inquilinos.mean(axis=0)

    inquilinos_similares = similitud_promedio.sort_values(ascending=False)

    inquilinos_similares = inquilinos_similares.drop(id_inquilinos)

    topn_inquilinos = inquilinos_similares.head(topn)

    registros_similares = df.loc[topn_inquilinos.index]
    registros_buscados = df.loc[id_inquilinos]

    resultado = pd.concat(
        [registros_buscados.T, registros_similares.T],
        axis=1
    )

    similitud_series = pd.Series(
        data=topn_inquilinos.values,
        index=topn_inquilinos.index,
        name="Similitud"
    )

    return resultado, similitud_series