import re, difflib, requests, tldextract
from datetime import datetime, timezone
from urllib.parse import urlparse

RISKY_TLDS = {"top", "xyz", "click", "link", "info", "online", "site", "live",
              "icu", "buzz", "shop", "support", "rest", "cam", "work"}
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly",
              "rb.gy", "shorturl.at", "tiny.cc"}
BRANDS = ["paypal", "amazon", "google", "apple", "microsoft", "netflix", "whatsapp",
          "facebook", "instagram", "sbi", "hdfc", "icici", "axisbank", "paytm",
          "phonepe", "flipkart", "fedex", "dhl", "usps", "correos", "irs", "hmrc"]


def domain_age(domain: str):
    """Returns (age_in_days or None, registry_status)."""
    try:
        r = requests.get(f"https://rdap.org/domain/{domain}", timeout=8)
        if r.status_code == 404:
            return None, "not found in domain registry"
        if r.status_code != 200:
            return None, "registry lookup unavailable"
        for e in r.json().get("events", []):
            if e.get("eventAction") == "registration":
                d = datetime.fromisoformat(e["eventDate"].replace("Z", "+00:00"))
                return (datetime.now(timezone.utc) - d).days, "registered"
        return None, "registered, date unknown"
    except Exception:
        return None, "registry lookup failed"


def check_url(url: str) -> dict:
    explicit_http = url.lower().startswith("http://")
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    p = urlparse(url)
    host = (p.hostname or "").lower()
    ext = tldextract.extract(host)
    registered = f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain
    flags = []

    if re.fullmatch(r"[\d.]+", host):
        flags.append("uses a raw IP address instead of a domain")
    if "xn--" in host:
        flags.append("punycode domain (possible look-alike characters)")
    if ext.suffix.split(".")[-1] in RISKY_TLDS:
        flags.append(f"high-risk domain ending .{ext.suffix}")
    if registered in SHORTENERS:
        flags.append("URL shortener hides the real destination")
    if explicit_http:
        flags.append("no HTTPS")
    if host.count("-") >= 2:
        flags.append("many hyphens in domain")
    for b in BRANDS:
        if b in host and ext.domain != b:
            flags.append(f"contains brand '{b}' but the real domain is {registered}")
        elif ext.domain != b and difflib.SequenceMatcher(None, ext.domain, b).ratio() >= 0.8:
            flags.append(f"look-alike of brand '{b}'")

    age, status = domain_age(registered)
    if age is not None and age < 90:
        flags.append(f"domain is only {age} days old")
    if status == "not found in domain registry":
        flags.append("domain does not exist in the registry")

    return {"url": url, "registered_domain": registered, "domain_age_days": age,
            "registry_status": status, "red_flags": flags}


TOOLS = [
    {
        "type": "function",
        "name": "check_url",
        "description": "Inspect a link or domain for phishing signs: look-alike brands, "
                       "risky endings, shorteners, missing HTTPS, and domain age.",
        "parameters": {
            "type": "object",
            "properties": {"url": {"type": "string", "description": "The link or domain"}},
            "required": ["url"],
        },
    },
    {"type": "web_search"},
]

TOOL_FUNCS = {"check_url": check_url}