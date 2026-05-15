"""
Collect metadata of all elements from https://www.saucedemo.com
using Playwright (Python) and save it into a text file.

Install:
    pip install playwright
    playwright install

Run:
    python collect_metadata.py
"""

from playwright.sync_api import sync_playwright
import json
from datetime import datetime


OUTPUT_FILE = "saucedemo_metadata.txt"


def collect_element_metadata(page):
    """
    Collect metadata for all DOM elements.
    """

    script = """
    () => {
        function getXPath(element) {
            if (element.id)
                return `//*[@id="${element.id}"]`;

            const parts = [];

            while (element && element.nodeType === Node.ELEMENT_NODE) {
                let index = 1;
                let sibling = element.previousElementSibling;

                while (sibling) {
                    if (sibling.tagName === element.tagName) {
                        index++;
                    }
                    sibling = sibling.previousElementSibling;
                }

                const tagName = element.tagName.toLowerCase();
                const pathIndex = index > 1 ? `[${index}]` : '';
                parts.unshift(`${tagName}${pathIndex}`);

                element = element.parentElement;
            }

            return '/' + parts.join('/');
        }

        const elements = Array.from(document.querySelectorAll('*'));

        return elements.map((el, idx) => {
            const rect = el.getBoundingClientRect();

            return {
                index: idx,
                tag: el.tagName.toLowerCase(),
                id: el.id || '',
                class: el.className || '',
                name: el.getAttribute('name') || '',
                type: el.getAttribute('type') || '',
                value: el.getAttribute('value') || '',
                text: (el.innerText || '').trim().substring(0, 200),
                placeholder: el.getAttribute('placeholder') || '',
                aria_label: el.getAttribute('aria-label') || '',
                role: el.getAttribute('role') || '',
                href: el.getAttribute('href') || '',
                src: el.getAttribute('src') || '',
                xpath: getXPath(el),
                css_selector: el.id
                    ? `#${el.id}`
                    : el.className
                        ? `${el.tagName.toLowerCase()}.${el.className.toString().replace(/\\s+/g, '.')}`
                        : el.tagName.toLowerCase(),
                visible: !!(
                    el.offsetWidth ||
                    el.offsetHeight ||
                    el.getClientRects().length
                ),
                enabled: !el.disabled,
                x: rect.x,
                y: rect.y,
                width: rect.width,
                height: rect.height
            };
        });
    }
    """

    return page.evaluate(script)


def save_metadata(metadata, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Metadata Collection Time: {datetime.now()}\n")
        f.write("=" * 120 + "\n\n")

        for item in metadata:
            f.write(json.dumps(item, indent=4, ensure_ascii=False))
            f.write("\n\n")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            viewport={"width": 1440, "height": 2000}
        )

        print("Opening website...")
        page.goto("https://www.saucedemo.com", wait_until="networkidle")

        print("Collecting metadata...")
        metadata = collect_element_metadata(page)

        print(f"Collected {len(metadata)} elements")

        print(f"Saving to {OUTPUT_FILE}...")
        save_metadata(metadata, OUTPUT_FILE)

        browser.close()

        print("Done!")


if __name__ == "__main__":
    main()