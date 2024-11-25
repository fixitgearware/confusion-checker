import requests
import sys
import logging
import time
import urllib3
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] - %(message)s')

DEPENDENCIES_URL = {
    'python': 'https://pypi.org/project/{package_name}/',
    'js': 'https://registry.npmjs.org/{package_name}/'
}

# Read URLs from standard input and strip whitespace
urls = [line.strip() for line in sys.stdin if line.strip()]

def get_random_user_agent() -> str:
    """Generate a random User-Agent string."""
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    return user_agent_rotator.get_random_user_agent()

def is_unclaimed(package_name: str, language: str) -> Tuple[bool, int]:
    """Check if a package name is unclaimed on the respective package manager."""
    ua = get_random_user_agent()
    dependencies_url = DEPENDENCIES_URL[language]
    try:
        r = requests.head(dependencies_url.format(package_name=package_name), headers={"User-Agent": ua}, timeout=10)
        logger.debug(f"Status code for package {package_name}: {r.status_code}")
        return r.status_code not in {200, 302}, r.status_code
    except requests.RequestException as e:
        logger.error(f"Error checking package {package_name}: {e}")
        return False, 0

def get_dependencies(url: str) -> Tuple[List[str], str]:
    """Fetch dependencies from a package.json or requirements.txt URL."""
    try:
        logger.debug(f"Fetching dependencies from {url}...")
        r = requests.get(url, verify=False, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        all_dependencies = []
        if 'package.json' in url:
            response_json = r.json()
            dependencies = response_json.get('dependencies', {})
            dev_dependencies = response_json.get('devDependencies', {})
            all_dependencies.extend(dependencies.keys())
            all_dependencies.extend(dev_dependencies.keys())
            language = 'js'
        else:
            response = r.text
            all_dependencies.extend(line.strip() for line in response.splitlines() if line.strip())
            language = 'python'
        return all_dependencies, language
    except requests.RequestException as e:
        logger.error(f"Error fetching dependencies from {url}: {e}")
        return [], ""
    except ValueError:
        logger.error(f"Invalid JSON in response from {url}")
        return [], ""

def check_url_dependencies(url: str):
    """Check all dependencies for a given URL."""
    vulnerabilities = []
    dependencies, language = get_dependencies(url)
    if not dependencies or not language:
        logger.warning(f"No dependencies found or unable to determine language for URL: {url}")
        return url, vulnerabilities
    
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(is_unclaimed, dependency, language): dependency for dependency in dependencies}
        for future in as_completed(futures):
            dependency = futures[future]
            try:
                vulnerable, status_code = future.result()
                if vulnerable:
                    vulnerabilities.append({"package_name": dependency, "status_code": status_code, "language": language})
            except Exception as e:
                logger.error(f"Error checking dependency {dependency}: {e}")
    return url, vulnerabilities

def main():
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(check_url_dependencies, url): url for url in urls}
        for future in as_completed(futures):
            url, vulnerabilities = future.result()
            for dependency in vulnerabilities:
                logger.info(f"[VULN] {url} [{dependency['package_name']}|{dependency['status_code']}|{dependency['language']}]")

if __name__ == "__main__":
    main()

