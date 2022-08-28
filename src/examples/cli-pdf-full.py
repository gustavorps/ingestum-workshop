import argparse
import uuid
import pathlib

from ingestum import engine
from ingestum import manifests
from ingestum import pipelines
from ingestum import transformers
from ingestum.utils import stringify_document


def generate_pipeline():
    pipeline = pipelines.base.Pipeline(
        name='default',
        pipes=[
            # Extract all tables from the PDF into
            # a collection.
            pipelines.base.Pipe(
                name="tables",
                sources=[pipelines.sources.Manifest(source="pdf")],
                steps=[
                    transformers.PDFSourceCreateTabularCollectionDocument(
                        first_page=-1, last_page=-1, options={"line_scale": 15}
                    )
                ],
            ),
            # Create a new collection with the Markdown
            # version of each of these tables.
            pipelines.base.Pipe(
                name="tables-replacements",
                sources=[
                    pipelines.sources.Pipe(
                        name="tables",
                    )
                ],
                steps=[
                    transformers.CollectionDocumentTransform(
                        transformer=transformers.TabularDocumentCreateMDPassage()  # noqa: E251
                    )
                ],
            ),
            # Extract all shapes (e.g. figures) from the PDF
            # into a collection.
            pipelines.base.Pipe(
                name="shapes",
                sources=[pipelines.sources.Manifest(source="pdf")],
                steps=[
                    transformers.PDFSourceShapesCreateResourceCollectionDocument(  # noqa: E251
                        directory="output", first_page=-1, last_page=-1
                    )
                ],
            ),
            # Create a new collection with text references
            # (e.g. file://shape.png) for each shape.
            pipelines.base.Pipe(
                name="shapes-replacements",
                sources=[pipelines.sources.Pipe(name="shapes")],
                steps=[
                    transformers.CollectionDocumentTransform(
                        transformer=transformers.ResourceCreateTextDocument()
                    )
                ],
            ),
            # Extract all images (e.g. PNG images) from the
            # PDF into a collection.
            pipelines.base.Pipe(
                name="images",
                sources=[pipelines.sources.Manifest(source="pdf")],
                steps=[
                    transformers.PDFSourceImagesCreateResourceCollectionDocument(  # noqa: E251
                        directory="output", first_page=-1, last_page=-1
                    )
                ],
            ),
            # Create a new collection with text references
            # (e.g. file://image.png) for every image.
            pipelines.base.Pipe(
                name="images-replacements",
                sources=[pipelines.sources.Pipe(name="images")],
                steps=[
                    transformers.CollectionDocumentTransform(
                        transformer=transformers.ResourceCreateTextDocument()
                    )
                ],
            ),
            # Merge all previously extracted tables, shapes
            # and images (extractables) into a single
            # collection.
            pipelines.base.Pipe(
                name="extractables",
                sources=[
                    pipelines.sources.Pipe(name="tables"),
                    pipelines.sources.Pipe(name="shapes"),
                ],
                steps=[transformers.CollectionDocumentMerge()],
            ),
            # Merge all previously extracted tables, shapes
            # and images (extractables) into a single
            # collection.
            pipelines.base.Pipe(
                name="extractables",
                sources=[
                    pipelines.sources.Pipe(name="extractables"),
                    pipelines.sources.Pipe(name="images"),
                ],
                steps=[transformers.CollectionDocumentMerge()],
            ),
            # Merge all previously created Markdown and text
            # references (replacements) into a single
            # collection.
            pipelines.base.Pipe(
                name="replacements",
                sources=[
                    pipelines.sources.Pipe(name="tables-replacements"),
                    pipelines.sources.Pipe(name="shapes-replacements"),
                ],
                steps=[transformers.CollectionDocumentMerge()],
            ),
            # Merge all previously created Markdown and text
            # references (replacements) into a single
            # collection.
            pipelines.base.Pipe(
                name="replacements",
                sources=[
                    pipelines.sources.Pipe(name="replacements"),
                    pipelines.sources.Pipe(name="images-replacements"),
                ],
                steps=[transformers.CollectionDocumentMerge()],
            ),
            # Extract all human-readable text fom the PDF, except
            # for the extractables, and replace these with Markdown
            # tables and text references.
            pipelines.base.Pipe(
                name="text",
                sources=[
                    pipelines.sources.Manifest(source="pdf"),
                    pipelines.sources.Pipe(name="extractables"),
                    pipelines.sources.Pipe(name="replacements"),
                ],
                steps=[
                    transformers.PDFSourceCreateTextDocumentReplacedExtractables(  # noqa: E251
                        first_page=-1, last_page=-1
                    ),
                ],
            )
        ]
    )
    return pipeline


def generate_manifest(local_path, destination, first_page, last_page):
    manifest = manifests.base.Manifest(
        sources=[
            manifests.sources.PDF(
                id='id',
                pipeline='default',
                first_page=first_page,
                last_page=last_page,
                location=manifests.sources.locations.Local(
                    path=local_path
                ),
                destination=manifests.sources.destinations.Local(
                    directory=str(destination.absolute())
                ))])
    return manifest


def ingest(local_path, first_page, last_page):
    destination = pathlib.Path(f'./.data/{uuid.uuid1()}/')
    manifest = generate_manifest(local_path, destination, first_page, last_page)
    pipeline = generate_pipeline()

    results, *_ = engine.run(
        manifest=manifest,
        pipelines=[pipeline],
        pipelines_dir=None,
        artifacts_dir=None,
        workspace_dir=None,
    )
    print(destination)
    return results[0]


def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command', required=True)
    subparser.add_parser('export')
    ingest_parser = subparser.add_parser('ingest')
    ingest_parser.add_argument('path')
    ingest_parser.add_argument('first_page', type=int)
    ingest_parser.add_argument('last_page', type=int)
    args = parser.parse_args()

    if args.command == 'export':
        output = generate_pipeline()
    else:
        output = ingest(args.path, args.first_page, args.last_page)

    print(stringify_document(output))


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    # python src/examples/cli-pdf-full.py ingest src/ingestum/tests/data/test.pdf 1 3
    main()
