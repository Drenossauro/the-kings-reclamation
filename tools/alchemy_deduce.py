# -*- coding: utf-8 -*-
"""
Deduz o codigo de alquimia a partir das tentativas, como um Mastermind.

Nao depende da seed: usa so o que o jogo devolve no Alchemical Waste
(blackPins / whitePins), reproduzindo o algoritmo de AlchemyRecipeBase.

  whitePins bruto: para cada pedestal, casa o aspecto contra o code restante
  blackPins: casa (code[i], inputs[i]) contra os pedestais restantes
  whitePins final = bruto - blackPins
"""
import itertools, json, io, os, sys


def pins(code, inputs, attempt):
    """
    code    : lista de indices de aspectus, um por input (o segredo)
    inputs  : lista de ids de ingrediente da receita, na ordem do JSON
    attempt : lista de (input_id, aspect_idx) colocados nos pedestais
    """
    # whitePins bruto: aspecto presente no code, em qualquer lugar
    remaining_code = list(code)
    white = 0
    for _, asp in attempt:
        for j, c in enumerate(remaining_code):
            if c == asp:
                white += 1
                remaining_code.pop(j)
                break

    # blackPins: par (aspecto, ingrediente) correto
    remaining = list(attempt)
    black = 0
    for i, inp in enumerate(inputs):
        for j, (a_inp, a_asp) in enumerate(remaining):
            if code[i] == a_asp and inp == a_inp:
                black += 1
                remaining.pop(j)
                break
    return black, white - black


def candidates(inputs, n_aspects, observations):
    """observations: lista de (attempt, black, white)."""
    out = []
    for code in itertools.product(range(n_aspects), repeat=len(inputs)):
        if all(pins(code, inputs, att) == (b, w) for att, b, w in observations):
            out.append(code)
    return out


def load(recipe_name):
    HERE = os.path.dirname(os.path.abspath(__file__))
    DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
    em = json.load(io.open(os.path.join(DATA, "embers.json"), encoding="utf-8"))
    for a in em["alchemy"]:
        if a.get("name") == recipe_name or a.get("path", "").endswith("/" + recipe_name):
            return a
    raise SystemExit(f"receita '{recipe_name}' nao encontrada")


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "ember_crystal_cluster"
    a = load(name)
    inputs = [x["id"] for x in a["inputs"]]
    asp = [x["id"].split("/")[-1].upper() for x in a["aspects"]]
    print(f"receita : {a.get('path')}")
    print(f"aspectus: {dict(enumerate(asp))}")
    print(f"inputs  : {[i.split(':')[-1].split('/')[-1] for i in inputs]}")
    print(f"espaco  : {len(asp)}^{len(inputs)} = {len(asp)**len(inputs)} codigos\n")

    # tentativa que o solver por seed sugeriu
    import alchemy_solver as A
    SEED = -729460952624480606
    guess = A.solve(SEED, a["path"], len(asp), len(inputs))
    attempt = [(inputs[i], guess[i]) for i in range(len(inputs))]
    print("tentativa sugerida pelo solver (indice de aspectus por input):")
    for i, inp in enumerate(inputs):
        print(f"   {inp.split(':')[-1].split('/')[-1]:<14} + {asp[guess[i]]}")

    print("\nse os pontos observados forem (brilhantes, palidos), sobram:")
    print("  brilh. palidos | candidatos")
    for b in range(len(inputs) + 1):
        for w in range(len(inputs) + 1 - b):
            c = candidates(inputs, len(asp), [(attempt, b, w)])
            if c:
                print(f"  {b:>6} {w:>7} | {len(c):>3} codigo(s)"
                      + (f"  -> {[ [asp[i] for i in x] for x in c[:2] ]}" if len(c) <= 3 else ""))
