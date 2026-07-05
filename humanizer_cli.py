#!/usr/bin/env python
import os
import sys
import re
import random
import argparse
import tokenize
import io
import unicodedata
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class DummyColor:
        def __getattr__(self, name):
            return ""
    Fore = DummyColor()
    Style = DummyColor()

def print_header():
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "       🤖 -> 🧑  HUMAN TEXT & CODE GENERATOR  <- 🤖")
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)

def detect_language(content: str, filename: str = "") -> str:
    """Detects if the input is python, c, or plain text."""
    if filename:
        ext = os.path.splitext(filename)[1].lower()
        if ext == ".py":
            return "python"
        elif ext in [".c", ".h", ".cpp", ".hpp"]:
            return "c"
            
    # Fallback to structural checks
    if content.startswith("#include") or "int main(" in content:
        return "c"
    if "def " in content or "import " in content or content.startswith("#!"):
        # Check shebang
        first_line = content.splitlines()[0] if content else ""
        if "python" in first_line:
            return "python"
        return "python"
        
    return "text"

def humanize_text_anomalies(text: str, language: str = "fr", is_comment: bool = False) -> str:
    """Injects human-like anomalies (typos, sentence rewriting, accent dropping) into text."""
    p_lowercase_initial = random.uniform(0.08, 0.20)
    p_drop_common_accents = random.uniform(0.06, 0.16)
    p_mobile_spacing = random.uniform(0.08, 0.20)
    p_keyboard_typo = random.uniform(0.02, 0.08)
    p_sentence_boundary = random.uniform(0.15, 0.35)
    p_keep_final_period = random.uniform(0.35, 0.65)
    p_no_accents_entire_text = random.uniform(0.01, 0.05)

    # 1. Lowercase initial character
    if not is_comment and random.random() < p_lowercase_initial and len(text) > 1:
        text = text[0].lower() + text[1:]

    # 2. Drop French accents on common words
    if language.lower() == "fr" and random.random() < p_drop_common_accents:
        accents_map = {"très": "tres", "équipe": "equipe", "détail": "detail", "accueil": "acceuil"}
        for orig, replacement in accents_map.items():
            if orig in text:
                text = text.replace(orig, replacement)

    # 3. Mobile formatting spacing
    if random.random() < p_mobile_spacing:
        text = text.replace(" !", "!").replace(" ?", "?").replace(" :", ":")

    # 4. Introduce keyboard typo
    if random.random() < p_keyboard_typo:
        words = text.split()
        if len(words) > 3:
            idx = random.randint(1, len(words) - 1)
            word = words[idx]
            if len(word) > 4 and word.isalpha():
                char_idx = random.randint(1, len(word) - 1)
                word = word[:char_idx] + word[char_idx] + word[char_idx:]
                words[idx] = word
                text = " ".join(words)

    # 5. Sentence boundary rewrite: random % chance to turn sentence boundaries (. ! ?) into a comma
    # and lowercase the subsequent letter if it's inside the text and not at the end
    def replace_boundary(match):
        punctuation = match.group(1)
        space = match.group(2)
        next_char = match.group(3)
        if random.random() < p_sentence_boundary:
            return "," + space + next_char.lower()
        return punctuation + space + next_char

    text = re.sub(r'([.!?])(\s+)([a-zA-ZÀ-ÿ])', replace_boundary, text)

    # 6. Trailing punctuation
    if text.endswith('.'):
        if random.random() > p_keep_final_period:
            text = text[:-1].strip()

    # 7. Strip all accents from entire text
    if random.random() < p_no_accents_entire_text:
        nfkd_form = unicodedata.normalize('NFKD', text)
        text = "".join([c for c in nfkd_form if not unicodedata.combining(c)])

    return text

def humanize_python(code: str) -> str:
    """Humanizes Python comments and adds slight variations in operators spacing."""
    try:
        tokens = list(tokenize.tokenize(io.BytesIO(code.encode('utf-8')).readline))
    except Exception:
        # Fallback if syntax error prevents tokenization
        return code

    lines = code.splitlines(keepends=True)
    modified = 0

    # Process comments in reverse order so line replacement index is stable
    for tok in reversed(tokens):
        if tok.type == tokenize.COMMENT:
            start_line, start_col = tok.start
            end_line, end_col = tok.end
            comment_text = tok.string
            
            if comment_text.startswith('#'):
                prefix = '#'
                content = comment_text[1:]
                
                # Protect shebangs and directives
                if content.strip().startswith('!') or 'type:' in content or 'coding:' in content:
                    continue
                    
                humanized_content = humanize_text_anomalies(content, is_comment=True)
                new_comment = prefix + humanized_content
                
                line_idx = start_line - 1
                orig_line = lines[line_idx]
                lines[line_idx] = orig_line[:start_col] + new_comment + orig_line[end_col:]
                modified += 1

    code_with_comments = "".join(lines)
    # Vary operator spacing
    code_final = vary_operator_spacing(code_with_comments, "python")
    return code_final, modified

def humanize_c(code: str) -> str:
    """Humanizes C/C++ comments (single line and multi line) and varies spacing."""
    # Match double quoted string, single quoted char, single-line comment, or multi-line comment
    pattern = re.compile(
        r'("(?:[^"\\]|\\.)*")|'      # Group 1: Double quoted strings
        r"('(?:[^'\\]|\\.)*')|"      # Group 2: Single quoted chars
        r'(//.*?)(?=\r?\n|$)|'       # Group 3: Single line comment
        r'(/\*[\s\S]*?\*/)'          # Group 4: Multi line comment
    )
    
    modified_count = [0] # List wrapper to allow mutation in nested function
    
    def replacer(match):
        g1 = match.group(1)
        g2 = match.group(2)
        g3 = match.group(3)
        g4 = match.group(4)
        
        if g1:
            return g1
        elif g2:
            return g2
        elif g3:
            content = g3[2:]
            modified_count[0] += 1
            return "//" + humanize_text_anomalies(content, is_comment=True)
        elif g4:
            content = g4[2:-2]
            modified_count[0] += 1
            return "/*" + humanize_text_anomalies(content, is_comment=True) + "*/"
        return match.group(0)

    code_comments = pattern.sub(replacer, code)
    code_final = vary_operator_spacing(code_comments, "c")
    return code_final, modified_count[0]

def vary_operator_spacing(code: str, language: str) -> str:
    """Safely varies spacing around operators like =, +, -, *, / without touching strings/comments."""
    if language == 'c':
        pattern = re.compile(
            r'("(?:[^"\\]|\\.)*")|'      # Group 1: Double quoted strings
            r"('(?:[^'\\]|\\.)*')|"      # Group 2: Single quoted chars
            r'(//.*?)(?=\r?\n|$)|'       # Group 3: Single line comment
            r'(/\*[\s\S]*?\*/)|'         # Group 4: Multi line comment
            r'([a-zA-Z0-9_])\s*([=+*/-])\s*([a-zA-Z0-9_])' # Group 5, 6, 7: Operator between operands
        )
        def replacer(match):
            g1 = match.group(1)
            g2 = match.group(2)
            g3 = match.group(3)
            g4 = match.group(4)
            if g1: return g1
            if g2: return g2
            if g3: return g3
            if g4: return g4
            
            left, op, right = match.group(5), match.group(6), match.group(7)
            if random.random() < 0.12:
                spacing_choice = random.choice([
                    f"{left}{op}{right}",
                    f"{left} {op} {right}",
                    f"{left}  {op} {right}",
                    f"{left} {op}  {right}"
                ])
                return spacing_choice
            return match.group(0)
        return pattern.sub(replacer, code)
        
    elif language == 'python':
        pattern = re.compile(
            r'("(?:[^"\\]|\\.)*")|'      # Group 1: Double quoted strings
            r"('(?:[^'\\]|\\.)*')|"      # Group 2: Single quoted chars
            r'(#.*)|'                    # Group 3: Python comment
            r'([a-zA-Z0-9_])\s*([=+*/-])\s*([a-zA-Z0-9_])' # Group 4, 5, 6: Operator between operands
        )
        def replacer(match):
            g1 = match.group(1)
            g2 = match.group(2)
            g3 = match.group(3)
            if g1: return g1
            if g2: return g2
            if g3: return g3
            
            left, op, right = match.group(4), match.group(5), match.group(6)
            if random.random() < 0.12:
                spacing_choice = random.choice([
                    f"{left}{op}{right}",
                    f"{left} {op} {right}",
                    f"{left}  {op} {right}",
                    f"{left} {op}  {right}"
                ])
                return spacing_choice
            return match.group(0)
        return pattern.sub(replacer, code)
    return code

def main():
    parser = argparse.ArgumentParser(description="Humanize text or code comments and spacing.")
    parser.add_argument("path", nargs="?", help="Path to the file to humanize. If empty, reads from stdin.")
    parser.add_argument("-w", "--write", action="store_true", help="Overwrite the file in-place.")
    parser.add_argument("-o", "--output", help="Output file path.")
    parser.add_argument("-t", "--text", action="store_true", help="Force plain text processing.")
    parser.add_argument("-p", "--python", action="store_true", help="Force Python processing.")
    parser.add_argument("-c", "--c-code", action="store_true", help="Force C/C++ processing.")
    
    args = parser.parse_args()

    print_header()

    content = ""
    filename = ""

    if args.path:
        if os.path.exists(args.path):
            filename = args.path
            print(Fore.BLUE + f"[*] Reading file: {filename}")
            with open(args.path, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            # Treats the path parameter as raw string content
            content = args.path
            print(Fore.BLUE + "[*] Processing raw input string...")
    else:
        # Read from stdin
        print(Fore.BLUE + "[*] Reading from standard input (stdin)...")
        content = sys.stdin.read()

    if not content.strip():
        print(Fore.RED + "[!] Error: No content to process.")
        sys.exit(1)

    # Language selection
    if args.text:
        lang = "text"
    elif args.python:
        lang = "python"
    elif args.c_code:
        lang = "c"
    else:
        lang = detect_language(content, filename)

    print(Fore.YELLOW + f"[*] Detected language / format: {lang.upper()}")

    # Process content
    output = ""
    modified = 0

    if lang == "python":
        output, modified = humanize_python(content)
        print(Fore.GREEN + f"[+] Humanized {modified} comments and applied spacing variations in Python code.")
    elif lang == "c":
        output, modified = humanize_c(content)
        print(Fore.GREEN + f"[+] Humanized {modified} comments and applied spacing variations in C code.")
    else:
        output = humanize_text_anomalies(content)
        print(Fore.GREEN + "[+] Humanized plain text content.")

    # Write output
    if args.write and filename:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(output)
        print(Fore.GREEN + Style.BRIGHT + f"[✓] Overwritten in-place: {filename}")
    elif args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(Fore.GREEN + Style.BRIGHT + f"[✓] Written to: {args.output}")
    else:
        print(Fore.YELLOW + "\n--- HUMANIZED OUTPUT ---")
        print(output)
        print(Fore.YELLOW + "------------------------\n")

if __name__ == "__main__":
    main()
