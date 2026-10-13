# Setup Guide

Follow these steps in order. Total time: about 10 minutes, most of it
waiting for `pip install`.

## 1. Get the folder

You already have it (`RAG-Training-Kit/`). To share it with someone else,
just zip this whole folder and send it -- it's self-contained.

## 2. Install Python 3.10+

Check what you have:

```bash
python3 --version
```

If it's below 3.10, install a newer Python first (python.org, or your OS's
package manager).

## 3. Create a virtual environment

From inside `RAG-Training-Kit/`:

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**
```powershell
py -m venv venv
venv\Scripts\Activate.ps1
```

Your prompt should now show `(venv)` at the start.

## 4. Install the dependencies

```bash
pip install -r requirements.txt
```

This installs LangChain, Chroma, the OpenAI client, Jupyter, and everything
else the notebooks and the `rag_assistant` package need.

Then install the project's own package in "editable" mode, so
`from rag_assistant... import ...` works from inside the notebooks:

```bash
pip install -e .
```

## 5. Add your OpenAI API key

Copy the template and fill it in:

```bash
cp .env.example .env        # macOS/Linux
copy .env.example .env      # Windows
```

Open `.env` and replace the placeholder with a real key from
https://platform.openai.com/api-keys:

```
OPENAI_API_KEY=sk-...your real key...
```

`.env` is already in `.gitignore` -- it will not get committed or shared if
you put this project under version control.

**A note on cost:** every notebook makes real API calls (embeddings + a
small chat model). Running all three notebooks top to bottom typically costs
a few cents, not dollars -- but it is not free, because it is not a toy.

## 6. Register the Jupyter kernel (recommended)

So Jupyter/VS Code use this project's venv, not your system Python:

```bash
python -m ipykernel install --user --name rag-training-kit --display-name "RAG Training Kit"
```

When you open a notebook, pick the **"RAG Training Kit"** kernel.

## 7. Run the notebooks

Open `docs/` in Jupyter, JupyterLab, or VS Code, and run in this order:

1. `1_Hands_On_RAG_Walkthrough.ipynb`
2. `2_Visual_RAG_Explainer.ipynb`
3. `3_RAG_From_Scratch_Live.ipynb`
4. `Guardrails_Live_Demo.ipynb` (no API key needed -- safe to run any time)

Run cells top to bottom with Shift+Enter. Each notebook's first code cell
("the key gate") checks for your API key and stops with a clear message if
it's missing -- fix `.env` and re-run that one cell, no need to restart.

To launch classic Jupyter from the terminal instead of VS Code:

```bash
jupyter notebook docs/
```

## Troubleshooting

**`ModuleNotFoundError: No module named 'rag_helpers'`**
This happens if your notebook's kernel starts in a different working
directory than the `docs/` folder (VS Code, classic Jupyter, and JupyterLab
don't always agree). The first code cell in every notebook already searches
for `rag_helpers.py` in the current folder and every parent folder, so this
should not happen -- but if it does, the fix is either:
- Open the notebook file directly from inside `docs/` (don't open the
  parent folder and navigate in), or
- In VS Code, add this to your `.vscode/settings.json`:
  ```json
  { "jupyter.notebookFileRoot": "${fileDirname}" }
  ```

**`ModuleNotFoundError: No module named 'rag_assistant'`**
You skipped `pip install -e .` (step 4), or you're running a kernel that
isn't this project's venv (step 6).

**"No OpenAI API key found"**
Check `.env` exists in the project root (not inside `docs/`), and that the
line is exactly `OPENAI_API_KEY=sk-...` with no quotes, no spaces around
`=`, and starts with `sk-`.

**Chroma / SQLite errors on first run**
Delete the auto-created `chroma/` folder in the project root and re-run the
vector-store cell -- it rebuilds automatically.

## What to do next

- Read `README.md` for a map of what each notebook covers.
- Open `RAG_Complete_Training_Deck.pptx` for a slide-deck version of the
  same material, useful for teaching a group.
- To share this kit with someone else, zip the whole `RAG-Training-Kit/`
  folder (your `.env` and `venv/` are excluded automatically if you use
  your OS's "zip, respecting .gitignore" option, or just delete those two
  before zipping) and send it -- the recipient starts again from step 3.
