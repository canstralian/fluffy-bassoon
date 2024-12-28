import os
import re
import argparse
from datetime import datetime

def scan_directory(directory):
    """
    Scans the specified directory for files and analyzes their content for potential security vulnerabilities.

    Args:
        directory (str): The path to the directory to be scanned.

    Returns:
        dict: A dictionary containing filenames as keys and lists of detected vulnerabilities as values.
    """
    vulnerabilities = {}  # Dictionary to store vulnerabilities for each file

    # Check if the provided directory exists
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory {directory} does not exist.")

    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        # Initialize an empty list to store vulnerabilities for the current file
        file_vulnerabilities = []

        # Open the file and read its content
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()

            # Check for hardcoded sensitive information (e.g., passwords)
            if re.search(r'password\s*=\s*["\'].*["\']', content, re.IGNORECASE):
                file_vulnerabilities.append('Hardcoded password detected.')

            # Check for the use of insecure functions
            insecure_functions = ['eval', 'exec', 'open']
            for func in insecure_functions:
                if re.search(rf'\b{func}\b', content):
                    file_vulnerabilities.append(f'Use of insecure function: {func}.')

        # If vulnerabilities were found, add them to the dictionary
        if file_vulnerabilities:
            vulnerabilities[filename] = file_vulnerabilities

    return vulnerabilities

def generate_report(vulnerabilities):
    """
    Generates a report of detected vulnerabilities.

    Args:
        vulnerabilities (dict): A dictionary containing filenames and their associated vulnerabilities.

    Returns:
        str: A formatted string report of the detected vulnerabilities.
    """
    if not vulnerabilities:
        return "No vulnerabilities detected."

    report = f"Vulnerability Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "=" * 50 + "\n"

    for filename, issues in vulnerabilities.items():
        report += f"\nFile: {filename}\n"
        for issue in issues:
            report += f"  - {issue}\n"

    return report

def main():
    """
    The main function that parses command-line arguments, scans the specified directory,
    and generates a report of detected vulnerabilities.
    """
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(description="Scan a directory for potential security vulnerabilities in Python files.")
    parser.add_argument('directory', type=str, help="The path to the directory to be scanned.")

    # Parse the command-line arguments
    args = parser.parse_args()

    try:
        # Scan the directory for vulnerabilities
        vulnerabilities = scan_directory(args.directory)

        # Generate and print the report
        report = generate_report(vulnerabilities)
        print(report)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
