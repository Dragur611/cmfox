# REQUERIMIENTO 1: Uso estricto de Ubuntu 24.04 (Noble Numbat)
FROM ubuntu:24.04

# Variables de entorno para ejecución silente y configuración base
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Bogota

# 1. ACTUALIZACIÓN DEL SISTEMA Y DEPENDENCIAS GRÁFICAS (Soporte t64)
# Se instalan paquetes de ventanas, visualización web y bibliotecas de bajo nivel
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv \
    xvfb x11vnc supervisor xterm \
    novnc websockify \
    fluxbox \
    wget curl unzip git \
    libgtk-3-0 libx11-xcb1 \
    # Resolución crítica para Ubuntu 24.04 
    libasound2t64 libatk-bridge2.0-0t64 libatk1.0-0t64 \
    libgbm1 libnss3 libxcomposite1 libxdamage1 \
    libxrandr2 libxkbcommon0 \
    # Dependencias base para tipografía
    fontconfig fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# 2. ENTORNO VIRTUAL DE PYTHON (Cumplimiento de PEP 668 en Ubuntu)
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# 3. INSTALACIÓN DE CAMOUFOX Y HERRAMIENTAS NATIVAS [18]
# Se especifica la variante [geoip] recomendada encarecidamente para proxy
RUN pip install --no-cache-dir -U "camoufox[geoip]" python-dotenv

# El comando 'fetch' de Camoufox descarga el binario parcheado del motor Gecko
# los modelos estadísticos de BrowserForge y los Addons por defecto [18, 19]
RUN camoufox fetch

# 4. APROVISIONAMIENTO CRÍTICO DE COHERENCIA TIPOGRÁFICA
# Para evitar el rechazo masivo por inconsistencia de métricas de fuentes [3, 5],
# el directorio local 'fonts/' provisto por el operador debe contener los archivos.ttf
RUN mkdir -p /usr/local/share/fonts/camoufox_fonts
COPY./fonts/ /usr/local/share/fonts/camoufox_fonts/
# Forzar la reindexación de la caché de fuentes del sistema operativo 
RUN fc-cache -f -v

# 5. INTEGRACIÓN DE LA APLICACIÓN HEXAGONAL
WORKDIR /app
COPY src/ /app/src/
COPY main.py /app/main.py
COPY.env /app/.env

# 6. CONFIGURACIÓN DEL ORQUESTADOR DE PROCESOS (Supervisor)
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh

# Exponer el puerto para visualización web noVNC
EXPOSE 8080

ENTRYPOINT ["/opt/entrypoint.sh"]