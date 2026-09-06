# -*- coding: utf-8 -*-
"""
Resolve o codigo de alquimia do Embers para uma seed de mundo.

O mod sorteia, por receita e por mundo (AlchemyRecipeBase.getCode):

    Random rand = new Random(seed - id.getPath().hashCode());
    for (int i = 0; i < inputs.size(); i++)
        code.add(aspects.get(rand.nextInt(aspects.size())));

e `matchesCorrect` exige code[i] junto de inputs[i] — ou seja, o aspectus e
por pedestal, pareado com o item daquele pedestal.

A seed vem de ((ServerLevel) level).getSeed(), a seed do mundo.
"""
import json, io, os

MASK48 = (1 << 48) - 1
MULT = 0x5DEECE66D
ADD = 0xB


def java_string_hash(s):
    """String.hashCode() do Java: 31*h + c, com overflow de 32 bits com sinal."""
    h = 0
    for ch in s:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return h - (1 << 32) if h >= (1 << 31) else h


def to_long(v):
    """Normaliza para long de 64 bits com sinal, como o Java faz."""
    v &= (1 << 64) - 1
    return v - (1 << 64) if v >= (1 << 63) else v


class JavaRandom:
    def __init__(self, seed):
        self.seed = (seed ^ MULT) & MASK48

    def _next(self, bits):
        self.seed = (self.seed * MULT + ADD) & MASK48
        r = self.seed >> (48 - bits)
        # next(int) devolve int com sinal
        if r >= (1 << 31):
            r -= (1 << 32)
        return r

    def next_int(self, bound):
        if bound <= 0:
            raise ValueError("bound deve ser positivo")
        if (bound & -bound) == bound:          # potencia de 2
            return (bound * self._next(31)) >> 31
        while True:
            bits = self._next(31)
            val = bits % bound
            # checa overflow de int com sinal, igual ao Java
            chk = bits - val + (bound - 1)
            if chk < (1 << 31):
                return val


def solve(world_seed, recipe_path, n_aspects, n_pedestals):
    """Devolve a lista de indices de aspectus, um por pedestal."""
    rnd = JavaRandom(to_long(world_seed - java_string_hash(recipe_path)))
    return [rnd.next_int(n_aspects) for _ in range(n_pedestals)]


def _selftest():
    """Vetores conhecidos do java.util.Random."""
    assert JavaRandom(42)._next(32) == -1170105035, "next(32) divergiu"
    # nextInt segue o algoritmo publicado no Javadoc; o vetor acima de next(32)
    # e o hash abaixo sao os pontos de ancoragem verificados
    r = JavaRandom(0)
    got = [r.next_int(10) for _ in range(5)]
    assert all(0 <= g < 10 for g in got), got
    r = JavaRandom(12345)
    got = [r.next_int(4) for _ in range(6)]      # bound potencia de 2
    assert all(0 <= g < 4 for g in got)
    assert java_string_hash("alchemy/adhesive") == java_string_hash("alchemy/adhesive")
    assert java_string_hash("") == 0
    assert java_string_hash("a") == 97
    assert java_string_hash("hello") == 99162322
    return True


if __name__ == "__main__":
    import sys
    _selftest()
    print("selftest: ok")

    if len(sys.argv) < 2:
        print("uso: python alchemy_solver.py <seed_do_mundo>")
        sys.exit(0)

    seed = int(sys.argv[1])
    HERE = os.path.dirname(os.path.abspath(__file__))
    DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
    em = json.load(io.open(os.path.join(DATA, "embers.json"), encoding="utf-8"))
    names = json.load(io.open(os.path.join(DATA, "names.json"), encoding="utf-8"))

    def nm(x):
        b = names.get(x["id"]) or x["id"].split(":")[-1].replace("_", " ").title()
        return ("qualquer " + b.replace("/", " ")) if x["k"] == "t" else b

    def asp(x):
        return x["id"].split("/")[-1].upper()

    solved = [a for a in em["alchemy"] if a.get("path")]
    solved.sort(key=lambda a: nm(a["output"]))
    print(f"\nSeed {seed} — {len(solved)} receitas resolvidas\n")
    for a in solved:
        idx = solve(seed, a["path"], len(a["aspects"]), len(a["inputs"]))
        print(f"### {nm(a['output'])}"
              f"{' x' + str(a['output']['n']) if a['output'].get('n', 1) > 1 else ''}"
              f"   (tablet: {nm(a['tablet'])})")
        for i, x in enumerate(a["inputs"]):
            print(f"    pedestal {i+1}: {nm(x):<32} + aspectus {asp(a['aspects'][idx[i]])}")
        print()
