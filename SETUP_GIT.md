# 🔧 Instalación de Git en Windows

## Opción 1: Descargar e Instalar (Recomendado)

1. **Descargar Git:**
   - Ve a: https://git-scm.com/download/win
   - Se descargará automáticamente el instalador

2. **Instalar:**
   - Ejecuta el instalador descargado
   - Acepta todas las opciones por defecto
   - Clic en "Next" hasta finalizar
   - Reinicia tu terminal/PowerShell

3. **Verificar instalación:**
   ```powershell
   git --version
   ```

## Opción 2: Instalar con Winget (Más Rápido)

```powershell
winget install --id Git.Git -e --source winget
```

## Opción 3: Instalar con Chocolatey

```powershell
choco install git
```

---

## Después de Instalar

Configura tu identidad:

```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

¡Listo! Ahora puedes usar Git desde tu terminal.
