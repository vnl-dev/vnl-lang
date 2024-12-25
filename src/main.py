import subprocess
import os
import sqlite3
import json

def execute_code(language, code):
    if language == 'python':
        command = ['python', '-c', code]
    elif language == 'javascript':
        command = ['node', '-e', code]
    elif language == 'typescript':
        with open('temp.ts', 'w') as f:
            f.write(code)
        subprocess.run(['tsc', 'temp.ts'])
        result = subprocess.run(['node', 'temp.js'], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    elif language == 'bash':
        command = ['bash', '-c', code]
    elif language == 'html':
        with open('temp.html', 'w') as f:
            f.write(code)
        os.system('start temp.html')
        return "HTML code executed. Check your browser."
    elif language == 'css':
        with open('temp.css', 'w') as f:
            f.write(code)
        os.system('start temp.css')
        return "CSS code executed. Check your browser."
    elif language == 'php':
        command = ['php', '-r', code]
    elif language == 'ruby':
        command = ['ruby', '-e', code]
    elif language == 'json':
        try:
            json_data = json.loads(code)
            pretty_json = json.dumps(json_data, indent=4)
            return pretty_json
        except json.JSONDecodeError as e:
            return f"JSON error: {e}"
    elif language == 'sql':
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        try:
            cursor.execute(code)
            conn.commit()
            if cursor.description:
                result = cursor.fetchall()
                return result
            else:
                return "SQL executed successfully."
        except sqlite3.Error as e:
            return f"SQL error: {e}"
        finally:
            conn.close()
    elif language == 'perl':
        command = ['perl', '-e', code]
    elif language == 'lua':
        command = ['lua', '-e', code]
    elif language == 'c':
        with open('temp.c', 'w') as f:
            f.write(code)
        command = ['gcc', 'temp.c', '-o', 'temp_c_exec']
        subprocess.run(command)
        result = subprocess.run(['./temp_c_exec'], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    elif language == 'cpp':
        with open('temp.cpp', 'w') as f:
            f.write(code)
        command = ['g++', 'temp.cpp', '-o', 'temp_cpp_exec']
        subprocess.run(command)
        result = subprocess.run(['./temp_cpp_exec'], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    elif language == 'java':
        with open('Temp.java', 'w') as f:
            f.write(code)
        subprocess.run(['javac', 'Temp.java'])
        result = subprocess.run(['java', 'Temp'], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    elif language == 'go':
        with open('temp.go', 'w') as f:
            f.write(code)
        result = subprocess.run(['go', 'run', 'temp.go'], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    elif language == 'rust':
        with open('temp.rs', 'w') as f:
            f.write(code)
        subprocess.run(['rustc', 'temp.rs'])
        result = subprocess.run(['./temp'], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    elif language == 'swift':
        with open('temp.swift', 'w') as f:
            f.write(code)
        result = subprocess.run(['swift', 'temp.swift'], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    else:
        return "Unsupported language"

    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else result.stderr

def select_language(command):
    if command.startswith("selectCode language ('"):
        languages = command[len("selectCode language ('"):-2].split(", ")
        return languages[0]  # For simplicity, we'll just pick the first language for now
    return None

def read_vnl_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
    
    if len(lines) < 2:
        return None, None

    language_command = lines[0].strip()
    code = ''.join(lines[1:])

    return select_language(language_command), code

# Example usage
file_path = 'script.vnl'
selected_language, user_code = read_vnl_file(file_path)

if selected_language:
    output = execute_code(selected_language, user_code)
    print(f"Output from {selected_language}:\n{output}")
else:
    print("Invalid .vnl file format or language selection command")
