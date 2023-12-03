# %%
import csv
from urllib.parse import urlparse
import requests
import whois
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import socket
import dns.resolver
from googlesearch import search

# %%
def check_ssl_state(url):
    if "https://" in url:
        try:
            response = requests.head(url, verify=True)
            return 1
        except:
            return 0
    else:
        return -1

# %%
def check_domain_registration_length(url, days_threshold=365):
    try:
        domain_info = whois.whois(url)
        expiration_date = domain_info.expiration_date
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
        if expiration_date is not None and (expiration_date - datetime.now()).days <= days_threshold:
            return -1
        else:
            return 1
    except whois.parser.PywhoisError:
        return 0

# %%
def check_favicon(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')
        favicon_link = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')

        if favicon_link:
            favicon_href = favicon_link.get('href')
            absolute_favicon_url = urljoin(url, favicon_href)
            return -1 if urlparse(url).netloc != urlparse(absolute_favicon_url).netloc else 1
        else:
            return 1

    except requests.exceptions.RequestException: #no favicon
        return 0

# %%
def check_ports(url):
    try:
        hostname = urlparse(url).hostname
        open_ports = [80, 443]
        closed_ports = [21, 22, 23, 445, 1433, 1521, 3306, 3389]
        open_ports_status = all(is_port_open(hostname, port) for port in open_ports)
        closed_ports_status = all(not is_port_open(hostname, port) for port in closed_ports)
        return 1 if open_ports_status and closed_ports_status else -1

    except socket.gaierror as e:
        # print(f"Error: {e}")
        return 0

def is_port_open(hostname, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  
        server_address = (hostname, port)
        result = sock.connect_ex(server_address)
        sock.close()
        return result == 0

    except socket.error as e:
        # print(f"Error: {e}")
        return 0

# %%
def check_request_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  

        soup = BeautifulSoup(response.text, 'html.parser')
        total_requests = 0
        external_requests = 0

        for tag in soup.find_all(['img', 'video', 'audio']):
            src = tag.get('src')
            if src:
                total_requests += 1
                absolute_url = urljoin(url, src)
                if urlparse(absolute_url).netloc != urlparse(url).netloc:
                    external_requests += 1

        if total_requests == 0:
            return -1  

        percentage = (external_requests / total_requests) * 100

        if percentage < 22:
            return 1
        elif 22 <= percentage <= 61:
            return 0
        else:
            return -1
    except requests.exceptions.RequestException as e:
        return 0

# %%
def check_url_of_anchor(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  

        soup = BeautifulSoup(response.text, 'html.parser')
        total_anchors = 0
        external_anchors = 0
        no_webpage_anchors = 0

        for tag in soup.find_all('a'):
            href = tag.get('href')
            if href:
                total_anchors += 1
                absolute_url = urljoin(url, href)
                parsed_url = urlparse(absolute_url)

                if parsed_url.netloc != urlparse(url).netloc:
                    external_anchors += 1

                if not parsed_url.path:
                    no_webpage_anchors += 1

        if total_anchors == 0:
            return -1  

        percentage = (external_anchors + no_webpage_anchors) / total_anchors * 100

        if percentage < 31:
            return 1
        elif 31 <= percentage <= 67:
            return 0
        else:
            return -1

    except requests.exceptions.RequestException as e:
        # print(f"Error: {e}")
        return 0

# %%
def check_links_in_tags(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
    except requests.exceptions.RequestException as e:
        # print(f"Error fetching URL: {e}")
        return -1

    soup = BeautifulSoup(html_content, 'html.parser')
    meta_tags = soup.find_all(['meta', 'script', 'link'])
    total_links = 0
    links_within_tags = 0

    for tag in meta_tags:
        tag_content = str(tag)
        links_within_tags += tag_content.count("href=")  

    percentage_links_within_tags = (links_within_tags / total_links) * 100 if total_links != 0 else 0

    if percentage_links_within_tags < 17:
        return 1
    elif 17 <= percentage_links_within_tags <= 81:
        return 0
    else:
        return -1

# %%
def check_sfh(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
    except requests.exceptions.RequestException as e:
        # print(f"Error fetching URL: {e}")
        return 0

    soup = BeautifulSoup(html_content, 'html.parser')
    form_tag = soup.find('form')

    if form_tag:
        action_attribute = form_tag.get('action', '')

        if not action_attribute or action_attribute == "about:blank":
            return -1
        else:
            parsed_action_url = urlparse(action_attribute)
            parsed_url = urlparse(url)
            if parsed_action_url.hostname and parsed_action_url.hostname != parsed_url.hostname:
                return 0
            else:
                return 1
    else:
        return -1

# %%
def check_mail(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
    except requests.exceptions.RequestException as e:
        # print(f"Error fetching URL: {e}")
        return 0

    soup = BeautifulSoup(html_content, 'html.parser')
    mail_functions = soup.find_all(string=lambda text: "mail()" in text)
    mailto_links = soup.find_all(href=lambda href: href and "mailto:" in href)

    if mail_functions or mailto_links:
        return -1
    else:
        return 1

# %%
def check_abnormal_url(url):
    parsed_url = urlparse(url)

    if parsed_url.hostname and parsed_url.hostname in url:
        return 1
    else:
        return -1

# %%
def check_redirect(url):
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()
        redirects_count = len(response.history)

        if redirects_count <= 1:
            return 1
        elif 2 <= redirects_count < 4:
            return 0
        else:
            return -1

    except requests.exceptions.RequestException as e:
        # print(f"Error checking redirects: {e}")
        return 0

# %%
def check_onMouseOver(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
    except requests.exceptions.RequestException as e:
        # print(f"Error fetching URL: {e}")
        return 0

    soup = BeautifulSoup(html_content, 'html.parser')
    onmouseover_elements = soup.find_all(onmouseover=True)

    for element in onmouseover_elements:
        onmouseover_code = element.get('onMouseOver', '')
        if 'window.status' in onmouseover_code:
            return -1

    return 1

# %%
def check_rightClick(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
    except requests.exceptions.RequestException as e:
        # print(f"Error fetching URL: {e}")
        return 0

    soup = BeautifulSoup(html_content, 'html.parser')
    script_tags = soup.find_all('script')

    for script_tag in script_tags:
        script_code = script_tag.string
        if script_code and "event.button==2" in script_code and "return false" in script_code:
            return -1
    return 1

# %%
def check_popup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
    except requests.exceptions.RequestException as e:
        # print(f"Error fetching URL: {e}")
        return 0

    soup = BeautifulSoup(html_content, 'html.parser')
    script_tags = soup.find_all('script')

    for script_tag in script_tags:
        script_code = script_tag.string
        if script_code and "window.open" in script_code and "document.createElement('input')" in script_code:
            return -1
    return 1

# %%
def check_iframe(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
    except requests.exceptions.RequestException as e:
        # print(f"Error fetching URL: {e}")
        return 0

    soup = BeautifulSoup(html_content, 'html.parser')
    iframe_tags = soup.find_all('iframe')

    if iframe_tags:
        return -1  
    else:
        return 1   

# %%
def check_age_of_domain(url):
    try:
        domain = url.split('//')[-1].split('/')[0]
        domain_info = whois.whois(domain)
        creation_date = domain_info.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date:
            today = datetime.now()
            age_in_months = (today - creation_date).days // 30

            if age_in_months >= 6:
                return 1
            else:
                return -1
        else:
            return -1
    except whois.parser.PywhoisError as e:
        # print(f"Error performing WHOIS lookup: {e}")
        return 0

# %%
def check_dns_record(url):
    try:
        domain = url.split('//')[-1].split('/')[0]
        answers = dns.resolver.resolve(domain, 'A')

        if not answers or not answers.rrset.items:
            return -1
        else:
            return 1

    except dns.resolver.NXDOMAIN:
        return -1
    except dns.resolver.Timeout:
        # print("DNS query timed out")
        return 0
    except Exception as e:
        # print(f"Error checking DNS records: {e}")
        return 0

# %%
def check_google_index(url):
    try:
        results = list(search(f"site:{url}"))
        
        for result in results:
            if url in result:
                return 1  
        return -1 

    except Exception as e:
        # print(f"Error performing Google search: {e}")
        return 0

# %%
def get_external_links_count(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        all_links = soup.find_all('a', href=True)
        base_url = requests.utils.urlparse(url).netloc
        external_links_count = sum(1 for link in all_links if not link['href'].startswith(base_url))

        return external_links_count

    except requests.exceptions.RequestException as e:
        # print(f"Error fetching URL: {e}")
        return 0

def check_links_to_webpage(url):
    external_links_count = get_external_links_count(url)

    if external_links_count == -1:
        return -1  
    elif 0 < external_links_count <= 2:
        return 0  
    else:
        return 1  

# %%
def compare_url_to_top_lists(url, top_domains, top_ips):
    try:
        url_domain = requests.utils.urlparse(url).netloc
        url_ip = socket.gethostbyname(url_domain)
    except requests.exceptions.RequestException as e:
        # print(f"Error parsing URL: {e}")
        return 0
    except:
        return 0

    is_domain_in_top_list = url_domain in top_domains
    is_ip_in_top_list = url_ip in top_ips

    return -1 if is_domain_in_top_list or is_ip_in_top_list else 1


# %%
def process_url(url):
    # Parse the URL
    parsed_url = urlparse(url)

    # Initialize the dictionary to store attribute values
    attributes = {}

    # 1. having_IP_Address
    try:
        attributes['Having_IP_Address'] = -1 if parsed_url.hostname.replace('.', '').isdigit() else 1
    except:
        attributes['Having_IP_Address'] = 1

    # 2. URL_Length
    attributes['URL_Length'] = 1 if len(url) < 54 else (0 if 54 <= len(url) <= 75 else -1)

    # 3. Shortining_Service
    attributes['Shortining_Service'] = -1 if "tinyurl.com" in url else 1

    # 4. having_At_Symbol
    attributes['Having_At_Symbol'] = -1 if '@' in parsed_url.netloc else 1

    # 5. double_slash_redirecting
    attributes['Double_Slash_Redirecting'] = -1 if '//' in url[7:] else 1

    # 6. Prefix_Suffix
    attributes['Prefix_Suffix'] = -1 if '-' in parsed_url.netloc else 1

    # 7. having_Sub_Domain
    attributes['Having_Sub_Domain'] = -1 if parsed_url.hostname.count('.') == 1 else (0 if parsed_url.hostname.count('.') == 0 else 1)

    # 8. SSLfinal_State
    attributes['SSLfinal_State'] = check_ssl_state(url)

    # 9. Domain_registeration_length
    attributes['Domain_Registeration_Length'] = check_domain_registration_length(url)

    # 10. Favicon
    attributes['Favicon'] = check_favicon(url)

    # 11. Ports
    attributes['Ports'] = check_ports(url)

    # 12. HTTPS_token
    subdomain = parsed_url.hostname.split('.')[0] if parsed_url.hostname else None
    attributes['HTTPS_token'] = 1 if subdomain is None or 'https' not in subdomain else -1
    
    # 13. Request_URL
    attributes['Request_URL'] = check_request_url(url)

    # 14. URL_of_Anchor
    attributes['URL_of_Anchor'] = check_url_of_anchor(url)

    # 15. Links_in_tags
    attributes['Links_in_tags'] = check_links_in_tags(url)

    # 16. SFH
    attributes['SFH'] = check_sfh(url)

    # 17. Submitting_to_email
    attributes['Submitting_To_Email'] = check_mail(url)

    # 18. Abnormal_URL
    attributes['Abnormal_URL'] = check_abnormal_url(url)

    # 19. Redirect
    attributes['Redirect'] = check_redirect(url)

    # 20. on_mouseover
    attributes['On_MouseOver'] = check_onMouseOver(url)

    # 21. RightClick
    attributes['RightClick'] = check_rightClick(url)

    # 22. popUpWidnow
    attributes['PopUpWidnow'] = check_popup(url)

    # 23. Iframe
    attributes['IFrame'] = check_iframe(url)

    # 24. age_of_domain
    attributes['Age_Of_Domain'] = check_age_of_domain(url)

    # 25. DNSRecord
    attributes['DNSRecord'] = check_dns_record(url)

    # Attributes 26 & 27 are omitted, as they require APIs which are now deprecated.

    # 28. Google_Index
    attributes['Google_Index'] = check_google_index(url)

    # 29. Links_pointing_to_page
    attributes['Links_pointing_to_page'] = check_links_to_webpage(url)

    # 30. Statistical_report
    top_domains = ["esy.es", "hol.es", "000webhostapp.com", "16mb.com", "bit.ly", "for-our.info", "beget.tech", "blogspot.com", "weebly.com", "raymannag.ch"]
    top_ips = ["146.112.61.108", "31.170.160.61", "67.199.248.11", "67.199.248.10", "69.50.209.78", "192.254.172.78", "216.58.193.65", "23.234.229.68", "173.212.223.160", "60.249.179.122"]
    attributes['Statistical_report'] = compare_url_to_top_lists(url, top_domains, top_ips)

    return attributes


# %%
# url = "https://www.youtube.com"
# attributes = process_url(url)
# print(attributes)

# %%
def append_to_csv(file_path, attributes):
    file_exists = True
    try:
        with open(file_path, 'r') as file:
            pass
    except FileNotFoundError:
        file_exists = False

    with open(file_path, 'a', newline='') as csvfile:
        fieldnames = attributes.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(attributes)

# %%
# csv_file_path = "processed_urls.csv"
# append_to_csv(csv_file_path, attributes)


