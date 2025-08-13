import ipaddress

def is_valid_ip(ip: str) -> bool:
    """
    Validates if the given IP address is a public IP address.

    Parameters:
        ip (str): The IP address to validate.

    Returns:
        bool: True if the IP address is valid and public, False otherwise.
    """

    try:
        ip_obj = ipaddress.ip_address(ip)
        return not ip_obj.is_private
    except ValueError:
        return False
    

