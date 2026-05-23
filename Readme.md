## GNSS interference tool

This is a small Python app for GNSS signal spectrum visualization and interference analysis. It shows demo cases and custom cases, then compares PSD overlap and SSC between signals.

### Setup

**Open terminal**

Clone the project first.

```bash
git clone https://github.com/raman976/assignment.git
cd assignment
```

Create a virtual environment.

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

Install the dependencies.

```bash
pip install -r requirements.txt
```

Run the app.

```bash
python main.py
```

The app will be started.

**Note:- If the GUI is not visible please look in the Taskbar of your OS, a icon will be visible please click on it.**

For windows user if the terminal shows dependency errors then please delete the venv and recreate it.


### Pipeline

The app has demo examples with fixed values. The demo tab compares the reference BOC(5,2) signal with MBOC(6,1,1/11) or BPSK(10).

It also has a custom analysis tab where the center frequency, bandwidths, sampling frequency, number of bits, and comparison signal can be changed.

In both cases the app computes the PSD for the two signals, overlays the graphs, and then computes SSC from the overlap inside the receiver bandwidth.
