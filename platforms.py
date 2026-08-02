"""
Módulo de gestión de plataformas multimedia
- Detección automática de plataformas
- Características específicas por plataforma
- Opciones de descarga personalizadas
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from urllib.parse import urlparse


class Platform(Enum):
    """Enumeración de plataformas soportadas"""
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    X = "x"  # Twitter
    THREADS = "threads"
    PINTEREST = "pinterest"
    REDDIT = "reddit"
    VIMEO = "vimeo"
    DAILYMOTION = "dailymotion"
    SOUNDCLOUD = "soundcloud"
    OTHER = "other"


@dataclass
class PlatformInfo:
    """Información sobre una plataforma"""
    name: str
    friendly_name: str
    domains: List[str]
    supports_video: bool
    supports_audio: bool
    supports_playlist: bool
    requires_auth: bool
    age_restriction: bool
    formats: List[str]
    description: str


class PlatformDetector:
    """Detecta y gestiona plataformas multimedia"""
    
    PLATFORM_REGISTRY = {
        Platform.YOUTUBE: PlatformInfo(
            name="youtube",
            friendly_name="YouTube",
            domains=["youtube.com", "youtu.be", "youtube-nocookie.com"],
            supports_video=True,
            supports_audio=True,
            supports_playlist=True,
            requires_auth=False,
            age_restriction=True,
            formats=["mp4", "webm", "mkv"],
            description="Plataforma de video compartido más grande del mundo"
        ),
        
        Platform.TIKTOK: PlatformInfo(
            name="tiktok",
            friendly_name="TikTok",
            domains=["tiktok.com", "vm.tiktok.com", "vt.tiktok.com"],
            supports_video=True,
            supports_audio=True,
            supports_playlist=False,
            requires_auth=False,
            age_restriction=False,
            formats=["mp4"],
            description="Red social de videos cortos"
        ),
        
        Platform.INSTAGRAM: PlatformInfo(
            name="instagram",
            friendly_name="Instagram",
            domains=["instagram.com", "instagr.am"],
            supports_video=True,
            supports_audio=False,
            supports_playlist=False,
            requires_auth=True,
            age_restriction=False,
            formats=["mp4", "jpg"],
            description="Red social de fotos y videos"
        ),
        
        Platform.FACEBOOK: PlatformInfo(
            name="facebook",
            friendly_name="Facebook",
            domains=["facebook.com", "fb.watch", "fb.com"],
            supports_video=True,
            supports_audio=False,
            supports_playlist=False,
            requires_auth=True,
            age_restriction=False,
            formats=["mp4"],
            description="Red social con contenido multimedia"
        ),
        
        Platform.X: PlatformInfo(
            name="x",
            friendly_name="X (Twitter)",
            domains=["twitter.com", "x.com"],
            supports_video=True,
            supports_audio=False,
            supports_playlist=False,
            requires_auth=False,
            age_restriction=False,
            formats=["mp4"],
            description="Red social de publicaciones cortas"
        ),
        
        Platform.THREADS: PlatformInfo(
            name="threads",
            friendly_name="Threads",
            domains=["threads.net"],
            supports_video=True,
            supports_audio=False,
            supports_playlist=False,
            requires_auth=True,
            age_restriction=False,
            formats=["mp4"],
            description="Red social de Meta similar a Twitter"
        ),
        
        Platform.PINTEREST: PlatformInfo(
            name="pinterest",
            friendly_name="Pinterest",
            domains=["pinterest.com", "pin.it"],
            supports_video=True,
            supports_audio=False,
            supports_playlist=False,
            requires_auth=False,
            age_restriction=False,
            formats=["mp4", "jpg", "png"],
            description="Red social de descubrimiento visual"
        ),
        
        Platform.REDDIT: PlatformInfo(
            name="reddit",
            friendly_name="Reddit",
            domains=["reddit.com"],
            supports_video=True,
            supports_audio=True,
            supports_playlist=False,
            requires_auth=False,
            age_restriction=False,
            formats=["mp4", "webm"],
            description="Agregador de contenido y comunidades"
        ),
        
        Platform.VIMEO: PlatformInfo(
            name="vimeo",
            friendly_name="Vimeo",
            domains=["vimeo.com"],
            supports_video=True,
            supports_audio=False,
            supports_playlist=False,
            requires_auth=False,
            age_restriction=False,
            formats=["mp4"],
            description="Plataforma de alojamiento de videos profesionales"
        ),
        
        Platform.DAILYMOTION: PlatformInfo(
            name="dailymotion",
            friendly_name="Dailymotion",
            domains=["dailymotion.com"],
            supports_video=True,
            supports_audio=False,
            supports_playlist=True,
            requires_auth=False,
            age_restriction=False,
            formats=["mp4"],
            description="Plataforma de streaming de videos"
        ),
        
        Platform.SOUNDCLOUD: PlatformInfo(
            name="soundcloud",
            friendly_name="SoundCloud",
            domains=["soundcloud.com"],
            supports_video=False,
            supports_audio=True,
            supports_playlist=True,
            requires_auth=False,
            age_restriction=False,
            formats=["mp3", "m4a"],
            description="Plataforma de distribución de música y audio"
        ),
    }
    
    @staticmethod
    def detect_platform(url: str) -> Platform:
        """
        Detecta la plataforma de una URL
        
        Args:
            url: URL a analizar
            
        Returns:
            Platform: Plataforma detectada
        """
        if not url:
            return Platform.OTHER
        
        url_lower = url.lower()
        
        # Búsqueda en el registro de plataformas
        for platform, info in PlatformDetector.PLATFORM_REGISTRY.items():
            for domain in info.domains:
                if domain in url_lower:
                    return platform
        
        return Platform.OTHER
    
    @staticmethod
    def get_platform_info(platform: Platform) -> Optional[PlatformInfo]:
        """
        Obtiene información sobre una plataforma
        
        Args:
            platform: Platform enum
            
        Returns:
            PlatformInfo o None
        """
        return PlatformDetector.PLATFORM_REGISTRY.get(platform)
    
    @staticmethod
    def get_output_dir(platform: Platform, base_dir: str = "downloads") -> str:
        """
        Obtiene el directorio de salida para una plataforma
        
        Args:
            platform: Platform enum
            base_dir: Directorio base
            
        Returns:
            Ruta del directorio
        """
        platform_name = platform.value if isinstance(platform, Platform) else platform
        return f"{base_dir}/{platform_name.title()}"
    
    @staticmethod
    def supports_format(platform: Platform, format_type: str) -> bool:
        """
        Verifica si una plataforma soporta un tipo de formato
        
        Args:
            platform: Platform enum
            format_type: Tipo de formato (video, audio, image)
            
        Returns:
            bool: Si soporta o no
        """
        info = PlatformDetector.get_platform_info(platform)
        if not info:
            return False
        
        if format_type.lower() == "video":
            return info.supports_video
        elif format_type.lower() == "audio":
            return info.supports_audio
        elif format_type.lower() == "image":
            return "jpg" in info.formats or "png" in info.formats
        
        return False


class PlatformRequirements:
    """Gestiona requisitos y advertencias por plataforma"""
    
    WARNINGS = {
        Platform.INSTAGRAM: [
            "⚠️ Puede requerir credenciales de usuario",
            "⚠️ El contenido privado no es accesible",
            "⚠️ Rate limiting posible",
        ],
        Platform.FACEBOOK: [
            "⚠️ Requiere autenticación para algunos contenidos",
            "⚠️ Contenido privado no es accesible",
            "⚠️ Algunos videos pueden estar protegidos",
        ],
        Platform.TIKTOK: [
            "⚠️ Descarga sin watermark puede no estar disponible",
            "⚠️ Rate limiting agresivo",
            "⚠️ Requiere espera entre descargas",
        ],
        Platform.X: [
            "⚠️ Videos privados requieren autenticación",
            "⚠️ Algunos contenidos pueden estar limitados",
        ],
        Platform.THREADS: [
            "⚠️ Plataforma relativamente nueva",
            "⚠️ Puede requerir actualizaciones frecuentes",
        ],
    }
    
    REQUIREMENTS = {
        Platform.INSTAGRAM: ["ffmpeg"],
        Platform.FACEBOOK: ["ffmpeg"],
        Platform.TIKTOK: ["ffmpeg"],
        Platform.SOUNDCLOUD: ["ffmpeg"],
        Platform.YOUTUBE: ["ffmpeg"],
    }
    
    @staticmethod
    def get_warnings(platform: Platform) -> List[str]:
        """Obtiene advertencias para una plataforma"""
        return PlatformRequirements.WARNINGS.get(platform, [])
    
    @staticmethod
    def get_requirements(platform: Platform) -> List[str]:
        """Obtiene requisitos para una plataforma"""
        return PlatformRequirements.REQUIREMENTS.get(platform, [])
    
    @staticmethod
    def print_platform_info(platform: Platform):
        """Imprime información detallada de una plataforma"""
        info = PlatformDetector.get_platform_info(platform)
        if not info:
            return
        
        print(f"\n{'='*60}")
        print(f"📱 {info.friendly_name}")
        print(f"{'='*60}")
        print(f"Descripción: {info.description}")
        print(f"Video: {'✓' if info.supports_video else '✗'}")
        print(f"Audio: {'✓' if info.supports_audio else '✗'}")
        print(f"Playlists: {'✓' if info.supports_playlist else '✗'}")
        print(f"Requiere Autenticación: {'✓' if info.requires_auth else '✗'}")
        print(f"Restricción de Edad: {'✓' if info.age_restriction else '✗'}")
        print(f"Formatos: {', '.join(info.formats)}")
        
        warnings = PlatformRequirements.get_warnings(platform)
        if warnings:
            print("\nAdvertencias:")
            for warning in warnings:
                print(f"  {warning}")
        
        requirements = PlatformRequirements.get_requirements(platform)
        if requirements:
            print(f"\nRequisitos: {', '.join(requirements)}")
        
        print(f"{'='*60}\n")


class URLExtractor:
    """Extrae información útil de URLs"""
    
    @staticmethod
    def extract_video_id(url: str, platform: Platform) -> Optional[str]:
        """
        Extrae el ID del video según la plataforma
        
        Args:
            url: URL del video
            platform: Platform detectada
            
        Returns:
            ID del video o None
        """
        if platform == Platform.YOUTUBE:
            if 'youtu.be' in url:
                return url.split('/')[-1].split('?')[0]
            elif 'youtube.com' in url:
                parts = url.split('v=')
                if len(parts) > 1:
                    return parts[1].split('&')[0]
        
        elif platform == Platform.TIKTOK:
            if '/video/' in url:
                return url.split('/video/')[1].split('?')[0]
        
        elif platform == Platform.INSTAGRAM:
            if '/p/' in url or '/reel/' in url:
                parts = url.split('/')
                return parts[-2]
        
        elif platform == Platform.VIMEO:
            if 'vimeo.com/' in url:
                return url.split('/')[-1].split('?')[0]
        
        return None
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """Normaliza una URL removiendo parámetros innecesarios"""
        if not url:
            return url
        
        # Remover parámetros de tracking
        url = url.split('?')[0]
        url = url.rstrip('/')
        
        # Asegurar que tenga protocolo
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        return url
