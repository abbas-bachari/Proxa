import json
def get_flag_emoji(country_code):

    if not country_code or len(country_code) != 2:
        return "🌐"

    return "".join(chr(127397 + ord(c)) for c in country_code.upper())

class IpInfo():
    def __init__(self,ip_address,country_name='',country_code='',source=''):
        """
        Initializes an IpInfo object with the given parameters

        Parameters:
            ip_address (str): The IP address of the proxy
            country_name (str): The name of the country of the proxy
            country_code (str): The 2-letter country code of the proxy
            source (str): The source of the information
        """

        self.ip_address=ip_address
        self.country_name=country_name or 'Unknown'
        self.country_code=country_code or 'Unknown'
        self.flag=get_flag_emoji(country_code=country_code)
        self.source=source


    
    def to_dict(self):
        """
        Returns a dictionary representation of the IpInfo object

        Returns:
            dict: A dictionary with the ip address, country name, and country code
        """

        return {
            "ip_address": self.ip_address,
            "country_name": self.country_name,
            "country_code": self.country_code,
            "flag":self.flag
        }

    def __str__(self):
        return json.dumps(self.to_dict())