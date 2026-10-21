"""Aula 3 — Exemplo 2: embeddings colocam SIGNIFICADO em números.

Como rodar:
    uv run python aulas/aula_03_modelos/02_embeddings_aipim.py             # real (centavos de centavo)
    MODO=fake uv run python aulas/aula_03_modelos/02_embeddings_aipim.py   # simulado

Gera o mapa de calor em saidas/aula03_similaridade.png
"""

import matplotlib

matplotlib.use("Agg")  # salva em arquivo, sem precisar de tela
import matplotlib.pyplot as plt

from assistente_ia.adapters.vector_store.memoria import cosseno
from assistente_ia.config import PASTA_SAIDAS, descrever_ambiente
from assistente_ia.container import criar_embeddings

print(descrever_ambiente(), "\n")

palavras = ["aipim", "mandioca", "macaxeira", "pão francês", "cacetinho", "bolacha", "biscoito", "carro"]
vetores = criar_embeddings().vetorizar_textos(palavras)
print(f"Cada palavra virou um vetor com {len(vetores[0])} números.\n")

matriz = [[cosseno(a, b) for b in vetores] for a in vetores]

print(f"{'':>12}" + "".join(f"{p[:9]:>10}" for p in palavras))
for palavra, linha in zip(palavras, matriz, strict=True):
    print(f"{palavra:>12}" + "".join(f"{v:>10.2f}" for v in linha))

PASTA_SAIDAS.mkdir(exist_ok=True)
figura, eixo = plt.subplots(figsize=(8, 6))
imagem = eixo.imshow(matriz, cmap="YlOrBr", vmin=0, vmax=1)
eixo.set_xticks(range(len(palavras)), palavras, rotation=45, ha="right")
eixo.set_yticks(range(len(palavras)), palavras)
eixo.set_title("Similaridade de cosseno entre embeddings")
figura.colorbar(imagem)
figura.tight_layout()
arquivo = PASTA_SAIDAS / "aula03_similaridade.png"
figura.savefig(arquivo, dpi=120)
print(f"\nMapa de calor salvo em {arquivo}")
print("Compare: no modo REAL, aipim/mandioca/macaxeira ficam próximos. No modo FAKE, não. Por quê?")
