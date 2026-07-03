# Conda / Anaconda Setup Guide

This guide explains how to set up the course environment using Conda or Anaconda.

The project includes an `environment.yaml` file, which defines the Python version and all the packages needed for the course.

---

## 1. Prerequisites

Before starting, install one of the following:

- [Anaconda](https://www.anaconda.com/download)
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- [Mambaforge / Miniforge](https://conda-forge.org/download/)

Anaconda is the easiest option for beginners. Miniconda or Miniforge are lighter-weight alternatives.

---

## 2. Open a terminal

### macOS / Linux

Open the **Terminal** app.

### Windows

Open **Anaconda Prompt** from the Start Menu.

Alternatively, you can use PowerShell if Conda has already been initialised there.

---

## 3. Go to the project folder

Navigate to the folder containing the course files.

For example:

```bash
cd path/to/practical-ai-engineering
```

You should be in the same folder as the `environment.yaml` file.

You can check this by running:

```bash
ls
```

On Windows Anaconda Prompt, you can use:

```bat
dir
```

You should see something like:

```text
environment.yaml
pyproject.toml
README.md
day_2/
day_4/
```

---

## 4. Create the Conda environment

Run:

```bash
conda env create -f environment.yaml
```

This will create a new Conda environment called:

```text
practical-ai-engineering
```

The first installation may take a few minutes.

---

## 5. Activate the environment

After the environment has been created, activate it:

```bash
conda activate practical-ai-engineering
```

You should now see the environment name at the start of your terminal prompt, for example:

```text
(practical-ai-engineering)
```

---

## 6. Register the Jupyter kernel

Run:

```bash
python -m ipykernel install --user \
  --name practical-ai-engineering \
  --display-name "Python 3.13 - Practical AI Engineering"
```

On Windows Anaconda Prompt, you can run it as a single line:

```bat
python -m ipykernel install --user --name practical-ai-engineering --display-name "Python 3.13 - Practical AI Engineering"
```

This makes the environment available inside JupyterLab and notebooks.

---

## 7. Start JupyterLab

Run:

```bash
jupyter lab
```

JupyterLab should open in your browser.

When opening a notebook, select the kernel:

```text
Python 3.13 - Practical AI Engineering
```

---

## 8. Check that the setup works

From the activated environment, run:

```bash
python -c "import agent_workshop, rag_workshop; print('Imports OK')"
```

If everything is installed correctly, you should see:

```text
Imports OK
```

You can also check the Python version:

```bash
python --version
```

You should see Python 3.13.

---

## 9. Updating the environment

If the `environment.yaml` file changes later, update your environment with:

```bash
conda env update -f environment.yaml --prune
```

Then reactivate the environment:

```bash
conda activate practical-ai-engineering
```

---

## 10. Removing the environment

If you need to delete the environment and start again, run:

```bash
conda deactivate
conda env remove -n practical-ai-engineering
```

Then recreate it:

```bash
conda env create -f environment.yaml
conda activate practical-ai-engineering
```

---

## 11. Common issues

### `conda: command not found`

Conda is either not installed or has not been added to your terminal.

Use **Anaconda Prompt** on Windows, or reinstall Anaconda / Miniconda and make sure Conda is initialised.

---

### `EnvironmentFileNotFound: environment.yaml`

You are not in the correct project folder.

Move into the folder containing `environment.yaml` and try again:

```bash
cd path/to/practical-ai-engineering
conda env create -f environment.yaml
```

---

### The Jupyter kernel does not appear

Make sure the environment is activated:

```bash
conda activate practical-ai-engineering
```

Then register the kernel again:

```bash
python -m ipykernel install --user \
  --name practical-ai-engineering \
  --display-name "Python 3.13 - Practical AI Engineering"
```

Restart JupyterLab afterwards.

---

### Package installation fails

First, make sure Conda is up to date:

```bash
conda update conda
```

Then try recreating the environment:

```bash
conda env remove -n practical-ai-engineering
conda env create -f environment.yaml
```

If the issue is related to Python 3.13 compatibility, use the course fallback environment if one is provided, or ask the instructor for the Python 3.12 version of the environment file.

---

## 12. Daily usage

Each time you return to the course project, open a terminal, go to the project folder, and activate the environment:

```bash
cd path/to/practical-ai-engineering
conda activate practical-ai-engineering
jupyter lab
```

Then select the correct notebook kernel:

```text
Python 3.13 - Practical AI Engineering
```
