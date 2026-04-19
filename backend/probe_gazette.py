"""Probe eGazette structure"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from curl_cffi import requests
from bs4 import BeautifulSoup

# Main page
r = requests.get('https://egazette.gov.in', impersonate='chrome', verify=False)
soup = BeautifulSoup(r.text, 'lxml')

# Check all links with keywords
print("=== Links with gazette/notification/order keywords ===")
count = 0
for a in soup.find_all('a', href=True):
    t = a.get_text(strip=True).encode('ascii','replace').decode()
    h = a['href']
    combined = f"{t} {h}".lower()
    if any(kw in combined for kw in ['gazette', 'notification', 'order', 'circular', 'extraordinary', 'ordinary']):
        if t and len(t) > 3:
            print(f"  {t[:80]} -> {h[:120]}")
            count += 1
            if count >= 15:
                break

# Check PDFs
pdf_links = [a for a in soup.find_all('a', href=True) if '.pdf' in a['href'].lower()]
print(f"\nPDF links on main page: {len(pdf_links)}")
for a in pdf_links[:5]:
    t = a.get_text(strip=True).encode('ascii','replace').decode()[:60]
    print(f"  {t} -> {a['href'][:120]}")

# Check for navigable sub-pages
print("\n=== All unique internal paths ===")
paths = set()
for a in soup.find_all('a', href=True):
    h = a['href']
    if h.startswith('/') and not h.startswith('//'):
        paths.add(h.split('?')[0])
for p in sorted(paths)[:20]:
    print(f"  {p}")
