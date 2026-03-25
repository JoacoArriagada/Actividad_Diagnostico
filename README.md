# 📊 GitHub Method Word Miner

Este proyecto es una herramienta de análisis estático diseñada para identificar, extraer y visualizar en tiempo real las palabras más utilizadas en los nombres de métodos y funciones de repositorios públicos en GitHub (Python y Java).

## 🏗️ Arquitectura del Sistema
El sistema sigue un modelo **Productor-Consumidor** altamente desacoplado, orquestado mediante contenedores Docker:

1.  **Miner (Productor):** * Interactúa con la API REST de GitHub para buscar repositorios populares.
    * **Análisis Sintáctico:** Utiliza `ast` (Python) y `javalang` (Java) para extraer nombres de métodos reales, evitando los "falsos positivos" de las expresiones regulares simples.
    * **Normalización:** Descompone convenciones `camelCase` y `snake_case` en palabras individuales.
2.  **Storage (Comunicación):** * Utiliza una base de datos **SQLite** montada sobre un volumen compartido.
    * Implementa el modo **WAL (Write-Ahead Logging)**, permitiendo escrituras del Miner y lecturas del Visualizer de forma simultánea y en tiempo real sin bloqueos de archivo.
3.  **Visualizer (Consumidor):**
    * Interfaz web interactiva construida con **Streamlit**.
    * Muestra métricas de palabras únicas, frecuencias totales y un ranking (Top-N) parametrizable.

## 🛡️ Relación con la Ciberseguridad
Aunque parece un proyecto de software general, este tipo de herramientas son la base para:
* **Reconocimiento de Metadatos:** Análisis de tendencias de desarrollo en organizaciones.
* **SAST (Static Application Security Testing):** Identificación de funciones sensibles o patrones de código inseguro.

## 🛠️ Requisitos Previos
* [Docker](https://www.docker.com/) y Docker Compose instalados.
* Un **Personal Access Token (PAT)** de GitHub (sin permisos especiales requeridos para repositorios públicos).

## 🚀 Instrucciones de Ejecución

1.  **Configurar credenciales:**
    Crea un archivo `.env` en la raíz del proyecto y añade tu token:
    ```env
    GITHUB_TOKEN=ghp_tu_token_aqui
    ```

2.  **Iniciar el sistema:**
    Ejecuta el siguiente comando en tu terminal:
    ```bash
    docker compose up --build
    ```

3.  **Ver resultados:**
    Accede a la interfaz web en tu navegador:
    ```text
    http://localhost:8501
    ```

## 🧠 Decisiones de Diseño
* **Modularidad:** El código está dividido en módulos atómicos (`src/`), facilitando el mantenimiento y la escalabilidad (ej: cambiar SQLite por Redis sin tocar la lógica del Miner).
* **Eficiencia de Red:** Se optó por descargar archivos específicos vía API en lugar de realizar un `git clone` completo, optimizando drásticamente el uso de ancho de banda y almacenamiento.
* **Robustez:** Implementación de manejo de **Rate Limits** de la API de GitHub para asegurar la ejecución continua.

---
**Desarrollado por:** [Joaquín Arriagada](https://github.com/JoacoArriagada)  
*Estudiante de Ingeniería Civil Informática - Universidad de la Frontera (UFRO)*
