# -*- coding: utf-8 -*-

#
# Copyright (c) 2020 Sorcero, Inc.
#
# This file is part of Sorcero's Language Intelligence platform
# (see https://www.sorcero.com).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#


import os
from typing import Any, Callable
import copy

from pydantic import BaseModel
from typing import Optional
from typing_extensions import Literal

from ingestum import documents
from ingestum import sources
from ingestum.transformers.base import BaseTransformer
from ingestum.transformers.xls_source_create_tabular_document import Transformer as XLSTransformer

__script__ = os.path.basename(__file__).replace(".py", "")


class TabuleMapTypesTransformer(BaseTransformer):
    """
    Transforms a `XLS` source input into a `Collection` documents where each
    document is a `Tabular` document for each XLS sheet.
    """
    """
    Transforms a `Tabular` document into another `Tabular` document where a new
    empty column is inserted at the given position.

    :param position: Starting position for the new columns
    :type position: int
    :param columns: The number of new columns
    :type columns: int
    """

    class ArgumentsModel(BaseModel):
        func: Callable[..., Any]

    class InputsModel(BaseModel):
        document: documents.Tabular

    class OutputsModel(BaseModel):
        document: documents.Tabular

    arguments: ArgumentsModel
    inputs: Optional[InputsModel]
    outputs: Optional[OutputsModel]

    type: Literal[__script__] = __script__

    def transform(self, document: documents.Tabular) -> documents.Tabular:
        super().transform(document=document)

        rows = len(document.content)
        columns = len(document.content[0]) if rows else 0
        content = tuple(self.arguments.func(c) for c in copy.copy(document.content)[1:])
        print(content)
        return documents.Tabular(
            # document,
            content=content,
            rows=rows,
            columns=columns,
        )
