from __future__ import annotations

import argparse
import csv
import os
import sys
from collections import Counter
from pathlib import Path


_DLL_DIRECTORY_HANDLES = []


def configure_rasterio_env() -> None:
    env_prefix = Path(sys.prefix)
    for key, relative in {
        "GDAL_DATA": ("Library", "share", "gdal"),
        "PROJ_LIB": ("Library", "share", "proj"),
    }.items():
        candidate = env_prefix.joinpath(*relative)
        if candidate.exists():
            os.environ.setdefault(key, str(candidate))

    for relative in [("Library", "bin"), ("DLLs",), ()]:
        candidate = env_prefix.joinpath(*relative)
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


def infer_background_values(src, edge_size: int = 512, min_ratio: float = 0.20) -> set[int]:
    import numpy as np

    counts: Counter[int] = Counter()
    total = 0
    for window in edge_windows(src.width, src.height, edge_size=edge_size):
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

    dominant_value, dominant_count = counts.most_common(1)[0]
    background = {int(dominant_value)}

    # Agrega valores muy frecuentes de borde que sean blanco/negro puro de paleta.
    for value, count in counts.most_common(20):
        ratio = count / max(total, 1)
        color = cmap.get(value)
        if ratio < min_ratio:
            continue
        if color:
            r, g, b = color[:3]
            is_near_white = r >= 245 and g >= 245 and b >= 245
            is_near_black = r <= 10 and g <= 10 and b <= 10
            if is_near_white or is_near_black:
                background.add(int(value))

    return background


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


def infer_rgb_background_colors(src, edge_size: int = 512, min_ratio: float = 0.20) -> set[tuple[int, int, int]]:
    import numpy as np

    counts: Counter[tuple[int, int, int]] = Counter()
    total = 0
    for window in edge_windows(src.width, src.height, edge_size=edge_size):
        data = src.read([1, 2, 3], window=window)
        rgb = np.moveaxis(data, 0, 2).reshape(-1, 3)
        colors, color_counts = np.unique(rgb, axis=0, return_counts=True)
        for color, count in zip(colors, color_counts):
            counts.update({tuple(int(v) for v in color): int(count)})
        total += int(rgb.shape[0])

    if not counts:
        raise ValueError("No se pudieron leer bordes RGB para inferir fondo.")

    background = {counts.most_common(1)[0][0]}
    for color, count in counts.most_common(20):
        ratio = count / max(total, 1)
        r, g, b = color
        is_near_white = r >= 245 and g >= 245 and b >= 245
        is_near_black = r <= 10 and g <= 10 and b <= 10
        if ratio >= min_ratio and (is_near_white or is_near_black):
            background.add(color)
    return background


def find_valid_bbox_rgb(src, background_colors: set[tuple[int, int, int]]) -> tuple[int, int, int, int] | None:
    import numpy as np

    col_min = row_min = None
    col_max = row_max = None
    colors = list(background_colors)

    for _, window in src.block_windows(1):
        rgb = src.read([1, 2, 3], window=window)
        background_mask = np.zeros((rgb.shape[1], rgb.shape[2]), dtype=bool)
        for r, g, b in colors:
            background_mask |= (rgb[0] == r) & (rgb[1] == g) & (rgb[2] == b)
        valid = ~background_mask
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

    cmap = src.colormap(1)
    lookup = np.zeros((256, 3), dtype="uint8")
    for value, color in cmap.items():
        if 0 <= int(value) <= 255:
            lookup[int(value), :] = color[:3]
    return lookup


def normalize_streaming(
    source_path: Path,
    output_path: Path,
    background_values: set[int] | None = None,
    edge_size: int = 512,
    tile_size: int = 512,
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
        "error": "",
    }

    try:
        if not source_path.exists():
            raise FileNotFoundError(f"No existe origen: {source_path}")

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
                bbox = find_valid_bbox(src, background_values)
            else:
                background_colors = infer_rgb_background_colors(src, edge_size=edge_size)
                row["background_values"] = "|".join(",".join(str(v) for v in color) for color in sorted(background_colors))
                bbox = find_valid_bbox_rgb(src, background_colors)
            if bbox is None:
                raise ValueError("No se encontraron pixeles validos despues de remover fondo.")
            col_min, row_min, col_max, row_max = bbox
            row["bbox"] = f"{col_min},{row_min},{col_max},{row_max}"

            out_width = col_max - col_min + 1
            out_height = row_max - row_min + 1
            row["output_width"] = str(out_width)
            row["output_height"] = str(out_height)

            output_path.parent.mkdir(parents=True, exist_ok=True)
            temp_output = output_path.with_name(f"{output_path.stem}.tmp{output_path.suffix}")
            if temp_output.exists():
                temp_output.unlink()

            src_window = Window(col_min, row_min, out_width, out_height)
            profile = src.profile.copy()
            profile.update(
                driver="GTiff",
                width=out_width,
                height=out_height,
                count=3,
                dtype="uint8",
                transform=window_transform(src_window, src.transform),
                tiled=True,
                blockxsize=tile_size,
                blockysize=tile_size,
                compress="deflate",
                zlevel=6,
                predictor=2,
                photometric="RGB",
                nodata=0,
                BIGTIFF="IF_SAFER",
            )
            for key in ["colormap", "photometric"]:
                profile.pop(key, None)

            lookup = rgb_lookup_from_colormap(src) if src.count == 1 else None
            background = np.array(sorted(background_values), dtype=src.dtypes[0]) if src.count == 1 else None

            with rasterio.open(temp_output, "w", **profile) as dst:
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
                            background_mask = np.zeros((read_height, read_width), dtype=bool)
                            for r, g, b in background_colors or set():
                                background_mask |= (rgb[0] == r) & (rgb[1] == g) & (rgb[2] == b)
                            if src.count >= 4:
                                source_alpha = src.read(4, window=read_window) > 0
                                valid_mask = (~background_mask) & source_alpha
                            else:
                                valid_mask = ~background_mask
                            alpha = valid_mask.astype("uint8") * 255

                        rgb[:, alpha == 0] = 0
                        dst.write(rgb, indexes=[1, 2, 3], window=write_window)
                        dst.write_mask(alpha, window=write_window)

                dst.colorinterp = (
                    rasterio.enums.ColorInterp.red,
                    rasterio.enums.ColorInterp.green,
                    rasterio.enums.ColorInterp.blue,
                )

            temp_output.replace(output_path)
            row["status"] = "ok"
    except Exception as exc:
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
        description="Normaliza TIFF RGB por streaming: paleta a RGB, fondo transparente, compresion DEFLATE y sin perdida de resolucion."
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
    return parser.parse_args()


def recursive_tifs(input_dir: Path, output_folder_name: str) -> list[Path]:
    output_key = output_folder_name.lower()
    paths = []
    for path in input_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".tif", ".tiff"}:
            continue
        if any(part.lower() == output_key for part in path.parts):
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
        proj_dll = env_prefix / "Library" / "bin" / "proj_9.dll"
        message = [
            "No se pudo importar rasterio en el ambiente configurado.",
            f"Python: {sys.executable}",
            f"Prefix: {sys.prefix}",
            f"gdal.dll existe: {gdal_dll.exists()} ({gdal_dll})",
            f"proj_9.dll existe: {proj_dll.exists()} ({proj_dll})",
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

    print(f"Fuentes: {len(jobs)}")
    print(f"Salida: {'directorio unico ' + str(args.output_dir) if args.output_dir else 'subfolder ' + args.output_folder_name + ' junto al origen'}")
    for source, output in jobs:
        print(f"Normalizando streaming: {source} -> {output}", flush=True)
        rows.append(
            normalize_streaming(
                source_path=source,
                output_path=output,
                background_values=background_values,
                edge_size=args.edge_size,
                tile_size=args.tile_size,
            )
        )

    report = report_dir / "normalizacion_streaming_resultados.csv"
    write_csv(report, rows)
    errors = [row for row in rows if row["status"] == "error"]
    print(f"CSV: {report}")
    print(f"Errores: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
