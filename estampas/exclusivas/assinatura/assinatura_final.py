"""Assinatura MODESTINO final: cada laçada do rascunho do Jorge vira UMA curva contínua.
Nos cruzamentos, emenda o traço que chega com o que segue na mesma direção (como a mão fez),
depois alisa cada traço inteiro (spline) e aplica contorno uniforme com 3 faixas diagonais.
Rode da pasta: python3 assinatura_final.py"""
import os
import numpy as np
from scipy.interpolate import splprep, splev
import assinatura_suave as A

def emendar(segs):
    segs = [np.array(s, float)[:, ::-1] for s in segs]          # (x, y)
    def dire(s, ponta):  # direção saindo pela ponta
        a = s if ponta == 1 else s[::-1]
        k = min(12, len(a) - 1)
        v = a[-1] - a[-1 - k]; return v / (np.linalg.norm(v) + 1e-9)
    pontas = [(i, p) for i in range(len(segs)) for p in (0, 1)]
    pos = {(i, p): segs[i][-1 if p else 0] for i, p in pontas}
    par = {}
    cand = []
    for a in pontas:
        for b in pontas:
            if a[0] >= b[0]: continue
            if np.linalg.norm(pos[a] - pos[b]) > 14: continue
            cand.append((float(np.dot(dire(segs[a[0]], a[1]), -dire(segs[b[0]], b[1]))), a, b))
    for sc, a, b in sorted(cand, reverse=True):
        if sc < 0.3 or a in par or b in par: continue
        par[a], par[b] = b, a
    usado, tracos = set(), []
    for i in range(len(segs)):
        if i in usado: continue
        # anda até uma ponta livre
        cur, p = i, 0
        visto = {i}
        while (cur, p) in par and par[(cur, p)][0] not in visto:
            cur, q = par[(cur, p)]; visto.add(cur); p = 1 - q
        # agora percorre a partir de (cur, p)
        cadeia, ponta = [], p
        while True:
            usado.add(cur)
            s = segs[cur] if ponta == 0 else segs[cur][::-1]
            cadeia.append(s)
            fim = (cur, 1 - ponta)
            if fim not in par or par[fim][0] in usado: break
            cur, ponta = par[fim]
        tracos.append(np.vstack(cadeia))
    return tracos

def alisar(a):
    a = a[::3]
    if len(a) < 8: return a
    _, idx = np.unique(np.round(a, 1), axis=0, return_index=True); a = a[np.sort(idx)]
    tck, _ = splprep([a[:, 0], a[:, 1]], s=len(a) * 14.0, k=3)
    x, y = splev(np.linspace(0, 1, max(20, len(a))), tck)
    return np.c_[x, y]

def main():
    esq = A.esqueleto()
    segs = A.caminhos(esq)
    tracos = [alisar(t) for t in emendar(segs)]
    tracos = [t for t in tracos if np.linalg.norm(t[-1] - t[0]) + len(t) > 60]
    A.salvar(tracos) if hasattr(A, 'salvar') else None
    return tracos

if __name__ == '__main__':
    t = main(); print(len(t), 'traços contínuos')
