# ❓ Preguntas Frecuentes (FAQ)

## Preguntas de Instalación

### ¿Cómo instalo FFmpeg?

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows (Chocolatey):**
```powershell
choco install ffmpeg
```

**Windows (Scoop):**
```powershell
scoop install ffmpeg
```

**Termux:**
```bash
pkg install ffmpeg
```

### ¿Cómo verifico que FFmpeg está instalado?
```bash
ffmpeg -version
```

Debe mostrar la versión de FFmpeg.

### ¿Qué versión de Python necesito?
Python 3.7 o superior. Verifica con:
```bash
python3 --version
```

### ¿Funciona en Python 2?
No. Python 2 fue descontinuado. Debes usar Python 3.7+.

---

## Preguntas de Uso

### ¿Por qué obtengo error "URL not found"?
1. Verifica que la URL sea correcta
2. El video puede estar eliminado o ser privado
3. Algunos videos solo están disponibles en ciertos países
4. Intenta con `--info` para verificar acceso

### ¿Por qué no se descarga el audio completamente?
Posibles causas:
- **Conexión interrumpida**: Usa `--max-retries 5`
- **Timeout corto**: Cambia `--timeout 60` (60 segundos)
- **FFmpeg no instalado**: Comprueba con `ffmpeg -version`
- **Sin espacio en disco**: Verifica espacio disponible

### ¿Cómo descargo una playlist?

```bash
# YouTube playlist
python3 main.py -u "https://youtube.com/playlist?list=PLAYLIST_ID" --playlist --format 720p

# SoundCloud playlist
python3 main.py -u "https://soundcloud.com/usuario/sets/nombre" --audio
```

### ¿Puedo descargar videos privados o de amigos?
No. Solo se pueden descargar videos públicos y accesibles sin autenticación. Los videos privados, de grupos cerrados o con restricción de acceso no se pueden descargar por razones de privacidad y seguridad.

### ¿Hay límite de descarga simultánea?
La versión actual descarga de uno en uno. Para lotes, solo procesa secuencialmente con pausa entre descargas (configurable en `config.yaml`).

### ¿Se puede resumir una descarga interrumpida?
Actualmente no. Si se interrumpe, el archivo se descargará nuevamente. Esta característica podría agregarse en futuras versiones.

### ¿Cómo extraigo solo audio sin descargar video?
```bash
python3 main.py -u "URL" --audio
```

Esto descarga automáticamente el mejor audio disponible sin video.

### ¿Qué formatos de audio soporta?
- **mp3** (defecto, más compatible)
- **m4a** (mejor para Apple)
- **aac** (standard para Android)
- **opus** (compresión moderna)
- **vorbis** (open source)
- **wav** (sin comprensión)

### ¿Cuál es la mejor calidad de audio kbps?
- **320 kbps**: Máxima calidad (más grande)
- **256 kbps**: Muy buena calidad
- **192 kbps**: Buena calidad (recomendado)
- **128 kbps**: Calidad aceptable (más pequeño)

Para música: 320 kbps es lo mejor.
Para voz/podcasts: 192 kbps es suficiente.

---

## Preguntas de Termux

### ¿Cómo hago que Termux acceda a almacenamiento?
```bash
termux-setup-storage
```

Permitir acceso cuando lo pida. Luego usar:
```bash
cd ~/storage/downloads
python3 main.py -u "URL" -o ./
```

### ¿Por qué es lenta la descarga en Termux?
1. Los datos móviles son más lentos que WiFi
2. Tu conexión puede ser limitada
3. El servidor puede estar limitando velocidad

**Soluciones:**
- Usa WiFi en lugar de datos móviles
- Conecta a un servidor cercano a tu ubicación (mejora con VPN)
- Descarga en menor calidad: `--format 480p` o `--format 360p`
- Descarga solo audio: `--audio --quality 128`

### ¿Cómo veo los archivos descargados en Termux?
```bash
# Ver archivos descargados
ls -la ~/storage/downloads/

# O abre en la aplicación de archivos
cd ~/storage/downloads
```

### ¿Puedo descargar a tarjeta SD en Termux?
No directamente. Termux solo tiene acceso al almacenamiento interno. Debes copiar después:
```bash
# Descargar a almacenamiento interno
python3 main.py -u "URL" -o ~/storage/downloads/

# Copiar a SD (si está montada)
cp ~/storage/downloads/archivo /mnt/sdcard/
```

### ¿Puedo usar Termux con WiFi por hotspot?
Sí, pero será más lento. Usa:
- WiFi directo cuando sea posible
- `--format 360p` o `--format 480p` para datos limitados
- `--audio` en lugar de video completo

### ¿Cómo ejecuto Termux en segundo plano?
Descarga en segundo plano:
```bash
# Ejecutar en segundo plano
nohup python3 main.py -f urls.txt --format 720p &

# Ver progreso
tail -f ./logs/downloads_*.log
```

---

## Preguntas de Configuración

### ¿Dónde edito la configuración?
Abre `config.yaml` con un editor de texto:

```bash
# Termux/Linux
nano config.yaml
# o
vim config.yaml

# Windows
notepad config.yaml
```

### ¿Qué opciones puedo cambiar?
- Directorios de salida por plataforma
- Formato y calidad de video/audio
- Número de reintentos y timeouts
- Nivel de logging
- Activar/desactivar plataformas

Ver `config.yaml` con comentarios explicativos.

### ¿Cómo uso una configuración personalizada?
```bash
# Crear configuración personalizada
cp config.yaml mi_config.yaml
nano mi_config.yaml

# Usar la configuración
python3 main.py -u "URL" --config mi_config.yaml
```

### ¿Cómo cambio el directorio de salida por defecto?
Opción 1: Edita `config.yaml`:
```yaml
output_dirs:
  base: "/ruta/personalizada"
```

Opción 2: Usa línea de comandos:
```bash
python3 main.py -u "URL" -o "/ruta/personalizada/"
```

---

## Preguntas de Plataformas

### ¿Soporta TikTok?
Sí, pero:
- Sin watermark limitado (depende de yt-dlp)
- Rate limiting agresivo (puede requerir esperas)
- Algunos videos pueden estar bloqueados

```bash
python3 main.py -u "https://tiktok.com/@usuario/video/..." --format best
```

### ¿Soporta Instagram?
Sí, pero:
- Puede requerir autenticación para algunos contenidos
- Contenido privado no es accesible
- Rate limiting posible

```bash
python3 main.py -u "https://instagram.com/p/POSTID/" --format best
```

### ¿Soporta Facebook?
Sí, solo:
- Videos públicos
- Puede requerir autenticación
- Algunos videos están protegidos

```bash
python3 main.py -u "https://facebook.com/usuario/videos/..." --format best
```

### ¿Puedo descargar de TikTok sin watermark?
Depende de yt-dlp y de la disponibilidad de versiones sin watermark. No se garantiza.

### ¿Soporta streaming en vivo?
No. Solo contenido ya grabado y publicado.

### ¿Cuál es la plataforma con mejor compatibilidad?
**YouTube** - Máxima compatibilidad, pocas restricciones, mejor documentación.

---

## Preguntas de Logs

### ¿Dónde están los logs?
En la carpeta `./logs/`:
```bash
# Ver últimos logs
ls -la logs/

# Ver último log general
cat logs/general_*.log

# Ver errores
cat logs/errors_*.log

# Ver descargas
cat logs/downloads_*.log
```

### ¿Qué información contienen los logs?
- **general_*.log**: Eventos de la aplicación
- **errors_*.log**: Errores y excepciones
- **downloads_*.log**: Registro de descargas (JSON)

### ¿Cómo limpio los logs antiguos?
```bash
# Ver tamaño de logs
du -sh logs/

# Eliminar logs más antiguos de 7 días
find logs/ -name "*.log" -mtime +7 -delete

# O simplemente borrar todos
rm logs/*.log
```

### ¿Cómo veo logs en tiempo real?
```bash
# Ver logs generales en tiempo real
tail -f logs/general_*.log

# O descargas específicamente
tail -f logs/downloads_*.log
```

---

## Preguntas de Espacio en Disco

### ¿Cuánto espacio ocupan los archivos?
Aproximadamente:
- **Video 1080p**: 500MB - 2GB por hora
- **Video 720p**: 300MB - 1GB por hora
- **Video 480p**: 100MB - 500MB por hora
- **Audio MP3 320kbps**: 30MB - 50MB por hora

### ¿Cómo verifico espacio disponible?
```bash
# Linux/Termux
df -h

# Windows PowerShell
Get-Volume
```

### ¿Puedo descargar a USB?
Sí, especifica la ruta:
```bash
python3 main.py -u "URL" -o "/media/usb/downloads/"
```

---

## Preguntas Legales

### ¿Es legal descargar de estas plataformas?
Depende del contenido y derechos de autor:
- ✅ Contenido con licencia CC (creative commons)
- ✅ Contenido de dominio público
- ✅ Tu propio contenido
- ❌ Contenido con derechos de autor sin permiso
- ❌ Contenido protegido por DRM

**Siempre respeta los términos de servicio de cada plataforma.**

### ¿Puedo compartir videos descargados?
No, solo para uso personal. Compartir requiere permiso del creador.

### ¿Puedo monetizar contenido descargado?
No sin permiso del creador. Violarías derechos de autor.

### ¿Qué pasa si descargo contenido protegido?
La responsabilidad es tuya. La herramienta no elude DRM o restricciones legales.

---

## Preguntas de Resolución de Problemas

### El programa se congela descargando
1. Interrumpe con Ctrl+C
2. Aumenta el timeout: `--timeout 60`
3. Usa menos reintentos: `--max-retries 1`
4. Cambia de WiFi o conexión

### "Connection refused" o "Connection timeout"
1. Verifica tu conexión a internet
2. Intenta con VPN
3. Aumenta timeout: `--timeout 60`
4. Usa proxy si es necesario en `config.yaml`

### "No space left on device"
1. Verifica espacio: `df -h`
2. Usa calidad menor: `--format 360p`
3. Descarga solo audio: `--audio`
4. Libera espacio o usa otro disco

### Error: "This video is not available"
1. El video fue eliminado
2. Está en lista privada
3. Está restringido geográficamente
4. Intenta con VPN
5. Usa `--info` para verificar

### Muy lenta la descarga
1. Cambia de WiFi
2. Usa calidad menor
3. Cierra otras aplicaciones
4. Verifica velocidad: `speedtest`
5. Usa `--format 360p` o `--audio`

---

## Preguntas de Desarrollo

### ¿Cómo modifico el código?
El código está documentado. Archivos principales:
- `main.py` - CLI
- `downloader.py` - Lógica de descarga
- `config.py` - Configuración
- `utils.py` - Utilidades
- `platforms.py` - Plataformas

Cada módulo tiene docstrings explicativos.

### ¿Cómo agrego una plataforma?
1. Edita `platforms.py`
2. Agrega info en `PLATFORM_REGISTRY`
3. Yt-dlp probablemente ya la soporte

### ¿Cómo contribuyo?
1. Fork el repo
2. Crea rama para tu feature
3. Commit los cambios
4. Push y abre Pull Request

---

## Preguntas Misceláneas

### ¿Puedo usar esto en producción?
Sí, está lista para producción. Código modular y bien documentado.

### ¿Se requiere API key o token?
No. Solo se necesita acceso público a contenido.

### ¿Soporte para proxies?
Sí, configurable en `config.yaml`:
```yaml
proxy:
  enabled: true
  http: "http://proxy.com:8080"
  https: "https://proxy.com:8080"
```

### ¿Puedo programar descargas?
Sí, con cron (Linux) o Task Scheduler (Windows):

```bash
# Linux - cada 6 horas
0 */6 * * * cd /path/multimedia-downloader && python3 main.py -f urls.txt --format 720p
```

### ¿Puedo hacer donaciones?
Este proyecto es de código abierto y gratuito. ¡Comparte y difunde!

---

**¿Tu pregunta no está aquí?** Revisa los logs o usa `--debug` para más información.

**Última actualización:** 2024
