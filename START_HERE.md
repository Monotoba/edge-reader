# 🚀 START HERE — Edge Reader Setup & Scripts

Welcome! This guide will get you up and running in under 2 minutes.

## Choose Your Platform

### 🐧 Linux / 🍎 macOS

Run this command to set up everything:

```bash
bash setup.sh
```

Then use these commands:
```bash
bash run.sh         # Launch the app
bash test.sh        # Run tests
```

### 🪟 Windows (PowerShell) ← Recommended

Run this command to set up everything:

```powershell
.\setup.ps1
```

Then use these commands:
```powershell
.\run.ps1           # Launch the app
.\test.ps1          # Run tests
```

### 🪟 Windows (Command Prompt)

Run this command to set up everything:

```cmd
setup.bat
```

Then use these commands:
```cmd
run.bat             # Launch the app
test.bat            # Run tests
```

---

## What Just Happened?

We've added **13 comprehensive files** to your project:

### 📚 Documentation (Read These)
1. **QUICKSTART.md** — 2-minute quick start (you are reading an enhanced version)
2. **SETUP.md** — Detailed platform-specific setup guide
3. **SCRIPTS.md** — Technical documentation for all scripts
4. **DOCS_AND_SCRIPTS.md** — Complete index and summary

### 🔧 Automation Scripts (Use These)
5. **setup.sh** / **setup.bat** / **setup.ps1** — Initialize your environment
6. **run.sh** / **run.bat** / **run.ps1** — Launch the application
7. **test.sh** / **test.bat** / **test.ps1** — Run the test suite

---

## 3-Step Setup

### Step 1: Run Setup (5 minutes)

Choose your platform:

**Linux/macOS:**
```bash
bash setup.sh
```

**Windows (PowerShell):**
```powershell
.\setup.ps1
```

**Windows (Command Prompt):**
```cmd
setup.bat
```

This will:
- ✅ Check that Python 3.10+ is installed
- ✅ Create a Python virtual environment
- ✅ Install Edge Reader and all dependencies
- ✅ Verify everything is working

### Step 2: Launch the App

**Linux/macOS:**
```bash
bash run.sh
```

**Windows (PowerShell):**
```powershell
.\run.ps1
```

**Windows (Command Prompt):**
```cmd
run.bat
```

The Edge Reader GUI will open.

### Step 3: Verify Tests Pass

**Linux/macOS:**
```bash
bash test.sh
```

**Windows (PowerShell):**
```powershell
.\test.ps1
```

**Windows (Command Prompt):**
```cmd
test.bat
```

You should see something like `passed in 1.23s`.

---

## ✨ You're Done!

Your Edge Reader environment is ready. Now:

1. **Open a document** — Click "Open Document"
2. **Choose a voice** — Select language and voice
3. **Generate audio** — Click "Generate Offline Bundle"
4. **Listen** — Click "Play"
5. **Save bundle** — Save as `.edgevoice.zip` for offline use

---

## 📖 Learn More

| Topic | File |
|-------|------|
| 2-minute quick reference | QUICKSTART.md |
| Detailed setup instructions | SETUP.md |
| How to use each script | SCRIPTS.md |
| Overview and index | DOCS_AND_SCRIPTS.md |
| Application features | README.md |
| How to use the app | help/USER_MANUAL.md |
| Troubleshooting | help/TROUBLESHOOTING.md |

---

## 🔧 Everyday Commands

Once setup is complete, here are the commands you'll use:

### Run the app
```bash
bash run.sh         # Linux/macOS
.\run.ps1           # Windows PowerShell
run.bat             # Windows Command Prompt
```

### Run tests
```bash
bash test.sh        # Linux/macOS
.\test.ps1          # Windows PowerShell
test.bat            # Windows Command Prompt
```

### Development (manual)
```bash
source .venv/bin/activate    # Linux/macOS: activate venv
.\.venv\Scripts\Activate.ps1 # Windows: activate venv
python -m edge_reader        # Run directly
pytest -v                    # Run tests verbosely
ruff format src/ tests/      # Format code
```

---

## ❓ Common Questions

**Q: Do I need to run setup.sh every time?**  
A: No, just once. Then use run.sh or run.bat to launch the app.

**Q: The setup failed. What do I do?**  
A: See the "Troubleshooting" section in SETUP.md.

**Q: Can I use Python 3.9?**  
A: No, Python 3.10+ is required. Install from python.org.

**Q: Do I need Calibre?**  
A: Only if you want to read MOBI/AZW3 ebook formats. See SETUP.md.

**Q: Can I run this without the scripts?**  
A: Yes! See "Manual Setup" in SETUP.md for step-by-step instructions.

**Q: What if I get "Permission denied" on Linux/macOS?**  
A: Run `chmod +x setup.sh run.sh test.sh` to make them executable.

**Q: What if PowerShell says scripts are disabled on Windows?**  
A: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` then try again.

---

## 📋 Files Added

```
DocReader/
├── START_HERE.md              ← You are here
├── QUICKSTART.md              ← Quick 2-minute start
├── SETUP.md                   ← Detailed guide
├── SCRIPTS.md                 ← Script documentation
├── DOCS_AND_SCRIPTS.md        ← Complete index
├── setup.sh / setup.bat / setup.ps1   ← Setup (run once)
├── run.sh / run.bat / run.ps1         ← Launch app
├── test.sh / test.bat / test.ps1      ← Run tests
└── ... (existing files)
```

---

## 🎯 Next Steps

1. **Run setup:**
   - Linux/macOS: `bash setup.sh`
   - Windows PowerShell: `.\setup.ps1`
   - Windows Command Prompt: `setup.bat`

2. **Launch the app:**
   - Linux/macOS: `bash run.sh`
   - Windows PowerShell: `.\run.ps1`
   - Windows Command Prompt: `run.bat`

3. **Read the user manual:**
   - See `help/USER_MANUAL.md`

---

## 💡 Pro Tips

- **Activate the virtual environment once** and run commands directly:
  ```bash
  source .venv/bin/activate    # Linux/macOS
  python -m edge_reader        # Run directly
  pytest                        # Run tests directly
  ```

- **Run tests with more details:**
  ```bash
  bash test.sh -v              # Verbose
  bash test.sh -x              # Stop on first failure
  bash test.sh tests/test_bundle.py  # Specific file
  ```

- **Development**: See SCRIPTS.md → Advanced Usage

---

## ✅ Checklist

After setup, verify:
- [ ] Python 3.10+ is installed
- [ ] Virtual environment created in `.venv/`
- [ ] All dependencies installed
- [ ] `bash run.sh` launches the app
- [ ] `bash test.sh` passes all tests

---

## 🆘 Need Help?

1. **Quick issues:** See SETUP.md → Troubleshooting
2. **Using the app:** See help/USER_MANUAL.md
3. **Script details:** See SCRIPTS.md
4. **General help:** See help/GETTING_STARTED.md

---

**Ready? Run your setup command above and you'll be done in 5 minutes! 🎉**

After setup, see QUICKSTART.md for the essential 2-minute reference.
