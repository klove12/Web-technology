import re
import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import builtwith
import httpx
from jsbeautifier import beautify
import time

def fetch_html_content(url):
    headers = {'User-Agent': generate_user_agent()}
    response = requests.get(url, headers=headers)
    return response.text

def identify_javascript_libraries(html_content):
    script_tags = re.findall(r'<script[^>]*src=["\'](.*?)["\']', html_content)
    js_libraries = []
    
    for script in script_tags:
        if script.endswith('.js'):
            js_libraries.append(script)
    
    return js_libraries

def identify_python_libraries():
    # You can customize this list with common Python libraries you want to identify
    python_libraries = ["flask", "django", "requests", "numpy", "pandas"]
    
    identified_libraries = []
    
    for lib in python_libraries:
        try:
            __import__(lib)
            identified_libraries.append(lib)
        except ImportError:
            pass
    
    return identified_libraries

def identify_html_frameworks(html_content):
    html_frameworks = ["bootstrap", "foundation", "bulma"]
    identified_frameworks = []
    
    for framework in html_frameworks:
        if framework in html_content.lower():
            identified_frameworks.append(framework)
    
    return identified_frameworks

def identify_nodejs(url):
    try:
        response = httpx.get(url)
        headers = response.headers
        if "x-powered-by" in headers and "node" in headers["x-powered-by"].lower():
            return True
    except Exception:
        pass
    
    return False

def identify_sql(url):
    # You would need to customize this function based on the specific SQL technologies you want to identify
    sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE", "FROM", "JOIN"]
    identified_sql_keywords = []
    
    html_content = fetch_html_content(url)
    beautified_html = beautify(html_content)
    
    for keyword in sql_keywords:
        if keyword in beautified_html:
            identified_sql_keywords.append(keyword)
    
    return identified_sql_keywords

def identify_aspnet(url):
    try:
        response = requests.head(url)
        server_header = response.headers.get('Server', '').lower()
        if 'aspnet' in server_header:
            return True
    except Exception:
        pass
    
    return False

def identify_cpp(url):
    try:
        response = requests.head(url)
        server_header = response.headers.get('Server', '').lower()
        if 'cppcms' in server_header:
            return True
    except Exception:
        pass
    
    return False

def identify_php_usage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Check for PHP in the URL path
        if re.search(r'\.php', response.url):
            return "Php detected"

        # Check for PHP in response headers
        if 'X-Powered-By' in response.headers:
            if 'PHP' in response.headers['X-Powered-By']:
                return "Php detected"

        # Check for PHP keywords in response content
        if 'php' in response.text.lower():
            return "Php detected"

        # Check for common PHP file extensions in script tags
        script_tags = re.findall(r'<script[^>]*src=["\'](.*?)["\']', response.text)
        php_extensions = ['.php', '.phtml', '.php3', '.php4', '.php5', '.php7']
        for script in script_tags:
            for ext in php_extensions:
                if ext in script:
                    return "Php detected"

    except Exception:
        pass

    return False


def identify_web_technologies(url):
    html_content = fetch_html_content(url)
    
    js_libraries = identify_javascript_libraries(html_content)
    python_libraries = identify_python_libraries()
    html_frameworks = identify_html_frameworks(html_content)
    is_nodejs = identify_nodejs(url)
    sql_keywords = identify_sql(url)
    is_aspnet = identify_aspnet(url)  # Add ASP.NET identification
    is_cpp = identify_cpp(url)  # Add C++ identification
    is_php = identify_php_usage(url)
    identified_technologies = {
        "JavaScript Libraries": js_libraries,
        "Python Libraries": python_libraries,
        "HTML Frameworks": html_frameworks,
        "Node.js": is_nodejs,
        "SQL Keywords": sql_keywords,
        "ASP.NET": is_aspnet,  # Include ASP.NET detection in the result
        "C++": is_cpp,  # Include C++ detection in the result
        "PHP": is_php
    }
    
    return identified_technologies

if __name__ == "__main__":
    website_url = "https://www.youtube.com"
    technologies = identify_web_technologies(website_url)

    print("Identified Web Technologies (Current):")
    for category, tech_list in technologies.items():
        if tech_list:
            print(f"{category}: {tech_list}")
        else:
            print(f"{category}: None")
            print("Sleeping for 1 minute before the next check...")
        time.sleep(60)
            

              
