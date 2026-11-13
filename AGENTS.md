# Guía para agentes

## Propósito

Extraer el texto de los IDOs (Word) y, con la API de Azure AI Foundry, redactar los textos del
Input CCI. Ver `README.md` para la estructura y los notebooks.

## Cómo escribir código

- Antes de escribir, revisar o refactorizar código, seguir la skill
  `.agents/skills/karpathy-guidelines/SKILL.md`: hacer explícitos los supuestos, preferir lo
  simple, cambiar solo lo necesario y definir cómo se verifica el resultado.
- Notebooks: nombre `00.00_titulo.ipynb` y secciones LOAD LIBRARIES, LOAD DATA, PROCESS DATA y
  SAVE DATA, con explicaciones en español y celdas cortas.
- Rutas desde `caf_input_cci_preparatoria/config.py`. La lógica validada en notebooks pasa luego
  al paquete `caf_input_cci_preparatoria/`.
- Ruff, 99 caracteres por línea: `make format` antes de entregar.

## Datos y credenciales

- `data/raw/` no se modifica. Resultados de trabajo en `data/interim/`, finales en
  `data/processed/`.
- La clave de Azure va en `.env` (ignorado por Git): `AZUREOPENAI_API_ENDPOINT`,
  `AZUREOPENAI_API_KEY`, `AZUREOPENAI_DEPLOYMENT`. Nunca imprimir sus valores.
