# 🤖 -> 🧑 Humanizer: Natural Text & Code Anomaly Generator

A lightweight, production-grade CLI utility written in Python that helps your generated content look indistinguishable from organic human inputs. It dynamically rewrites plain text and code structures (comments, layout spacing) with natural humanizing mutations.

## ✨ Features

- **🎯 Language Auto-Detection**: Seamlessly detects whether the input is **Python**, **C/C++**, or **Plain Text** using syntax heuristics.
- **🛡️ Code Protection**: Never breaks syntax or compilation. Only humanizes comments while keeping string literals, shebangs, type hints, and code constructs fully functional.
- **✨ Micro-Layout Variations**: Simulates casual human coding by randomly altering spacing around binary operators (`=`, `+`, `-`, `*`, `/`) in C and Python files.
- **🎲 Fully Dynamic Probabilities**: No hardcoded thresholds. Every run randomly fluctuates anomaly frequencies to prevent static fingerprinting.
- **💬 Text Humanizer Anomalies**:
  - **Sentence Boundaries**: Converts select periods, question marks, and exclamation marks into commas while lowercasing the following letter (inside text, not at the end).
  - **Accent Dropping**: Option-based full accent removal or word-level dropping of common French accents.
  - **Keyboard Typos**: Injects rare double-letters or layout neighbor typos.
  - **Trailing Period Stripping**: Drops trailing sentence periods to mimic quick mobile messages.
- **🎨 Beautiful Console Logs**: Integrated colorized CLI reporting powered by `colorama`.

---

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/humanizer.git
   cd humanizer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Usage

```bash
usage: humanizer_cli.py [-h] [-w] [-o OUTPUT] [-t] [-p] [-c] [path]
```

### Positional Arguments
- `path`: The path to the file to process. If omitted, reads from standard input (`stdin`).

### Options
- `-h, --help`: Show help instructions.
- `-w, --write`: Overwrite the processed file in-place.
- `-o, --output`: Save output to a specific file.
- `-t, --text`: Force plain text mode.
- `-p, --python`: Force Python code mode.
- `-c, --c-code`: Force C/C++ code mode.

---

## 📖 Examples

### 1. Processing Text (CLI raw input)
```bash
python humanizer_cli.py -t "Le service était parfait. Les plats étaient très bons."
```
*Output:*
```
Le service était parfait, les plats étaient très bons
```

### 2. Processing Python Code In-Place
```bash
python humanizer_cli.py -w my_script.py
```
*Input:*
```python
def sum_values(a, b):
    # Très important: calculer la somme.
    return a + b
```
*Output:*
```python
def sum_values(a, b):
    # Très important, calculer la somme
    return a+b
```

### 3. Processing C Code from standard input
```bash
cat main.c | python humanizer_cli.py -c
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
