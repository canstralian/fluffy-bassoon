import os
import re

def read_file(file_path):
    """
    Reads the content of a file.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The content of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If an I/O error occurs while reading the file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

def detect_hardcoded_passwords(content):
    """
    Detects hardcoded passwords in the given content.

    Args:
        content (str): The content of the file to be analyzed.

    Returns:
        bool: True if hardcoded passwords are detected, False otherwise.
    """
    pattern = r'password\s*=\s*["\'].*["\']'
    return bool(re.search(pattern, content, re.IGNORECASE))

def detect_insecure_functions(content):
    """
    Detects the use of insecure functions in the given content.

    Args:
        content (str): The content of the file to be analyzed.

    Returns:
        list: A list of insecure functions used in the content.
    """
    insecure_functions = ['eval', 'exec', 'open']
    detected_functions = [func for func in insecure_functions if func in content]
    return detected_functions
