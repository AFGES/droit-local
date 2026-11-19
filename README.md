# Droit local d'Alsace-Moselle

Lois et règlements locaux d'Alsace-Moselle traduits et publiés en 2013, mis en ligne sur
<https://droit-local.afges.org/>.

Dépôt de référence : <https://git.afges.eu/pages/droit-local>. Le dépôt GitHub `AFGES/droit-local` n'en est
qu'un miroir en lecture seule.

## Structure

- `content/textes/<catégorie>/` : un fichier Markdown par texte.
- `scripts/` : outils de mise en forme (`format_texts.py`, `mark_terms.py`, `extract_laws.py`).
- `layouts/`, `assets/`, `themes/` : site Hugo (thème PaperMod en sous-module).

## Développement

Les outils sont gérés par [mise](https://mise.jdx.dev/) (`mise install`).

```sh
hugo server            # prévisualisation locale
dprint fmt             # mise en forme
markdownlint-cli2 "content/**/*.md" "archetypes/*.md"
scripts/format_texts.py --dry-run
```

## Publication

Chaque push sur `main` lance le workflow Forgejo `.forgejo/workflows/publish.yaml` : vérification (`dprint`,
`markdownlint-cli2`), build Hugo, puis publication sur git-pages.
