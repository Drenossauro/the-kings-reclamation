# -*- coding: utf-8 -*-
"""
Objetivos: o eixo de navegacao da wiki.

Em vez de "um mod = uma pagina", cada pagina responde a uma pergunta que o
jogador faz quando trava. A prosa da o caminho; os blocos `rotas` sao
resolvidos pelo banco de receitas em tempo de execucao, entao a pagina nao
envelhece quando o pack mudar.

Campos de um objetivo:
  id       arquivo gerado (obj-<id>.html)
  nav      rotulo curto no seletor
  titulo   H1
  lede     paragrafo de abertura
  quando   quando voce cai nesta pagina (mostrado como badge)
  blocos   lista de secoes:
             {"h": titulo, "html": prosa}                  -> texto
             {"h": titulo, "itens": [id, ...], "nota": ""} -> receitas do banco
"""

GOALS = [
    # ------------------------------------------------------------------ 1
    {
        "id": "sobreviver",
        "nav": "Sobreviver",
        "titulo": "Sobreviver ao começo",
        "lede": "Você acordou num deserto morto, sem minério e sem árvore viva. "
                "Esta página cobre as primeiras horas: o que dá pra quebrar, o que dá "
                "pra comer e como tirar o primeiro metal do chão.",
        "quando": "primeiras horas · antes de ter terra",
        "blocos": [
            {"h": "O que existe no mundo", "html": """
<p>Vale internalizar isso antes de perder tempo: <strong>nenhum minério gera</strong>,
os únicos biomas são deserto morto, e as únicas árvores são mortas. Variantes de pedra
ainda geram, e <strong>areia e argila existem debaixo d'água</strong>.</p>
<p>Zombie villager e bruxa não spawnam — não há como tirar recurso deles. Aranha só
aparece na versão <em>cave spider</em>, venenosa. Wandering trader está desligado e a
dificuldade é travada em <strong>hard</strong>.</p>"""},
            {"h": "Cobre: o primeiro metal", "html": """
<p>Nas ruínas há <strong>Oxidized Cut Copper</strong>. Raspe a ferrugem com um machado
até virar Cut Copper, e processe na <strong>Cutting Board</strong> do Farmer's Delight —
rende cerca de <strong>8 lingotes por bloco</strong> (6 garantidos, +2 a 75%, +1 a 50%).</p>""",
             "itens": ["minecraft:copper_ingot"]},
            {"h": "A fonte infinita de cobre que ninguém conta", "html": """
<div class="note secret"><span class="lbl">Não está em nenhuma quest</span>
<p>Segure uma <strong>tigela (Bowl)</strong> e clique com botão direito em
<strong>gravel</strong>. Aparece <em>"Sifting for copper..."</em> e há
<strong>25% de chance</strong> de sair um copper nugget. Repetível, sem custo, sem
ferramenta. É a melhor fonte de cobre do começo.</p></div>"""},
            {"h": "Madeira e comida", "html": """
<p>As árvores mortas dão <strong>Dead Log</strong> → <strong>Flimsy Planks</strong>, e
cada log tem <strong>10% de chance de dropar carvão vegetal</strong> direto. A cutting
board também tira mais carvão e scrap wood deles.</p>
<p><strong>Peixe</strong> é a comida inicial — fatiar na cutting board rende mais. A
<strong>Flimsy Door</strong> quebra sozinha de vez em quando; é proposital.</p>"""},
            {"h": "Ajustes que evitam dor de cabeça", "html": """
<div class="note warn"><span class="lbl">Faça agora</span>
<p><strong>Desligue a proteção do claim</strong> (OPAC). Ela quebra fake players, que é
como boa parte das máquinas do pack age. Recomendação do próprio autor do pack.</p>
<p>Junte todo livro-guia no <strong>Akashic Tome</strong>. E lembre que
<kbd>R</kbd> mostra como fazer e <kbd>U</kbd> mostra onde usa, no EMI.</p></div>"""},
        ],
    },
    # ------------------------------------------------------------------ 2
    {
        "id": "terra",
        "nav": "Terra e grama",
        "titulo": "Fazer terra e grama",
        "lede": "O gargalo de abertura do pack. Terra não existe: você precisa criá-la "
                "por alquimia. E grama não é craft — é ritual.",
        "quando": "logo após o cobre · destrava tudo",
        "blocos": [
            {"h": "Terra, via Theurgy", "html": """
<p>Todo item se decompõe em três princípios, e recombinando os três você cria o item.
As três máquinas ficam <strong>em cima de um Pyromantic Brazier</strong>.</p>
<div class="tbl"><table>
<thead><tr><th>Princípio</th><th>O que é</th><th>Máquina</th></tr></thead><tbody>
<tr><td><strong>Mercury</strong></td><td>a energia — genérico</td><td>Distiller</td></tr>
<tr><td><strong>Salt</strong></td><td>o corpo — o "tipo"</td><td>Calcination Oven</td></tr>
<tr><td><strong>Sulfur</strong></td><td>a alma — qual item é</td><td>Liquefaction Cauldron</td></tr>
</tbody></table></div>
<p>O <strong>Dried Earth</strong> lembra que já foi terra: liquefazendo ele com Sal
Ammoniac sai <strong>Dirt Sulfur</strong>. Junte os três no <strong>Incubator</strong>.</p>""",
             "itens": ["minecraft:dirt", "theurgy:sal_ammoniac_accumulator"]},
            {"h": "Grama, via ritual", "html": """
<p>Com terra vêm sementes de tufos sobreviventes. Use <strong>Mutandis</strong>
(bruxaria) para transformar <em>dead bushes</em> em saplings de verdade, cresça uma
árvore e aplique <strong>Brilliant Fiber</strong> nas folhas: elas douram e viram
<strong>Gold Leaf</strong> → <strong>Gold Powder</strong>.</p>
<p>Com 4 <strong>Wood Stands</strong> e 16 Gold Powder em volta de um birch sapling você
faz o <strong>Ritual of the Forest</strong>, que produz as <strong>Pasture Seeds</strong>.</p>
<div class="note warn"><span class="lbl">Bug do mod</span>
<p>Regador <strong>não</strong> inicia o Ritual of the Forest.</p></div>""",
             "itens": ["botania:grass_seeds", "naturesaura:gold_powder"]},
            {"h": "Depois da grama", "html": """
<p>Bonemeal numa área grande de grama gera <strong>flores</strong>, que dão tinta e
destravam Botania. E com aura alta o <strong>Dried Earth vira Dirt sozinho</strong> —
veja <a href="obj-energia.html">Energia</a> para a parte de aura.</p>"""},
        ],
    },
    # ------------------------------------------------------------------ 3
    {
        "id": "metal",
        "nav": "Metal",
        "titulo": "Conseguir metal",
        "lede": "Sem minério no mundo, todo metal vem de alquimia, abelha, planta ou "
                "cristal. Abaixo, a rota de cada um — e todas as receitas reais do "
                "seu pack para obtê-lo.",
        "quando": "o tempo todo · é o recurso mais escasso",
        "blocos": [
            {"h": "Ferro: a rota do sangue de planta", "html": """
<p>Colha <strong>Mandrake Root</strong> <em>à noite</em> (de dia ela grita; faça
Earmuffs). Ela produz sangue: ponha o Sal Ammoniac Accumulator
<strong>em cima de um Fluid Vessel</strong> — não do tank — para obter
<strong>Hemoglobic Fluid</strong>.</p>
<p>Use o fluido como <strong>solvente no Liquefaction Cauldron</strong> para liquefazer
cobre: o ferro do fluido converte o sulfur de cobre em <strong>Iron Sulfur</strong>.
Junte com Mineral Salt (calcine carvão) e Mercury no Incubator.</p>""",
             "itens": ["minecraft:iron_ingot"]},
            {"h": "Cobre renovável", "html": """
<p>Além da bateia com tigela em gravel, a flor <strong>Cuprosia</strong> (AgriCraft)
extrai cobre da água. Ela só cresce em crop stick <strong>alagado</strong> e, com
strength 1, <strong>só em gravel</strong>.</p>""",
             "itens": ["minecraft:copper_ingot"]},
            {"h": "Chumbo, Dawnstone e o resto do Embers", "html": """
<p><strong>Raw Lead</strong> sai de ferro infundido em natureza + nether bricks + spruce
sapling — e traz o Ancient Codex junto. <strong>Dawnstone</strong> vem do Mixer
Centrifuge, com cobre e ouro fundidos entrando por <strong>lados diferentes</strong>.</p>""",
             "itens": ["embers:lead_ingot", "embers:dawnstone_ingot", "embers:silver_ingot"]},
            {"h": "Ouro: a jogada do Pure Daisy", "html": """
<p>Receita exclusiva deste pack: a <strong>Pure Daisy</strong> converte
<strong>Golden Nether Brick</strong> em <strong>Nether Gold Ore</strong>. É assim que
se faz ouro aqui.</p>""",
             "itens": ["minecraft:gold_ingot"]},
            {"h": "Zinco e os crystal seeds", "html": """
<p>Zinco vem de <strong>Crystal Seed</strong>: uma attuned stone carregada vira semente
que converte ember em metal puro, alimentada por <strong>Ember Injector</strong>.</p>
<div class="note warn"><span class="lbl">O pack reescreveu isso</span>
<p>As receitas originais de crystal seed foram removidas. As novas exigem
<strong>Attuned Stone Charged</strong> (Enchanted) e <strong>runas</strong> (Botania).
E <strong>Gold, Silver e Tin Crystal Seed não têm substituta</strong> — sumiram.</p>
<p>Mover um cristal <strong>reseta o nível</strong> dele.</p></div>""",
             "itens": ["create:zinc_ingot", "mekanism:ingot_osmium", "mekanism:ingot_steel"]},
            {"h": "O loop que multiplica metal", "html": """
<p>Com o Theurgy avançado dá pra transmutar metal em metal. O
<strong>Fermentation Vat</strong> converte entre tipos e o <strong>Digestion Vat</strong>
entre raridades, na proporção <strong>4 do tier anterior ↔ 1 do próximo</strong>.</p>
<p>O caminho famoso: iron sulfur → common metal niter → 4 abundant metal niter →
<strong>4 copper sulfur</strong>. Ou seja, <strong>4 cobre por ferro</strong>, e os vats
aceitam redstone, então dá pra automatizar.</p>"""},
        ],
    },
    # ------------------------------------------------------------------ 4
    {
        "id": "energia",
        "nav": "Energia",
        "titulo": "Conseguir energia",
        "lede": "São cinco energias diferentes e elas não se substituem: Ember, Aura, "
                "Mana, Source e RF. Cada máquina quer a sua. Esta página diz qual você "
                "precisa e como conseguir.",
        "quando": "quando uma máquina não liga",
        "blocos": [
            {"h": "Qual energia serve para quê", "html": """
<div class="tbl"><table>
<thead><tr><th>Energia</th><th>Mod</th><th>Move</th></tr></thead><tbody>
<tr><td><strong>Ember</strong></td><td>Embers</td><td>fundição, estampagem, alquimia de aspectus</td></tr>
<tr><td><strong>Aura</strong></td><td>Nature's Aura</td><td>Natural Altar, transmutações, Altar of Birthing</td></tr>
<tr><td><strong>Mana</strong></td><td>Botania</td><td>flores, Terrasteel, e vira RF no Mana Fluxfield</td></tr>
<tr><td><strong>Source</strong></td><td>Ars Nouveau</td><td>encantamento, rituais, familiares</td></tr>
<tr><td><strong>RF</strong></td><td>Mekanism / AE2</td><td>máquinas, reatores, rede ME</td></tr>
</tbody></table></div>"""},
            {"h": "Ember: infinito, no fundo do mundo", "html": """
<p>O <strong>Ember Bore</strong> vai <strong>sobre a bedrock</strong>, com um
<strong>Mechanical Core</strong> em cima. Precisa de 3 blocos de
<code>embers:world_bottom</code> encostando nas lâminas, abaixo de <strong>Y −57</strong>.
Sai Ember Shard 60%, Crystal 20%, Grit 20%.</p>
<div class="note warn"><span class="lbl">Regra do Embers</span>
<p><strong>Quase tudo precisa de sinal de redstone.</strong> Máquina parada quase sempre
é alavanca faltando. E use o <strong>Tinker's Lens</strong> pra ver o fluxo.</p></div>
<p>Detalhes e a escalada de eficiência estão no <a href="embers.html">guia do Embers</a>.</p>""",
             "itens": ["embers:ember_bore", "embers:copper_cell"]},
            {"h": "Aura: por chunk, e não volta sozinha", "html": """
<p>A aura é <strong>por chunk</strong> e <strong>não se regenera</strong>. Se o Natural
Altar parou, é isso. Segure o <strong>Environmental Eye</strong> pra medir.</p>
<p><strong>Drena:</strong> Natural Altar, Bottled Sunlight, Biome Globes, Conversion
Catalyst. <strong>Repõe:</strong> Ancient Sapling, Flower Generator (varie as flores!),
plantações e criação de animais.</p>
<div class="note tip"><span class="lbl">Regra prática</span>
<p>Altar sustentável = altar <strong>+ 2 ou 3 geradores no mesmo chunk</strong>. O altar
nunca leva a aura a negativo — ele só para de funcionar.</p></div>""",
             "itens": ["naturesaura:nature_altar", "naturesaura:flower_generator"]},
            {"h": "Mana e RF", "html": """
<p>Comece pelo <strong>Endoflame</strong>. Depois Thermalily (lava), Entropinnyum (TNT,
um dos melhores) e Munchdew (folhas). Use <strong>Sparks</strong> no lugar de spreaders
quando o volume crescer.</p>
<p>Para RF, o caminho curto é o <strong>Mana Fluxfield</strong>: aponte um spreader nele
e sai RF. Depois, <strong>Aerated Essence</strong> no Gas-Burning Generator carrega o
mid-game inteiro.</p>""",
             "itens": ["botania:mana_fluxfield", "mekanismgenerators:gas_burning_generator"]},
        ],
    },
    # ------------------------------------------------------------------ 5
    {
        "id": "comida",
        "nav": "Comida",
        "titulo": "Plantar e comer",
        "lede": "Sementes existem, mas nasceram adaptadas à seca: produzem pouco. "
                "AgriCraft é o sistema que conserta isso, e é onde a maioria trava.",
        "quando": "assim que tiver terra",
        "blocos": [
            {"h": "Os cinco stats", "html": """
<div class="tbl"><table>
<thead><tr><th>Stat</th><th>Efeito</th></tr></thead><tbody>
<tr><td><strong>Fertility</strong></td><td>chance de ser escolhida como mãe</td></tr>
<tr><td><strong>Gain</strong></td><td>quanto produz ao colher</td></tr>
<tr><td><strong>Growth</strong></td><td>velocidade</td></tr>
<tr><td><strong>Mutativity</strong></td><td>chance do cruzamento ser bom</td></tr>
<tr><td><strong>Strength</strong></td><td>amplia os solos e ambientes aceitos</td></tr>
</tbody></table></div>
<div class="note tip"><span class="lbl">O truque que muda o início</span>
<p>Plante em <strong>cruz (+)</strong> com o crop stick vazio no meio: o cruzamento passa
a ter <strong>4 chances</strong> de escolher pais em vez de 2.</p>
<p>E <strong>Strength</strong> é o stat mais subestimado — com ele alto, a planta aceita
solos que normalmente recusaria.</p></div>
<p>A tabela completa de requisitos e as 124 mutações estão em
<a href="plantas.html">Plantas</a>.</p>"""},
            {"h": "Cozinha", "html": """
<p>O <strong>Cooking Table</strong> é o coração: crafta qualquer comida com o que estiver
nos gabinetes. Módulos: Fridge, Oven, Sink (água infinita), Tool Rack e Cow in a Jar.</p>
<p><strong>Organic Compost</strong> vira <strong>Rich Soil</strong>, que cresce mais
rápido que farmland. E o <strong>Composter</strong> transforma semente sobrando em
bonemeal.</p>""",
             "itens": ["cookingforblockheads:cooking_table", "farmersdelight:organic_compost"]},
        ],
    },
    # ------------------------------------------------------------------ 6
    {
        "id": "automatizar",
        "nav": "Automatizar",
        "titulo": "Automatizar recursos",
        "lede": "Quando a coleta manual vira gargalo. Abelhas e Mystical Agriculture são "
                "as duas rotas grandes; nenhuma é obrigatória, e as duas mudam o jogo.",
        "quando": "meio de jogo · quando cansar de minerar",
        "blocos": [
            {"h": "Abelhas: a rota mais confortável", "html": """
<p>Desbloqueia cedo. Apiary + Scoop, e abelhas Wasteland usam <strong>dead bushes</strong>
como flores.</p>
<div class="note warn"><span class="lbl">A regra que trava todo mundo</span>
<p>Especialidades <strong>só saem com a abelha "ecstatic"</strong> — o clima da casa tem
que bater <strong>exatamente</strong> com o preferido dela. Ou você cria essa tolerância,
ou usa <strong>frames</strong> pra ajustar temperatura e umidade.</p></div>
<p>Há abelha para metal, mineral e até produto mágico. As 77 espécies e 85 mutações estão
em <a href="abelhas.html">Abelhas</a>.</p>"""},
            {"h": "Mystical Agriculture", "html": """
<p><strong>Prosperity Shard</strong> sai de copper nugget na cutting board (15%) ou, bem
melhor, 1:1 no <strong>Enrichment Chamber</strong>.</p>
<p>A escada é Inferium → Prudentium → Tertium → Imperium → Supremium, e
<strong>todos os tiers também saem no Metallurgic Infuser</strong>.</p>
<div class="note warn"><span class="lbl">Pegadinha</span>
<p><strong>Essence seeds não são clonáveis</strong> — você precisa de 2 ou mais para
começar a melhorar stats.</p></div>""",
             "itens": ["mysticalagriculture:prosperity_shard", "mysticalagriculture:inferium_essence"]},
            {"h": "Colheita e logística", "html": """
<p>Colheita automática: <strong>Drum of the Wild</strong> + hopperhock (Botania),
<strong>Harvester</strong> (Mystical Agriculture) ou <strong>Mechanical Harvester</strong>
(Create). Para mover item sem tubo, o <strong>Starbuncle</strong> do Ars resolve.</p>"""},
        ],
    },
    # ------------------------------------------------------------------ 7
    {
        "id": "gemas",
        "nav": "Gemas",
        "titulo": "Conseguir gemas e cristais",
        "lede": "Diamante, lápis, ametista e quartzo não existem no mundo. Todos passam "
                "por Blood Magic — e é esse gargalo que destrava Ars Nouveau e AE2.",
        "quando": "quando precisar de diamante ou lápis",
        "blocos": [
            {"h": "A porta: Alchemical Reaction Chamber", "html": """
<p>Você precisa de um <strong>Blood Altar tier 3</strong> para fazer Imbued Slates, que
fazem a <strong>Alchemical Reaction Chamber</strong>. Ela produz
<strong>diamante, lápis e ametista</strong>.</p>
<p>Para chegar lá: Soul Snares nos monstros (antes de matar) dão Demonic Will;
o auto-sacrifício alimenta o altar. Quanto <strong>mais will você carrega, mais will
os monstros dropam</strong>.</p>""",
             "itens": ["minecraft:diamond", "minecraft:amethyst_shard", "minecraft:lapis_lazuli"]},
            {"h": "Tornando renovável", "html": """
<p><strong>Budding Amethyst</strong> sai de um ritual wiccano sobre um bloco de ametista.
O pentagrama de <strong>arcane ashes</strong> no altar dá <strong>+1,5×</strong> de
capacidade.</p>
<p>Para AE2: <strong>Charger + diamante enriquecido</strong> dá certus quartz; jogar um
bloco de certus na água com charged certus faz <strong>budding quartz</strong>.
Diferente da ametista, o certus <strong>degrada</strong> e precisa ser re-semeado.</p>""",
             "itens": ["minecraft:budding_amethyst", "ae2:charged_certus_quartz_crystal"]},
        ],
    },
    # ------------------------------------------------------------------ 8
    {
        "id": "vida",
        "nav": "Vida animal",
        "titulo": "Trazer os animais de volta",
        "lede": "Não existe animal no mundo. Você precisa literalmente fabricar a "
                "primeira galinha — e a partir dela, o resto da fauna.",
        "quando": "depois da aura estável",
        "blocos": [
            {"h": "A primeira galinha", "html": """
<p>Na <strong>Offering Table</strong> você infunde itens em versões empoderadas. Com os
quatro amálgamas do pack (Feather-Flesh, Blooded, Mana-Dosed e Infused) sai o
<strong>Chicken Spawn Egg</strong>.</p>
<div class="note warn"><span class="lbl">A Offering Table mudou neste pack</span>
<p>A receita normal do Nature's Aura <strong>foi removida</strong>. A única via é
<strong>alquimia do Embers</strong>, e ela consome um <strong>Runic Altar</strong>
inteiro. A combinação de aspectus está no
<a href="embers.html">solver do Embers</a>.</p></div>""",
             "itens": ["naturesaura:offering_table", "minecraft:chicken_spawn_egg"]},
            {"h": "Altar of Birthing", "html": """
<p>Em área de <strong>aura alta</strong>, acasalar mobs gera <strong>Spirits of
Birthing</strong>. Jogue o spirit e os reagentes no altar para invocar criaturas novas —
inclusive Siren, Whirlisprig, Drygmy, Wixie e Starbuncle.</p>
<p>O <strong>Drygmy</strong> merece destaque: ele gera drops e XP de mobs
<strong>sem matar nenhum</strong>.</p>""",
             "itens": ["naturesaura:animal_spawner"]},
        ],
    },
    # ------------------------------------------------------------------ 9
    {
        "id": "endgame",
        "nav": "Reclamar o mundo",
        "titulo": "Reclamar biomas e abrir o End",
        "lede": "A reta final: devolver os biomas ao mundo e, com as seis essências "
                "atuadas, abrir o portal do End.",
        "quando": "endgame",
        "blocos": [
            {"h": "Ritual of Reclamation", "html": """
<p>Exige aspected will crystals, gaia fragments e ethereal slates. Está no
<strong>Reclamation Rituals</strong>, o livro exclusivo do pack.</p>
<div class="note warn"><span class="lbl">Atenção</span>
<p>O ritual <strong>pode apagar blocos</strong>. Execute longe de qualquer coisa que
você preze.</p></div>
<p>O resultado é um <strong>Reclaimed Biome</strong>, onde <strong>spawns naturais voltam
a acontecer</strong>.</p>"""},
            {"h": "As seis essências", "html": """
<p>Colete com a <strong>Biome Bottle</strong> segurando botão direito num bioma vivo —
<strong>agachado enche a stack inteira</strong>. A versão atuada exige attuned stone
carregada, hellforged ingot e 2 gaia spirits.</p>
<div class="tbl"><table>
<thead><tr><th>Essência</th><th>Bioma</th><th>Reagente-chave</th></tr></thead><tbody>
<tr><td>Hellish</td><td>nether vivo</td><td>— (a primeira)</td></tr>
<tr><td>Arid</td><td>deserto</td><td>artifício anão de alta potência</td></tr>
<tr><td>Mycelic</td><td>mushroom fields</td><td>prática wiccana</td></tr>
<tr><td>Watery</td><td>warm ocean</td><td>magia elemental + plutônio</td></tr>
<tr><td>Lush</td><td>bamboo forest</td><td>maestria botânica + plutônio</td></tr>
<tr><td>Icy</td><td>snowy slopes</td><td>polônio + sorvete de baunilha + shattered singularities</td></tr>
</tbody></table></div>
<p>Com as seis, um ritual caro produz o <strong>End Portal</strong> — ainda faltam os
Eyes of Ender. Depois é matar o dragão.</p>""",
             "itens": ["reclamation_util:filled_biome_bottle", "reclamation_util:attuned_biome_bottle"]},
        ],
    },
]
