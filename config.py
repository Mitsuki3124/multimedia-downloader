"""
Módulo de configuración para multimedia-downloader
- Carga de configuración desde YAML
- Validación de parámetros
- Merging de argumentos CLI con configuración
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Gestiona la configuración de la aplicación"""
    
    DEFAULT_CONFIG_PATH = "config.yaml"
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Inicializa el gestor de configuración
        
        Args:
            config_path: Ruta personalizada al archivo de configuración
        """
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self.config = self._load_config()
        self._validate_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Carga la configuración desde YAML"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                f"Archivo de configuración no encontrado: {self.config_path}"
            )
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            if config is None:
                raise ValueError("El archivo de configuración está vacío")
            
            return config
        except yaml.YAMLError as e:
            raise ValueError(f"Error al parsear YAML: {e}")
        except Exception as e:
            raise Exception(f"Error al cargar configuración: {e}")
    
    def _validate_config(self):
        """Valida que la configuración contenga las secciones necesarias"""
        required_sections = [
            'output_dirs', 'video', 'audio', 'download', 'logging', 'platforms'
        ]
        
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Configuración incompleta: falta sección '{section}'")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de configuración con soporte para notación de punto
        
        Args:
            key: Clave de configuración (ej: "video.format", "download.max_retries")
            default: Valor por defecto si la clave no existe
            
        Returns:
            Valor de configuración
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        Establece un valor de configuración con soporte para notación de punto
        
        Args:
            key: Clave de configuración (ej: "video.format")
            value: Nuevo valor
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_output_dir(self, platform: str) -> str:
        """
        Obtiene el directorio de salida para una plataforma
        
        Args:
            platform: Nombre de la plataforma
            
        Returns:
            Ruta del directorio de salida
        """
        dirs = self.config.get('output_dirs', {})
        output_dir = dirs.get(platform, dirs.get('other', 'downloads'))
        
        # Crear directorio si no existe
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        return output_dir
    
    def get_yt_dlp_opts(self, platform: str = "youtube", 
                        format_type: str = "video") -> Dict[str, Any]:
        """
        Genera opciones de yt-dlp basadas en la configuración
        
        Args:
            platform: Nombre de la plataforma
            format_type: Tipo de formato ("video", "audio", "image")
            
        Returns:
            Diccionario con opciones para yt-dlp
        """
        opts = {
            'quiet': False,
            'no_warnings': False,
            'user_agent': self.config.get('user_agent'),
        }
        
        # Configuración de descarga
        download_cfg = self.config.get('download', {})
        opts['socket_timeout'] = download_cfg.get('socket_timeout', 30)
        opts['retries'] = download_cfg.get('max_retries', 3)
        opts['sleep_interval'] = download_cfg.get('sleep_interval', 2)
        opts['http_chunk_size'] = 10485760  # 10MB
        
        # SSL
        if not self.config.get('ssl_verify', True):
            opts['check_formats'] = False
        
        # Proxy
        proxy_cfg = self.config.get('proxy', {})
        if proxy_cfg.get('enabled'):
            if proxy_cfg.get('http'):
                opts['proxy'] = proxy_cfg.get('http')
        
        # Output template
        naming_cfg = self.config.get('naming', {})
        pattern = naming_cfg.get('pattern', '%(title)s.%(ext)s')
        output_dir = self.get_output_dir(platform)
        opts['outtmpl'] = os.path.join(output_dir, pattern)
        
        # Configuración por tipo de formato
        if format_type == "video":
            video_cfg = self.config.get('video', {})
            format_str = self._build_format_string(video_cfg.get('format', 'best'))
            opts['format'] = format_str
            opts['postprocessors'] = []
        
        elif format_type == "audio":
            audio_cfg = self.config.get('audio', {})
            opts['format'] = 'bestaudio/best'
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_cfg.get('format', 'mp3'),
                'preferredquality': audio_cfg.get('quality', '192'),
            }]
            opts['outtmpl'] = os.path.join(output_dir, 
                                          naming_cfg.get('pattern', '%(title)s.%(ext)s'))
        
        elif format_type == "image":
            image_cfg = self.config.get('image', {})
            opts['format'] = f"bestvideo[ext={image_cfg.get('format', 'jpg')}]"
        
        # Metadatos y subtítulos
        metadata_cfg = self.config.get('metadata', {})
        if metadata_cfg.get('download_subtitles'):
            opts['writesubtitles'] = True
            opts['subtitle_langs'] = [metadata_cfg.get('subtitle_lang', 'es')]
        
        opts['writeinfojson'] = metadata_cfg.get('extract', True)
        opts['writethumbnail'] = True
        
        return opts
    
    def _build_format_string(self, format_quality: str) -> str:
        """
        Construye una cadena de formato para yt-dlp
        
        Args:
            format_quality: Calidad deseada (best, 1080p, 720p, etc.)
            
        Returns:
            Cadena de formato de yt-dlp
        """
        quality_map = {
            'best': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            '1080p': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]',
            '720p': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]',
            '480p': 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]',
            '360p': 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]',
            'audio_only': 'bestaudio[ext=m4a]/bestaudio',
        }
        
        return quality_map.get(format_quality, quality_map['best'])
    
    def merge_cli_args(self, args: Dict[str, Any]):
        """
        Fusiona argumentos de CLI con configuración existente
        
        Args:
            args: Diccionario con argumentos CLI
        """
        for key, value in args.items():
            if value is not None:
                self.set(key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Retorna toda la configuración como diccionario"""
        return self.config.copy()
    
    def save_to_file(self, filepath: str):
        """
        Guarda la configuración actual a un archivo YAML
        
        Args:
            filepath: Ruta del archivo de destino
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False)
        except Exception as e:
            raise Exception(f"Error al guardar configuración: {e}")
    
    def print_summary(self):
        """Imprime un resumen de la configuración actual"""
        print("\n" + "="*60)
        print("📋 CONFIGURACIÓN ACTIVA")
        print("="*60)
        print(f"Video Format: {self.get('video.format')}")
        print(f"Audio Format: {self.get('audio.format')}")
        print(f"Output Base: {self.get('output_dirs.base')}")
        print(f"Max Retries: {self.get('download.max_retries')}")
        print(f"Timeout: {self.get('download.timeout')}s")
        print(f"Logging Level: {self.get('logging.level')}")
        print("="*60 + "\n")


class ConfigValidator:
    """Valida valores de configuración"""
    
    VALID_VIDEO_FORMATS = ['best', '1080p', '720p', '480p', '360p', 'audio_only']
    VALID_AUDIO_FORMATS = ['mp3', 'm4a', 'aac', 'opus', 'vorbis', 'wav']
    VALID_IMAGE_FORMATS = ['jpg', 'png', 'webp']
    VALID_LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    VALID_PLATFORMS = ['youtube', 'tiktok', 'instagram', 'facebook', 'x', 
                       'threads', 'pinterest', 'reddit', 'vimeo', 'soundcloud']
    
    @staticmethod
    def validate_video_format(format_str: str) -> bool:
        """Valida formato de video"""
        return format_str in ConfigValidator.VALID_VIDEO_FORMATS
    
    @staticmethod
    def validate_audio_format(format_str: str) -> bool:
        """Valida formato de audio"""
        return format_str in ConfigValidator.VALID_AUDIO_FORMATS
    
    @staticmethod
    def validate_log_level(level: str) -> bool:
        """Valida nivel de logging"""
        return level in ConfigValidator.VALID_LOG_LEVELS
    
    @staticmethod
    def validate_quality(quality: int) -> bool:
        """Valida calidad de audio (kbps)"""
        valid_qualities = [128, 192, 256, 320]
        return quality in valid_qualities
    
    @staticmethod
    def validate_retries(retries: int) -> bool:
        """Valida número de reintentos"""
        return 0 <= retries <= 10
    
    @staticmethod
    def validate_timeout(timeout: int) -> bool:
        """Valida timeout en segundos"""
        return 5 <= timeout <= 300
