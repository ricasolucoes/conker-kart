# Guia de Publicação na Google Play Store — Conker-Kart

Este guia contém as instruções completas para submeter o aplicativo **Conker-Kart** na Google Play Store através do console da **Sierra Tecnologia**.

---

## 1. Requisitos Prévios

1. **Conta de Desenvolvedor do Google Play Console:**
   * Ativa e verificada sob a titularidade da **Sierra Tecnologia**.
2. **Keystore de Produção:**
   * Gere a chave de assinatura com o comando abaixo (guarde as senhas e o arquivo `.jks` em local seguro):
   ```bash
   keytool -genkeypair -v -keystore release.keystore \
     -alias conkerkart -keyalg RSA -keysize 2048 -validity 10000 \
     -dname "CN=Sierra Tecnologia, O=Rica Solucoes, C=BR"
   ```
3. **Android App Bundle (.aab):**
   * O Google Play exige o formato `.aab` para todos os novos aplicativos (não mais `.apk` solto).

---

## 2. Assets Visuais Prontos no Repositório

Todos os arquivos gráficos necessários já estão gerados nas dimensões exatas exigidas pelo Google Play Console:

| Asset | Arquivo no Repositório | Resolução | Exigência Google Play |
|---|---|---|---|
| **Ícone do App** | `assets/store/icon_512.png` | 512 x 512 px (PNG 32-bit) | Obrigatório |
| **Gráfico de Recursos** | `assets/store/feature_graphic_1024x500.png` | 1024 x 500 px (PNG/JPEG) | Obrigatório |
| **Captura de Tela 1** | `assets/store/screenshot_1.png` | 1920 x 1080 px (16:9) | Obrigatório (mín. 4) |
| **Vídeo Promocional** | Produzido via Google Flow (`docs/GOOGLE_FLOW_VIDEO_PROMPTS.md`) | Link YouTube 1080p | Opcional / Recomendado |

---

## 3. Informações da Ficha da Loja

### Nome do App
`Conker-Kart: Arcade Racing`

### Breve Descrição (até 80 caracteres)
`Corridas insanas de kart arcade com nitro, drifts e personagens irreverentes!`

### Descrição Completa (até 4000 caracteres)
```
Prepare-se para o caos sobre rodas com Conker-Kart!

Acelere em pistas cheias de perigos, saltos espetaculares, nitros e armadilhas hilárias. Escolha o seu piloto favorito entre personagens irreverentes e customize seu estilo de pilotagem em disputas de alta velocidade!

🏁 RECURSOS DO JOGO:
• Pilotos Carismáticos: Conker e seu Nitro Rod veloz, Berri e sua máquina veloz Pink Fury, e o imponente Rei Pantera no seu Golden Tank!
• Física Arcade Precisa: Drifts afiados, saltos vertiginosos e turbos flamejantes.
• Armas e Power-ups: Jogue avelãs explosivas, chicletes e desvie de obstáculos na pista.
• Múltiplas Dificuldades e Modos: Dispute Grandes Prêmios, Contra o Relógio e Corridas Rápidas.

ℹ️ INFORMAÇÕES DE CÓDIGO ABERTO:
Este jogo é desenvolvido pela Sierra Tecnologia e baseado no motor de código aberto SuperTuxKart (distribuído sob licença GNU General Public License v3). O código-fonte correspondente e todos os arquivos deste projeto estão disponíveis publicamente em:
https://github.com/ricasolucoes/conker-kart
```

---

## 4. Política de Privacidade & Conformidade

* Crie uma URL pública de Política de Privacidade (por exemplo, `https://ricasolucoes.com/privacidade/conker-kart`).
* Classificação indicativa: O jogo possui violência cartunesca cômica (faixa recomendada: Livre a 10 anos).
* Declaração de Direitos: Todos os créditos ao motor SuperTuxKart e seus mantenedores estão mantidos nos termos da GPLv3.
