"""
Módulo de utilidades para multimedia-downloader
- Detección de Sistema Operativo
- Gestión de logs
- Extracción de metadatos
- Manejo de rutas y archivos
"""

import os
import sys
import logging
import json
import platform
from datetime import datetime
from pathlib import Path
from colorama import Fore, Style, init

# Inicializar colorama para soporte de colores en Windows y Termux
init(autoreset=True)


class SystemDetector:
    """Detecta el sistema operativo y sus características"""
    
    @staticmethod
    def get_os():
        """Retorna el SO actual"""
        return platform.system().lower()
    
    @staticmethod
    def is_termux():
        """Verifica si se ejecuta en Termux"""
        return os.path.exists("/data/data/com.termux")
    
    @staticmethod
    def is_windows():
        """Verifica si es Windows"""
        return platform.system() == "Windows"
    
    @staticmethod
    def is_linux():
        """Verifica si es Linux"""
        return platform.system() == "Linux"
    
    @staticmethod
    def get_os_info():
        """Retorna información completa del SO"""
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "is_termux": SystemDetector.is_termux(),
            "python_version": sys.version
        }


class LogManager:
    """Gestiona logs detallados de descarga y errores"""
    
    def __init__(self, log_dir="./logs", level="INFO"):
        """
        Inicializa el gestor de logs
        
        Args:
            log_dir: Directorio donde se guardan los logs
            level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.level = getattr(logging, level, logging.INFO)
        
        # Crear nombres de archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.general_log = self.log_dir / f"general_{timestamp}.log"
        self.error_log = self.log_dir / f"errors_{timestamp}.log"
        self.download_log = self.log_dir / f"downloads_{timestamp}.log"
        
        # Configurar loggers
        self._setup_loggers()
    
    def _setup_loggers(self):
        """Configura los diferentes loggers"""
        # Logger general
        self.logger = logging.getLogger("multimedia_downloader")
        self.logger.setLevel(self.level)
        
        # Handler para archivo general
        general_handler = logging.FileHandler(self.general_log, encoding="utf-8")
        general_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
        )
        self.logger.addHandler(general_handler)
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter(
                f"{Fore.CYAN}[%(levelname)s]{Style.RESET_ALL} %(message)s"
            )
        )
        self.logger.addHandler(console_handler)
        
        # Logger de errores
        self.error_logger = logging.getLogger("errors")
        self.error_logger.setLevel(logging.ERROR)
        error_handler = logging.FileHandler(self.error_log, encoding="utf-8")
        error_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s - %(exc_info)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
        )
        self.error_logger.addHandler(error_handler)
        
        # Logger de descargas
        self.download_logger = logging.getLogger("downloads")
        self.download_logger.setLevel(logging.INFO)
        download_handler = logging.FileHandler(self.download_log, encoding="utf-8")
        download_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
        )
        self.download_logger.addHandler(download_handler)
    
    def info(self, msg):
        """Log nivel INFO"""
        self.logger.info(f"{Fore.BLUE}ℹ{Style.RESET_ALL} {msg}")
    
    def success(self, msg):
        """Log nivel SUCCESS (personalizado)"""
        self.logger.info(f"{Fore.GREEN}✓{Style.RESET_ALL} {msg}")
    
    def warning(self, msg):
        """Log nivel WARNING"""
        self.logger.warning(f"{Fore.YELLOW}⚠{Style.RESET_ALL} {msg}")
    
    def error(self, msg, exc=None):
        """Log nivel ERROR"""
        self.logger.error(f"{Fore.RED}✗{Style.RESET_ALL} {msg}")
        if exc:
            self.error_logger.exception(f"Error: {msg}")
    
    def debug(self, msg):
        """Log nivel DEBUG"""
        self.logger.debug(f"{Fore.MAGENTA}[DEBUG]{Style.RESET_ALL} {msg}")
    
    def log_download(self, url, filename, status, duration=None, size=None):
        """Registra información de descarga"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "url": url,
            "filename": filename,
            "status": status,
            "duration_seconds": duration,
            "size_bytes": size
        }
        self.download_logger.info(json.dumps(log_entry, ensure_ascii=False))
        return log_entry
    
    def get_log_paths(self):
        """Retorna las rutas de los archivos de log"""
        return {
            "general": str(self.general_log),
            "errors": str(self.error_log),
            "downloads": str(self.download_log)
        }


class MetadataExtractor:
    """Extrae metadatos de contenido multimedia"""
    
    @staticmethod
    def format_duration(seconds):
        """Convierte segundos a formato HH:MM:SS"""
        if seconds is None:
            return "N/A"
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    @staticmethod
    def format_size(bytes_size):
        """Convierte bytes a formato legible"""
        if bytes_size is None:
            return "N/A"
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024
        return f"{bytes_size:.2f} TB"
    
    @staticmethod
    def extract_from_info(info_dict):
        """
        Extrae metadatos relevantes de un diccionario de info de yt-dlp
        
        Args:
            info_dict: Diccionario con información del video
            
        Returns:
            dict: Metadatos formateados
        """
        if not info_dict:
            return None
        
        metadata = {
            "id": info_dict.get("id", "N/A"),
            "title": info_dict.get("title", "Sin título"),
            "uploader": info_dict.get("uploader", "N/A"),
            "upload_date": info_dict.get("upload_date", "N/A"),
            "duration": MetadataExtractor.format_duration(info_dict.get("duration")),
            "view_count": f"{info_dict.get('view_count', 0):,}",
            "like_count": f"{info_dict.get('like_count', 0):,}",
            "comment_count": f"{info_dict.get('comment_count', 0):,}",
            "description_length": len(info_dict.get("description", "")),
            "formats_available": len(info_dict.get("formats", [])),
            "ext": info_dict.get("ext", "N/A"),
            "width": info_dict.get("width", "N/A"),
            "height": info_dict.get("height", "N/A"),
            "fps": info_dict.get("fps", "N/A"),
        }
        
        return metadata
    
    @staticmethod
    def print_metadata_table(metadata):
        """Imprime metadatos en formato tabla"""
        if not metadata:
            print(f"{Fore.YELLOW}No hay metadatos disponibles{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 METADATOS DEL CONTENIDO{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        
        for key, value in metadata.items():
            print(f"{Fore.GREEN}{key.replace('_', ' ').title():<25}{Style.RESET_ALL} {value}")
        
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")


class FileManager:
    """Gestiona operaciones con archivos y rutas"""
    
    @staticmethod
    def create_directory(path):
        """Crea un directorio si no existe"""
        Path(path).mkdir(parents=True, exist_ok=True)
        return Path(path)
    
    @staticmethod
    def sanitize_filename(filename):
        """Sanitiza nombres de archivo para todos los SO"""
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename.strip()
    
    @staticmethod
    def read_urls_from_file(filepath):
        """
        Lee URLs desde un archivo de texto
        
        Args:
            filepath: Ruta del archivo
            
        Returns:
            list: Lista de URLs válidas
        """
        urls = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    url = line.strip()
                    if url and not url.startswith('#'):  # Ignora líneas vacías y comentarios
                        urls.append(url)
            return urls
        except FileNotFoundError:
            raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
        except Exception as e:
            raise Exception(f"Error al leer archivo: {e}")
    
    @staticmethod
    def get_file_size(filepath):
        """Obtiene el tamaño de un archivo"""
        try:
            return os.path.getsize(filepath)
        except:
            return None
    
    @staticmethod
    def file_exists(filepath):
        """Verifica si un archivo existe"""
        return Path(filepath).exists()


class URLValidator:
    """Valida URLs y detecta plataformas"""
    
    PLATFORM_PATTERNS = {
        "youtube": ["youtube.com", "youtu.be", "youtube-nocookie.com"],
        "tiktok": ["tiktok.com", "vm.tiktok.com", "vt.tiktok.com"],
        "instagram": ["instagram.com", "instagr.am"],
        "facebook": ["facebook.com", "fb.watch", "fb.com"],
        "x": ["twitter.com", "x.com"],
        "threads": ["threads.net"],
        "pinterest": ["pinterest.com", "pin.it"],
        "reddit": ["reddit.com"],
        "vimeo": ["vimeo.com"],
        "dailymotion": ["dailymotion.com"],
        "soundcloud": ["soundcloud.com"],
    }
    
    @staticmethod
    def is_valid_url(url):
        """Valida si una URL tiene formato correcto"""
        return url.startswith(("http://", "https://"))
    
    @staticmethod
    def detect_platform(url):
        """Detecta la plataforma de una URL"""
        url_lower = url.lower()
        for platform, patterns in URLValidator.PLATFORM_PATTERNS.items():
            for pattern in patterns:
                if pattern in url_lower:
                    return platform
        return "other"
    
    @staticmethod
    def get_output_dir(platform_name, output_dirs):
        """Obtiene el directorio de salida para una plataforma"""
        return output_dirs.get(platform_name, output_dirs.get("other"))


class ProgressTracker:
    """Rastrea el progreso de descargas y procesos"""
    
    def __init__(self, total_items):
        """Inicializa el rastreador"""
        self.total_items = total_items
        self.completed = 0
        self.failed = 0
        self.skipped = 0
        self.start_time = datetime.now()
    
    def increment_completed(self):
        """Incrementa el contador de completados"""
        self.completed += 1
    
    def increment_failed(self):
        """Incrementa el contador de errores"""
        self.failed += 1
    
    def increment_skipped(self):
        """Incrementa el contador de omitidos"""
        self.skipped += 1
    
    def get_progress(self):
        """Retorna el progreso actual"""
        return {
            "total": self.total_items,
            "completed": self.completed,
            "failed": self.failed,
            "skipped": self.skipped,
            "percentage": (self.completed / self.total_items * 100) if self.total_items > 0 else 0,
            "elapsed_time": (datetime.now() - self.start_time).total_seconds()
        }
    
    def print_summary(self):
        """Imprime un resumen del progreso"""
        progress = self.get_progress()
        elapsed = int(progress["elapsed_time"])
        
        print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📈 RESUMEN DE DESCARGA{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ Completados: {progress['completed']}{Style.RESET_ALL}")
        print(f"{Fore.RED}✗ Errores: {progress['failed']}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⊘ Omitidos: {progress['skipped']}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}📊 Progreso: {progress['percentage']:.1f}%{Style.RESET_ALL}")
        print(f"{Fore.BLUE}⏱ Tiempo total: {elapsed}s{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")
