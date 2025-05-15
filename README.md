
## 🔐 Litrix — Your Friendly Cybersecurity Assistant

**Litrix** is an interactive command-line tool built in Python that helps you explore and automate common cybersecurity tasks — from learning Linux commands to understanding MITRE ATT\&CK methodologies.

---

### ✨ Features

1. **📂 Linux Command Help**
   Get simple explanations and usage for essential Linux commands — perfect for beginners or quick lookups.

2. **🛠️ Script Writing Automation**
   Automate common security scripting patterns with intelligent assistance. Generate useful shell or Python scripts on the fly.

3. **🕵️‍♀️ MITRE-Based Hacking Methodology**
   Explore real-world hacking techniques categorized by **MITRE ATT\&CK** (Enterprise, Mobile, ICS). Search tactics, techniques, and descriptions interactively using public JSON threat data.

---

### 🧪 Preview

```bash
------------------------------------------------------
         Welcome to Litrix ^_^
------------------------------------------------------
I can help you with a few things related to cybersecurity.
------------------------------------------------------

Main Menu:
1. Linux Command Help
2. Script Writing Automation
3. Hacking Methodology Explanation
4. Exit
```

---

### 📁 Directory Structure

```
├── main.py                  # Main entry script
├── linuxcommand.py          # Linux command help module
├── scripts.py               # Script automation module
├── methodologies.py         # MITRE methodology search and display
├── enterprise-attack.json   # MITRE data (Enterprise)
├── mobile-attack.json       # MITRE data (Mobile)
├── ics-attack.json          # MITRE data (ICS)
├── __pycache__/             # Auto-generated Python bytecode
```

---

### ⚙️ Requirements

* Python 3.8+
* Transformers (`pip install transformers`)
* Internet for NLP-based features (if used in `scripts.py`)
* MITRE ATT\&CK JSON datasets (you can download them [here](https://attack.mitre.org/resources/))

---

### 🚀 Run the Program

```bash
python3 main.py
```

---
