#!/bin/bash

# Script de instalación para Multimedia Downloader
# Compatible con: Termux, Linux (Ubuntu, Debian, Fedora, Arch)
# Autor: Kaelthar (ThornEldritch)

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir con colores
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Detectar sistema operativo
detect_os() {
    if [ -f "/data/data/com.termux" ] || [ -d "$PREFIX/tmp" ]; then
        echo "termux"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            echo "$ID"
        else
            echo "linux"
        fi
    else
        echo "unsupported"
    fi
}

# Detectar gestor de paquetes
detect_package_manager() {
    local os=$1
    
    case $os in
        termux)
            echo "apt"
            ;;
        ubuntu|debian)
            echo "apt"
            ;;
        fedora|rhel|centos)
            echo "dnf"
            ;;
        arch|manjaro)
            echo "pacman"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

# Instalar dependencias del sistema
install_system_dependencies() {
    local os=$1
    local pm=$2
    
    print_info "Instalando dependencias del sistema..."
    
    case $pm in
        apt)
            sudo apt update
            sudo apt install -y python3 python3-pip python3-dev ffmpeg git curl
            ;;
        dnf)
            sudo dnf install -y python3 python3-pip python3-devel ffmpeg git curl
            ;;
        pacman)
            sudo pacman -Syu --noconfirm
            sudo pacman -S --noconfirm python pip ffmpeg git curl
            ;;
        *)
            print_warning "Gestor de paquetes no reconocido. Instala manualmente:"
            print_warning "  - Python 3.7+"
            print_warning "  - pip"
            print_warning "  - ffmpeg"
            print_warning "  - git"
            ;;
    esac
}

# Instalar en Termux
install_termux() {
    print_info "Detectado: Termux"
    
    print_info "Actualizando pkg..."
    pkg update
    pkg upgrade -y
    
    print_info "Instalando dependencias..."
    pkg install -y python pip ffmpeg git
    
    print_info "Instalando paquetes Python..."
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
    
    print_success "Instalación en Termux completada"
    
    print_info "Comandos útiles para Termux:"
    echo "  • Ver logs: cat ./logs/general*.log"
    echo "  • Ejecutar: python3 main.py --help"
}

# Instalar en Linux genérico
install_linux() {
    local distro=$1
    local pm=$2
    
    print_info "Detectado: Linux ($distro)"
    
    # Instalar dependencias del sistema
    install_system_dependencies "$distro" "$pm"
    
    # Instalar paquetes Python
    print_info "Instalando paquetes Python..."
    pip3 install --upgrade pip setuptools wheel
    pip3 install -r requirements.txt
    
    print_success "Instalación completada"
}

# Función principal
main() {
    clear
    echo -e "${BLUE}"
    cat << "EOF"
╔════════════════════════════════════════════════════════════╗
║     Multimedia Downloader - Script de Instalación         ║
║     Compatible: Termux, Linux (Ubuntu, Debian, Fedora)    ║
║     Autor: Kaelthar (ThornEldritch)                       ║
╚════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    
    # Detectar SO
    os=$(detect_os)
    
    if [ "$os" = "unsupported" ]; then
        print_error "Sistema operativo no soportado"
        print_info "Sistemas soportados: Termux, Ubuntu, Debian, Fedora, Arch, etc."
        exit 1
    fi
    
    print_success "Sistema operativo detectado: $os"
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        print_warning "Python3 no encontrado"
        
        if [ "$os" = "termux" ]; then
            install_termux
        else
            pm=$(detect_package_manager "$os")
            install_linux "$os" "$pm"
        fi
    else
        python_version=$(python3 --version 2>&1 | awk '{print $2}')
        print_success "Python3 encontrado: $python_version"
        
        # Instalar paquetes Python
        if [ "$os" = "termux" ]; then
            install_termux
        else
            pm=$(detect_package_manager "$os")
            install_linux "$os" "$pm"
        fi
    fi
    
    # Crear directorios necesarios
    print_info "Creando directorios..."
    mkdir -p downloads logs
    mkdir -p downloads/{YouTube,TikTok,Instagram,Facebook,X,Threads,Pinterest,Reddit,Vimeo,SoundCloud,Otros}
    
    # Hacer ejecutable main.py
    chmod +x main.py
    
    # Crear alias (opcional)
    if [ -f "$HOME/.bashrc" ]; then
        if ! grep -q "alias mdl=" "$HOME/.bashrc"; then
            print_info "Agregando alias al .bashrc..."
            echo "alias mdl='python3 $PWD/main.py'" >> "$HOME/.bashrc"
            source "$HOME/.bashrc"
            print_success "Alias 'mdl' creado"
        fi
    fi
    
    print_success "═════════════════════════════════════════════════════════"
    print_success "¡Instalación completada exitosamente!"
    print_success "═════════════════════════════════════════════════════════"
    
    echo ""
    print_info "Primeros pasos:"
    echo "  1. Ver ayuda:        python3 main.py --help"
    echo "  2. Ver info sistema: python3 main.py --system-info"
    echo "  3. Descargar video:  python3 main.py -u 'https://...' --format best"
    echo "  4. Extraer audio:    python3 main.py -u 'https://...' --audio"
    echo ""
    
    if [ -f "$HOME/.bashrc" ]; then
        print_info "También puedes usar: mdl --help"
    fi
    
    echo ""
}

# Ejecutar
main "$@"
