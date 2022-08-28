from typing_extensions import Literal

from ingestum import sources
from ingestum.manifests.sources.base import BaseSource


class Source(BaseSource):

    type: Literal["scielo"] = "scielo"

    query: str
    query_placeholder: str = ""

    def get_source(self, output_dir, cache_dir):
        return sources.Scielo()
