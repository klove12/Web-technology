import re
import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import builtwith
import httpx
from jsbeautifier import beautify

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

def identify_web_technologies(url):
    html_content = fetch_html_content(url)
    
    js_libraries = identify_javascript_libraries(html_content)
    python_libraries = identify_python_libraries()
    html_frameworks = identify_html_frameworks(html_content)
    is_nodejs = identify_nodejs(url)
    sql_keywords = identify_sql(url)
    
    identified_technologies = {
        "JavaScript Libraries": js_libraries,
        "Python Libraries": python_libraries,
        "HTML Frameworks": html_frameworks,
        "Node.js": is_nodejs,
        "SQL Keywords": sql_keywords
    }
    
    return identified_technologies

if __name__ == "__main__":
    website_url = "https://google.com"
    technologies = identify_web_technologies(website_url)

    print("Identified Web Technologies:")
    for category, tech_list in technologies.items():
        if tech_list:
            print(f"{category}: {tech_list}")
        else:
            print(f"{category}: None")
