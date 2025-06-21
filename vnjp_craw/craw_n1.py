from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re
import csv
import os

domains = [
    "/mimi-kara-n1-goi/unit-1.html",
    "/mimi-kara-n1-goi/unit-2.html",
    "/mimi-kara-n1-goi/unit-3.html",
    "/mimi-kara-n1-goi/unit-4.html",
    "/mimi-kara-n1-goi/unit-5.html",
    "/mimi-kara-n1-goi/unit-6.html",
    "/mimi-kara-n1-goi/unit-7.html",
    "/mimi-kara-n1-goi/unit-8.html",
    "/mimi-kara-n1-goi/unit-9.html",
    "/mimi-kara-n1-goi/unit-10.html",
    "/mimi-kara-n1-goi/unit-11.html",
    "/mimi-kara-n1-goi/unit-12.html",
    "/mimi-kara-n1-goi/unit-13.html",
    "/mimi-kara-n1-goi/unit-14.html"
]

for domain in domains:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = f"https://www.vnjpclub.com{domain}"
    driver.get(url)
    html = driver.page_source
    driver.quit()
    time.sleep(2)
    soup = BeautifulSoup(html, "html.parser")
    lines = []
    for boxtv in soup.select(".boxtv"):
        match = re.match(r"^(\d+)\.\s*(.+)", boxtv.select_one(".tuvung").text.strip())
        furigana_element = boxtv.select_one(".tuvung b ruby rt")
        furigana = furigana_element.text.strip() if furigana_element is not None else ""
        if match:
            number = match.group(1)
            new_word = match.group(2) 
        arr_hanviet = boxtv.select("[class^='hanviet']")
        hanviet = [el.text.strip() for el in arr_hanviet][0]
        
        arr_meaning = boxtv.find_all(class_=re.compile(r"^nghia\d*"))
        meaning = [el.text.strip() for el in arr_meaning][0]
        vidu_boxes = boxtv.select(".vidubox")
        pairs = []
        if vidu_boxes is not None:
            for example in vidu_boxes:
                first_example_element = example.select_one(".tuvung")
                first_example = first_example_element.text.strip() if first_example_element is not None else ""
                first_example_vi_element = example.select_one(".tuvung")

                first_example_vi = first_example_vi_element.find_next_sibling("div", class_="nghiavidu").text.strip() if first_example_vi_element is not None else ""
                
                vidu_container = example.find("div", class_="vidunotfirst")
                pairs.append([first_example, first_example_vi])

                if vidu_container is not None:
                    tuvung_elements = vidu_container.find_all("div", class_="tuvung")
                    for tuvung in tuvung_elements:
                        nghia_div = tuvung.find_next_sibling("div", class_="nghiavidu")
                        example_html = tuvung.text.strip()
                        meaning_text = nghia_div.text.strip() if nghia_div else ""
                        pairs.append([example_html, meaning_text])

        lines.append({
            "stt": number,
            "word": new_word,
            "furigana": furigana,
            "Sino-Vietnamese": hanviet,
            "meaning": meaning,
            "example": pairs})

        # print(f"{number}, {meaning}")
    csv_file = "output_n1.csv"
    file_exists = os.path.isfile(csv_file) and os.path.getsize(csv_file) > 0
    with open(csv_file, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["stt", "word", "furigana", "Sino-Vietnamese", "meaning", "example"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(lines)
