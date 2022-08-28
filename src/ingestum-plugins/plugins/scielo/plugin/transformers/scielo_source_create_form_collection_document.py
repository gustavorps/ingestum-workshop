import os
import json
import logging
import urllib.error
import urllib.parse

import requests
from pydantic import BaseModel
from typing import Optional
from bs4 import BeautifulSoup
from typing_extensions import Literal

from ingestum import documents
from ingestum import sources
from ingestum.transformers.base import BaseTransformer

__logger__ = logging.getLogger("ingestum")
__script__ = os.path.basename(__file__).replace(".py", "")


class Transformer(BaseTransformer):
    """
    Transforms a `scielo` source into a `Collection` of `Ontology` forms. Given a expr, pull the clincal trials from clinicaltrials.org

    :param query: The search string to pass to a Scielo query
    :type query: str
    """

    class ArgumentsModel(BaseModel):
        query: str

    class InputsModel(BaseModel):
        source: sources.Scielo

    class OutputsModel(BaseModel):
        document: documents.Collection

    arguments: ArgumentsModel
    inputs: Optional[InputsModel]
    outputs: Optional[OutputsModel]

    type: Literal[__script__] = __script__

    def extract(self):
        url = f'https://search.scielo.org/?q={self.arguments.query}&count=50'
        content = []
        try:
            response = requests.get(url)
            response.raise_for_status()
        except Exception as e:
            __logger__.warning(
                "full text extraction failed",
                extra={
                    "props": {
                        "transformer": self.type,
                        "url": url,
                        "error": str(e),
                    }
                },
            )
        else:
            soup = BeautifulSoup(response.content, "lxml")
            body_node = soup.body

            for item in body_node.select(".results .item"):
                title = item.select_one('.title')
                content.append(
                    documents.Form.new_from(
                        None, 
                        origin=url,
                        content={'name': title.text},
                    )
                )

        return content

    def transform(self, source):
        super().transform(source=source)

        content = self.extract()

        return documents.Collection.new_from(
            source, content=content, context=self.context(exclude=["query"])
        )
