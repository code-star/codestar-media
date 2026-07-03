![](./animated/animated_dark.svg#gh-dark-mode-only)
![](./animated/animated_light.svg#gh-light-mode-only)

---

# Codestar Media and Branding

## Installing

To install the Python 3 dependencies, run:

```sh
brew install poetry
poetry install
```

## Generating hoodie visuals

To generate the hoodie templates, run:

```sh
poetry run python scripts/render_hoodies.py templates
```

To generate just one template, run:

```sh
poetry run python scripts/render_hoodies.py templates/name.json
```

For the SVG generation to work, you need to install Inkscape, and install all the fonts in `/fonts/`.

## Regenerating resources

To re-generate all the logos (if the master logo was modified), run:

```sh
rm -rf logos
poetry run python scripts/process.py
poetry run python scripts/convert.py
```

## Spelling of Codestar

It's **Codestar**, not:

- ~~CODESTAR~~
- ~~CODE.STAR~~
- ~~Code.Star~~
- ~~Code Star~~
