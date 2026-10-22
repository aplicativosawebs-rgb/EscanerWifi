# =======================================================
# librerias.py — Instalador multiplataforma PROFESIONAL
# Windows + Linux + Kali Linux
# Manejo correcto de venv, rutas con espacios y sudo
# =======================================================

import subprocess
import sys
import platform
import os
import shutil


# -------------------------------------------------------
# LIBRERÍAS REQUERIDAS
# -------------------------------------------------------

DEPENDENCIAS = [

    # --- UI ---
    "PyQt6",

    # --- Red y escaneo ---
    "scapy",
    "requests",
    "psutil",
    "mac-vendor-lookup",
    "pywifi",
    "ifaddr",
    "urllib3",
    "certifi",
    "chardet",
    "idna",
    "python-nmap",
    "netifaces",
    "speedtest-cli",

    # --- Utilidades generales ---
    "colorama",
    "setuptools",
    "wheel",
    "future",
    "python-dotenv",
    "qt-material",

    # --- IA / Machine Learning ---
    "scikit-learn",
    "numpy",
    "pandas",
    "matplotlib",

    # --- PDF / Documentos ---
    "pdfplumber",
    "PyMuPDF",
    "reportlab",
    "fpdf",
    "weasyprint",
    "pypdf",
    "PyPDF2",
    "python-docx",
]


# -------------------------------------------------------
# HERRAMIENTAS DE LINUX
# -------------------------------------------------------

LINUX_TOOLS = [
    "nmap",
    "net-tools",
    "iproute2",
    "arp-scan"
]


# -------------------------------------------------------
# DETECCIÓN DEL SISTEMA
# -------------------------------------------------------

SO = platform.system()

ES_LINUX = SO == "Linux"
ES_WINDOWS = SO == "Windows"


# -------------------------------------------------------
# RUTAS DEL ENTORNO VIRTUAL
# -------------------------------------------------------

VENV_DIR = os.path.abspath("venv")

if ES_WINDOWS:
    VENV_PY = os.path.join(VENV_DIR, "Scripts", "python.exe")
    VENV_PIP = os.path.join(VENV_DIR, "Scripts", "pip.exe")
else:
    VENV_PY = os.path.join(VENV_DIR, "bin", "python")
    VENV_PIP = os.path.join(VENV_DIR, "bin", "pip")


# -------------------------------------------------------
# EJECUTAR COMANDOS
# -------------------------------------------------------

def run(cmd, check=True):
    """
    Ejecuta un comando de forma segura.

    cmd debe ser una lista:
        ["python", "-m", "pip", "install", "PyQt6"]

    Esto evita problemas con rutas que contienen espacios.
    """

    try:
        print(f"\n> {' '.join(map(str, cmd))}")

        subprocess.run(
            cmd,
            check=check
        )

        return True

    except subprocess.CalledProcessError as e:

        print(f"\n❌ Error ejecutando el comando.")
        print(f"   Código de salida: {e.returncode}")

        return False

    except FileNotFoundError:

        print(f"\n❌ No se encontró el comando:")
        print(f"   {cmd[0]}")

        return False


# -------------------------------------------------------
# EJECUTAR COMANDO Y OBTENER SALIDA
# -------------------------------------------------------

def run_output(cmd):
    try:

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )

        return result.stdout.strip()

    except Exception:
        return ""


# -------------------------------------------------------
# VERIFICAR ROOT EN LINUX
# -------------------------------------------------------

def verificar_permisos_root():

    if not ES_LINUX:
        return

    if os.geteuid() != 0:

        print("\n🔐 Se requieren permisos de administrador.")
        print("🔄 Reiniciando automáticamente con sudo...\n")

        python_exec = sys.executable
        script = os.path.abspath(sys.argv[0])

        os.execvp(
            "sudo",
            [
                "sudo",
                python_exec,
                script,
                *sys.argv[1:]
            ]
        )


# -------------------------------------------------------
# DETECTAR GESTOR DE PAQUETES
# -------------------------------------------------------

def detectar_gestor():

    gestores = [
        "apt",
        "dnf",
        "yum",
        "pacman",
        "zypper",
        "apk"
    ]

    for gestor in gestores:

        if shutil.which(gestor):
            return gestor

    return None


# -------------------------------------------------------
# INSTALAR HERRAMIENTAS LINUX
# -------------------------------------------------------

def instalar_herramientas_linux():

    if not ES_LINUX:
        return True

    print("\n🔧 Verificando herramientas del sistema...\n")

    gestor = detectar_gestor()

    if not gestor:

        print("⚠️ No se detectó ningún gestor de paquetes.")
        return False

    faltantes = []

    for tool in LINUX_TOOLS:

        if shutil.which(tool):

            print(f"  ✅ {tool} ya está instalado")

        else:

            print(f"  ❌ {tool} faltante")
            faltantes.append(tool)

    if not faltantes:

        print("\n✅ Todas las herramientas del sistema están instaladas.")
        return True

    print("\n📦 Herramientas faltantes:")
    print("   " + ", ".join(faltantes))

    print("\n📥 Instalando herramientas...\n")

    if gestor == "apt":

        if not run(["apt", "update"]):
            return False

        if not run(["apt", "install", "-y", *faltantes]):
            return False

    elif gestor in ["dnf", "yum"]:

        if not run([gestor, "install", "-y", *faltantes]):
            return False

    elif gestor == "pacman":

        if not run(["pacman", "-Syu", "--noconfirm"]):
            return False

        if not run(["pacman", "-S", "--noconfirm", *faltantes]):
            return False

    elif gestor == "zypper":

        if not run(["zypper", "refresh"]):
            return False

        if not run(["zypper", "install", "-y", *faltantes]):
            return False

    elif gestor == "apk":

        if not run(["apk", "update"]):
            return False

        if not run(["apk", "add", *faltantes]):
            return False

    print("\n✅ Herramientas del sistema instaladas correctamente.")

    return True


# -------------------------------------------------------
# CREAR VENV
# -------------------------------------------------------

def crear_venv():

    if os.path.exists(VENV_DIR):

        print("🟩 Entorno virtual ya existe.")

        return True

    print("🟦 Creando entorno virtual...")

    python_base = shutil.which("python3") or shutil.which("python")

    if not python_base:

        print("❌ No se encontró Python.")
        return False

    return run([
        python_base,
        "-m",
        "venv",
        VENV_DIR
    ])


# -------------------------------------------------------
# OBTENER PYTHON DEL ENTORNO
# -------------------------------------------------------

def obtener_python():

    if ES_WINDOWS:

        # Si existe un venv, utilizarlo.
        if os.path.isfile(VENV_PY):
            return VENV_PY

        # En caso contrario, utilizar el Python actual.
        return sys.executable

    else:

        if os.path.isfile(VENV_PY):
            return VENV_PY

        return sys.executable


# -------------------------------------------------------
# ACTUALIZAR PIP
# -------------------------------------------------------

def actualizar_pip(python_path):

    print("\n⬆️ Actualizando pip, setuptools y wheel...\n")

    return run([
        python_path,
        "-m",
        "pip",
        "install",
        "--upgrade",
        "pip",
        "setuptools",
        "wheel"
    ])


# -------------------------------------------------------
# VERIFICAR PAQUETE
# -------------------------------------------------------

def paquete_instalado(python_path, paquete):

    try:

        result = subprocess.run(
            [
                python_path,
                "-m",
                "pip",
                "show",
                paquete
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )

        return result.returncode == 0

    except Exception:

        return False


# -------------------------------------------------------
# INSTALAR DEPENDENCIAS
# -------------------------------------------------------

def instalar_dependencias(python_path):

    print("\n📦 Verificando dependencias...\n")

    faltantes = []

    for pkg in DEPENDENCIAS:

        if paquete_instalado(python_path, pkg):

            print(f"  ✅ {pkg} ya está instalado")

        else:

            print(f"  📥 {pkg} faltante")

            faltantes.append(pkg)

    if not faltantes:

        print("\n✅ Todas las dependencias ya están instaladas.")

        return True

    print("\n📦 Instalando dependencias faltantes...\n")

    errores = []

    for pkg in faltantes:

        print(f"\n📥 Instalando {pkg}...")

        resultado = run([
            python_path,
            "-m",
            "pip",
            "install",
            pkg
        ])

        if resultado:

            print(f"  ✅ {pkg} instalado correctamente")

        else:

            print(f"  ❌ No se pudo instalar {pkg}")

            errores.append(pkg)

    print("\n" + "=" * 60)

    if errores:

        print("❌ Se produjeron errores durante la instalación.")
        print("\nPaquetes que fallaron:")

        for pkg in errores:
            print(f"   - {pkg}")

        print("=" * 60)

        return False

    print("✅ Todas las dependencias fueron instaladas correctamente.")
    print("=" * 60)

    return True


# -------------------------------------------------------
# VERIFICAR INSTALACIÓN FINAL
# -------------------------------------------------------

def verificar_instalacion(python_path):

    print("\n🔎 Verificando instalación final...\n")

    # Verificar Python
    try:

        resultado = subprocess.run(
            [
                python_path,
                "--version"
            ],
            capture_output=True,
            text=True,
            check=True
        )

        print(f"🐍 {resultado.stdout.strip()}")

    except Exception:

        print("❌ No se pudo ejecutar el Python del entorno.")
        return False

    # Verificar PyQt6
    try:

        subprocess.run(
            [
                python_path,
                "-c",
                "import PyQt6; print('PyQt6 OK')"
            ],
            check=True
        )

        print("✅ PyQt6 funciona correctamente.")

    except Exception:

        print("❌ PyQt6 no está disponible.")
        return False

    return True


# -------------------------------------------------------
# FLUJO PRINCIPAL
# -------------------------------------------------------

def verificar_librerias():

    print("=" * 60)
    print("🚀 INICIANDO CONFIGURACIÓN DEL ENTORNO")
    print("=" * 60)

    print(f"\n💻 Sistema operativo: {SO}")
    print(f"🐍 Python actual: {sys.executable}")

    # ---------------------------------------------------
    # LINUX
    # ---------------------------------------------------

    if ES_LINUX:

        verificar_permisos_root()

        if not instalar_herramientas_linux():

            print("\n❌ No se pudieron instalar las herramientas de Linux.")
            return False

        if not crear_venv():

            print("\n❌ No se pudo crear el entorno virtual.")
            return False

    # ---------------------------------------------------
    # PYTHON A UTILIZAR
    # ---------------------------------------------------

    python = obtener_python()

    print(f"\n🐍 Python seleccionado:")
    print(f"   {python}")

    if not os.path.isfile(python):

        print("\n❌ El Python seleccionado no existe.")
        print(f"   {python}")

        return False

    # ---------------------------------------------------
    # PIP
    # ---------------------------------------------------

    if not actualizar_pip(python):

        print("\n❌ No se pudo actualizar pip.")
        return False

    # ---------------------------------------------------
    # DEPENDENCIAS
    # ---------------------------------------------------

    if not instalar_dependencias(python):

        print("\n❌ La instalación de dependencias no terminó correctamente.")

        return False

    # ---------------------------------------------------
    # VERIFICACIÓN FINAL
    # ---------------------------------------------------

    if not verificar_instalacion(python):

        print("\n❌ La verificación final falló.")

        return False

    # ---------------------------------------------------
    # ÉXITO
    # ---------------------------------------------------

    print("\n" + "=" * 60)
    print("🎉 ENTORNO CONFIGURADO CORRECTAMENTE")
    print("=" * 60)
    print(f"💻 Sistema: {SO}")
    print(f"🐍 Python: {python}")
    print("=" * 60)

    return True


# -------------------------------------------------------
# EJECUCIÓN
# -------------------------------------------------------

if __name__ == "__main__":

    exito = verificar_librerias()

    if not exito:

        print("\n❌ La configuración del entorno presentó errores.")
        sys.exit(1)

    print("\n✅ Instalador finalizado correctamente.")