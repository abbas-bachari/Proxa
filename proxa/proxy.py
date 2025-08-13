from .ip_info import IpInfo
from urllib.parse import urlparse
import requests
from .utils import is_valid_ip
from requests.exceptions import ProxyError, ConnectTimeout, ReadTimeout
class Proxy:
    """
    Proxy is a utility class that represents a single proxy configuration and provides
    multiple formats for integration with different libraries and services.

    It supports parsing from both string and dictionary formats, and includes methods
    for converting the proxy to formats compatible with Telethon, requests, and general usage.

    Parameters:
        proxy (str | dict):
            - A proxy string (e.g., "http://user:pass@host:port")
            - A dictionary with keys: 'type', 'host', 'port', 'user', 'password'

    Attributes:
        type (str): Proxy scheme (e.g., 'http', 'socks5')
        host (str): Proxy hostname or IP address
        port (int): Proxy port number
        user (str | None): Optional username for authentication
        password (str | None): Optional password for authentication

    Properties:
        url (str):
            Full proxy URL including authentication if available.

        for_telethon (tuple):
            Proxy configuration formatted for use with Telethon.

        for_requests (dict):
            Dictionary format for use with the requests library.

        to_dict (dict):
            Dictionary representation of the proxy configuration.

    Methods:
        check() -> IpInfo | None:
            Attempts to verify the proxy by querying external IP services.
            Returns an IpInfo object if successful, otherwise None.

    Exceptions:
        TypeError:
            Raised if the input is neither a string nor a dictionary.

        ValueError:
            Raised if required fields (type, host, port) are missing or invalid.

    Example:
        >>> proxy = Proxy("http://user:pass@127.0.0.1:8080")
        >>> print(proxy.url)
        >>> print(proxy.for_requests)
        >>> ip_info = proxy.get_ip_info()
        >>> print(ip_info)

    """


    def __init__(self, proxy: str | dict):
        """
        Initializes a Proxy object from a string or dictionary.

        Args:
            proxy (str | dict):
                - A string with the proxy URL (e.g., "http://user:pass@host:port")
                - A dictionary with keys: 'type', 'host', 'port', 'user', 'password'

        Raises:
            TypeError: If the input is neither a string nor a dictionary.

            ValueError: If required fields (type, host, port) are missing or invalid.
        """
        if isinstance(proxy, dict):
            self.type = proxy.get('type', 'http')
            self.host = proxy.get('host')
            self.port = int(proxy.get('port')) if proxy.get('port') else None
            self.user = proxy.get('user')
            self.password = proxy.get('password')
        elif isinstance(proxy, str):
            if "://" not in proxy:
                proxy = "http://" + proxy
            parsed = urlparse(proxy)
            self.type = parsed.scheme or 'http'
            self.host = parsed.hostname
            self.port = parsed.port
            self.user = parsed.username
            self.password = parsed.password
        else:
            raise TypeError("Proxy must be a string or dict")

        if not all([self.type, self.host, self.port]):
            raise ValueError(f"Invalid proxy data: {proxy}")

    @property
    def url(self) -> str:
        """Returns the full proxy URL including authentication if available."""
        if self.user and self.password:
            return f"{self.type}://{self.user}:{self.password}@{self.host}:{self.port}"
        return f"{self.type}://{self.host}:{self.port}"

    @property
    def for_telethon(self) -> tuple:
        """
        Proxy configuration formatted for use with Telethon.

        If the proxy requires authentication, the tuple will contain 6 elements:
            (type, host, port, use_auth, user, password)

        Otherwise, the tuple will contain 3 elements:
            (type, host, port)

        Returns:
            tuple
        """

        if self.user and self.password:
            return (self.type, self.host, self.port, True, self.user, self.password)
        return (self.type, self.host, self.port)
    @property
    def for_requests(self):
        """
        Dictionary format for use with the requests library.

        Returns:
            dict: A dictionary containing 'http' and 'https' keys with the proxy URL
        """
        proxy_url=self.url
        return {'http':proxy_url,'https':proxy_url}
    @property
    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the proxy configuration.

        The dictionary will contain the 'type', 'host', and 'port' keys, and
        optionally 'user' and 'password' if they are set.

        Returns:
            dict: A dictionary representation of the proxy configuration.
        """
        data = {
            "type": self.type,
            "host": self.host,
            "port": self.port
        }
        if self.user and self.password:
            data["user"] = self.user
            data["password"] = self.password
        return data

    def check(self,timeout=5):
   
        """
        Attempts to verify the proxy by querying external IP services.

        Args:
            timeout (int): Maximum time in seconds to wait for a response from each service.

        Returns:
            status (bool): True if the proxy is working, False otherwise.
            ip_info (IpInfo | None): An IpInfo object with information about the
                current IP address if the proxy is working, otherwise None.
            error (str | None): An error message if the proxy fails to work, otherwise None.

        Raises:
            TypeError: If the input type is invalid.

            ValueError: If the input is invalid or if the proxy is not working.

        Example:
            >>> proxy = Proxy("http://user:pass@127.0.0.1:8080")
            >>> status, ip_info, error = proxy.check()
            >>> if status:
            >>>     print(ip_info)
            >>> else:
            >>>     print(error)
        """
        urls = [
            'http://ip-api.com/json/',
            'https://api.myip.com',
            "https://ipwho.is",
            'https://icanhazip.com',
            'http://httpbin.org/ip',
            'https://api.ipify.org/'
        ]

        headers ={ 
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Accept": "application/json"} 
            

        for address in urls:
            ip_info = None
            try:
                response = requests.get(address, timeout=timeout, headers=headers, proxies=self.for_requests)
                if response.status_code != 200:
                    continue

                match address:
                    case 'http://ip-api.com/json/':
                        data = response.json()
                        ip = data.get("query")
                        if ip:
                            ip_info = IpInfo(ip, data.get("country"), data.get("countryCode"),source=address)

                    case 'https://ipwho.is':
                        data = response.json()
                        ip = data.get("ip")
                        if ip:
                            ip_info = IpInfo(ip, data.get("country"), data.get("country_code"),source=address)

                    case 'https://api.myip.com':
                        data = response.json()
                        ip = data.get("ip")
                        if ip:
                            ip_info = IpInfo(ip, data.get("country"), data.get("cc"),source=address)

                    case 'https://icanhazip.com' | 'https://api.ipify.org/':
                        ip = response.text.strip()
                        if is_valid_ip(ip):
                            ip_info = IpInfo(ip,source=address)

                    case 'http://httpbin.org/ip':
                        data = response.json()
                        ip = data.get("origin")
                        if ip:
                            ip = ip.split(',')[0].strip()
                            if is_valid_ip(ip):
                                ip_info = IpInfo(ip,source=address)
                if ip_info:
                    return True, ip_info, None

            except (ProxyError, ConnectTimeout, ReadTimeout) as e:
                return False, None, str(e)
            except Exception as e:
                continue
                
        return False, None, "All services failed"
    
    def __repr__(self):
        return f"<Proxy {self.url}>"

    def __str__(self):
        return self.url
