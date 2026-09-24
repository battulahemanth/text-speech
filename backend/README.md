# Backend

Local FastAPI text-to-speech API powered by Piper.

## Setup on Windows

```powershell
cd path\to\text-speach
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
python -c "import multipart; print('python-multipart is installed')"
```

If PowerShell blocks activation, run this once in PowerShell and then activate the environment again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

The `python-multipart` package is required because the transcription endpoint accepts uploaded files. Always run `python -m pip` after activating `.venv` so the package is installed into the same Python environment that starts the API.

The voice model files belong in `voices/`.

## Run

```powershell
cd backend
python -m uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

## Run the frontend

Open a second terminal from the project root:

```powershell
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite, usually `http://localhost:5173`.

## Fix: Form data requires python-multipart

If FastAPI still reports that `python-multipart` is missing, stop Uvicorn and run these commands from the project root:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install python-multipart
python -c "import sys, multipart; print(sys.executable); print(multipart.__file__)"
cd backend
python -m uvicorn app.main:app --reload
```

The printed executable must be inside this project’s `.venv` directory. If it points to `C:\Python313\python.exe`, the virtual environment is not active; use the `.venv\Scripts\Activate.ps1` command above.
