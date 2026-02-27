import pandas as pd
from datetime import datetime


def calcular(df):
    resultados = {}

    if df.empty:
        resultados["error"] = "El archivo está vacío."
        return resultados

    df.columns = df.columns.str.strip().str.lower()

    columnas_necesarias = ["sueldo", "fechanac", "nombre"]

    for col in columnas_necesarias:
        if col not in df.columns:
            resultados["error"] = f"Falta la columna obligatoria: {col}"
            return resultados

    df["sueldo"] = pd.to_numeric(df["sueldo"], errors="coerce")
    df["fechanac"] = pd.to_datetime(df["fechanac"], errors="coerce")

    df = df.dropna(subset=["sueldo", "fechanac"])

    if df.empty:
        resultados["error"] = "No hay datos válidos para calcular."
        return resultados

    resultados["sueldo_max"] = float(df["sueldo"].max())

    persona_joven = df.loc[df["fechanac"].idxmax()]
    resultados["persona_mas_joven"] = persona_joven["nombre"]

    hoy = datetime.today()
    edades = (hoy - df["fechanac"]).dt.days / 365
    resultados["edad_promedio"] = round(edades.mean(), 1)
  
    return resultados