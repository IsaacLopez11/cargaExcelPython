import pandas as pd


def procesar_ventas(df):

    resultados = {}

    if df.empty:
        resultados["error"] = "El archivo está vacío."
        return resultados

    # Normalizar columnas
    df.columns = df.columns.str.strip().str.lower()

    columnas_necesarias = [
        "fecha",
        "producto",
        "categoria",
        "precio unitario",
        "cantidad",
        "vendedor"
    ]

    for col in columnas_necesarias:
        if col not in df.columns:
            resultados["error"] = f"Falta la columna: {col}"
            return resultados

    # Convertir tipos
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["precio unitario"] = pd.to_numeric(df["precio unitario"], errors="coerce")
    df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")

    df = df.dropna()

    # Crear columna total
    df["total"] = df["precio unitario"] * df["cantidad"]

    # =============================
    # 📊 CÁLCULOS
    # =============================

    # Ventas por mes
    df["mes"] = df["fecha"].dt.to_period("M").astype(str)
    ventas_mes = df.groupby("mes")["total"].sum().to_dict()

    # Ventas por categoría
    ventas_categoria = df.groupby("categoria")["total"].sum().to_dict()

    # Vendedor Top 1
    ventas_vendedor = df.groupby("vendedor")["total"].sum()
    top_vendedor = ventas_vendedor.idxmax()

    resultados["ventas_mes"] = ventas_mes
    resultados["ventas_categoria"] = ventas_categoria
    resultados["top_vendedor"] = top_vendedor

    return resultados, df.to_dict(orient="records")