import os
from itertools import cycle
from .proxy import Proxy
import random

class ProxyManager:
    """
    ProxyManager is a utility class for managing a collection of proxy configurations,
    supporting rotation, addition, removal, and access to the current proxy.

    This class is ideal for use cases such as web scraping, API testing, or load distribution
    where multiple proxies are needed and should be cycled through efficiently.

    Parameters:
        proxies (str | dict | list):
            - A single proxy string (e.g., "http://user:pass@host:port")
            - A dictionary with proxy keys (e.g., {"http": "...", "https": "..."})
            - A list of proxy strings or dictionaries
            - A file path containing proxy entries (one per line)

    Attributes:
        current (Proxy):
            Returns the currently selected proxy from the cycle. If none has been selected yet,
            it initializes with the first proxy in the cycle.

    Methods:
        next() -> Proxy:
            Advances to the next proxy in the cycle and returns it.

        add(proxy: str | dict):
            Adds a new proxy to the list. Raises ValueError if the format is invalid.

        remove(proxy: Proxy | str):
            Removes the specified proxy from the list. If the list becomes empty,
            the cycle is reset.

        __len__() -> int:
            Returns the number of proxies currently managed.

        __repr__() -> str:
            Returns a summary string showing the number of proxies.

    Exceptions:
        TypeError:
            Raised if the input type is invalid.

        ValueError:
            Raised if no valid proxies are provided or if an added proxy is invalid.

    Example:
        >>> manager = ProxyManager(["http://proxy1.com", "http://proxy2.com"])
        >>> proxy = manager.current
        >>> proxy = manager.next()
        >>> manager.add("http://proxy3.com")
        >>> manager.remove("http://proxy1.com")
        >>> print(len(manager))
    """


    def __init__(self, proxies: str | dict | list):
        
        """
        Initializes a ProxyManager instance with a list of proxy configurations.

        Args:
            proxies (str | dict | list):
                - A single proxy string (e.g., "http://user:pass@host:port")
                - A dictionary with proxy keys (e.g., {"http": "...", "https": "..."})
                - A list of proxy strings or dictionaries
                - A file path containing proxy entries (one per line)

        Raises:
            TypeError: If the input type is invalid.

            ValueError: If no valid proxies are provided or if an added proxy is invalid.
        """

        self._proxy_list = []

        if isinstance(proxies, dict) or isinstance(proxies, str) and not os.path.exists(proxies):
            # Single proxy (dict or string)
            proxy_obj = Proxy(proxies)
            self._proxy_list.append(proxy_obj)
        elif isinstance(proxies, list):
            for p in proxies:
                try:
                    proxy_obj = Proxy(p)
                    self._proxy_list.append(proxy_obj)
                except (ValueError, TypeError):
                    continue  # Ignore invalid proxies
        elif isinstance(proxies, str) and os.path.exists(proxies):
            with open(proxies, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        proxy_obj = Proxy(line)
                        self._proxy_list.append(proxy_obj)
                    except (ValueError, TypeError):
                        continue
        else:
            raise TypeError("Input must be a proxy string, dict, list or a valid file path")

        if not self._proxy_list:
            raise ValueError("No valid proxies provided")

        self._proxy_cycle = cycle(self._proxy_list)
        self._current = None

    @property
    def current(self) -> Proxy:
        """
        Returns the currently selected proxy in the cycle.

        If no proxy has been selected yet, it initializes with the first proxy
        in the cycle.

        Returns:
            Proxy: The currently selected proxy.
        """

        if self._current is None:
            self._current = next(self._proxy_cycle)
        return self._current

    def next(self) -> Proxy:
        """
        Returns the next proxy in the cycle.

        Returns:
            Proxy: The next proxy
        """
        self._current = next(self._proxy_cycle)
        return self._current

    def add(self, proxy: str | dict):
        """
        Adds a new proxy to the list of proxies

        Args:
            proxy (str | dict): A proxy string or dictionary

        Raises:
            ValueError: If the proxy is already in the list or is invalid
        """
        try:
            proxy_obj = Proxy(proxy)
            if proxy_obj.url in [p.url for p in self._proxy_list]:
                return  
            self._proxy_list.append(proxy_obj)
            self._proxy_cycle = cycle(self._proxy_list)
        except (ValueError, TypeError):
            raise ValueError("Invalid proxy format")


    def all(self) -> list[Proxy]:
        """Returns a list of all proxies in the manager
        """
       
        return self._proxy_list

    def remove(self, proxy: Proxy | str):
        """Remove a proxy from the list of proxies

        Args:
            proxy (str | Proxy): Proxy to remove from the list

        Raises:
            ValueError: If the proxy is not a string or a Proxy object
        """
        if isinstance(proxy, str):
            proxy = Proxy(proxy)
        self._proxy_list = [p for p in self._proxy_list if p.url != proxy.url]
        if not self._proxy_list:
            self._current = None
            self._proxy_cycle = cycle([])
        else:
            self._proxy_cycle = cycle(self._proxy_list)
            self._current = None

    def get_working_proxy(self) -> Proxy | None:
        """
        Returns the first working proxy from the list of proxies, or None if all proxies are not working.

        A proxy is considered working if it can be used to query the external IP services.

        This method does not modify the list of proxies, it simply returns the first working one.

        :return: The first working proxy, or None if all proxies are not working.
        """
        for proxy in self._proxy_list:
            status,ip_info,error=proxy.check()
            if status:
                return proxy
        return None

    def shuffle(self):
        """
        Shuffles the list of proxies and resets the cycle.
        This can be useful if you want to randomly select a proxy from the list
        or if you want to re-order the proxies after adding or removing some.

        .. note::
            This method does not check if the proxies are valid or not.
            It simply shuffles the list and resets the cycle.
        """
        random.shuffle(self._proxy_list)
        self._proxy_cycle = cycle(self._proxy_list)
        self._current = None

    def as_dict_list(self) -> list:
        """
        Returns a list of dictionaries representing the proxies in the manager.

        Each dictionary contains the proxy details in the following format:

        .. code-block:: python

            {
                "type": "http",
                "host": "127.0.0.1",
                "port": 8080,
                "user": "username",
                "password": "password"
            }

        Returns:
            list: A list of dictionaries representing the proxies in the manager.
        """
        return [proxy.to_dict for proxy in self._proxy_list]


    


    def __len__(self):
        return len(self._proxy_list)

    def __repr__(self):
        return f"<ProxyManager proxies={len(self._proxy_list)}>"









    
