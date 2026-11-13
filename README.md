# RELAX

Repositorio del proyecto de grado **RELAX** (Redes de Energía Libre para el
Aprendizaje eXploratorio): implementación de redes neuronales basadas en
codificación predictiva (*predictive coding*) e inferencia activa.

## Structure

```
RELAX/
├── environment.yml                  # conda environment (Python + all libraries)
├── third_party/
│   └── PredictiveCoding/            # Bogacz-group PC library (git submodule, our fork)
├── tutorial_free_energy_network/    # exercises from Bogacz's free-energy tutorial
└── scripts/                         # helper scripts
```

## Setup

### 1. Clone (including the submodule)

```bash
git clone --recurse-submodules git@github.com:tomas-gr/RELAX.git
cd RELAX
```

If you already cloned without `--recurse-submodules`, `third_party/PredictiveCoding`
will be empty. Fill it with:

```bash
git submodule update --init
```

### 2. Create the environment

```bash
conda env create -f environment.yml
conda activate relax
```

This also installs the predictive coding library in *editable* mode, so
`import predictive_coding` works from anywhere, and edits to
`third_party/PredictiveCoding/predictive_coding/` take effect immediately.

After changing `environment.yml`, update the environment with:

```bash
conda env update -f environment.yml --prune
```

## The predictive coding library (submodule)

`third_party/PredictiveCoding` is a **git submodule**: a separate git repository
nested inside this one. RELAX only records *which commit* of it to use.

- Our fork: <https://github.com/tomas-gr/PredictiveCoding> (remote `origin`)
- Original: <https://github.com/Bogacz-Group/PredictiveCoding> (remote `upstream`, fetch only)

Changes to the library are committed **inside** `third_party/PredictiveCoding`
and pushed to the fork. Then, in RELAX, commit the updated submodule pointer:

```bash
cd third_party/PredictiveCoding
git add <files> && git commit -m "..." && git push
cd ../..
git add third_party/PredictiveCoding && git commit -m "Update PC library"
```

To bring in new changes from the Bogacz group:

```bash
cd third_party/PredictiveCoding
git fetch upstream
git merge upstream/main
```
