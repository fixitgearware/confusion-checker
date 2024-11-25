# DISCLAIMER:
- FixitGearWare Security is in no way, the owner of this source code or claiming to be the owner of this project. However, we did a bit of code refactoring as the initial repository, had some issues. Therefore, we urge you to follow the original owner of this project, to give them the due credit and appreciate their works. Thanks!


# Dependency Confusion Checker

**Dependency Confusion Checker** is a Python-based tool for identifying potential dependency confusion vulnerabilities in JavaScript (`package.json`) and Python (`requirements.txt`) projects. Dependency Confusion attack, is one critical vulnerability that could be potentially exploited by a malicious hacker. This form of 
vulnerability occurs, when packages (known as dependencies) that are necessary for an application to execute have same naming convention on both the private and public
repository of the author of the package. 
By default, when certain commands like "pip install*" are executed to install packages, both private and public repositories are compared, and the most trusted repository (in this case the private repository) is selected, the package pulled into the users device, and gets installed. 
When there seems to be an overlapping in both repositories (public and private), the public becomes the selected. 
The impact of the public being the selected, is that a malicious hacker could write a dependency, while assigning a value indicating the package to be a higher version aka latest version. If a user tries to install the requirements, the selected repository becomes that belonging to the malicious hacker. This certainly, would lead to whatever malicious intent the code embbeded in the package by the hacker, is instructed to do. In most cases users are injected with a backdoor, giving the malicious hacker unrestricted access to the impacted users device. 


## Features

- Checks for potential dependency confusion vulnerabilities in both JavaScript (`package.json`) and Python (`requirements.txt`) dependencies.
- Parses dependency files and checks for package availability in public registries.
- Flags dependencies that may cause dependency confusion based on version inconsistencies between private and public repositories.

## Prerequisites

- Python 3.6+
- Internet connection (to check against public registries)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/fixitgearware/confusion-checker.git
   cd confusion-checker
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt --break-system-packages
   ```
   
3. Update your system just for formalities; should there be any packages broken when installing the requirements.txt
   
   ```bash
   sudo apt-get update && sudo apt-get full-upgrade -y
   ```
   

## Usage

This tool is designed to take input from `stdin` and expects a `requirements.txt` file (for Python) or `package.json` (for JavaScript) in the URL. The main script `check.py` reads the input and processes each dependency to detect potential dependency confusion vulnerabilities.

### Running the Tool

To run the tool, use the following command:

FOR URLS IN A TEXT FILE:

```bash
cat urls.txt | python path_to_tool/check.py 
```
Example:

cat apple1.txt | python ~/Desktop/confusion-checker/check.py



FOR SINGLE LIVE DOMAIN:

```bash
echo https://www.example1.com | python path_to_tool/check.py
```
Example:

echo https://www.facebook.com | python ~/Desktop/confusion-checker/check.py


### Example Output

The tool will output a list of dependencies that may be vulnerable to dependency confusion:

```plaintext
[VULN] https://redacted-js.com/package.json [package-notfound|404|js]
[VULN] https://redacted-py.com/requirements.txt [package-notfound|404|python]
```

### Exit Codes

- `0`: No issues found.
- `1`: Potential dependency confusion vulnerabilities detected.

## How It Works

1. The `check.py` script reads from `stdin` to receive the list of dependencies.
2. For each dependency, it:
   - Checks if the package exists on public registries such as PyPI (for Python) or npm (for JavaScript).
   - Compares versions to identify inconsistencies.
   - Flags any packages that may lead to dependency confusion.

3. Results are printed in the console (your terminal), listing any vulnerable packages found.

## License

This project is licensed under the MIT License.

---

**Note**: This tool is intended for security analysis purposes. Always use responsibly and only on projects for which you have authorization.


## OWNER AND ORIGINAL AUTHOR

Rdzp Github: https://github.com/rdzsp/dependency-confusion-checker

