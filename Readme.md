## GNSS interference tool

This is a small Python app for GNSS signal spectrum visualization and interference analysis. It shows demo cases and custom cases, then compares PSD overlap and SSC between signals.

### [Detailed Project Report](https://docs.google.com/document/d/1OvkTVlbKaXY_EhUf0I-sqjorMGBsRhW4w38ztqyXMIM/edit?usp=sharing)

## Setup

#### Open terminal

#### Clone the project first.

```bash
git clone https://github.com/raman976/assignment.git
cd assignment
```

#### Create a virtual environment.

macOS and Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
python -m venv venv
venv\Scripts\activate.bat
```

#### Install the dependencies.

```bash
pip install -r requirements.txt
```

#### Run the app.

```bash
python main.py
```

#### The app will be started.

**Note:- If the GUI is not visible please look in the Taskbar of your OS, an icon will be visible please click on it.**

**For windows, if the terminal shows dependency errors then please delete the venv and recreate it or try directly running from global or check the python version.**

#### For deleting venv in Windows if terminal gives error.

```bash
rmdir /s /q venv
```


