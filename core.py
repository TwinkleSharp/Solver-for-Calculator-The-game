from ast import literal_eval


class meta:
    _k = lambda self, k, m, r, s: k    
    _m = lambda self, k, m, r, s: m    
    _s = lambda self, k, m, r, s: r + s
    
    def __init__(self, attrs, /):
        for key, val in attrs.items():
            setattr(self, key, val)
    
    def __call__(self, K, M, R, S, drop):
        k = self._k(K, M, R, S)
        m = self._m(K, M, R, S)
        s = self._s(K, M, R, S)
        s = drop(s) if s is not None and len(s) <= 6 else None
        return k, m, s


_k = lambda func: type("meta_k", (meta,), {"_k": func})
_m = lambda func: type("meta_m", (meta,), {"_m": func})
_s = lambda func: type("meta_s", (meta,), {"_s": func})

hack = _k( lambda self, k, m, r, s: k + literal_eval(self.op)               )   # hack: '[%]#' (% [=] + [or] -)
save = _m( lambda self, k, m, r, s: s                                       )   # save: 'Store'
abba = _s( lambda self, k, m, r, s: r + s + s[::-1]                         )   # abba: 'Mirror'
addi = _s( lambda self, k, m, r, s: f"{int(r + s) + (self.i + k)}"          )   # addi: '+#'
comp = _s( lambda self, k, m, r, s: r + s.translate(self._trans)            )   # comp: 'Inv10'
comp._trans = str.maketrans("123456789", "987654321")                           #
conv = _s( lambda self, k, m, r, s: r + s.replace(self.x, self.y)           )   # conv: '#=>#'
cube = _s( lambda self, k, m, r, s: r + f"{int(s) ** 3}"                    )   # cube: 'x^3' [or] '^3'
dcba = _s( lambda self, k, m, r, s: r + s[::-1]                             )   # dcba: 'Reverse'
detl = _s( lambda self, k, m, r, s: r + "0" + s[1:]                         )   # detl: '>>'
detr = _s( lambda self, k, m, r, s: r + "0" + s[:-1]                        )   # detr: '<<'
divi = _s( lambda self, k, m, r, s: self.d(*divmod(int(r + s), self.i + k)) )   # divi: '/#'
divi.d = lambda self, quotient, module: str(quotient) if module == 0 else None  #
emmi = _s( lambda self, k, m, r, s: r + str(self.i + k) + s                 )   # emmi: '>#'
imme = _s( lambda self, k, m, r, s: r + s + str(self.i + k)                 )   # imme: '#' [or] '<#'
load = _s( lambda self, k, m, r, s: (r + s + m) if m else None              )   # load: '$'
muli = _s( lambda self, k, m, r, s: f"{int(r + s) * (self.i + k)}"          )   # muli: 'x#' [or] '*#'
negi = _s( lambda self, k, m, r, s: ("" if r else "-") + s                  )   # negi: '+/-'
quad = _s( lambda self, k, m, r, s: f"{int(s) ** 2}"                        )   # quad: 'x^2' [or] '^2'
rotl = _s( lambda self, k, m, r, s: r + s[1:] + s[0]                        )   # rotl: 'Shift<'
rotr = _s( lambda self, k, m, r, s: r + s[-1] + s[:-1]                      )   # rotr: 'Shift>'
subi = _s( lambda self, k, m, r, s: f"{int(r + s) - (self.i + k)}"          )   # subi: '-#'
sumi = _s( lambda self, k, m, r, s: r + f"{sum(map(int, [*s]))}"            )   # sumi: 'SUM'


def join(v, Y):
    pow_v = 10 ** v
    pow_Y = 10 ** Y
    # 5 <- v -- Y -> 0
    def drop(s):
        num = int(s)
        sgn = 1 if num >= 0 else -1
        num = abs(num)
        while num >= pow_v:
            vH, vL = divmod(num, pow_v)
            sh, dp = divmod(vH, 10)
            num = int(sh * pow_v + dp * pow_Y + vL)
        return str(sgn * num)
    return drop


def solve(move, init, goal, drop, func):
    if drop == None:
        drop = lambda s: str(int(s)) # Avoid leading zero
    idx_func = tuple(enumerate(func))
    def step(move, K, M, S):
        if move == 0:
            return None
        R = ""
        if S[0] == "-":
            R, S = "-", S[1:]
        for i, f in idx_func:
            k, m, s = f(K, M, R, S, drop)
            if s is None:
                yield None
            elif s == goal:
                yield (i,)
            else:
                yield from ((i,) + x for x in step(move-1, k, m, s) if x)
    return filter(None, step(move, 0, None, init))


args_to_data = lambda move, init, goal, drop, func: {
    "move": move,
    "init": init,
    "goal": goal,
    "drop": drop,
    "func": func,
    }


data_to_args = lambda data: tuple(
    map(data.__getitem__, ("move", "init", "goal", "drop", "func")))

    
solution_min = lambda *args: min(solve(*args), key=len, default=())
