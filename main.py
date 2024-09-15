from curl_cffi import requests


def get_status_code(url: str):
    return requests.get(url, impersonate="chrome").status_code


if __name__ == "__main__":
    x = ["abc", "def", "ghi"]
    x = "\n".join(x)
    print(x)
