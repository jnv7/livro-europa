# A Europa, País a País

Livro infantil com um cartão por país da Europa (geográfica — **50 países**,
incluindo Turquia e o Cáucaso), no mesmo espírito do
"Portugal, Distrito a Distrito".

## Ficheiros

| Ficheiro | O que é |
|---|---|
| `index.html` | O livro. Abre no browser; trata da renderização, dos cartões e das quebras de página. |
| `dados-paises.js` | Os dados de todos os países. **É aqui que se edita o conteúdo.** Lista JSON dentro de uma variável (lê-se de `file://` sem servidor). |
| `mapas/europa.svg` | Mapa da Europa com os 50 países pintados e rotulados. |
| `CREDITOS-FOTOS.md` | Autor e licença de cada foto de monumento. |
| `pdf/livro-europa.pdf` | Export para impressão (18 páginas). |

## Como usar

1. Abre `index.html` num browser (Chrome de preferência).
2. Exportar: **Imprimir → Guardar como PDF**, tamanho **A4**, margens **Nenhumas**,
   com **"Gráficos de fundo"** ativado.

**Precisa de internet** ao abrir/imprimir: as bandeiras (CDN jsdelivr) e as fotos
dos monumentos (Wikimedia Commons) são carregadas online. Se faltar rede, os
cartões aparecem à mesma, sem imagem (a bandeira mostra o código do país).

## Configuração

No topo do `<script>` em `index.html`:

```js
const CONFIG = {
  colunas: 2,          // cartões por linha
  linhas: 2,           // linhas por folha  -> 4 cartões por folha
  mostrarFoto: true,   // foto do monumento em cada cartão
  bandeirasBase: 'https://cdn.jsdelivr.net/gh/lipis/flag-icons@7.5.0/flags/4x3/',
  tituloFolha: 'A Europa, País a País'
};
```

- `colunas` × `linhas` = número **fixo** de cartões por folha.
- A partir de 6/folha os cartões compactam-se; a partir de 9/folha escondem a foto
  e a curiosidade.
- `mostrarFoto: false` volta ao cartão só-texto (aguenta mais cartões por folha).

## Editar os dados

Cada país em `dados-paises.js`:

```js
{
  "nome": "Portugal",
  "endonimo": "Portugal",           // nome na língua oficial
  "iso": "pt",                      // código de 2 letras (bandeira)
  "ue": true,                       // membro da UE -> emoji 🇪🇺 no governo
  "capital": "Lisboa",
  "cidades": ["Lisboa", "Porto", "Coimbra"],  // capital primeiro (fica a negrito)
  "populacao": 10467000,            // número cru de habitantes
  "area": 92230,                    // km²
  "moeda": "Euro (€)",
  "idioma": "Português (e mirandês)",
  "governo": "República semipresidencial",
  "monumento": "Mosteiro dos Jerónimos, Lisboa",
  "foto": "https://commons.wikimedia.org/wiki/Special:FilePath/...jpg?width=620",
  "fotoCredito": "ficheiro — autor / licença · Wikimedia Commons",
  "curiosidade": "..."
}
```

- **Ordem da lista = ordem no livro** (por região, de Portugal para fora).
- Rankings de população e área são **calculados** — não se escrevem.
- Trocar uma foto: mete outro URL `Special:FilePath/<Ficheiro>?width=620` e
  atualiza o `fotoCredito`.

## Mapa

`mapas/europa.svg` é o "Blank map of Europe" (Wikimedia, CC BY-SA 3.0) com um
`<style>` injetado que pinta os países do livro e uma camada de rótulos.
Se acrescentares/removeres países, o mapa **não** se atualiza sozinho — é preciso
voltar a correr o gerador (guardado no histórico do projeto) ou editar o SVG à mão.

## Créditos

- Bandeiras: [flag-icons](https://github.com/lipis/flag-icons) (lipis) — MIT / domínio público.
- Mapa: "Blank map of Europe", *maix* (Wikimedia Commons), CC BY-SA 3.0 — cores adaptadas.
- Fotos: Wikimedia Commons, licenças livres — ver `CREDITOS-FOTOS.md`.
- Texto elaborado com recurso a IA; números arredondados, sem valor oficial.
- Sem fins comerciais.
