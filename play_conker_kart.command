#!/usr/bin/env bash
# ==============================================================================
# Conker-Kart Launcher (SuperTuxKart Mod)
# Sierra Tecnologia / ricasolucoes
# ==============================================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "=========================================================="
echo "          🐿️  CONKER-KART: BAD FUR SPEED  🏁"
echo "=========================================================="
echo "Carregando 10 personagens clássicos do Conker..."
echo "- Conker, Berri, Panther King, The Great Mighty Poo"
echo "- Prof. Von Kriplespac, Gregg, Tediz, Buga, Franky, King Bee"
echo ""

# Sincroniza karts caso haja alterações
mkdir -p "$HOME/Library/Application Support/supertuxkart/addons/karts"
mkdir -p "$HOME/Library/Application Support/SuperTuxKart/Addons/karts"
cp -r "$DIR/karts/"* "$HOME/Library/Application Support/supertuxkart/addons/karts/" 2>/dev/null
cp -r "$DIR/karts/"* "$HOME/Library/Application Support/SuperTuxKart/Addons/karts/" 2>/dev/null

echo "Iniciando o jogo..."
if [ -d "/Applications/SuperTuxKart.app" ]; then
    open -a /Applications/SuperTuxKart.app
else
    echo "SuperTuxKart não encontrado em /Applications/SuperTuxKart.app"
    exit 1
fi

echo "Jogo iniciado com sucesso! Divirta-se!"
