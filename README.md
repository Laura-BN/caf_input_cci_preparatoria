# caf_input_cci_preparatoria

Extracción del texto de los IDOs y redacción asistida por LLM (Azure AI Foundry) de los textos
del Input CCI. Sigue la estructura de [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/):
primero se prototipa en notebooks y luego la lógica validada pasa a `caf_input_cci_preparatoria/`.

## Notebooks

Los notebooks se organizan por paso del flujo de trabajo; el número del notebook empieza por el
número del paso, y sus tablas intermedias van en una carpeta con el mismo nombre del paso
dentro de `data/interim/`. Hoy están implementados los pasos 2, 3 y 4 (este último, sin la
PPT de la reunión).

### 2. IDOs - Input CCI (`notebooks/2. IDOs - Input CCI/`)

Llega un IDO, se registra en el Input CCI y se llenan sus datos, evidencia, recomendaciones y
concepto, que luego sirven de insumo para la Preparatoria.

| Notebook | Qué hace | Lee | Escribe |
|---|---|---|---|
| `02.00_ejecutar_todo.ipynb` | Ejecuta 02.01 a 02.05 en orden con el kernel del proyecto y se detiene en el primer fallo | Los cinco notebooks | Resumen en el notebook y filas nuevas en `reports/2. IDOs - Input CCI_historico_ejecuciones.xlsx` (IDOs nuevos, llamadas y tokens de Azure) |
| `02.01_extraccion_texto_idos.ipynb` | Extrae del Word la ficha, los montos, el financiamiento verde y ocho secciones (local, sin API); las 3, 4.1 y 5.1 son para el insumo del paso 3 | `data/raw/2. IDOs - Input CCI/` | `data/interim/2. IDOs - Input CCI/02.01_extraccion_idos/idos.csv` |
| `02.02_redaccion_textos_idos.ipynb` | Redacta gran sector, objetivo, pertinencia e intervención con Azure; reutiliza respuestas por huella del Word | `idos.csv` | `data/interim/2. IDOs - Input CCI/02.02_redaccion_idos/idos_redaccion.csv` |
| `02.03_evidencia_repositorio.ipynb` | Selecciona filas del repositorio y redacta evidencia y factores de impacto con Azure; reutiliza respuestas por huella del mensaje y verifica citas | `idos_redaccion.csv` y `data/raw/1. Protocolo de evidencia.xlsx` | `data/interim/2. IDOs - Input CCI/02.03_evidencia_repositorio/idos_evidencia.csv` |
| `02.04_concepto_priorizacion.ipynb` | Redacta con Azure la decisión y el concepto de priorización, con conceptos históricos como ejemplos de estilo; reutiliza respuestas por huella del mensaje | `idos_evidencia.csv` y `data/raw/Libros excel/Input CCI.xlsx` | `data/interim/2. IDOs - Input CCI/02.04_concepto_priorizacion/idos_concepto.csv` |
| `02.05_excel_input_cci.ipynb` | Genera el Input CCI con listas desplegables y la columna Revisar, sin API | `idos_concepto.csv` | `data/processed/2. Input CCI.xlsx` |

Los notebooks van en cadena: cada uno lee el CSV del anterior y le agrega columnas, así que se
ejecutan en orden. Cada CSV es también la caché de su notebook: un IDO que no cambió no vuelve a
llamar a Azure. Para usar `02.00`, ejecuta `uv sync` para disponer de nbclient y nbformat y
cierra en Positron los notebooks del paso antes de iniciarlo; `02.02`–`02.04` requieren conexión
para llamar a Azure. `2. Input CCI.xlsx` se regenera completo en cada corrida.

Formato de nombre `00.00_titulo.ipynb`; secciones LOAD LIBRARIES, LOAD DATA, PROCESS DATA y
SAVE DATA. Los notebooks que usen la API leen del `.env` de la raíz `AZUREOPENAI_API_ENDPOINT`,
`AZUREOPENAI_API_KEY` y `AZUREOPENAI_DEPLOYMENT`.

### 3. Insumo Evid+Recom (`notebooks/3. Insumo Evid+Recom/`)

Para una operación PPI se arma el insumo de Evidencia + Recomendaciones que se envía a los
ejecutivos. Parte de la tabla final del paso 2 y del texto completo del repositorio, no de la
síntesis del Input CCI. Solo los IDOs PPI pasan a este paso.

**Para procesar un IDO nuevo**: se pone el Word en `data/raw/2. IDOs - Input CCI/` y se corre
`03.00_ejecutar_todo.ipynb`. Ejecuta el `02.00` (Input CCI) y luego del `03.01` al `03.04`
(insumo en Word, si es PPI); solo ese IDO llama a Azure.

| Notebook | Qué hace | Lee | Escribe |
|---|---|---|---|
| `03.00_ejecutar_todo.ipynb` | Ejecuta el `02.00` y del `03.01` al `03.04` en orden, se detiene en el primer fallo y anota IDOs PPI nuevos, Word generados, llamadas y tokens de Azure | Los notebooks de los pasos 2 y 3 | Filas nuevas en `reports/3. Insumo Evid+Recom_historico_ejecuciones.xlsx` |
| `03.01_datos_ido.ipynb` | Toma solo los IDOs PPI del paso 2 y reúne el texto completo (R, S, T) de las filas del repositorio que eligió el `02.03`, con ajuste manual opcional (local, sin API) | `idos_concepto.csv` y `data/raw/1. Protocolo de evidencia.xlsx` | `data/interim/3. Insumo Evid+Recom/03.01_datos_ido/idos_insumo.csv` y `filas_repositorio.csv` |
| `03.02_seccion1_evidencia.ipynb` | Redacta con Azure la sección 1 (resumen, cobertura, impactos, qué tener en cuenta en el diseño, referencias) con el texto completo de las filas; el nivel de confianza sale de la columna U del repositorio; verifica citas y referencias; reutiliza respuestas por huella del mensaje | Las dos tablas del `03.01` | `data/interim/3. Insumo Evid+Recom/03.02_seccion1_evidencia/idos_seccion1.csv` |
| `03.03_seccion2_implicaciones.ipynb` | Redacta con Azure la sección 2 (implicaciones para la operación) uniendo las recomendaciones y lecciones del repositorio (S, T) con las secciones 2.2, 2.3, 3, 4.1 y 5.1 del IDO; señala vacíos del IDO; reutiliza respuestas por huella del mensaje | `idos_seccion1.csv` y `filas_repositorio.csv` | `data/interim/3. Insumo Evid+Recom/03.03_seccion2_implicaciones/idos_seccion2.csv` |
| `03.04_word_insumo.ipynb` | Arma un Word por IDO con las secciones 1 y 2, la sección 3 (Sí/No y concepto) tomada del paso 2 como borrador y las referencias (local, sin API, con `python-docx`) | `idos_seccion2.csv` | `data/processed/3. Insumo Evid+Recom/Evid+Recom - <operación>.docx` |

Los Word se reescriben en cada corrida: lo que se edite a mano debe hacerse en una copia.

### 4. Preparatoria CCI (`notebooks/4. Preparatoria CCI/`)

Llegan los documentos de una sesión del CCI (IDO, DEC, reportes de crédito de renovaciones,
dispensas, enmiendas) y se llena una fila por documento con las columnas A–R de la hoja
`CCI-2026` del Excel *Preparación CCI y CFE - VPE y GPID*, más `Revisar`.

**Para una sesión nueva**: se crea `data/raw/4. Preparatoria CCI/<fecha>/` (por ejemplo,
`13 de noviembre de 2026`) con los PDF numerados de la agenda (`01. …pdf`) y se corre
`04.00_ejecutar_todo.ipynb`. Solo los documentos nuevos llaman a Azure.

| Notebook | Qué hace | Lee | Escribe |
|---|---|---|---|
| `04.00_ejecutar_todo.ipynb` | Ejecuta del `04.01` al `04.05` en orden, se detiene en el primer fallo y anota documentos nuevos, llamadas y tokens de Azure | Los notebooks del paso 4 | Filas nuevas en `reports/4. Preparatoria CCI_historico_ejecuciones.xlsx` |
| `04.01_documentos.ipynb` | Lee el texto de cada PDF; los escaneados (sin texto) se renderizan como imágenes JPG por página (local, sin API) | `data/raw/4. Preparatoria CCI/<fecha>/` | `data/interim/4. Preparatoria CCI/04.01_documentos/documentos.csv` y `paginas/` |
| `04.02_ficha_documentos.ipynb` | Extrae con Azure la ficha del documento: tipo, nombre, país, riesgo, producto, monto, FV, CT, agenda, texto de la columna Operación y aporte al desarrollo de las líneas; reutiliza respuestas por huella | `documentos.csv` | `04.02_ficha_documentos/fichas.csv` |
| `04.03_cruce_registros.ipynb` | Busca la operación por nombre y país en el Input CCI (paso 2 e histórico), en las preparatorias anteriores (hojas `CCI-2026` y `CCI-2025`) y en los insumos Evid+Recom; `ajustes_cruce` corrige el cruce a mano (local, sin API) | `fichas.csv` y los Excel de `data/raw/Libros excel/` | `04.03_cruce_registros/cruce.csv` |
| `04.04_alertas_preguntas.ipynb` | Redacta con Azure las alertas, la frase de priorización y las preguntas sugeridas, con el documento completo y lo que trajo el cruce; reutiliza respuestas por huella | `cruce.csv` y `documentos.csv` | `04.04_alertas_preguntas/alertas_preguntas.csv` |
| `04.05_excel_preparatoria.ipynb` | Arma el Excel con listas desplegables y la columna Revisar; en IDO y aprobaciones copia la evidencia y las recomendaciones del Input CCI (local, sin API) | `alertas_preguntas.csv` | `data/processed/4. Preparatoria CCI.xlsx` |

`4. Preparatoria CCI.xlsx` se regenera completo en cada corrida y no modifica el Excel
institucional: sus filas se copian a mano. La Retroalimentación DADMI y el semáforo de las
recomendaciones se completan a mano.

## Entorno

```sh
make requirements   # uv sync
```

En Positron, elegir el intérprete **uv: caf_input_cci_preparatoria** como kernel.

Para instalar Codex y conectarlo con Azure OpenAI de CAF, ver el manual
[`Manual_Codex_Azure_CAF.txt.rtf`](docs/Manual_Codex_Azure_CAF.txt.rtf).
Esa configuración es solo para Codex: los notebooks que llaman a la API leen su propio `.env`
en la raíz del proyecto (ver arriba las variables `AZUREOPENAI_*`).
