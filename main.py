#!/usr/bin/env python3
"""
Multimedia Downloader - CLI Professional
Herramienta para descargar contenido multimedia desde múltiples plataformas
Compatible con: YouTube, TikTok, Instagram, Facebook, X, Threads, Pinterest, Reddit, Vimeo, SoundCloud, etc.
Compatible con: Windows, Linux, macOS, Termux
"""

import sys
import os
import argparse
import json
from pathlib import Path
from typing import Optional, List
from datetime import datetime

# Importar módulos locales
from config import ConfigManager, ConfigValidator
from utils import (
    LogManager, SystemDetector, FileManager, MetadataExtractor, URLValidator
)
from platforms import PlatformDetector, PlatformRequirements, Platform
from downloader import MediaDownloader, PlaylistProcessor, BulkProcessor

# Información de versión
VERSION = "1.0.0"
AUTHOR = "Kaelthar (ThornEldritch)"


class CLI:
    """Interfaz de línea de comandos principal"""
    
    def __init__(self):
        """Inicializa la CLI"""
        self.parser = self._build_parser()
        self.config = None
        self.logger = None
        self.downloader = None
    
    def _build_parser(self) -> argparse.ArgumentParser:
        """Construye el parser de argumentos"""
        parser = argparse.ArgumentParser(
            prog="multimedia-downloader",
            description=f"Descargador Multimedia Profesional v{VERSION}",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Ejemplos de uso:

  # Descargar un video de YouTube en 1080p
  python3 main.py -u "https://youtube.com/watch?v=..." --format 1080p

  # Descargar audio de un video
  python3 main.py -u "https://youtube.com/watch?v=..." --audio --quality 320

  # Descargar desde un archivo con múltiples URLs
  python3 main.py -f urls.txt --format best --audio

  # Descargar una playlist completa
  python3 main.py -u "https://youtube.com/playlist?list=..." --playlist

  # Ver información de una URL sin descargar
  python3 main.py -u "https://youtube.com/watch?v=..." --info

  # Usar configuración personalizada
  python3 main.py -u "https://..." --config custom_config.yaml
            """
        )
        
        # Argumentos obligatorios
        input_group = parser.add_mutually_exclusive_group(required=True)
        input_group.add_argument(
            '-u', '--url',
            type=str,
            help='URL individual para descargar'
        )
        input_group.add_argument(
            '-f', '--file',
            type=str,
            help='Archivo de texto con URLs (una por línea)'
        )
        
        # Opciones de formato
        format_group = parser.add_argument_group('Opciones de Formato')
        format_group.add_argument(
            '--format',
            choices=['best', '1080p', '720p', '480p', '360p', 'audio_only'],
            default='best',
            help='Calidad de video (defecto: best)'
        )
        format_group.add_argument(
            '--audio',
            action='store_true',
            help='Extrae solo el audio'
        )
        format_group.add_argument(
            '--audio-format',
            choices=['mp3', 'm4a', 'aac', 'opus', 'vorbis', 'wav'],
            default='mp3',
            help='Formato de audio (defecto: mp3)'
        )
        format_group.add_argument(
            '--quality',
            type=int,
            choices=[128, 192, 256, 320],
            help='Calidad de audio en kbps'
        )
        
        # Opciones de descarga
        download_group = parser.add_argument_group('Opciones de Descarga')
        download_group.add_argument(
            '-o', '--output',
            type=str,
            help='Directorio de salida personalizado'
        )
        download_group.add_argument(
            '--playlist',
            action='store_true',
            help='Descarga playlist completa'
        )
        download_group.add_argument(
            '--max-retries',
            type=int,
            default=3,
            help='Máximo número de reintentos (defecto: 3)'
        )
        download_group.add_argument(
            '--timeout',
            type=int,
            default=30,
            help='Timeout en segundos (defecto: 30)'
        )
        
        # Opciones de información
        info_group = parser.add_argument_group('Opciones de Información')
        info_group.add_argument(
            '--info',
            action='store_true',
            help='Muestra información sin descargar'
        )
        info_group.add_argument(
            '--platform-info',
            type=str,
            choices=['youtube', 'tiktok', 'instagram', 'facebook', 'x', 
                    'threads', 'pinterest', 'reddit', 'vimeo', 'soundcloud'],
            help='Muestra información de una plataforma'
        )
        
        # Opciones de configuración
        config_group = parser.add_argument_group('Configuración')
        config_group.add_argument(
            '--config',
            type=str,
            help='Ruta a archivo de configuración personalizado'
        )
        config_group.add_argument(
            '--save-config',
            type=str,
            help='Guarda la configuración actual a un archivo'
        )
        
        # Opciones generales
        parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Modo verbose con más detalles'
        )
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Modo debug con información detallada'
        )
        parser.add_argument(
            '--log-dir',
            type=str,
            default='./logs',
            help='Directorio para logs (defecto: ./logs)'
        )
        parser.add_argument(
            '--version',
            action='version',
            version=f'%(prog)s {VERSION}'
        )
        parser.add_argument(
            '--system-info',
            action='store_true',
            help='Muestra información del sistema'
        )
        
        return parser
    
    def run(self, args: Optional[List[str]] = None):
        """Ejecuta la aplicación"""
        try:
            parsed_args = self.parser.parse_args(args)
            
            # Inicializar configuración y logger
            self._initialize(parsed_args)
            
            # Mostrar información del sistema si se solicita
            if parsed_args.system_info:
                self._show_system_info()
                return 0
            
            # Mostrar información de plataforma si se solicita
            if parsed_args.platform_info:
                self._show_platform_info(parsed_args.platform_info)
                return 0
            
            # Mostrar información sin descargar
            if parsed_args.info:
                return self._show_info(parsed_args)
            
            # Ejecutar descarga
            return self._execute_download(parsed_args)
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Operación cancelada por el usuario{Style.RESET_ALL}")
            return 130
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            return 1
    
    def _initialize(self, args):
        """Inicializa configuración y logger"""
        try:
            # Cargar configuración
            config_path = args.config or "config.yaml"
            self.config = ConfigManager(config_path)
            
            # Determinar nivel de logging
            log_level = "DEBUG" if args.debug else ("INFO" if args.verbose else "INFO")
            
            # Inicializar logger
            self.logger = LogManager(args.log_dir, log_level)
            
            # Crear descargador
            self.downloader = MediaDownloader(self.config, self.logger)
            
            # Mostrar información de inicialización
            self.logger.info(f"🚀 Multimedia Downloader v{VERSION}")
            self.logger.info(f"Autor: {AUTHOR}")
            self.logger.debug(f"SO: {SystemDetector.get_os()}")
            
            if SystemDetector.is_termux():
                self.logger.info("✓ Ejecutando en Termux")
            
        except Exception as e:
            print(f"{Fore.RED}Error de inicialización: {e}{Style.RESET_ALL}")
            raise
    
    def _show_system_info(self):
        """Muestra información del sistema"""
        info = SystemDetector.get_os_info()
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 INFORMACIÓN DEL SISTEMA{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        for key, value in info.items():
            print(f"{Fore.GREEN}{key.replace('_', ' ').title():<20}{Style.RESET_ALL} {value}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    def _show_platform_info(self, platform_name: str):
        """Muestra información de una plataforma"""
        platform = Platform[platform_name.upper()]
        PlatformRequirements.print_platform_info(platform)
    
    def _show_info(self, args) -> int:
        """Muestra información sin descargar"""
        try:
            if args.url:
                return self._show_url_info(args.url)
            else:
                self.logger.error("Se requiere URL para mostrar información")
                return 1
        except Exception as e:
            self.logger.error(f"Error: {e}", exc=e)
            return 1
    
    def _show_url_info(self, url: str) -> int:
        """Muestra información de una URL"""
        self.logger.info(f"Extrayendo información de: {url}")
        
        platform = PlatformDetector.detect_platform(url)
        self.logger.info(f"Plataforma detectada: {platform.value}")
        
        # Mostrar información de la plataforma
        platform_info = PlatformDetector.get_platform_info(platform)
        if platform_info:
            print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}📱 {platform_info.friendly_name}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(f"Soporta Video: {'✓' if platform_info.supports_video else '✗'}")
            print(f"Soporta Audio: {'✓' if platform_info.supports_audio else '✗'}")
            print(f"Requiere Autenticación: {'✓' if platform_info.requires_auth else '✗'}")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        # Intentar extraer metadatos
        try:
            import yt_dlp
            yt_dlp_opts = self.config.get_yt_dlp_opts(platform.value, "video")
            yt_dlp_opts['skip_download'] = True
            yt_dlp_opts['quiet'] = False
            
            with yt_dlp.YoutubeDL(yt_dlp_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            
            metadata = MetadataExtractor.extract_from_info(info)
            MetadataExtractor.print_metadata_table(metadata)
            
            return 0
        
        except Exception as e:
            self.logger.warning(f"No se pudo extraer metadatos: {e}")
            return 1
    
    def _execute_download(self, args) -> int:
        """Ejecuta la descarga"""
        try:
            # Determinar tipo de formato
            format_type = "audio" if args.audio else "video"
            quality = args.format if not args.audio else None
            
            # URL única
            if args.url:
                self.logger.info(f"Descargando: {args.url}")
                
                if args.playlist:
                    playlist_processor = PlaylistProcessor(self.downloader, self.logger)
                    results = playlist_processor.download_playlist(
                        args.url, format_type, quality
                    )
                else:
                    success, message, metadata = self.downloader.download_single(
                        args.url, format_type, quality
                    )
                    results = {"success": success, "message": message}
            
            # Archivo con URLs
            elif args.file:
                self.logger.info(f"Leyendo URLs de: {args.file}")
                results = self.downloader.download_from_file(args.file, format_type, quality)
            
            # Guardar configuración si se solicita
            if args.save_config:
                self.config.save_to_file(args.save_config)
                self.logger.success(f"Configuración guardada: {args.save_config}")
            
            # Mostrar resumen
            print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}✓ Operación completada{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
            
            return 0
        
        except Exception as e:
            self.logger.error(f"Error en descarga: {e}", exc=e)
            return 1


def main():
    """Función principal"""
    cli = CLI()
    sys.exit(cli.run())


if __name__ == "__main__":
    try:
        # Importar colorama
        from colorama import Fore, Style, init
        init(autoreset=True)
    except ImportError:
        print("Error: colorama no está instalado. Ejecuta: pip install -r requirements.txt")
        sys.exit(1)
    
    main()
