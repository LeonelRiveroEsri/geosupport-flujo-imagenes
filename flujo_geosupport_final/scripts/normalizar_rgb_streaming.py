from __future__ import annotations

import argparse
import csv
import os
import shutil
import sys
import tempfile
from collections import Counter
from pathlib import Path


_DLL_DIRECTORY_HANDLES = []


def configure_rasterio_env() -> None:
    env_prefix = Path(sys.prefix)
    dll_candidates = [
        env_prefix / "Library" / "bin",
        env_prefix / "Scripts",
        env_prefix / "DLLs",
        env_prefix,
    ]

    # El notebook se ejecuta desde ArcGIS Pro y el subproceso puede heredar DLLs
    # de ArcGIS en PATH. Rasterio debe resolver primero las DLL de su ambiente.
    current_path = os.environ.get("PATH", "")
    path_parts = [str(path) for path in dll_candidates if path.exists()]
    os.environ["PATH"] = os.pathsep.join(path_parts + [current_path])

    for key, relative in {
        "GDAL_DATA": ("Library", "share", "gdal"),
        "PROJ_LIB": ("Library", "share", "proj"),
    }.items():
        candidate = env_prefix.joinpath(*relative)
        if candidate.exists():
            os.environ[key] = str(candidate)

    for candidate in dll_candidates:
        if candidate.exists() and hasattr(os, "add_dll_directory"):
            _DLL_DIRECTORY_HANDLES.append(os.add_dll_directory(str(candidate)))

    os.environ.setdefault("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")


configure_rasterio_env()


# INPUT_IMAGES: list[dict[str, str]] = [
#     {
#         "path": r"C:\amssclgis10.ams.gmams.cl\CL_MLP_PAO\Vuelos_Drone_Sin_Procesar\INPUT\20260206_Geosupport_segunda_entrega_Pendientes\SOLO_TIF_02Jun26\GEOSP-TRN-002740_GS_Ortofoto EM2_270526.tif",
#         "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_27_DME9-PA12-IIFF8.tif",
#     },
#     {
#         "path": r"C:\amssclgis10.ams.gmams.cl\CL_MLP_PAO\Vuelos_Drone_Sin_Procesar\INPUT\20260206_Geosupport_segunda_entrega_Pendientes\SOLO_TIF_02Jun26\GEOSP-TRN-002745_GS_ORTOFOTO_Tramo2 Linea 33kv E-48 - E-84_270526.tif",
#         "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_27_TORRES_E48_A_E84_PV4.tif",
#     },
#     {
#         "path": r"C:\amssclgis10.ams.gmams.cl\CL_MLP_PAO\Vuelos_Drone_Sin_Procesar\INPUT\20260206_Geosupport_segunda_entrega_Pendientes\SOLO_TIF_02Jun26\GEOSP-TRN-002761_GS_ORTOFOTO_Subestación El Mauro_290526.tif",
#         "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_29_Subestacion-El-Mauro-1.tif",
#     },
#     {
#         "path": r"C:\amssclgis10.ams.gmams.cl\CL_MLP_PAO\Vuelos_Drone_Sin_Procesar\INPUT\20260206_Geosupport_segunda_entrega_Pendientes\SOLO_TIF_02Jun26\GEOSP-TRN-002764_GS_ORTOFOTO_EB3_290526.tif",
#         "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_29_Subestacion-El-Mauro-2.tif",
#     },
#     {
#         "path": r"C:\amssclgis10.ams.gmams.cl\CL_MLP_PAO\Vuelos_Drone_Sin_Procesar\INPUT\20260206_Geosupport_segunda_entrega_Pendientes\SOLO_TIF_02Jun26\GEOSP-TRN-002781_GS_ORTOFOTO_EDT_310526.tif",
#         "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_31_EDT.tif",
#     },
#     {
#         "path": r"C:\amssclgis10.ams.gmams.cl\CL_MLP_PAO\Vuelos_Drone_Sin_Procesar\INPUT\20260206_Geosupport_segunda_entrega_Pendientes\SOLO_TIF_02Jun26\GEOSP-TRN-002786_GS_ORTOFOTO_Tramo 1 Línea 33 kV E-125 – ML EB2_300526.tif",
#         "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_30_MonteAranda-NSTC-Km-84p2-a-82p3.tif",
#     },
#     {
#         "path": r"C:\amssclgis10.ams.gmams.cl\CL_MLP_PAO\Vuelos_Drone_Sin_Procesar\INPUT\20260206_Geosupport_segunda_entrega_Pendientes\SOLO_TIF_02Jun26\GEOSP-TRN-002791_GS_ORTOFOTO_Tramo 2 Línea 33 kV E-085 – E-125_280526.tif",
#         "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_28_TORRE_E85_A_E_125.tif",
#     },
# ]
# INPUT_IMAGES: list[dict[str, str]] = [
#     {
#         "path": r"\\amssclgis10.ams.gmams.cl\CL_MLP_PAO\Vuelos_Drone_Sin_Procesar\INPUT\Pendientes\CL_MLP_PAO_IF_Ortho_26_05_17_EV2.tif",
#         "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_17_EV2.tif",
#     }
# ]
# INPUT_IMAGES: list[dict[str, str]] = [
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_10_ED1",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_10_ED1"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_13_NSTC-Km-50p3-a-51",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_13_NSTC-Km-50p3-a-51"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_15_SRA-2-km-56p1-a-57p7-Area-2",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_15_SRA-2-km-56p1-a-57p7-Area-2"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_20_DME7_PA7_IF6",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_20_DME7_PA7_IF6"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_20_NSTC_Km_21_a_22_DME5",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_20_NSTC_Km_21_a_22_DME5"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_22_NSTC_km_4p4_a_7p0",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_22_NSTC_km_4p4_a_7p0"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_22_Subestacion-El-Mauro_A_E35-1",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_22_Subestacion-El-Mauro_A_E35-1"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_22_Subestacion-El-Mauro_A_E35-2",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_22_Subestacion-El-Mauro_A_E35-2"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_23_EDT",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_23_EDT"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_23_EM1",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_23_EM1"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_23_MonteAranda-NSTC-Km-84p2-a-82p3",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_23_MonteAranda-NSTC-Km-84p2-a-82p3"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_24_TORRES_E31_A_E48_PV4",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_24_TORRES_E31_A_E48_PV4"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_27_DME9-PA12-IIFF8",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_27_DME9-PA12-IIFF8"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_27_TORRES_E48_A_E84_PV4",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_27_TORRES_E48_A_E84_PV4"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_28_TORRES_E31_A_E48_PV4",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_28_TORRES_E31_A_E48_PV4"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_28_TORRE_E85_A_E_125",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_28_TORRE_E85_A_E_125"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_29_Patio-19B-y-Armado",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_29_Patio-19B-y-Armado"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_29_Subestacion-El-Mauro-1",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_29_Subestacion-El-Mauro-1"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_29_Subestacion-El-Mauro-2",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_29_Subestacion-El-Mauro-2"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_30_MonteAranda-NSTC-Km-84p2-a-82p3",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_30_MonteAranda-NSTC-Km-84p2-a-82p3"
#   },
#   {
#     "path": "\\\\amssclgis10.ams.gmams.cl\\CL_MLP_PAO\\Vuelos_Drone_Sin_Procesar\\INPUT\\PendientesSegundaEntrega\\FROM_NORMALICE\\CL_MLP_PAO_IF_Ortho_26_05_31_EDT",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_31_EDT"
#   }
# ]
# INPUT_IMAGES: list[dict[str, str]] = [
#   {
#     "path": r"C:\Users\esrlrivero_adm\Documents\Geosupport\amsa-pao-geosupport\imagenes\CL_MLP_PAO_IF_Ortho_26_05_10_DME9-PA12-IIFF8_normalizada.tif",
#     "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_10_DME9-PA12-IIFF8_normalizada.tif"
#   }
  
# ]

# INPUT_IMAGES: list[dict[str, str]] = [
#     {
#         "path": "c:\\Users\\esrlrivero_adm\\Documents\\Geosupport\\amsa-pao-geosupport\\flujo_geosupport_etapas\\26-07-07-Ajuste\\CL_MLP_PAO_IF_Ortho_26_05_27_TORRES_E48_A_E84_PV4_normalizada.tif",
#         "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_27_TORRES_E48_A_E84_PV4_normalizada.tif"
#     },
#     {
#         "path": "c:\\Users\\esrlrivero_adm\\Documents\\Geosupport\\amsa-pao-geosupport\\flujo_geosupport_etapas\\26-07-07-Ajuste\\CL_MLP_PAO_IF_Ortho_26_05_28_TORRE_E85_A_E_125_normalizada.tif",
#         "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_28_TORRE_E85_A_E_125_normalizada.tif"
#     },
#     {
#         "path": "c:\\Users\\esrlrivero_adm\\Documents\\Geosupport\\amsa-pao-geosupport\\flujo_geosupport_etapas\\26-07-07-Ajuste\\CL_MLP_PAO_IF_Ortho_26_05_30_MonteAranda-NSTC-Km-84p2-a-82p3_normalizada.tif",
#         "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_30_MonteAranda-NSTC-Km-84p2-a-82p3_normalizada.tif"
#     }
# ]
INPUT_IMAGES: list[dict[str, str]] = [
    {
        "path": r"C:\Users\esrlrivero_adm\Documents\Geosupport\amsa-pao-geosupport\imagenes\2026-07-09\CL_MLP_PAO_IF_Ortho_26_05_13_NSTC-Km-50p3-a-51.tif",
        "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_13_NSTC-Km-50p3-a-51.tif"
    },
    {
        "path": r"C:\Users\esrlrivero_adm\Documents\Geosupport\amsa-pao-geosupport\imagenes\2026-07-09\CL_MLP_PAO_IF_Ortho_26_05_20_NSTC_Km_21_a_22_DME5.tif",
        "destination_path": "CL_MLP_PAO_IF_Ortho_26_05_20_NSTC_Km_21_a_22_DME5.tif"
    }
]

def edge_windows(width: int, height: int, edge_size: int = 512):
    edge_size = max(1, min(edge_size, width, height))
    return [
        ((0, edge_size), (0, width)),
        ((height - edge_size, height), (0, width)),
        ((0, height), (0, edge_size)),
        ((0, height), (width - edge_size, width)),
    ]


def sampled_edge_windows(width: int, height: int, edge_size: int = 512):
    edge_size = max(1, min(edge_size, width, height))
    col_positions = sorted({0, max(0, (width - edge_size) // 2), max(0, width - edge_size)})
    row_positions = sorted({0, max(0, (height - edge_size) // 2), max(0, height - edge_size)})
    windows = []
    for col in col_positions:
        windows.append(((0, edge_size), (col, col + edge_size)))
        windows.append(((height - edge_size, height), (col, col + edge_size)))
    for row in row_positions:
        windows.append(((row, row + edge_size), (0, edge_size)))
        windows.append(((row, row + edge_size), (width - edge_size, width)))
    return windows


def infer_background_values(src, edge_size: int = 512, min_ratio: float = 0.20) -> set[int]:
    import numpy as np

    counts: Counter[int] = Counter()
    total = 0
    for window in sampled_edge_windows(src.width, src.height, edge_size=edge_size):
        data = src.read(1, window=window)
        values, value_counts = np.unique(data, return_counts=True)
        counts.update({int(value): int(count) for value, count in zip(values, value_counts)})
        total += int(data.size)

    if not counts:
        raise ValueError("No se pudieron leer bordes para inferir fondo.")

    cmap = {}
    try:
        cmap = src.colormap(1)
    except Exception:
        cmap = {}

    background = set()
    for value, count in counts.most_common(20):
        ratio = count / max(total, 1)
        if ratio < min_ratio:
            continue
        color = cmap.get(value)
        if color:
            r, g, b = color[:3]
        else:
            r = g = b = int(value)

        is_near_white = r >= 245 and g >= 245 and b >= 245
        is_near_black = r <= 10 and g <= 10 and b <= 10
        if is_near_white or is_near_black:
            background.add(int(value))

    return background


def read_rgb_edge_sample(src, window):
    import numpy as np

    data = src.read([1, 2, 3], window=window)
    return np.moveaxis(data, 0, 2).reshape(-1, 3)


def background_mask_rgb(rgb, background_colors: set[tuple[int, int, int]]):
    import numpy as np

    if not background_colors:
        return np.zeros((rgb.shape[1], rgb.shape[2]), dtype=bool)

    background_mask = np.zeros((rgb.shape[1], rgb.shape[2]), dtype=bool)
    for r, g, b in background_colors:
        is_white = r >= 245 and g >= 245 and b >= 245
        is_black = r <= 10 and g <= 10 and b <= 10
        if is_white:
            background_mask |= (rgb[0] >= 245) & (rgb[1] >= 245) & (rgb[2] >= 245)
        elif is_black:
            background_mask |= (rgb[0] <= 10) & (rgb[1] <= 10) & (rgb[2] <= 10)
        else:
            background_mask |= (rgb[0] == r) & (rgb[1] == g) & (rgb[2] == b)
    return background_mask


def infer_rgb_background_colors(src, edge_size: int = 512, min_ratio: float = 0.20) -> set[tuple[int, int, int]]:
    import numpy as np

    counts: Counter[tuple[int, int, int]] = Counter()
    total = 0
    for window in sampled_edge_windows(src.width, src.height, edge_size=edge_size):
        rgb = read_rgb_edge_sample(src, window)
        colors, color_counts = np.unique(rgb, axis=0, return_counts=True)
        for color, count in zip(colors, color_counts):
            counts.update({tuple(int(v) for v in color): int(count)})
        total += int(rgb.shape[0])

    if not counts:
        raise ValueError("No se pudieron leer bordes RGB para inferir fondo.")

    background = set()
    for color, count in counts.most_common(50):
        ratio = count / max(total, 1)
        r, g, b = color
        is_near_white = r >= 245 and g >= 245 and b >= 245
        is_near_black = r <= 10 and g <= 10 and b <= 10
        if ratio >= min_ratio and (is_near_white or is_near_black):
            background.add(color)
    return background


def find_valid_bbox_rgb(src, background_colors: set[tuple[int, int, int]]) -> tuple[int, int, int, int] | None:
    import numpy as np

    if not background_colors:
        return 0, 0, src.width - 1, src.height - 1

    col_min = row_min = None
    col_max = row_max = None

    for _, window in src.block_windows(1):
        rgb = src.read([1, 2, 3], window=window)
        valid = ~background_mask_rgb(rgb, background_colors)
        if not valid.any():
            continue
        rows, cols = np.where(valid)
        w_col_min = int(window.col_off + cols.min())
        w_col_max = int(window.col_off + cols.max())
        w_row_min = int(window.row_off + rows.min())
        w_row_max = int(window.row_off + rows.max())
        col_min = w_col_min if col_min is None else min(col_min, w_col_min)
        col_max = w_col_max if col_max is None else max(col_max, w_col_max)
        row_min = w_row_min if row_min is None else min(row_min, w_row_min)
        row_max = w_row_max if row_max is None else max(row_max, w_row_max)

    if col_min is None:
        return None
    return int(col_min), int(row_min), int(col_max), int(row_max)


def find_valid_bbox(src, background_values: set[int]) -> tuple[int, int, int, int] | None:
    import numpy as np

    col_min = row_min = None
    col_max = row_max = None
    background = np.array(sorted(background_values), dtype=src.dtypes[0])

    for _, window in src.block_windows(1):
        data = src.read(1, window=window)
        valid = ~np.isin(data, background)
        if not valid.any():
            continue
        rows, cols = np.where(valid)
        w_col_min = int(window.col_off + cols.min())
        w_col_max = int(window.col_off + cols.max())
        w_row_min = int(window.row_off + rows.min())
        w_row_max = int(window.row_off + rows.max())
        col_min = w_col_min if col_min is None else min(col_min, w_col_min)
        col_max = w_col_max if col_max is None else max(col_max, w_col_max)
        row_min = w_row_min if row_min is None else min(row_min, w_row_min)
        row_max = w_row_max if row_max is None else max(row_max, w_row_max)

    if col_min is None:
        return None
    return int(col_min), int(row_min), int(col_max), int(row_max)


def rgb_lookup_from_colormap(src):
    import numpy as np

    if src.count >= 3:
        return None

    try:
        cmap = src.colormap(1)
    except Exception:
        cmap = {}
    lookup = np.zeros((256, 3), dtype="uint8")
    if cmap:
        for value, color in cmap.items():
            if 0 <= int(value) <= 255:
                lookup[int(value), :] = color[:3]
    else:
        lookup[:, 0] = np.arange(256, dtype="uint8")
        lookup[:, 1] = np.arange(256, dtype="uint8")
        lookup[:, 2] = np.arange(256, dtype="uint8")
    return lookup


def raster_artifacts(path: Path) -> list[Path]:
    return [
        path,
        path.with_name(f"{path.name}.msk"),
        path.with_name(f"{path.name}.aux.xml"),
        path.with_name(f"{path.name}.ovr"),
        path.with_name(f"{path.name}.xml"),
    ]


def raster_artifacts_size(path: Path) -> int:
    return sum(artifact.stat().st_size for artifact in raster_artifacts(path) if artifact.exists())


def cleanup_raster_artifacts(path: Path) -> None:
    for artifact in raster_artifacts(path):
        if artifact.exists():
            artifact.unlink()


def normalize_streaming(
    source_path: Path,
    output_path: Path,
    background_values: set[int] | None = None,
    edge_size: int = 512,
    tile_size: int = 512,
    compression: str = "jpeg",
    jpeg_quality: int = 85,
    deflate_level: int = 6,
    enforce_max_source_size: bool = True,
    min_jpeg_quality: int = 60,
    masked_fill_value: int = 255,
    build_overviews: bool = False,
    write_internal_mask: bool = True,
    output_layout: str = "tiled",
    write_nodata: bool = False,
    skip_bbox_scan: bool = False,
) -> dict[str, str]:
    import numpy as np
    import rasterio
    from rasterio.windows import Window, transform as window_transform

    row = {
        "source_path": str(source_path),
        "output_path": str(output_path),
        "status": "",
        "source_bands": "",
        "source_width": "",
        "source_height": "",
        "background_values": "",
        "bbox": "",
        "output_width": "",
        "output_height": "",
        "compression": compression,
        "source_bytes": "",
        "output_bytes": "",
        "jpeg_quality_used": "",
        "size_status": "",
        "masked_fill_value": str(masked_fill_value),
        "overviews": "true" if build_overviews else "false",
        "mask_mode": "internal" if write_internal_mask else "none",
        "output_layout": output_layout,
        "nodata_mode": "value" if write_nodata else "none",
        "bbox_mode": "full_extent" if skip_bbox_scan else "scan",
        "error": "",
    }

    try:
        if not source_path.exists():
            raise FileNotFoundError(f"No existe origen: {source_path}")

        source_bytes = source_path.stat().st_size
        row["source_bytes"] = str(source_bytes)

        with rasterio.open(source_path, sharing=False) as src:
            row["source_bands"] = str(src.count)
            row["source_width"] = str(src.width)
            row["source_height"] = str(src.height)

            if src.count not in (1, 3, 4) and src.count < 3:
                raise ValueError(f"Cantidad de bandas no soportada: {src.count}")

            background_colors = None
            if src.count == 1:
                if background_values is None:
                    background_values = infer_background_values(src, edge_size=edge_size)
                row["background_values"] = "|".join(str(v) for v in sorted(background_values))
                bbox = (0, 0, src.width - 1, src.height - 1) if skip_bbox_scan else find_valid_bbox(src, background_values)
            else:
                background_colors = infer_rgb_background_colors(src, edge_size=edge_size)
                row["background_values"] = "|".join(",".join(str(v) for v in color) for color in sorted(background_colors))
                bbox = (0, 0, src.width - 1, src.height - 1) if skip_bbox_scan else find_valid_bbox_rgb(src, background_colors)
            if bbox is None:
                raise ValueError("No se encontraron pixeles validos despues de remover fondo.")
            col_min, row_min, col_max, row_max = bbox
            row["bbox"] = f"{col_min},{row_min},{col_max},{row_max}"

            out_width = col_max - col_min + 1
            out_height = row_max - row_min + 1
            row["output_width"] = str(out_width)
            row["output_height"] = str(out_height)

            output_path.parent.mkdir(parents=True, exist_ok=True)
            temp_dir = Path(tempfile.mkdtemp(prefix=f"{output_path.stem}_", dir=output_path.parent))
            temp_output = temp_dir / f"{output_path.stem}.tmp{output_path.suffix}"
            if temp_output.exists():
                temp_output.unlink()

            src_window = Window(col_min, row_min, out_width, out_height)
            profile = src.profile.copy()
            for key in [
                "colormap",
                "photometric",
                "nodata",
                "compress",
                "compression",
                "predictor",
                "zlevel",
                "jpeg_quality",
                "interleave",
                "tiled",
                "blockxsize",
                "blockysize",
            ]:
                profile.pop(key, None)

            compression = compression.lower().strip()
            if compression not in {"jpeg", "deflate"}:
                raise ValueError(f"Compresion no soportada: {compression}. Use jpeg o deflate.")

            output_layout = output_layout.lower().strip()
            if output_layout not in {"tiled", "stripped"}:
                raise ValueError(f"Layout no soportado: {output_layout}. Use tiled o stripped.")

            profile.update(
                driver="GTiff",
                width=out_width,
                height=out_height,
                count=3,
                dtype="uint8",
                transform=window_transform(src_window, src.transform),
                BIGTIFF="IF_SAFER",
            )
            if write_nodata:
                profile.update(nodata=int(masked_fill_value))
            effective_output_layout = output_layout
            # JPEG en tiras falla con rasters extremadamente anchos porque cada tira
            # conserva el ancho completo. El alto no tiene el mismo problema porque
            # se divide en multiples tiras. En esos casos se cambia a tiles manteniendo
            # NoData y sin mascara interna para conservar compatibilidad de consumo.
            if compression == "jpeg" and output_layout == "stripped" and out_width > 65000:
                effective_output_layout = "tiled"
            row["output_layout"] = effective_output_layout

            if effective_output_layout == "tiled":
                profile.update(
                    tiled=True,
                    blockxsize=tile_size,
                    blockysize=tile_size,
                )
            else:
                strip_rows = min(32, out_height)
                profile.update(
                    tiled=False,
                    blockysize=max(1, strip_rows),
                )

            lookup = rgb_lookup_from_colormap(src) if src.count == 1 else None
            background = np.array(sorted(background_values), dtype=src.dtypes[0]) if src.count == 1 else None

            def write_candidate(candidate_profile: dict, candidate_quality: int | None) -> None:
                cleanup_raster_artifacts(temp_output)
                mask_env = "YES" if write_internal_mask else "NO"
                with rasterio.Env(GDAL_TIFF_INTERNAL_MASK=mask_env):
                    with rasterio.open(temp_output, "w", **candidate_profile) as dst:
                        for out_row in range(0, out_height, tile_size):
                            read_height = min(tile_size, out_height - out_row)
                            for out_col in range(0, out_width, tile_size):
                                read_width = min(tile_size, out_width - out_col)
                                read_window = Window(col_min + out_col, row_min + out_row, read_width, read_height)
                                write_window = Window(out_col, out_row, read_width, read_height)

                                if src.count == 1:
                                    data = src.read(1, window=read_window)
                                    rgb = np.moveaxis(lookup[data], 2, 0)
                                    alpha = (~np.isin(data, background)).astype("uint8") * 255
                                else:
                                    rgb = src.read([1, 2, 3], window=read_window)
                                    background_mask = background_mask_rgb(rgb, background_colors or set())
                                    if src.count >= 4:
                                        source_alpha = src.read(4, window=read_window) > 0
                                        valid_mask = (~background_mask) & source_alpha
                                    else:
                                        valid_mask = ~background_mask
                                    alpha = valid_mask.astype("uint8") * 255

                                rgb[:, alpha == 0] = int(masked_fill_value)
                                dst.write(rgb, indexes=[1, 2, 3], window=write_window)
                                if write_internal_mask:
                                    dst.write_mask(alpha, window=write_window)

                        dst.colorinterp = (
                            rasterio.enums.ColorInterp.red,
                            rasterio.enums.ColorInterp.green,
                            rasterio.enums.ColorInterp.blue,
                        )

                if build_overviews:
                    from rasterio.enums import Resampling

                    with rasterio.Env(GDAL_TIFF_INTERNAL_MASK="YES"):
                        with rasterio.open(temp_output, "r+") as overview_dst:
                            factors = [2, 4, 8, 16, 32]
                            factors = [factor for factor in factors if overview_dst.width // factor >= 256 and overview_dst.height // factor >= 256]
                            if factors:
                                overview_dst.build_overviews(factors, Resampling.average)
                                overview_dst.update_tags(ns="rio_overview", resampling="average")

            candidate_qualities = [int(jpeg_quality)]
            for quality in [80, 75, 70, 65, int(min_jpeg_quality)]:
                if int(min_jpeg_quality) <= quality <= int(jpeg_quality) and quality not in candidate_qualities:
                    candidate_qualities.append(quality)

            best_candidate = None
            best_size = None
            best_quality = None
            attempts = candidate_qualities if compression == "jpeg" else [None]

            for quality in attempts:
                candidate_profile = profile.copy()
                if compression == "jpeg":
                    candidate_profile.update(
                        compress="jpeg",
                        photometric="YCbCr",
                        interleave="pixel",
                        jpeg_quality=int(quality),
                        JPEGTABLESMODE=3,
                    )
                else:
                    candidate_profile.update(
                        compress="deflate",
                        zlevel=int(deflate_level),
                        predictor=2,
                        photometric="RGB",
                    )

                write_candidate(candidate_profile, quality)
                candidate_size = raster_artifacts_size(temp_output)
                if best_size is None or candidate_size < best_size:
                    best_candidate = temp_output.with_name(f"{temp_output.stem}.best{temp_output.suffix}")
                    cleanup_raster_artifacts(best_candidate)
                    temp_output.replace(best_candidate)
                    temp_mask = temp_output.with_name(f"{temp_output.name}.msk")
                    best_mask = best_candidate.with_name(f"{best_candidate.name}.msk")
                    if temp_mask.exists():
                        temp_mask.replace(best_mask)
                    best_size = candidate_size
                    best_quality = quality
                else:
                    cleanup_raster_artifacts(temp_output)

                if not enforce_max_source_size or candidate_size <= source_bytes:
                    break

            cleanup_raster_artifacts(output_path)
            if enforce_max_source_size and best_size is not None and best_size > source_bytes:
                cleanup_raster_artifacts(best_candidate)
                shutil.copy2(source_path, output_path)
                row["status"] = "original_fallback_size_guard"
                row["size_status"] = "kept_original_because_normalized_was_larger"
                row["output_bytes"] = str(output_path.stat().st_size)
            else:
                best_candidate.replace(output_path)
                best_mask = best_candidate.with_name(f"{best_candidate.name}.msk")
                output_mask = output_path.with_name(f"{output_path.name}.msk")
                if best_mask.exists():
                    best_mask.replace(output_mask)
                row["status"] = "ok"
                row["size_status"] = "normalized_lte_source" if best_size <= source_bytes else "normalized_without_size_guard"
                row["output_bytes"] = str(raster_artifacts_size(output_path))
                row["jpeg_quality_used"] = "" if best_quality is None else str(best_quality)

            cleanup_raster_artifacts(temp_output)
            shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception as exc:
        try:
            if "temp_output" in locals():
                cleanup_raster_artifacts(temp_output)
            if "temp_dir" in locals():
                shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass
        row["status"] = "error"
        row["error"] = str(exc)

    return row


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "source_path",
        "output_path",
        "status",
        "source_bands",
        "source_width",
        "source_height",
        "background_values",
        "bbox",
        "output_width",
        "output_height",
        "compression",
        "source_bytes",
        "output_bytes",
        "jpeg_quality_used",
        "size_status",
        "masked_fill_value",
        "overviews",
        "mask_mode",
        "output_layout",
        "nodata_mode",
        "bbox_mode",
        "error",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_background_values(value: str | None) -> set[int] | None:
    if not value:
        return None
    return {int(part.strip()) for part in value.split(",") if part.strip()}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normaliza TIFF RGB por streaming: paleta/colormap a RGB, fondo transparente, compresion optimizada y sin cambiar resolucion."
    )
    parser.add_argument(
        "sources",
        nargs="+",
        type=Path,
        help="Directorio raiz o TIFF origen. Si recibe directorios, busca TIFF/TIFF recursivamente.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directorio unico de salida. Si se omite usa subfolder normalizadas dentro del directorio raiz.",
    )
    parser.add_argument("--output-folder-name", default="normalizadas", help="Subdirectorio junto al origen cuando no se indica --output-dir.")
    parser.add_argument("--background-values", default=None, help="Valores de fondo separados por coma. Ejemplo: 252")
    parser.add_argument("--edge-size", type=int, default=512)
    parser.add_argument("--tile-size", type=int, default=512)
    parser.add_argument(
        "--compression",
        choices=["jpeg", "deflate"],
        default="jpeg",
        help="Compresion de salida. jpeg reduce mucho el peso en ortofotos; deflate conserva compresion sin perdida pero puede aumentar tamano.",
    )
    parser.add_argument("--jpeg-quality", type=int, default=85, help="Calidad JPEG para --compression jpeg.")
    parser.add_argument("--deflate-level", type=int, default=6, help="Nivel DEFLATE para --compression deflate.")
    parser.add_argument(
        "--min-jpeg-quality",
        type=int,
        default=60,
        help="Calidad JPEG minima a probar cuando el archivo normalizado queda mayor al origen.",
    )
    parser.add_argument(
        "--allow-larger-output",
        action="store_true",
        help="Permite que la salida pese mas que el origen. Por defecto se evita.",
    )
    parser.add_argument(
        "--masked-fill-value",
        type=int,
        default=255,
        help="Valor RGB fisico usado fuera de la mascara. 255 evita bordes negros si ArcGIS recalcula piramides.",
    )
    parser.add_argument(
        "--build-overviews",
        action="store_true",
        help="Construye overviews internas con rasterio despues de normalizar.",
    )
    parser.add_argument(
        "--no-internal-mask",
        action="store_true",
        help="No escribe mascara interna. Recomendado para salidas que se usaran para crear TPK en ArcGIS Pro.",
    )
    parser.add_argument(
        "--output-layout",
        choices=["tiled", "stripped"],
        default="tiled",
        help="Organizacion interna del GeoTIFF. stripped se parece mas a los TIFF originales y es mas compatible con TPK.",
    )
    parser.add_argument(
        "--tpk-compatible",
        action="store_true",
        help="Modo de maxima compatibilidad con TPK: sin mascara interna, layout stripped, NoData=valor de fondo y sin overviews internas.",
    )
    parser.add_argument(
        "--no-nodata",
        action="store_true",
        help="No escribe NoData en la salida. Usar solo si el consumidor no soporta NoData en RGB.",
    )
    parser.add_argument(
        "--skip-bbox-scan",
        action="store_true",
        help="Evita el barrido completo para calcular recorte y conserva el extent completo. Mas rapido; el fondo se controla con mascara/NoData.",
    )
    parser.add_argument(
        "--force-crop-scan",
        action="store_true",
        help="Fuerza el barrido completo de pixeles para recortar fisicamente el rectangulo util.",
    )
    return parser.parse_args()


def recursive_tifs(input_dir: Path, output_folder_name: str) -> list[Path]:
    output_key = output_folder_name.lower()
    paths = []
    for path in input_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".tif", ".tiff"}:
            continue
        relative_parts = [part.lower() for part in path.relative_to(input_dir).parts[:-1]]
        if any(part == output_key or part.startswith("normalizadas") for part in relative_parts):
            continue
        if path.name.lower().endswith(".tmp.tif") or ".tmp" in path.name.lower():
            continue
        paths.append(path)
    return sorted(paths, key=lambda value: str(value).lower())


def build_jobs(sources: list[Path], output_dir: Path | None, output_folder_name: str) -> tuple[list[tuple[Path, Path]], Path]:
    jobs = []
    report_dir = output_dir
    for source in sources:
        source = source.resolve()
        if source.is_dir():
            folder_output = output_dir or source / output_folder_name
            report_dir = report_dir or folder_output
            for tif_path in recursive_tifs(source, output_folder_name):
                jobs.append((tif_path, folder_output / tif_path.name))
        elif source.is_file():
            folder_output = output_dir or source.parent / output_folder_name
            report_dir = report_dir or folder_output
            jobs.append((source, folder_output / source.name))
        else:
            folder_output = output_dir or source.parent / output_folder_name
            report_dir = report_dir or folder_output
            jobs.append((source, folder_output / source.name))
    if report_dir is None:
        report_dir = Path.cwd() / output_folder_name
    return jobs, report_dir


def validate_rasterio_runtime() -> None:
    try:
        import rasterio
    except Exception as exc:
        env_prefix = Path(sys.prefix)
        gdal_dll = env_prefix / "Library" / "bin" / "gdal.dll"
        proj_dlls = sorted((env_prefix / "Library" / "bin").glob("proj*.dll"))
        message = [
            "No se pudo importar rasterio en el ambiente configurado.",
            f"Python: {sys.executable}",
            f"Prefix: {sys.prefix}",
            f"gdal.dll existe: {gdal_dll.exists()} ({gdal_dll})",
            "proj dlls: " + (", ".join(path.name for path in proj_dlls) if proj_dlls else "no encontradas"),
            "Causa probable: mezcla o incompatibilidad de DLLs GDAL/PROJ/rasterio en el ambiente conda.",
            "Recrear el ambiente rasterio con versiones fijadas antes de ejecutar la normalizacion.",
            f"Error original: {type(exc).__name__}: {exc}",
        ]
        raise RuntimeError("\n".join(message)) from exc

    print(f"Rasterio OK: {rasterio.__version__}")


def main() -> int:
    args = parse_args()
    validate_rasterio_runtime()
    background_values = parse_background_values(args.background_values)
    jobs, report_dir = build_jobs(args.sources, args.output_dir, args.output_folder_name)
    rows = []
    write_internal_mask = not args.no_internal_mask
    output_layout = args.output_layout
    build_overviews = args.build_overviews
    write_nodata = False
    skip_bbox_scan = args.skip_bbox_scan
    if args.tpk_compatible:
        write_internal_mask = False
        output_layout = "stripped"
        build_overviews = False
        write_nodata = True
        skip_bbox_scan = True
        if args.jpeg_quality == 85:
            args.jpeg_quality = 75
    if args.no_nodata:
        write_nodata = False
    if args.force_crop_scan:
        skip_bbox_scan = False

    print(f"Fuentes: {len(jobs)}")
    print(f"Salida: {'directorio unico ' + str(args.output_dir) if args.output_dir else 'subfolder ' + args.output_folder_name + ' junto al origen'}")
    for source, output in jobs:
        print(f"Normalizando streaming: {source} -> {output}", flush=True)
        row = normalize_streaming(
            source_path=source,
            output_path=output,
            background_values=background_values,
            edge_size=args.edge_size,
            tile_size=args.tile_size,
            compression=args.compression,
            jpeg_quality=args.jpeg_quality,
            deflate_level=args.deflate_level,
            enforce_max_source_size=not args.allow_larger_output,
            min_jpeg_quality=args.min_jpeg_quality,
            masked_fill_value=args.masked_fill_value,
            build_overviews=build_overviews,
            write_internal_mask=write_internal_mask,
            output_layout=output_layout,
            write_nodata=write_nodata,
            skip_bbox_scan=skip_bbox_scan,
        )
        rows.append(row)
        if row.get("status") == "error":
            print(f"ERROR normalizando: {source}", flush=True)
            print(f"  {row.get('error')}", flush=True)
        else:
            print(f"OK normalizado: {output}", flush=True)

    report = report_dir / "normalizacion_streaming_resultados.csv"
    write_csv(report, rows)
    errors = [row for row in rows if row["status"] == "error"]
    print(f"CSV: {report}")
    print(f"Errores: {len(errors)}")
    for row in errors[:20]:
        print(f"- {row.get('source_path')}: {row.get('error')}", flush=True)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
