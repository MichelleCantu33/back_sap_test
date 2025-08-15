# utils_logs.py
from datetime import datetime

def key_linea(l):
    """Genera clave única para identificar una línea."""
    return f"{l.get('CodigoItem','')}|{l.get('LoteItem','')}|{l.get('TipoItem','')}"

def rows_to_line_objs(rows):
    """
    Convierte filas SQL a lista de dicts de líneas.
    rows: ("U_LS_ITEM","U_LS_ITEM_NAME","U_LS_CANT","U_LS_TIPO","U_LS_LOTE")
    """
    lineas = []
    for r in rows:
        lineas.append({
            "CodigoItem": r[0],
            "Descripcion": r[1],
            "CantidadItem": r[2],
            "TipoItem":    r[3],
            "LoteItem":    r[4]
        })
    return lineas

def diff_lineas(antes, despues):
    """
    Compara dos listas de líneas y devuelve:
    (agregadas, eliminadas, actualizadas)
    """
    mapa_antes = { key_linea(l): l for l in antes }
    mapa_despues = { key_linea(l): l for l in despues }

    agregadas = []
    eliminadas = []
    actualizadas = []

    # Agregadas o Actualizadas
    for k, lnew in mapa_despues.items():
        if k not in mapa_antes:
            agregadas.append(lnew)
        else:
            lold = mapa_antes[k]
            if (str(lold.get("CantidadItem")) != str(lnew.get("CantidadItem"))
                or str(lold.get("Descripcion","")) != str(lnew.get("Descripcion",""))
                or str(lold.get("TipoItem","")) != str(lnew.get("TipoItem",""))):
                actualizadas.append({"antes": lold, "despues": lnew})

    # Eliminadas
    for k, lold in mapa_antes.items():
        if k not in mapa_despues:
            eliminadas.append(lold)

    return agregadas, eliminadas, actualizadas
