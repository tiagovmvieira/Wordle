import requests

from typing import Union, List, Tuple, Dict

class APIClient:
    def __init__(self, base_url: str, api_headers: Dict[str, str]):
        self._base_url = base_url
        self._api_headers = api_headers

        self.session = requests.Session()
    
    def request(self, method: str, endpoint: str, params: Union[None, dict, List[Tuple]] = None, data: Union[None, Dict[str, any]] = None,
                headers: Union[None, Dict[str, str]] = None)-> requests.Response:
        r = self.session.request(
            method=method,
            url=f"{self._base_url}{endpoint}",
            params=params,
            json=data,
            headers=headers if headers else self._api_headers
        )

        r.raise_for_status()
        
        return r









