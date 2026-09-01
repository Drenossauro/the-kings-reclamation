# Manual do Reclamation — Reclaim the World (PT-BR)

> **Guia de progressão completo**, escrito a partir da *sua* instalação:
> `Reclamation 2.3.2` · Minecraft `1.20.1` · Forge `47.4.0` · 167 mods.
>
> Fontes: o questbook FTB da instância (10 capítulos, 558 quests) e os scripts
> KubeJS do pack (`kubejs/server_scripts/`, ~5.700 linhas que **reescrevem receitas**).
> Ou seja: o que está aqui bate com o seu jogo, não com a wiki genérica dos mods.

---

## Índice

- [1. Como ler este manual](#1-como-ler-este-manual)
- [2. As regras deste mundo](#2-as-regras-deste-mundo)
- [3. Ato 0 — Acordar e não morrer](#3-ato-0--acordar-e-não-morrer)
- [4. Ato 1 — Fazer terra (Theurgy / Spagyrics)](#4-ato-1--fazer-terra-theurgy--spagyrics)
- [5. Ato 2 — Fazer ferro (Enchanted + sangue de planta)](#5-ato-2--fazer-ferro-enchanted--sangue-de-planta)
- [6. Ato 3 — AgriCraft: genética de plantas](#6-ato-3--agricraft-genética-de-plantas)
- [7. Ato 4 — Fazer grama (Nature's Aura)](#7-ato-4--fazer-grama-natures-aura)
- [8. Ato 5 — Aura, Botania, Nether e Embers](#8-ato-5--aura-botania-nether-e-embers)
- [9. Ato 6 — Recriar a vida animal](#9-ato-6--recriar-a-vida-animal)
- [10. Ato 7 — Blood Magic, gemas e Ars Nouveau](#10-ato-7--blood-magic-gemas-e-ars-nouveau)
- [11. Ato 8 — Mekanism e AE2](#11-ato-8--mekanism-e-ae2)
- [12. Ato 9 — Reclamar o mundo e chegar ao End](#12-ato-9--reclamar-o-mundo-e-chegar-ao-end)
- [13. Linhas paralelas](#13-linhas-paralelas)
- [14. Gestão de Aura (a dúvida mais comum)](#14-gestão-de-aura-a-dúvida-mais-comum)
- [15. Segredos e mecânicas escondidas do pack](#15-segredos-e-mecânicas-escondidas-do-pack)
- [16. Erros comuns que travam o jogador](#16-erros-comuns-que-travam-o-jogador)
- [17. Referência rápida por mod](#17-referência-rápida-por-mod)
- [18. Os livros do pack](#18-os-livros-do-pack)

---

## 1. Como ler este manual

O Reclamation é um pack **semi-expert linear**: cada etapa desbloqueia a seguinte, e
pular etapa quase nunca funciona. Este manual segue a ordem real do questbook.

**A regra número um do pack:** muitas receitas foram alteradas. Sempre confira no EMI.

| Tecla | O que faz |
|---|---|
| `R` (com item sob o mouse) | mostra **como fazer** o item |
| `U` (com item sob o mouse) | mostra **onde o item é usado** |
| `M` | abre o mapa (Xaero) — usado pra *claim* e force-load de chunks |
| `F3+H` | liga/desliga tooltips avançados |

> Se algo neste manual divergir do seu EMI, **o EMI está certo** — ele lê o jogo rodando.

---

## 2. As regras deste mundo

O pack muda o mundo de forma agressiva. Entender isso economiza horas:

**Geração do mundo**
- **Nenhum minério gera. Nenhum.** Não existe carvão, ferro, cobre ou diamante pra minerar.
- Só existem biomas de deserto morto. Sem vegetação natural.
- As únicas árvores são **Dead Trees** (madeira morta, de baixa qualidade).
- Variantes de pedra ainda geram. **Areia e argila existem debaixo d'água.**
- Ainda chove.
- O bloco base do chão é o **Dried Earth** (bloco customizado do pack, tag `minecraft:dirt`).

**Mobs**
- **Zombie villagers e bruxas não spawnam.** Não há como conseguir recursos deles.
- Aranhas mutaram — só spawnam as versões **cave spider** (venenosas).
- Drops raros de ferro/cobre existem, mas são a exceção, não o plano.
- Wandering traders estão desligados; a dificuldade é forçada em **hard**.
- Chicken jockeys foram removidos (o pack cancela o spawn).

**Nether**
- Zero spawns naturais. Um único bioma. Sem minérios.
- Dá pra fazer o portal **colocando lava e água com balde** — mais fácil que minerar obsidiana.

**O objetivo**
Trazer terra → grama → plantas → animais → biomas de volta, e no fim abrir o End.

---

## 3. Ato 0 — Acordar e não morrer

**Capítulo do questbook:** *How The World Came To Be*

1. **Dead Logs** — quebre as árvores mortas. Elas dão `Dead Log`, que vira `Flimsy Planks`.
   - Dead Log tem **10% de chance de dropar carvão vegetal** direto (loot modifier do pack).
2. **Oxidized Cut Copper** — nas ruínas espalhadas pelo mapa.
   - **Raspe a ferrugem com um machado** até virar `Cut Copper`.
3. **Cutting Board (Farmer's Delight)** — é a ferramenta central do começo.
   - `Cut Copper` + picareta na cutting board → **6 lingotes de cobre garantidos**,
     +2 com 75% de chance, +1 com 50%. (Média ≈ 8 lingotes por bloco.)
   - Também serve pra tirar mais carvão e `Scrap Wood` de dead logs.
4. **Flimsy Door** — porta improvisada de scrap wood + cobre. **Ela quebra sozinha
   de vez em quando** e precisa ser recolocada. É proposital.
5. **Cama** — corda de aranha vira lã, lã vira cama. Ou faça um sleeping bag.
6. **Akashic Tome** — recompensa da quest "Too Many Books!?". Craft qualquer livro-guia
   com ele pra fundir todos num item só. Soco no ar destransforma.
7. **Claim de chunk** — abra o mapa (`M`) e arraste com botão direito pra reivindicar;
   arraste de novo pra **force-load**. Isso mantém processos passivos rodando.
   - **Dica importante do autor do pack:** desligue a proteção do claim. Ela quebra fake players
     (máquinas que agem como jogador).

**Peixe** ainda existe e é sua comida inicial. Fatiar peixe na cutting board rende mais.

---

## 4. Ato 1 — Fazer terra (Theurgy / Spagyrics)

Este é o gargalo de abertura do pack. Theurgy é alquimia: todo item se decompõe em
**três princípios**, e recombinando os três você "cria" o item.

| Princípio | O que representa | Máquina que extrai |
|---|---|---|
| **Mercury** (Mercúrio) | a *Energia* do item — genérico, intercambiável | **Distiller** |
| **Salt** (Sal) | o *Corpo* — o "tipo" do item | **Calcination Oven** |
| **Sulfur** (Enxofre) | a *Alma* — qual item exatamente é | **Liquefaction Cauldron** |

Todas as três máquinas ficam **em cima de um Pyromantic Brazier**, que precisa de combustível.

### Passo a passo

1. **Sal Ammoniac** — monte `Sal Ammoniac Tank` e ponha o `Sal Ammoniac Accumulator`
   **em cima** dele. Encha de água. Ele destila Sal Ammoniac lentamente.
   - Faça **baldes de cobre** (receita do pack: cobre + caminite blend).
2. **Alchemical Mercury** — `Distiller` sobre brazier. Destile **cobblestone, dried earth
   ou peixe cozido**. Materiais mais raros dão mais mercúrio.
3. **Alchemical Salt (Strata)** — `Calcination Oven` sobre brazier. Foque em **Strata salt**.
4. **Alchemical Sulfur (Dirt)** — `Liquefaction Cauldron` sobre brazier, **abastecido com
   Sal Ammoniac**. Coloque `Dried Earth` — ele "lembra" que já foi terra e vira **Dirt Sulfur**.
5. **Incubator** — o bloco que recombina. Sobre um brazier, com os três vasos
   (`salt vessel`, `sulfur vessel`, `mercury vessel`) grudados nas laterais.
   Encha cada vaso com o componente certo → sai **Dirt**.

🎉 **Você fez terra.** É o momento que destrava o pack inteiro.

> **Nota:** o pack removeu a duplicação `dirt → coarse dirt → dirt`. A nova receita
> é `2 dirt + 2 gravel → 2 coarse dirt`. Não tente farmar terra por aí.

---

## 5. Ato 2 — Fazer ferro (Enchanted + sangue de planta)

**Capítulo:** *The Hunt For Grass* (primeira metade)

Com terra, você planta. As sementes vêm de tufos de grama sobreviventes:
`wheat_seeds`, e as mágicas do mod **Enchanted**: `water_artichoke`, `wolfsbane`,
`mandrake`, `belladonna`, `snowbell`.

### A rota do ferro

1. **Mandrake Root** — colha **à noite** (de dia ela grita e te machuca).
   - Faça **Earmuffs** (protetor de ouvido) pra parar de tomar o grito.
   - Quanto maior o stat **Strength** do mandrake, menos ele acorda.
2. **Hemoglobic Fluid** — mandrake é literalmente uma planta que produz sangue.
   Ponha o `Sal Ammoniac Accumulator` **em cima de um `Fluid Vessel` (Embers)**, não em
   cima do tank. ⚠️ O Sal Ammoniac Tank só aceita sal ammoniac — **use o Fluid Vessel**.
3. **Iron Alchemical Sulfur** — use o hemoglobic fluid como **solvente no Liquefaction
   Cauldron** pra liquefazer cobre. O ferro do fluido converte o sulfur de cobre em ferro.
4. **Mineral Alchemical Salt** — calcine **carvão vegetal**, ou re-calcine muito Strata salt.
5. **Incubator**: Iron Sulfur + Mineral Salt + Mercury → **lingote de ferro**. ✅

### Bruxaria (Enchanted) — abre aqui

- **Witch's Cauldron**: caldeirão de ferro + **Anointing Paste** (feito das plantas mágicas).
  Encha com 3 baldes de água, ponha sobre uma fogueira pra ferver.
  - Se a poção estragar (fica marrom) você pôs ingrediente na ordem errada — esvazie com balde.
- **Mutandis** — mutagênico que transforma **dead bushes em saplings reais**. É assim que
  você recupera árvores.
- **Witch's Oven** — destila saplings em fumaças mágicas. **Fume Funnels** ao lado aumentam
  a chance de obter fumaça.
- **Altar (Enchanted)** — 2×3 de blocos de altar. Ele coleta energia da vida vegetal num
  raio de **16 blocos**. Quanto mais **variedade** de planta em volta (árvore, grama, flor,
  crop, cipó, abóbora, melão), mais poder — cada tipo tem um teto próprio.
  - **Upgrades no topo do altar:** Tocha `+0,5x` recarga · Skeleton/Husk Head `+1x` recarga
    e `+1x` capacidade · Chalice `+1x` capacidade. Depois: candelabro, wither skull, chalice cheio.
- **Attuned Stone** — permite crafts de bancada e, carregada, executar rituais **longe do altar**.
  ⚠️ A receita precisa de energia do altar: o caldeirão tem que estar no alcance.
- **Circle Magic** — chalks: `golden` (centro), `ritual`, `nether`, `otherwhere`.

---

## 6. Ato 3 — AgriCraft: genética de plantas

**Item de entrada:** `Wooden Crop Sticks`.

As plantas do Reclamation são **diploides**: cada uma tem dois valores por atributo
(ativo/dominante e inativo/recessivo). O **ativo** é o que funciona; o inativo entra no cruzamento.

### Os cinco stats

| Stat | Efeito |
|---|---|
| **Fertility** | chance da planta ser escolhida como pai no cruzamento |
| **Gain** | quanto ela produz ao ser colhida |
| **Growth** | velocidade de crescimento |
| **Mutativity** | chance do cruzamento ser *benéfico* |
| **Strength** | amplia as condições de solo/ambiente que a planta aceita |

**Strength é o stat mais subestimado.** Com strength alto, cactus cresce em farmland
normal e flores dispensam podzol.

### Como cruzar bem

- Cruze plantas de stats altos entre si; use **bonemeal nos crop sticks** pra acelerar.
- **Plante em formato de cruz (+)** com o crop stick vazio no meio: assim o cruzamento tem
  **4 chances** de escolher pais em vez de 2. Isso muda o jogo no início.
- Se a planta não cresce, **agache e olhe pra ela** — ela diz o solo de que precisa.
- Use `U` no EMI em cima da **semente** pra ver condições de crescimento;
  `R` na semente pra ver de que cruzamento ela sai.
- **Magnifying Glass** e **Seed Analyzer** mostram os stats. Espécie também pode ser recessiva.

### Duas plantas críticas

- **Cuprosia** — flor que extrai **cobre da água**. É a sua fonte renovável de cobre quando
  as ruínas acabarem.
  ⚠️ Só cresce em **crop stick alagado (waterlogged)** e, com strength 1, **só em gravel**.
- **Podzol** — cresça um 2×2 de spruce saplings; a árvore grande converte a terra (e o
  dried earth) embaixo em podzol. É onde as sementes de flor são plantadas.

**Composter** transforma sementes/crops extras em bonemeal — pare de caçar esqueleto de madrugada.

---

## 7. Ato 4 — Fazer grama (Nature's Aura)

O clímax do início do jogo. A grama vem de um **ritual**, não de um craft.

1. **Mutandis → saplings** (Ato 2) → cresça uma árvore de verdade.
2. **Brilliant Fiber** (`gold_fiber`) — feito na bruxaria. Aplique nas **folhas** de uma
   árvore e observe **se espalhar**.
3. Quebre as folhas douradas → **Gold Leaf** → moa em **Gold Powder**.
   - Mais tarde há um jeito melhor de fazer brilliant fiber, usando **blaze powder**.
4. **Ritual of the Forest**: 4× `Wood Stand` + 16× `Gold Powder` em volta de um
   **birch sapling**, com `Hay Block`, uma semente, `Hint of Rebirth` e
   `Breath of the Goddess` (ingredientes reais da receita no seu pack). Leva ~250 ticks.
5. Saída: **Pasture Seeds** (`botania:grass_seeds`) → espalha **grama** na terra em volta. 🌱

> ⚠️ **Bug conhecido do mod:** regador (watering can) **não** inicia o Ritual of the Forest.
> As instruções completas do ritual estão no **Book of Natural Aura**.

Com grama: **bonemeal numa área grande → flores** → tinta → o resto do jogo abre.

---

## 8. Ato 5 — Aura, Botania, Nether e Embers

**Capítulo:** *The Color Green* — é o capítulo mais denso do pack; quatro mods avançam juntos.

### 8.1 Nature's Aura

- **Bottling Sunlight** — faça a `Bottle and Cork` e **clique com o botão direito no ar**.
  Cada clique **consome aura do chunk** onde você está. É material de craft, não gerador.
  ⚠️ Faça suas garrafas **longe da base**, num chunk intocado.
- **Natural Altar** (multibloco) — 16 stone bricks, 4 chiseled stone bricks, 8 gold bricks,
  20 planks. Ele **drena aura do ambiente** pra transformar itens.
- **Environmental Eye** — segure na mão pra ver o nível de aura do chunk. Item obrigatório.
- **Infused Iron** — ferro infundido no altar. Ferramentas/armaduras com habilidades especiais,
  **reparáveis com aura**.
- **Geradores de aura** (leia a seção 14 deste manual):
  - **Ancient Sapling** — a árvore crescida, em aura baixa, **murcha as folhas gerando aura**.
  - **Flower Generator** — converte flores em aura. **Dieta variada!** Muita flor igual dá
    retorno decrescente.
  - **Aura Cache** — bateria portátil de aura. Com aura alta na área ela carrega sozinha.
    Agache com uma **botanist tool** (feita de infused iron) pra reparar itens usando o cache.
- **Catalisadores** (colocados **em cima de um dos 4 blocos de ouro inferiores do altar**):
  - **Crushing/Crumbling Catalyst** — mais bonemeal por osso, mais gold powder por folha,
    cobblestone → areia.
  - **Conversion/Transmutation Catalyst** — **areia → soul sand** (essencial pra "haunting"
    do Create e pra nether wart), netherrack → nylium.
- **Regrowth** — com aura alta o suficiente, **dried earth vira dirt sozinho**.
  Se quiser impedir isso numa área, use **Powder of Dried Stasis**.
- **Offering Table** (multibloco) — infunde itens em versões empoderadas. Coloque o item e
  jogue um **Spirit of Calling** em cima. Dá pra infundir vários itens com um spirit só.
- **Creational Catalyst** — remove o limite embutido dos geradores de aura. Late game.

### 8.2 Botania

- **Pure Daisy** + Petal Apothecary (encha de água, jogue as pétalas e depois a semente).
  - Converte log → **Livingwood**, stone → **Livingrock**.
  - E, receita **exclusiva do pack**: `Golden Nether Brick` (Nature's Aura) → **Nether Gold Ore**.
    É assim que você faz **ouro**.
- **Mana**: `Mana Spreader` + `Mana Pool` + **Endoflame** (primeiro gerador) + `Wand of the Forest`
  (usado pra ligar spreader ↔ flor/pool).
- **Runic Altar** → runas. Também faz mystical flower seeds.
- **Fel Pumpkin** — cabeça de blaze falsa. Sobre 2 barras de ferro vira um pseudo-blaze que
  **sempre dropa ≥10 blaze powder**. Esta é a sua fonte de blaze powder sem ir ao Nether farmar.
  - Com reagentes mágicos + a cabeça, o ritual invoca um **blaze real** (≥3 blaze rods).
- **Geradores alternativos**: Thermalily (lava), Entropinnyum (TNT, um dos melhores),
  Munchdew (folhas).
- **Alchemy Catalyst** (sob a mana pool) — flores↔flores, pedras↔pedras, flint↔gunpowder,
  ghast tear→ender pearl e, crucialmente, **flax → feather**.
- **Rod of the Lands** — mana → bloco de terra. "Terra quase de graça".
- **Orechid** (late) — gera minério em stone/deepslate. Custos no seu pack:
  deepslate ferro 250 / ouro 125 / cobre 75 · stone ferro 29.371 / ouro 2.647 / cobre 7.000.
  (Ou seja: **use deepslate**, a diferença é absurda.)

### 8.3 Embers Rekindled

- **Raw Lead** — feito de ferro infundido em natureza + nether bricks + spruce sapling.
  Recompensa: **Ancient Codex** e **Tinker Hammer**.
  - O Codex é confuso: **comece em "Natural Energy"**, botão direito nas entradas pra marcar
    como lidas, e **leia com atenção**.
- **Ember Bore** — coloque **sobre a bedrock**, com **Mechanical Core** em cima. Combustível
  dentro. Ember é praticamente infinito no subsolo.
  - **Use o Tinker's/Mechanical Lens** — ele explica visualmente o que cada máquina está fazendo.
- ⚠️ **Quase tudo no Embers precisa de sinal de redstone.** Prepare-se pra encher de alavancas.
- **Ember Activator** (+ Emitter/Receiver/Relay) → Activated Ember.
  - Ember Grit não gera ember por padrão: adicione um **Heat Exchanger** (×0,9 na produção,
    mas **+300 fixo** por item).
- **Copper Cell** (bateria) + **Ember Dial** (mostrador).
- **Melter + Stamper + Stamp Base** — funde metais e estampa placas (mais eficiente).
- **Mixer Centrifuge** — cobre fundido + ouro fundido em **lados diferentes** → **Dawnstone**.
- **Alchemy Tablet + Beam Cannon + Pedestais** — transmutação por **tentativa e erro**:
  você não sabe quais *aspectii* combinam com quais itens. Falhas geram **Alchemical Waste**;
  clique com ela na mão pra ver quantos acertos você teve.
  - **Codebreaking Slate** — processa vários wastes de uma vez e mostra também
    quantos aspectii certos você pôs no item errado.
  - **Mnemonic Inscriber** — anexado ao tablet + papel, **anota automaticamente** a combinação
    correta quando você acerta. Faça isso cedo.
- **Escalada de eficiência:** `Pressure Refinery` (1,5×, ou 3× sobre bloco de metal cercado de
  lava/fogo) → `Wildfire Stirling` (metade do consumo; o segundo dobra o ganho, o terceiro piora)
  → **Ignem Reactor** entre Catalysis e Combustion Chamber (**até 9×**).
- **Crystal Seeds** — attuned stone carregada vira semente que converte ember em metal puro.
  É assim que você obtém **Zinco**. ⚠️ Cristais sobem de nível com o tempo, mas
  **mover o cristal reseta o nível**.
- **Bin** — cole embaixo de uma máquina (ex.: stamp base) pra coletar a saída automaticamente.

### 8.4 Create (uso leve)

O pack usa pouco Create — não é obrigatório se aprofundar.

- Andesite Alloy no seu pack **usa chumbo (lead)**, não zinco.
- **Encased Fan** + soul sand → **haunting** → cobblestone vira **blackstone**
  (necessário pro Reformation Array do Theurgy). Também libera smelting/lavagem em massa.
- **Millstone**, **Basin**, **Mechanical Mixer/Press**, **Mechanical Pump** (bem mais rápido
  que a bomba de ember), **Spout**.
- Com **zinco** → brass → **Electron Tube** → **Mechanical Crafter**, **Factory Gauge**,
  **Packager / Chain Conveyor / Frogport**.
- **Blaze Burner** — capture o blaze invocado numa gaiola; sob um basin, brassagem eficiente.

### 8.5 Theurgy avançado (o loop de metais)

- **Reformation Array** — `source pedestal` + `target pedestal` + `result pedestal` +
  `sulfuric flux emitter` + `mercury catalyst`. Segure o emitter e clique em cada pedestal,
  depois ponha o emitter no catalyst.
  Converte sulfur → sulfur **do mesmo tier e tipo** (ex.: ferro → chumbo).
- **Fermentation Vat** — água + açúcar + sulfur, **shift+direito pra fechar** → **Alchemical Niter**.
  Niter converte entre **tipos diferentes** (mesma raridade).
- **Digestion Vat** — converte entre **raridades**: **4 do tier anterior ↔ 1 do próximo**.
  - **O loop famoso do pack:** iron sulfur → common metal niter → 4 abundant metal niter →
    **4 copper sulfur**. Ou seja, **4 cobre por ferro**. Automatizável (os vats aceitam redstone).
- **Mercury Catalyst + Caloric Flux Emitter** — converte mercúrio em **Mercury Flux (MF)**,
  que alimenta aparelhos alquímicos **sem precisar de brazier embaixo**.
  Um mercury shard ≈ um carvão em energia.

---

## 9. Ato 6 — Recriar a vida animal

**Capítulo:** *The Sound of Life*

1. **Offering Table** (Nature's Aura) → os quatro amálgamas customizados do pack:
   `Feather-Flesh Amalgam`, `Blooded Amalgam`, `Mana-Dosed Amalgam`, `Infused Amalgam`.
2. Com eles → **Chicken Spawn Egg**. Galinhas = **ovos** = a raiz de toda fauna.
3. **Altar of Birthing** (`naturesaura:animal_spawner`):
   - Em área de **aura alta**, **acasalar mobs gera Spirits of Birthing**.
   - Jogue o spirit + reagentes no altar → novas criaturas.
   - É também onde você invoca **Siren, Whirlisprig, Drygmy, Wixie, Starbuncle e bruxa**.

---

## 10. Ato 7 — Blood Magic, gemas e Ars Nouveau

### 10.1 Blood Magic

1. **Soul Snares** — jogue nos monstros **antes de matar** → dropam **Demonic Will**.
2. **Blood Altar** + **Sacrificial Dagger** (auto-sacrifício, no começo).
3. **Blank Slate** (pedra dopada em sangue) → slates de tier crescente:
   `Blank → Reinforced (T2) → Imbued (T3) → Demonic (T4) → Ethereal (T5)`.
   Cada tier exige o altar naquele tier, subido com **runas** em volta.
4. **Hellfire Forge (Soul Forge)** + **Tartaric Gem** — armazena will.
   > Quanto **mais will você carrega, mais will os monstros dropam**.
5. **Blood Orb** — clique com ele na mão pra vincular à sua rede de LP.
6. **Alchemy Table** → **Arcane Ashes** → **Divination Sigil**.
7. **Sentient Tools** — cortam almas sozinhas (adeus soul snares) e ficam mais fortes
   proporcionalmente ao will no inventário.
8. **Alchemical Reaction Chamber (T3)** → **diamante, lápis, ametista**. 💎
   Este é o desbloqueio de gemas do pack.
9. **Incense Altar** — multibloco livre de "tranquilidade"; no máximo dá até
   **4× life essence** por auto-sacrifício.
10. **Tainted Blood Pendant** (Botania) com Regeneração — torna o auto-sacrifício tolerável.
11. **Budding Amethyst** — ritual wiccano converte bloco de ametista na versão budding
    (fonte renovável). O **pentagrama de arcane ashes** no altar dá **+1,5× capacidade**.
12. **Demon Realm**:
    - **Edge of the Hidden Realm** → portal → **Tau Fruit** → **Blood Shards** → altar T4.
    - **Ritual Diviner Dusk** → **Pathway to the Endless Realm** → labirinto com
      inimigos fortes, loot e o minério **Demonite**.
13. **Crystallized Will** — `Demon Crucible` (queima will no ar) + `Demon Crystallizer`.
    Cada cristal além do primeiro custa 40 will e **queima em 50** — lucro líquido.
    - **Resonance of the Faceted Crystal** divide 1 cristal em 4 aspectados
      (corrosive, vengeful, destructive, steadfast). Automatizável inteiro.
14. **Automação de LP** — `Ritual of the Feathered Knife` ou `Well of Suffering` +
    **Ritual Tinkerer**. Com mobs regenerando, vira infinito.

### 10.2 Ars Nouveau (Source)

- **Archwood** — infunda um sapling magicamente ressonante com **Life Essence**.
  Dá pra converter entre os 5 tipos de archwood **numa mana pool**.
- **Imbuement Chamber** → **Source Gem** (de ametista ou lápis).
- **Sourcelinks** + **Source Jar** para gerar/armazenar Source líquido.
  ⚠️ **Crops de AgriCraft NÃO funcionam com o Agronomic Sourcelink** — plante do jeito normal.
- **Arcane Core + Enchanting Apparatus** — encantamentos e crafts especiais.
- **Ritual Brazier** — defesa de base, coleta automática de itens, voo.
- **Storage Lectern** + **Bookwyrm Charm** + **Repository** — sistema de armazenamento
  navegável e craftável, ligado por **Dominion Wand**.
- **Familiares** (todos invocados no Altar of Birthing):
  | Criatura | Como conseguir o token | O que faz |
  |---|---|---|
  | **Starbuncle** | dê gold nuggets | move itens (logística sem tubos) |
  | **Drygmy** | dê wilden horn | gera drops e XP de mobs **sem matar** |
  | **Whirlisprig** | cresça árvore perto | produz recursos naturais |
  | **Wixie** | dispel numa bruxa | crafta e faz poções |
  | **Siren** (Ars Elemental) | dê sea pickle | **pesca automática** por Source |
- **Amethyst Golem** — anime budding amethyst com o **Ritual of Awakening**; ele colheita,
  cresce e propaga ametista.
- **Wilden** — invocados com a Tablet of Summon Wilden. O **Wilden Chimera** (boss) dropa
  o item que destrava **magias tier 3**.
- **Magebloom** → fibra → **Warp Scroll** / **Stable Warp Scroll** (portais permanentes com
  moldura de Sourcestone + source jar cheio).

### 10.3 Botania late

- **Terra Plate** → **Terrasteel** (use **Sparks** no lugar de spreaders — muito mais rápido).
- **Sin Runes** (3º tier de runas).
- **Alfheim Portal** (2 Natura Pylons) — não transporta seres vivos, mas permite **comércio**.
  - Jogue o **Lexica Botania inteiro** dentro pra ganhar conteúdo extra
    (⚠️ não jogue seu Akashic Tome!).
- **Elven Spreader**, flores élficas, **Conjuration Catalyst** (duplica itens — adeus destilar
  redstone e glowstone), **Gaia Pylons** → **Guardian of Gaia** → **Gaia Spirits**.

---

## 11. Ato 8 — Mekanism e AE2

### Ordem correta

1. **Osmium** — oferte um **Imbued Slate** aos deuses, convertendo ferro.
2. **Energia**: **Mana Fluxfield** (Botania) — aponte um mana spreader nele e ele cospe RF.
   (O heat generator existe, mas é péssimo — não vale.)
3. **Metallurgic Infuser** → **Steel** (ferro + carvão).
4. **Steel Casing** → tudo o mais.
5. **Enrichment Chamber** → reagentes **8× mais eficientes** pro Infuser.
6. **Crusher** → **Bio Fuel** → **Bio-Generator**, ou refine em **Ethylene**.
   > ⚠️ O pack **nerfou a queima de ethylene**. Continua útil, só não é quebrado.
7. **Rotary Condensentrator** → **Aerated Essence** (life essence gaseificada) →
   **Gas-Burning Generator**. Esta é a energia que carrega o mid-game.
   - **Blooded Ethylene** (ethylene + aerated essence) queima ainda melhor.
8. **Processamento de minério, em escada:**
   | Etapa | Máquinas | Rendimento |
   |---|---|---|
   | 2× | Purification Chamber (+O₂) → clumps → dirty dust → enrich → smelt | 2 ingots/raw |
   | ~2,6× | Chemical Dissolution Chamber + Thermal Evaporation (brine→cloro→HCl) | 3 raw → 8 shards |
   | ~3,3× | Chemical Washer + Crystallizer + Injection Chamber (ácido sulfúrico) | 3 raw → 10 ingots |
9. **Upgrades**: *upgrade cards* (velocidade, eficiência) e *tier installers*
   (de 1 pra até 9 slots de processamento).
10. **Fission Reactor** → vapor → Industrial Turbine.
    - ⚠️ **Se você errar a operação, ele derrete e explode/irradia.** Faça pequeno, ou longe.
    - Resíduo → **Plutônio** e **Polônio** → **Supercritical Phase Shifter** → **Antimatéria**.
    - **Radioactive Waste Barrel** é praticamente a única coisa que segura o rejeito.
11. **QIO System** (polônio) — armazenamento digital sem energia, alcance **cross-dimensional
    ilimitado**, mas **não faz autocraft**.
12. **Fusion Reactor** — milhões de RF/t com deutério/trítio/D-T.

### AE2

1. **Certus Quartz** — `Charger` + **diamante enriquecido**.
2. **Budding Quartz** — jogue um bloco de certus quartz na água com charged certus.
   ⚠️ **Ele degrada** e precisa ser re-semeado (diferente da ametista).
3. **Fluix Crystal** — redstone + nether quartz + charged certus.
4. **Mysterious Cube** — um **ritual** atrai um meteoro reduzido com as presses.
   (Está no **Reclamation Rituals book**.)
5. **Inscriber** → circuitos → **ME Controller**.
6. Rede: cada face do controller dá **32 canais**; quase todo aparelho consome **1 canal**.
   - **Energy Acceptor** não usa canal — use ele pra energia, deixando as faces livres.
   - **Smart Cable** mostra os canais visualmente; **Dense Cable** carrega 32 em vez de 8.
   - **P2P Tunnels** multiplicam canais por canal (e transportam energia, químicos,
     mana botânico e Source).
7. **Autocraft**: `Pattern Provider` + `Molecular Assembler` + storage de crafting.
   - Escalando: **Assembler Matrix** (>4.000 patterns, **1 canal só**),
     **Quantum Computer Core** (256M + 8 co-processadores) → **Quantum Computer multiblock**.
8. **Extended/Advanced AE**: `Ex Inscriber` e `Ex Charger` (4 receitas em paralelo),
   **Circuit Slicer** (bloco → 9 circuitos), **Reaction Chamber**.

---

## 12. Ato 9 — Reclamar o mundo e chegar ao End

**Capítulos:** *The Touch Of...* e *The Taste of Power*

1. **Ritual of Reclamation** — exige aspected will crystals + gaia fragments + ethereal slates.
   Está no **Reclamation Rituals book**.
   ⚠️ **O ritual pode apagar blocos (void).** Execute longe de qualquer coisa que você preze.
2. Isso cria um **Reclaimed Biome** — céu azul, e **spawns naturais voltam a acontecer**
   (inclusive drygmy, whirlisprig e starbuncle raramente).
3. **Biome Essence** — `Empty Biome Bottle` → segure botão direito num bioma vivo.
   **Agachado, enche a stack inteira.**
4. **Attuned Biome Bottle** = attuned stone carregada + biome bottle + hellforged ingot +
   2 gaia spirits. Coleta essências **específicas**.
5. **As seis essências atuadas** (cada uma tem seu próprio ritual de terraformação):

   | Essência | Bioma alvo | Reagente-chave do ritual |
   |---|---|---|
   | **Hellish** | nether vivo | — (primeira, mais simples) |
   | **Arid** | deserto | artifício anão (Embers) de alta potência |
   | **Mycelic** | mushroom fields | prática wiccana clássica (Enchanted) |
   | **Watery** | warm ocean | magia elemental (Ars) + **plutônio** |
   | **Lush** | bamboo forest | maestria botânica + **plutônio** |
   | **Icy** | snowy slopes | **polônio** + sorvete de **baunilha** + shattered singularities + muita biome essence |

6. Com as seis → ritual (caro) → **End Portal**. Ainda precisa dos Eyes of Ender.
   - **Frame Remover** permite quebrar frames e blocos de portal com botão direito.
7. **Visite o End → mate o Ender Dragon.** 🏆 **Pack concluído.**

Depois disso: **Biome Globes** (ritual portátil, 16 usos, raio de 12 blocos — converte blocos
mas **não** coloca grama/árvores; ⚠️ **drenam MUITA aura**) e o capítulo de itens creative
(*The Taste of Power*): creative blaze cake, creative motor, creative ember source,
creative pool, creative source jar, creative energy cube, creative item cell.

---

## 13. Linhas paralelas

### 13.1 Complicated Bees — a linha de geração de recursos

Desbloqueia cedo (quest "Bees?!") e é **a rota mais confortável pra recursos** do pack.

- **Apiary** + **Scoop** (pra colher os ninhos).
- Abelhas **Wasteland / Desiccated / Dried** precisam de **dead bushes** como "flores".
- **Cadeia de melhoria:** Wasteland → Desiccated/Dried → **Rocky/Robust/Resilient**
  (precisam de **tuff embaixo do apiary**) → Common/Cultivated → Diligent (produtividade) /
  Noble (fertilidade, royal jelly) → nether: Crimson/Warped/Cursed → Haunted/Ghostly/Spectral
  (glowstone).
- 🔑 **Especialidades só saem quando a abelha está "ecstatic"** — o clima da casa precisa
  bater **exatamente** com o preferido dela. Ou você cria essa tolerância, ou usa **frames**
  pra ajustar temperatura/umidade.
- **Famílias que geram minério:** Cuprous, Ferrous, Plumbum, Argentum, Precious, Stannum,
  Zincum, Osimum, Radioactive · e minerais: Bituminous, Conductive, Luminous, Lapic, Amethyst,
  Dimantic, Emeradic, Quartz, Silicate, Fluorite.
- **Bees mágicas:** Natural (produz **Nature Essence** — necessária pras nature seeds),
  Botanic, Dawnstone, Willful, Source, Demonite, Terra.
- **Ferramentas:** Analyzer (custa 1 honey drop, mostra genes), Apid Library (mostra mutações
  possíveis), Microscope (pesquisa espécie → aumenta chance de mutação; ótimo destino
  pros drones sobrando).
- **Processamento:** Centrifuge + Furnace Generator → depois **Gyrofuge** (multibloco).
  Apiary → **Mellarium** (multibloco, muito mais slots de frame = *stacks* de comb por tick).
- **Upgrades** (propolis) — até 3 por máquina, **stacking multiplicativo**, igual aos frames.
- **Apiarist Gear** (feito de silk/propolis) — vestido completo, imuniza contra efeitos de abelha.
- ⚠️ **Não existe como tirar duas rainhas de um par.** Para mais ninhos, há um **ritual**
  (Reclamation Rituals book).

### 13.2 Mystical Agriculture

- **Prosperity Shard** — no seu pack: **copper nugget + picareta na cutting board (15% de chance)**,
  ou **Enrichment Chamber** (1:1, muito melhor quando tiver Mekanism).
- **Essence Farmland** (obrigatório pras essence seeds) + **Infusion Altar** com 8 pedestais.
- **Escada de essência:**
  `Inferium` (de matar mobs) → `Prudentium` (inferium + os 4 elementais **num Cauldron**)
  → `Tertium` (**Runic Altar** ou **Terra Plate**) → `Imperium` (Source + tertium,
  **Imbuement Chamber**) → `Supremium` (imperium ungido com **life essence**).
  - **Todos os tiers também podem ser feitos no Metallurgic Infuser** (o pack registra os
    infuse types `inferium/prudentium/tertium/imperium`).
- ⚠️ **Essence seeds não são clonáveis** — você precisa de 2+ pra começar a melhorar stats.
- **Growth Accelerators** aceleram o crop acima; tiers maiores têm **alcance maior**,
  então você empilha mais deles embaixo da farmland.
- **Watering Cans** — do Inferium até o **Awakened Supremium** (água infinita).
- **Harvester** — colheita 3×3, ampliável com machine upgrades.

### 13.3 Mob Safari (fotografia)

Linha secundária inteira baseada no mod **Exposure**: `Camera` + `Black and White Film` +
`Lightroom`. São ~75 fotos (mobs hostis, passivos, bosses, criaturas do Ars).
Recompensas são pilhas grandes de recurso (32 gunpowder, 16 ghast tears, nether star, etc.).
Completar tudo dá `Infinity Egg` + 32 creative blaze cakes + 16 pellets de antimatéria.

Dicas espalhadas nas quests: existe **ritual que concede Bad Omen** (pra pillagers),
o **sculk catalyst é craftável** e o **Sculk Awakener** converte um shrieker em um que
invoca Warden; o **sniffer egg é craftável**; wither skeleton vivo requer **Soulium Spawner**;
há **ritual que invoca o Elder Guardian**.

### 13.4 Comida e cozinha

- **Croptopia** (~60 crops + saplings frutíferos), **Farmer's Delight**, **Nether's Delight**.
- **Cooking for Blockheads** — o **Cooking Table** é o coração: crafta qualquer comida com
  o que estiver nos gabinetes.
  Módulos: **Fridge** (+ Ice Unit), **Oven** (+ Heating Unit pra rodar em energia),
  **Sink** (água infinita), **Tool Rack** (fornece panelas), **Cow in a Jar** (leite passivo —
  ⚠️ precisa ser fora do claim ou com proteção desligada), **Counter/Cabinet**.
- **ME Kitchen Station** (`appliedcooking`) — conecta a cozinha ao seu sistema ME.
- **Organic Compost** → **Rich Soil** (cresce mais rápido que farmland normal).
- **Colheita automática:** Horn/Drum of the Wild (Botania, + hopperhock = 100% automático),
  Harvester (Mystical Agriculture), Mechanical Harvester (Create).

### 13.5 Qualidade de vida

- **Via Romana** — viagem rápida por placas. Shift+clique esquerdo na placa inicial,
  depois na final, e **percorra o caminho a pé** por blocos de caminho.
  Se desviar, o trajeto é cancelado. Depois de vinculado, **soque a placa pra viajar**.
  Veja os blocos válidos buscando `#via_romana:path_block` no EMI.
- **Ferramentas AOE** — Hammer / Excavator (3×3) e **Broadaxe (3×3×3)**.
- **Sophisticated Backpacks / Storage**, **Storage Drawers** (+ Controller, Drawer Keys),
  **Building Gadgets 2** (precisam ser carregados), **Construction Wand**,
  **Rod of the Shifting Crust** (troca blocos por mana).
- **Chipped / Rechiseled / Copycats** — variantes decorativas quase infinitas.
- **Exposure, Xerca Music, Xerca Paint, Immersive Paintings** — conteúdo criativo/decorativo.

---

## 14. Gestão de Aura (a dúvida mais comum)

A aura do Nature's Aura é **por chunk** e **não se regenera sozinha**. Se o Natural Altar
parou de funcionar, é isso.

**Diagnóstico:** segure o **Environmental Eye**. Ande 16 blocos e a leitura muda —
é por chunk, então às vezes basta mover o altar para o chunk vizinho enquanto o antigo se recupera.

**O que DRENA aura:**
- Natural Altar (todo craft)
- **Bottled Sunlight** (cada clique com a Bottle and Cork)
- Biome Globes (muito)
- Conversion Catalyst

**O que REPÕE aura:**
| Gerador | Como funciona |
|---|---|
| **Ancient Sapling** | árvore crescida murcha as folhas quando a aura está baixa |
| **Flower Generator** | consome flores → aura. **Varie as espécies** ou o retorno cai |
| Crescimento de plantações / criação de animais | realimenta passivamente |
| **Creational Catalyst** (late) | remove o teto dos geradores |

**Regra prática:** altar sustentável = altar **+ 2 ou 3 geradores no mesmo chunk**.
O altar **nunca leva a aura a negativo** — ele simplesmente **para de funcionar**.

**Efeito colateral bom:** com aura alta, **dried earth vira dirt sozinho** e
**Aura Caches carregam sozinhos**.

---

## 15. Segredos e mecânicas escondidas do pack

Coisas que estão nos scripts KubeJS e **não aparecem no questbook**:

1. 🪙 **Bateia de cobre:** segure uma **Bowl (tigela)** e clique com botão direito em
   **gravel**. Aparece "Sifting for copper..." e há **25% de chance** de sair um copper nugget.
   Repetível, sem custo. É a melhor fonte de cobre do começo do jogo.
2. **Dead Log dropa carvão vegetal em 10% das vezes** ao ser quebrado.
3. **Cut Copper na cutting board rende ~8 lingotes por bloco** (6 garantidos + bônus).
4. **Prosperity Shard sai de copper nugget** na cutting board (15%) — muito antes do que
   a maioria dos jogadores percebe.
5. **Grama não dropa mais alho** (`enchanted:garlic` foi removido do loot).
6. **Wandering traders estão desligados** e a dificuldade é travada em **hard**.
7. **Chicken jockeys não spawnam** (o pack cancela).
8. As placas de metal (`create:copper_sheet`, `create:iron_sheet`) foram **removidas das tags**
   `forge:plates/*` — receitas de placa passam pelo **Stamper do Embers**.
9. O **Cold Frame** das abelhas teve durabilidade ajustada para 30 usos.
10. **Alder, Hawthorn e Rowan** (madeiras do Enchanted) têm receitas próprias no pack.
11. As lâmpadas do **Macaw's** usam **beeswax** no lugar de honeycomb vanilla.
12. **Ethylene foi nerfado** de propósito.

---

## 16. Erros comuns que travam o jogador

| Sintoma | Causa real |
|---|---|
| "O Natural Altar parou" | aura do chunk zerada — veja a seção 14 |
| "Bottled Sunlight não repõe aura" | ele **consome**; faça longe da base |
| "Hemoglobic fluid não sai" | o acumulador está sobre o **Sal Ammoniac Tank**; tem que ser o **Fluid Vessel** |
| "Ritual of the Forest não inicia" | regador não funciona (bug do mod) — use outro método |
| "A Cuprosia não cresce" | crop stick precisa estar **waterlogged**; com strength 1, só em **gravel** |
| "Minha planta não cresce" | agache e olhe pra ela: ela informa o solo necessário |
| "A máquina do Embers não faz nada" | falta **sinal de redstone** — quase tudo no Embers precisa |
| "Fake player / máquina não funciona no meu claim" | desligue a proteção do claim (OPAC) |
| "Pressure plate não ativa" | keybind OPAC (`'`) → desligue *Prot. Plates from Other* |
| "Cow in a Jar não pega a vaca" | OPAC bloqueia; faça fora do claim ou desligue proteção |
| "Receita do EMI parece errada" (destilaria) | ponha os ingredientes nos **dois slots que não são de jarro** |
| "Agronomic Sourcelink não gera nada" | ele **ignora crops de AgriCraft**; plante do jeito normal |
| "Meu budding certus quartz sumiu" | certus **degrada** com o tempo — precisa ser re-semeado |
| "Meu crystal seed do Embers voltou ao nível 1" | você moveu o cristal |
| "Meu Ignem Reactor não roda" | Catalysis e Combustion Chambers precisam de **combustível próprio** |

---

## 17. Referência rápida por mod

**Progressão obrigatória**
| Mod | Papel no pack |
|---|---|
| **Theurgy** | alquimia base — cria terra e ferro do nada; loop de metais no late |
| **Enchanted** | bruxaria — mutandis (saplings), altar de plantas, rituais, brilliant fiber |
| **AgriCraft** | genética de plantas — 5 stats, cruzamento, Cuprosia |
| **Nature's Aura** | aura por chunk, Natural Altar, ritual da grama, Offering Table, Altar of Birthing |
| **Botania** | mana, Pure Daisy (ouro!), Fel Pumpkin (blaze), Terrasteel, Alfheim |
| **Embers Rekindled** | ember infinito da bedrock, fundição, Dawnstone, alquimia por tentativa/erro |
| **Blood Magic** | gemas (diamante/lápis/ametista), Demon Realm, will |
| **Ars Nouveau** | Source, encantamentos, familiares, rituais, storage lectern |
| **Mekanism** | aço, energia, processamento de minério até 3,3×, reatores, antimatéria |
| **Applied Energistics 2** | armazenamento e autocraft digital |
| **Reclamation Util** | biome bottles, globes, frame remover — o endgame do pack |

**Geração de recursos (opcional, mas muito recomendado)**
Complicated Bees · Mystical Agriculture · Create

**Comida** Croptopia · Farmer's Delight · Nether's Delight · Cooking for Blockheads

**Utilitário/QoL** Sophisticated Backpacks/Storage · Storage Drawers · Building Gadgets 2 ·
Construction Wand · Via Romana · Akashic Tome · Jade · EMI · FTB Quests · Xaero's Maps ·
Open Parties and Claims · Quark · Supplementaries · Comforts · Gravestone · Clumps

**Decoração** Chipped · Rechiseled · Copycats · Macaw's (10 mods) · Create Deco ·
Simply Light · Antiblocks · Immersive Paintings

**Performance** Embeddium · Oculus · FerriteCore · ModernFix · ImmediatelyFast ·
Entity Culling · Krypton · Cupboard · GPU Memleak Fix

---

## 18. Os livros do pack

Junte todos no **Akashic Tome** logo no começo.

| Livro | Cobre |
|---|---|
| **FTB Quests** (`M` no jogo) | a espinha dorsal — 558 quests em 10 capítulos |
| **The Hermetica** (Modonomicon) | Theurgy / Spagyrics |
| **Book of Natural Aura** | Nature's Aura — inclui **os multiblocos e o Ritual of the Forest** |
| **Lexica Botania** | Botania (jogue no portal de Alfheim depois!) |
| **Ancient Codex** | Embers — comece em *Natural Energy*, leia com atenção |
| **Sanguine Scientiem** | Blood Magic — runas, rituais, Incense Altar |
| **Worn Notebook** | Ars Nouveau — familiares, glifos, rituais |
| **Apiarist Field Guide** | Complicated Bees — Mellarium, Gyrofuge, genética |
| **Reclamation Rituals** | 🔑 **exclusivo do pack** — ninhos de abelha, blaze real, budding amethyst, meteoro AE2, **terraformação e Ritual of Reclamation**. Faça: `livro + dried earth` |
| **AE2 Guide** (`guideme`) | redes, canais, autocraft |

---

*Manual gerado a partir da instância local em 31/08/2026 — Reclamation 2.3.2.*
*Se o pack for atualizado, receitas podem mudar: o EMI in-game é sempre a fonte definitiva.*
