# 🚀 Guía Rápida - Multimedia Downloader

Comandos listos para copiar y ejecutar en Termux, Linux o Windows.

## ⚙️ Instalación Rápida

### Termux
```bash
pkg update && pkg upgrade
git clone <url-del-repositorio>
cd multimedia-downloader
chmod +x install.sh
./install.sh
```

### Linux (Ubuntu/Debian)
```bash
git clone <url-del-repositorio>
cd multimedia-downloader
chmod +x install.sh
sudo ./install.sh
```

### Windows (PowerShell)
```powershell
git clone <url-del-repositorio>
cd multimedia-downloader
install.bat
```

---

## 📥 Comandos Básicos

### 1. Descargar video en mejor calidad (MP4 1080p)
```bash
python3 main.py -u "PEGA_LA_URL_AQUI" --format 1080p
```

### 2. Descargar video en 720p (más rápido)
```bash
python3 main.py -u "PEGA_LA_URL_AQUI" --format 720p
```

### 3. Descargar video en 480p (para datos limitados)
```bash
python3 main.py -u "PEGA_LA_URL_AQUI" --format 480p
```

### 4. Descargar solo audio (MP3 de máxima calidad)
```bash
python3 main.py -u "PEGA_LA_URL_AQUI" --audio --quality 320
```

### 5. Descargar audio en 192 kbps (más rápido)
```bash
python3 main.py -u "PEGA_LA_URL_AQUI" --audio --quality 192
```

### 6. Descargar en formato M4A (mejor para Apple)
```bash
python3 main.py -u "PEGA_LA_URL_AQUI" --audio --audio-format m4a --quality 256
```

---

## 📂 Descargas por Lotes

### 7. Descargar múltiples videos desde archivo
```bash
# Primero: edita urls.txt y agrega las URLs
# Luego ejecuta:
python3 main.py -f urls.txt --format 720p
```

### 8. Descargar muchos audios desde archivo
```bash
python3 main.py -f urls.txt --audio --audio-format mp3 --quality 256
```

### 9. Descargar con reintentos automáticos (para conexiones lentas)
```bash
python3 main.py -u "PEGA_LA_URL_AQUI" --format 720p --max-retries 5
```

---

## ▶️ Playlists y Colecciones

### 10. Descargar playlist completa de YouTube
```bash
python3 main.py -u "https://youtube.com/playlist?list=PLAYLIST_ID" --playlist --format 720p
```

### 11. Descargar playlist de SoundCloud
```bash
python3 main.py -u "https://soundcloud.com/usuario/sets/nombre-playlist" --audio --audio-format mp3
```

---

## 🔍 Información y Verificación

### 12. Ver información del video sin descargar
```bash
python3 main.py -u "PEGA_LA_URL_AQUI" --info
```

### 13. Ver información del sistema (Termux, SO, Python)
```bash
python3 main.py --system-info
```

### 14. Ver información de una plataforma específica
```bash
python3 main.py --platform-info youtube
# Opciones: youtube, tiktok, instagram, facebook, x, threads, pinterest, reddit, vimeo, soundcloud
```

### 15. Ver ayuda completa
```bash
python3 main.py --help
```

---

## 🗂️ Directorios y Archivos Personalizados

### 16. Descargar a una carpeta personalizada
```bash
python3 main.py -u "PEGA_LA_URL_AQUI" -o /ruta/personalizada/
```

### 17. Descargar en Termux a almacenamiento compartido
```bash
python3 main.py -u "PEGA_LA_URL_AQUI" -o ~/storage/downloads/
```

### 18. Descargar directamente en la carpeta de descargas de Windows
```bash
python3 main.py -u "PEGA_LA_URL_AQUI" -o "C:\Users\TuUsuario\Downloads\"
```

---

## 🔧 Configuración Avanzada

### 19. Usar archivo de configuración personalizado
```bash
# Primero: copia y edita config.yaml
cp config.yaml mi_config.yaml
# Edita mi_config.yaml en tu editor favorito
# Luego ejecuta:
python3 main.py -u "PEGA_LA_URL_AQUI" --config mi_config.yaml
```

### 20. Guardar la configuración actual
```bash
python3 main.py --config config.yaml --save-config mi_config_guardada.yaml
```

---

## 📊 Logging y Diagnóstico

### 21. Ver logs de descargas (últimas 50 líneas)
```bash
tail -50 logs/downloads_*.log
```

### 22. Ver todos los errores
```bash
cat logs/errors_*.log
```

### 23. Ver logs en vivo mientras descargas
```bash
python3 main.py -u "PEGA_LA_URL_AQUI" --verbose
```

### 24. Modo debug para solucionar problemas
```bash
python3 main.py -u "PEGA_LA_URL_AQUI" --debug
```

---

## 🎯 Casos de Uso Específicos

### YouTubers / Contenido Largo
```bash
# Descargar en 720p (balance calidad/tamaño)
python3 main.py -u "PEGA_LA_URL_AQUI" --format 720p

# O solo audio (más rápido)
python3 main.py -u "PEGA_LA_URL_AQUI" --audio --quality 320
```

### Músicos / Productores
```bash
# Descargar en máxima calidad de audio (320 kbps)
python3 main.py -u "PEGA_LA_URL_AQUI" --audio --quality 320 --audio-format mp3

# O en formato sin pérdida (si está disponible)
python3 main.py -u "PEGA_LA_URL_AQUI" --audio --audio-format wav
```

### Educación / Cursos
```bash
# Playlist de YouTube en 720p
python3 main.py -u "https://youtube.com/playlist?list=ID" --playlist --format 720p

# Con reintentos para conexiones inestables
python3 main.py -u "https://youtube.com/playlist?list=ID" --playlist --max-retries 5
```

### Datos Limitados / Móvil
```bash
# Mínima calidad para ahorrar datos
python3 main.py -u "PEGA_LA_URL_AQUI" --format 360p

# O solo audio comprimido
python3 main.py -u "PEGA_LA_URL_AQUI" --audio --quality 128
```

### Streaming de Redes Sociales
```bash
# TikTok en MP4
python3 main.py -u "https://tiktok.com/@usuario/video/12345..." --format best

# Instagram Reels
python3 main.py -u "https://instagram.com/reel/REELID/" --format 720p

# Videos de Twitter/X
python3 main.py -u "https://x.com/usuario/status/123456789" --format best
```

---

## 🌍 Ejemplos de Plataformas

### YouTube
```bash
# Video individual
python3 main.py -u "https://youtube.com/watch?v=dQw4w9WgXcQ" --format 720p

# Playlist
python3 main.py -u "https://youtube.com/playlist?list=PLxxxxxxxxxxxxxx" --playlist --format 720p
```

### TikTok
```bash
python3 main.py -u "https://www.tiktok.com/@usuario/video/1234567890123456789" --format best
```

### Instagram
```bash
# Post
python3 main.py -u "https://www.instagram.com/p/ABC123DEF456/" --format best

# Reel
python3 main.py -u "https://www.instagram.com/reel/ABC123DEF456/" --format best
```

### SoundCloud (Música)
```bash
# Canción individual
python3 main.py -u "https://soundcloud.com/usuario/nombre-cancion" --audio --quality 320

# Playlist
python3 main.py -u "https://soundcloud.com/usuario/sets/nombre-playlist" --audio --quality 320
```

### Facebook
```bash
python3 main.py -u "https://www.facebook.com/usuario/videos/1234567890/" --format 720p
```

### Twitter/X
```bash
python3 main.py -u "https://x.com/usuario/status/1234567890" --format best
```

---

## ⚡ Comandos Rápidos (Alias para Termux)

Para hacer más rápido, agrega a tu `.bashrc`:

```bash
# Alias para descargar video
alias mdl-video='python3 ~/multimedia-downloader/main.py -u'

# Alias para descargar audio
alias mdl-audio='python3 ~/multimedia-downloader/main.py -u --audio --quality 320'

# Alias para playlist
alias mdl-playlist='python3 ~/multimedia-downloader/main.py -u --playlist --format 720p'
```

Luego usa:
```bash
# Descargar video
mdl-video "https://youtube.com/watch?v=..."

# Descargar audio
mdl-audio "https://youtube.com/watch?v=..."

# Descargar playlist
mdl-playlist "https://youtube.com/playlist?list=..."
```

---

## 🆘 Soluciones Rápidas

### Error: "Python not found"
```bash
# Termux
pkg install python3

# Ubuntu/Debian
sudo apt install python3

# macOS
brew install python3
```

### Error: "FFmpeg not found"
```bash
# Termux
pkg install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Descarga muy lenta en Termux
```bash
# Usar calidad menor
python3 main.py -u "URL" --format 480p

# O solo audio
python3 main.py -u "URL" --audio --quality 128
```

### Permiso denegado en Termux
```bash
# Dar permisos de almacenamiento
termux-setup-storage

# Usar directorio de almacenamiento
python3 main.py -u "URL" -o ~/storage/downloads/
```

---

## 📝 Crear Archivo de URLs Rápidamente

### En Termux/Linux
```bash
# Crear archivo y editarlo
nano urls_para_descargar.txt

# Agregar URLs y presionar Ctrl+X, Y, Enter
# Luego descargar:
python3 main.py -f urls_para_descargar.txt --format 720p
```

### En Windows (PowerShell)
```powershell
# Crear archivo
echo "https://youtube.com/watch?v=..." > urls.txt
echo "https://tiktok.com/video/..." >> urls.txt

# Editar
notepad urls.txt

# Descargar
python3 main.py -f urls.txt --format 720p
```

---

## ✅ Checklist para Usar Correctamente

- [ ] Python 3.7+ instalado (`python3 --version`)
- [ ] FFmpeg instalado (`ffmpeg -version`)
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Carpetas creadas (`mkdir -p downloads logs`)
- [ ] URLs correctas y accesibles
- [ ] Respetas derechos de autor del contenido
- [ ] Tienes espacio suficiente en el disco
- [ ] Conexión a internet estable (para grandes archivos)

---

## 💡 Consejos Finales

1. **Para videos largos**: Usa `--format 480p` o `--format 720p` para equilibrar calidad y tamaño
2. **Para audio**: Siempre usa `--quality 320` si tienes espacio, es la mejor calidad MP3
3. **Para lotes**: Crea archivo `urls.txt` y usa `-f urls.txt` es más rápido que un URL por uno
4. **Para conexiones lentas**: Aumenta `--max-retries 5` y usa calidades menores
5. **En Termux**: Pedir permiso de almacenamiento con `termux-setup-storage` primero

---

**¿Necesitas más ayuda?** Usa `python3 main.py --help` para ver todas las opciones.

**Última actualización:** 2024
