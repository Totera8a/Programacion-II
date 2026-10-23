#!/usr/bin/env bash
set -e

BASE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DESTINO="${1:-$BASE}"

if [[ ! -f "$BASE/.venv/bin/activate" ]]; then
    echo "ERROR: No se encuentra .venv"
    read -r -p "Presioná Enter para cerrar..."
    exit 1
fi

if [[ ! -d "$DESTINO" ]]; then
    echo "ERROR: No se encuentra la carpeta de trabajo"
    read -r -p "Presioná Enter para cerrar..."
    exit 1
fi

exec bash --rcfile <(
    printf 'cd %q\nsource %q\n' \
        "$DESTINO" "$BASE/.venv/bin/activate"
) -i
