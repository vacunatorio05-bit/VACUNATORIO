# Vacunatorio Tres Cerritos

App para celular (se instala desde el navegador) para el vacunatorio del Centro de Salud del barrio Tres Cerritos, Salta Capital.

- Padrón de pacientes y vacunas faltantes según el Calendario Nacional de Vacunación.
- Registro de aplicaciones (lote, vacunador, establecimiento, condición, ESAVI).
- Escuelas por curso, visitas domiciliarias con GPS y mapa.
- Importa y exporta Excel. Funciona sin internet.

**Privacidad:** los datos de pacientes se guardan solo en el celular. Este repositorio contiene únicamente el programa. No es una app oficial del Ministerio de Salud ni reemplaza la carga en NomiVac/SISA.

## Para programadores
El código está en `src/app.html`. `python3 build.py` genera `index.html`, `sw.js` y `manifest.json` en la raíz (GitHub Pages).
