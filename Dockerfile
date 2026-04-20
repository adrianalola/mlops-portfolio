# ── Base image ─────────────────────────────────────────────────────────────────
# Python 3.11 slim = Python completo pero sin herramientas innecesarias
# Esto hace la imagen más pequeña y más segura
FROM python:3.11-slim

# ── Directorio de trabajo dentro del contenedor ────────────────────────────────
# Todo lo que hagamos a partir de aquí ocurre dentro de /app
WORKDIR /app

# ── Copiar e instalar dependencias PRIMERO ─────────────────────────────────────
# Por qué primero? Docker cachea capas. Si no cambias requirements.txt,
# no reinstala todo cada vez que cambias tu código. Ahorra mucho tiempo.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copiar el código de la aplicación ─────────────────────────────────────────
COPY app/ ./app/
COPY model_artifacts/ ./model_artifacts/

# ── Variables de entorno por defecto ──────────────────────────────────────────
ENV APP_ENV=production
ENV LOG_LEVEL=INFO
ENV PORT=8000

# ── Puerto que expone el contenedor ───────────────────────────────────────────
EXPOSE 8000

# ── Comando que se ejecuta cuando arranca el contenedor ───────────────────────
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
