"""
Módulo de descarga multimedia
- Lógica de descarga usando yt-dlp
- Manejo de errores y reintentos
- Extracción de metadatos
- Procesamiento de playlists y lotes
"""

import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import yt_dlp
from colorama import Fore, Style

from config import ConfigManager
from utils import (
    LogManager, MetadataExtractor, FileManager, 
    URLValidator, ProgressTracker, SystemDetector
)
from platforms import PlatformDetector, Platform, URLExtractor


class MediaDownloader:
    """Gestor principal de descargas multimedia"""
    
    def __init__(self, config: ConfigManager, logger: LogManager):
        """
        Inicializa el descargador
        
        Args:
            config: ConfigManager instance
            logger: LogManager instance
        """
        self.config = config
        self.logger = logger
        self.session_downloads = []
        self.session_errors = []
    
    def download_single(self, url: str, format_type: str = "video",
                       quality: Optional[str] = None) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Descarga un archivo multimedia individual
        
        Args:
            url: URL del contenido
            format_type: Tipo de formato (video, audio, image)
            quality: Calidad específica (opcional)
            
        Returns:
            Tupla (éxito, mensaje, metadatos)
        """
        # Validar URL
        if not URLValidator.is_valid_url(url):
            self.logger.error(f"URL inválida: {url}")
            return False, "URL inválida", {}
        
        # Normalizar URL
        url = URLExtractor.normalize_url(url)
        
        # Detectar plataforma
        platform = PlatformDetector.detect_platform(url)
        self.logger.debug(f"Plataforma detectada: {platform.value}")
        
        # Verificar si la plataforma soporta el formato
        if not PlatformDetector.supports_format(platform, format_type):
            msg = f"Plataforma {platform.value} no soporta formato {format_type}"
            self.logger.warning(msg)
            return False, msg, {}
        
        # Obtener opciones de yt-dlp
        yt_dlp_opts = self.config.get_yt_dlp_opts(platform.value, format_type)
        
        # Aplicar calidad específica si se proporciona
        if quality:
            yt_dlp_opts['format'] = self._build_quality_format(quality)
        
        # Realizar descarga con reintentos
        max_retries = self.config.get('download.max_retries', 3)
        retry_delay = self.config.get('download.retry_delay', 2)
        
        for attempt in range(max_retries + 1):
            try:
                self.logger.info(f"Descargando: {url} (intento {attempt + 1}/{max_retries + 1})")
                
                start_time = time.time()
                
                with yt_dlp.YoutubeDL(yt_dlp_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                
                duration = time.time() - start_time
                filename = info.get('filename', 'unknown')
                file_size = FileManager.get_file_size(filename)
                
                # Registrar descarga exitosa
                self.logger.success(f"Descargado: {info.get('title', 'Sin título')}")
                self.logger.log_download(url, filename, "success", duration, file_size)
                
                # Extraer metadatos
                metadata = MetadataExtractor.extract_from_info(info)
                
                self.session_downloads.append({
                    "url": url,
                    "platform": platform.value,
                    "title": info.get('title', 'Unknown'),
                    "filename": filename,
                    "status": "success",
                    "timestamp": datetime.now().isoformat(),
                    "duration": duration
                })
                
                return True, f"Descargado: {info.get('title')}", metadata
            
            except yt_dlp.utils.DownloadError as e:
                error_msg = f"Error de descarga: {str(e)}"
                self.logger.warning(error_msg)
                
                if attempt < max_retries:
                    self.logger.info(f"Reintentando en {retry_delay} segundos...")
                    time.sleep(retry_delay)
                    retry_delay *= 1.5  # Backoff exponencial
                else:
                    self.logger.error(error_msg, exc=e)
                    self.session_errors.append({
                        "url": url,
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    })
                    return False, error_msg, {}
            
            except Exception as e:
                error_msg = f"Error inesperado: {str(e)}"
                self.logger.error(error_msg, exc=e)
                
                if attempt < max_retries:
                    self.logger.info(f"Reintentando en {retry_delay} segundos...")
                    time.sleep(retry_delay)
                    retry_delay *= 1.5
                else:
                    self.session_errors.append({
                        "url": url,
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    })
                    return False, error_msg, {}
        
        return False, "Falló después de reintentos", {}
    
    def download_batch(self, urls: List[str], format_type: str = "video",
                      quality: Optional[str] = None) -> Dict[str, Any]:
        """
        Descarga múltiples archivos multimedia
        
        Args:
            urls: Lista de URLs
            format_type: Tipo de formato
            quality: Calidad específica
            
        Returns:
            Resumen de resultados
        """
        tracker = ProgressTracker(len(urls))
        results = {
            "total": len(urls),
            "successful": [],
            "failed": [],
            "skipped": []
        }
        
        self.logger.info(f"Iniciando descarga de {len(urls)} archivos")
        
        for idx, url in enumerate(urls, 1):
            self.logger.info(f"\n[{idx}/{len(urls)}] Procesando: {url}")
            
            # Validación rápida
            if not URLValidator.is_valid_url(url):
                self.logger.warning(f"URL inválida omitida: {url}")
                tracker.increment_skipped()
                results["skipped"].append(url)
                continue
            
            # Detectar si ya existe
            platform = PlatformDetector.detect_platform(url)
            video_id = URLExtractor.extract_video_id(url, platform)
            
            if self._already_downloaded(url, video_id):
                self.logger.warning(f"Ya descargado: {url}")
                tracker.increment_skipped()
                results["skipped"].append(url)
                continue
            
            # Intentar descarga
            success, message, metadata = self.download_single(url, format_type, quality)
            
            if success:
                tracker.increment_completed()
                results["successful"].append({
                    "url": url,
                    "message": message,
                    "metadata": metadata
                })
            else:
                tracker.increment_failed()
                results["failed"].append({
                    "url": url,
                    "error": message
                })
            
            # Aplicar sleep entre descargas (cortesía)
            sleep_interval = self.config.get('download.sleep_interval', 2)
            if idx < len(urls):
                self.logger.debug(f"Esperando {sleep_interval}s antes de siguiente descarga...")
                time.sleep(sleep_interval)
        
        # Imprimir resumen
        tracker.print_summary()
        
        return results
    
    def download_from_file(self, filepath: str, format_type: str = "video",
                          quality: Optional[str] = None) -> Dict[str, Any]:
        """
        Lee URLs de un archivo y descarga
        
        Args:
            filepath: Ruta al archivo con URLs
            format_type: Tipo de formato
            quality: Calidad específica
            
        Returns:
            Resumen de resultados
        """
        try:
            urls = FileManager.read_urls_from_file(filepath)
            self.logger.info(f"Cargadas {len(urls)} URLs desde {filepath}")
            return self.download_batch(urls, format_type, quality)
        except Exception as e:
            self.logger.error(f"Error al procesar archivo: {e}", exc=e)
            return {
                "total": 0,
                "successful": [],
                "failed": [],
                "skipped": [],
                "error": str(e)
            }
    
    def extract_playlist_info(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Extrae información de una playlist sin descargar
        
        Args:
            url: URL de la playlist
            
        Returns:
            Información de la playlist
        """
        try:
            yt_dlp_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': 'in_playlist'
            }
            
            with yt_dlp.YoutubeDL(yt_dlp_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            
            playlist_info = {
                "title": info.get('title', 'Unknown'),
                "uploader": info.get('uploader', 'Unknown'),
                "total_videos": len(info.get('entries', [])),
                "description": info.get('description', ''),
                "videos": []
            }
            
            for entry in info.get('entries', []):
                playlist_info["videos"].append({
                    "id": entry.get('id'),
                    "title": entry.get('title', 'Unknown'),
                    "url": entry.get('url', ''),
                    "duration": entry.get('duration', 0)
                })
            
            return playlist_info
        
        except Exception as e:
            self.logger.error(f"Error extrayendo info de playlist: {e}", exc=e)
            return None
    
    def extract_audio(self, url: str, quality: str = "192") -> Tuple[bool, str]:
        """
        Extrae audio de un video
        
        Args:
            url: URL del video
            quality: Calidad en kbps
            
        Returns:
            Tupla (éxito, mensaje)
        """
        return self.download_single(url, format_type="audio", quality=quality)[0:2]
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Retorna resumen de la sesión actual"""
        return {
            "total_downloads": len(self.session_downloads),
            "total_errors": len(self.session_errors),
            "downloads": self.session_downloads,
            "errors": self.session_errors,
            "timestamp": datetime.now().isoformat()
        }
    
    def save_session_log(self, filepath: str):
        """Guarda el log de la sesión en JSON"""
        try:
            summary = self.get_session_summary()
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            self.logger.success(f"Log de sesión guardado: {filepath}")
        except Exception as e:
            self.logger.error(f"Error guardando log: {e}", exc=e)
    
    def _build_quality_format(self, quality: str) -> str:
        """Construye formato para calidad específica"""
        quality_map = {
            'best': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            '1080p': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]',
            '720p': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]',
            '480p': 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]',
            '360p': 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]',
            'audio_only': 'bestaudio[ext=m4a]/bestaudio',
        }
        return quality_map.get(quality, quality_map['best'])
    
    def _already_downloaded(self, url: str, video_id: Optional[str]) -> bool:
        """Verifica si un video ya fue descargado"""
        # Implementación simple: verificar si existe en el registro de sesión
        for download in self.session_downloads:
            if download["url"] == url:
                return True
        return False


class PlaylistProcessor:
    """Procesa y descarga playlists completas"""
    
    def __init__(self, downloader: MediaDownloader, logger: LogManager):
        """
        Inicializa el procesador de playlists
        
        Args:
            downloader: MediaDownloader instance
            logger: LogManager instance
        """
        self.downloader = downloader
        self.logger = logger
    
    def download_playlist(self, url: str, format_type: str = "video",
                         quality: Optional[str] = None,
                         start_index: int = 1,
                         end_index: Optional[int] = None) -> Dict[str, Any]:
        """
        Descarga una playlist completa
        
        Args:
            url: URL de la playlist
            format_type: Tipo de formato
            quality: Calidad específica
            start_index: Índice inicial
            end_index: Índice final (None = todo)
            
        Returns:
            Resumen de descargas
        """
        self.logger.info(f"Extrayendo información de playlist...")
        
        playlist_info = self.downloader.extract_playlist_info(url)
        if not playlist_info:
            return {"error": "No se pudo extraer información de playlist"}
        
        self.logger.info(f"Playlist: {playlist_info['title']}")
        self.logger.info(f"Total de videos: {playlist_info['total_videos']}")
        
        # Extraer URLs de videos
        videos = playlist_info['videos']
        if end_index:
            videos = videos[start_index-1:end_index]
        else:
            videos = videos[start_index-1:]
        
        urls = [v['url'] for v in videos if v['url']]
        
        self.logger.info(f"Descargando {len(urls)} videos...")
        return self.downloader.download_batch(urls, format_type, quality)


class BulkProcessor:
    """Procesa descargas en lote desde múltiples fuentes"""
    
    def __init__(self, downloader: MediaDownloader, logger: LogManager):
        """
        Inicializa el procesador en lote
        
        Args:
            downloader: MediaDownloader instance
            logger: LogManager instance
        """
        self.downloader = downloader
        self.logger = logger
    
    def process_mixed_list(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Procesa una lista mixta de URLs, playlists y archivos
        
        Args:
            items: Lista con diccionarios de configuración
                  {"type": "url/playlist/file", "value": "...", "format": "video/audio", ...}
            
        Returns:
            Resumen consolidado
        """
        consolidated_results = {
            "total_items": len(items),
            "processed": 0,
            "successful": 0,
            "failed": 0,
            "items": []
        }
        
        for item in items:
            item_type = item.get('type', 'url')
            value = item.get('value')
            format_type = item.get('format', 'video')
            quality = item.get('quality')
            
            self.logger.info(f"\nProcesando {item_type}: {value}")
            
            try:
                if item_type == 'url':
                    success, msg, metadata = self.downloader.download_single(value, format_type, quality)
                    consolidated_results["processed"] += 1
                    if success:
                        consolidated_results["successful"] += 1
                    else:
                        consolidated_results["failed"] += 1
                
                elif item_type == 'playlist':
                    results = self.downloader.download_batch([value], format_type, quality)
                    consolidated_results["processed"] += 1
                    consolidated_results["successful"] += results['successful'].__len__()
                    consolidated_results["failed"] += results['failed'].__len__()
                
                elif item_type == 'file':
                    results = self.downloader.download_from_file(value, format_type, quality)
                    consolidated_results["processed"] += 1
                    consolidated_results["successful"] += len(results['successful'])
                    consolidated_results["failed"] += len(results['failed'])
                
                consolidated_results["items"].append({
                    "type": item_type,
                    "value": value,
                    "status": "processed"
                })
            
            except Exception as e:
                self.logger.error(f"Error procesando {item_type}: {e}", exc=e)
                consolidated_results["failed"] += 1
                consolidated_results["items"].append({
                    "type": item_type,
                    "value": value,
                    "status": "error",
                    "error": str(e)
                })
        
        return consolidated_results
