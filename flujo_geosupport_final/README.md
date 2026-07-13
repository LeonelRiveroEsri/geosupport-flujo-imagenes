# Flujo Geosupport Final

Este directorio compila el flujo validado para cargar entregas de imagenes drone PAO.

Configuracion central:

- `settings.json` contiene las rutas y parametros principales del flujo.
- Antes de ejecutar una nueva entrega, ajustar principalmente `input_folder_tifs`.
- Los notebooks leen este JSON para resolver rutas de entrada, salida normalizada, mosaic dataset, datastore, feature class de footprints, APRX base, grupos del mapa y ambiente rasterio.

Orden definitivo:

1. `notebooks/01_normalizar_rgb_streaming.ipynb`
   - Recibe el directorio raiz de imagenes.
   - Busca `.tif` y `.tiff` de forma recursiva.
   - Ejecuta `scripts/normalizar_rgb_streaming.py` por subprocess usando el Python del ambiente rasterio.
   - Normaliza por streaming para crear GeoTIFF RGB comprimidos.
   - Convierte colormap/paleta a RGB real y limpia fondo detectado desde bordes.
   - Escribe los resultados con el mismo nombre de archivo dentro de `normalizadas`.
   - Alternativamente puede ejecutarse directo con `scripts/normalizar_rgb_streaming.bat "RUTA\CARPETA_ENTRADA"`.

2. `notebooks/02_preparar_paths_datastore.ipynb`
   - Lee la carpeta `normalizadas`.
   - Resuelve la fecha por ranking: primero `json/fechas.json` o Excel si existe registro; si no, regex sobre el nombre del archivo.
   - Calcula sector por cruce espacial.
   - Define nombre oficial y path destino en el datastore.

3. `notebooks/03_cargar_copias_normalizadas_mosaico.ipynb`
   - Copia al datastore el TIFF normalizado y sus archivos asociados (`.tif.ovr`, `.tif.aux.xml`, `.xml`, etc.).
   - Ejecuta `AddRastersToMosaicDataset`.
   - Ejecuta `BuildFootprints`.
   - Actualiza campos criticos del mosaic dataset.

4. `notebooks/04_actualizar_footprints_indice.ipynb`
   - Exporta geometria `FOOTPRINT` desde el mosaic dataset.
   - Anexa geometria a la feature class de indice en GDB.
   - Renombra campos, recalcula `Nombre_de_Vuelo` y sincroniza de vuelta el mosaic dataset.

5. `notebooks/05_generar_mapx_mosaico_completo.ipynb`
   - Usa el mosaic dataset como inventario de nombres y paths.
   - Excluye overviews.
   - Agrega cada imagen al MAPX como raster directo referido al path del datastore.
   - Normaliza etiquetas y ordena capas para publicacion.

La documentacion funcional esta en `documentacion/index.html`.

