# Flujo Geosupport Imagenes PAO

Repositorio limpio para ejecutar el flujo final de carga de imagenes drone PAO.

El flujo esta compilado en `flujo_geosupport_final/` y se ejecuta por etapas:

1. `notebooks/01_normalizar_rgb_streaming.ipynb`
2. `notebooks/02_preparar_paths_datastore.ipynb`
3. `notebooks/03_cargar_copias_normalizadas_mosaico.ipynb`
4. `notebooks/04_actualizar_footprints_indice.ipynb`
5. `notebooks/05_generar_mapx_mosaico_completo.ipynb`

Antes de ejecutar una entrega, ajustar `flujo_geosupport_final/settings.json`.

La documentacion funcional esta en:

`flujo_geosupport_final/documentacion/index.html`

Los modulos reutilizables requeridos por los notebooks estan en `core/`.
