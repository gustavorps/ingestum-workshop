import argparse
import tempfile
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
            pipelines.base.Pipe(
                name='default',
                sources=[
                    pipelines.sources.Manifest(
                        source='text'
                    )
                ],
                steps=[
                    transformers.TextSourceCreateDocument(),
                    transformers.TextDocumentStringReplace(regexp='\n\n', replacement='\n'),
                    transformers.TextSplitIntoCollectionDocument(
                        separator='\n'
                    )
                ]
            )
        ]
    )
    return pipeline


def generate_manifest(local_path: pathlib.Path, destination):
    manifest = manifests.base.Manifest(
        sources=[
            manifests.sources.Text(
                id='id',
                pipeline='default',
                location=manifests.sources.locations.Local(
                    path=str(local_path.absolute())
                ),
                destination=manifests.sources.destinations.Local(
                    directory=destination.name
                )
            )
        ]
    )
    return manifest


def ingest(local_path):
    destination = tempfile.TemporaryDirectory()
    manifest = generate_manifest(local_path, destination)
    pipeline = generate_pipeline()

    results, *_ = engine.run(
        manifest=manifest,
        pipelines=[pipeline],
        pipelines_dir=None,
        artifacts_dir=None,
        workspace_dir=None,
    )

    destination.cleanup()

    return results[0]


def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command', required=True)
    subparser.add_parser('export')
    ingest_parser = subparser.add_parser('ingest')
    ingest_parser.add_argument('path')
    args = parser.parse_args()

    if args.command == 'export':
        output = generate_pipeline()
    else:
        output = ingest(pathlib.Path(args.path))

    print(stringify_document(output))


if __name__ == "__main__":
    # python src/examples/cli-text.py ingest src/ingestum/tests/data/test.txt
    main()
