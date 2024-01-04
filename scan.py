import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15"

def get_forms(url):
    soup = BeautifulSoup(s.get(url).content, "html.parser")
    return soup.find_all("form")

def form_details(form):
    detailsOfForm = {}
    action = form.attrs.get("action")
    method = form.attrs.get("method", "get")
    inputs = []

    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")

        inputs.append({
            "type": input_type,
            "name": input_name,
            "value": input_value
        })

    detailsOfForm['action'] = action
    detailsOfForm['method'] = method
    detailsOfForm['inputs'] = inputs

    return detailsOfForm


def vulnerable(response):
    errors = {"quoted string not properly terminated",
    "unclosed quotation mark after the character string ",
    "you have an error in you SQL syntax"
    }

    for error in errors:
        if error in response.content.decode().lower():
            return True

    return False


def sql_injection_scan(url):
    forms = get_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")

    for form in forms:
        details = form_details(form)  # Dönen değeri details değişkenine atamayı unutmayın

        for i in "\"'":
            data = {}
            for input_tag in details["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    data[input_tag['name']] = input_tag["value"] + i

                elif input_tag["type"] != "submit":
                    data[input_tag['name']] = f"test{i}"

            print(url)
            form_details(form)

            if details["method"] == "post":
                res = s.post(url, data=data)

            elif details["method"] == "get":
                res = s.get(url, params=data)

            if vulnerable(res):
                print("SQL Injection Attack vulnerability in link: ", url)
            else:
                print("No SQL injection attack vulnerability detected")
                break


if __name__ == "__main__":
    urlToBeChecked = "https://prplbx.com"  
    sql_injection_scan(urlToBeChecked)                                            

