#!/bin/bash
set -e

# Establecer variable de entorno gráfica global
export DISPLAY=:1

# Configuración de seguridad VNC (Requisito fundamental para redes compartidas)
echo "[*] Generando credenciales para la sesión interactiva VNC..."
mkdir -p ~/.vnc
x11vnc -storepasswd "operador123" ~/.vnc/passwd

# Redirigir el control a Supervisor para lanzar demonios en paralelo
echo "[*] Arrancando infraestructura gráfica y aplicación hexagonal..."
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf