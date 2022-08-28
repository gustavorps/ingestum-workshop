from typing_extensions import Literal

from ingestum.sources.base import BaseSource


class Source(BaseSource):
    """
    Class to support `scielo` input sources
    """

    type: Literal["scielo"] = "scielo"

    def get_metadata(self):
        return super().get_metadata()
