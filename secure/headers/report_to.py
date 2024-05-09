import json
from typing import Dict, Optional, Union
from typing import List


class ReportTo:
    """Configure reporting endpoints

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/report-to
    https://developers.google.com/web/updates/2018/09/reportingapi

    :param max_age: endpoint TIL in seconds
    :type max_age: int
    :param include_subdomains: enable for subdomains, defaults to False
    :type include_subdomains: bool, optional
    :param group: endpoint name, defaults to None
    :type group: Optional[str], optional
    :param endpoints: variable number of endpoints
    :type endpoints: List[Dict[str, Union[str, int]]]
    """

    def __init__(
        self,
        max_age: int,
        include_subdomains: bool = False,
        group: Optional[str] = None,
        *endpoints: List[Dict[str, Union[str, int]]],
    ) -> None:
        self.header = "Report-To"

        report_to_endpoints = json.dumps(endpoints)

        report_to_object: Dict[str, Union[str, int]] = {
            "max_age": max_age,
            "endpoints": report_to_endpoints,
        }

        if group:
            report_to_object["group"] = group

        if include_subdomains:
            report_to_object["include_subdomains"] = include_subdomains

        self.value = json.dumps(report_to_object)

    def set(self, value: str) -> "ReportTo":
        """Set custom value for `Report-To` header

        :param value: custom header value
        :type value: str
        :return: ReportTo class
        :rtype: ReportTo
        """
        self.value = value
        return self
