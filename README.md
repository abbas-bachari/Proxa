# Proxa

[![PyPI version](https://img.shields.io/pypi/v/proxa.svg?style=flat-square)](https://pypi.org/project/proxa/)
[![Python Version](https://img.shields.io/pypi/pyversions/proxa.svg?style=flat-square)](https://www.python.org/)
[![License](https://img.shields.io/pypi/l/proxa.svg?style=flat-square)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/proxa.svg?style=flat-square)](https://pypi.org/project/proxa/)
[![GitHub stars](https://img.shields.io/github/stars/abbas-bachari/proxa?style=flat-square)](https://github.com/abbas-bachari/proxa/stargazers)

> **Proxa** — A simple yet powerful Python library for managing and validating proxies.

---

## 📌 Features

- ✅ Easy proxy parsing from strings, dictionaries, or files
- 🔄 Automatic proxy rotation
- 🔀 Shuffle proxy list randomly
- 🧪 Built-in proxy checking with multiple IP lookup services
- 📦 Ready-to-use formats for `requests`, `Telethon`, and more
- ⚡ Lightweight and dependency-minimal

---

## 📥 Installation

```bash
pip install proxa
```

---

## 🚀 Quick Start

```python
from proxa import ProxyManager

# Initialize with a list of proxies
manager = ProxyManager([
    "http://user:pass@127.0.0.1:8080",
    "socks5://10.10.1.0:3128"
])

# Get the current proxy
proxy=manager.current

print(proxy.url)

# Rotate to the next proxy
proxy=manager.next()
print(proxy.url)

# Shuffle proxies to randomize order
manager.shuffle()
print("Proxies shuffled.")


# Check if proxy works and get IP info
status, ip_info, error = proxy.check()

if status:
    print("Proxy is working. IP info:", ip_info)
else:
    print("Proxy check failed. Error:", error)





# Check if a proxy works
working_proxy = manager.get_working_proxy()
if working_proxy:
    print("Working proxy:", working_proxy.url)



```

---

## 🛠 Usage Examples

### From a File

```python
manager = ProxyManager("proxies.txt")
```

### Add & Remove Proxies

```python
manager.add("http://new-proxy.com:8080")
manager.remove("http://user:pass@127.0.0.1:8080")
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Contribute

Contributions are welcome!

1. Fork the repo  
2. Create your feature branch  
3. Submit a pull request

---

Made with ❤️ by [Abbas Bachari](https://github.com/abbas-bachari)
