import argparse
import uuid
import pathlib

from ingestum import engine
from ingestum import manifests
from ingestum import pipelines
from ingestum import transformers
from ingestum.utils import stringify_document


def generate_pipeline(destination: pathlib.Path):
    pipeline = pipelines.base.Pipeline(
        name='default',
        pipes=[
            pipelines.base.Pipe(
                name='default',
                sources=[
                    pipelines.sources.Manifest(
                        source='html'
                    )
                ],
                steps=[
                    transformers.HTMLSourceCreateDocument(),
                    transformers.HTMLDocumentImagesExtract(
                        directory=str(destination.absolute())
                    ),
                    transformers.XMLCreateTextDocument()
                ]
            )
        ]
    )
    return pipeline


def generate_manifest(local_path, target, destination):
    manifest = manifests.base.Manifest(
        sources=[
            manifests.sources.HTML(
                id='id',
                pipeline='default',
                target=target,
                location=manifests.sources.locations.Local(
                    path=local_path
                ),
                destination=manifests.sources.destinations.Local(
                    directory=str(destination.absolute())
                )
            )
        ]
    )
    return manifest


def ingest(local_path, target):
    destination = pathlib.Path(f'./.data/{uuid.uuid1()}/')
    manifest = generate_manifest(local_path, target, destination)
    pipeline = generate_pipeline(destination)
    print(destination)

    results, *_ = engine.run(
        manifest=manifest,
        pipelines=[pipeline],
        pipelines_dir=None,
        artifacts_dir=None,
        workspace_dir=None,
    )


    return results[0]


def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command', required=True)
    subparser.add_parser('export')
    ingest_parser = subparser.add_parser('ingest')
    ingest_parser.add_argument('path')
    ingest_parser.add_argument('target')
    args = parser.parse_args()

    if args.command == 'export':
        output = generate_pipeline()
    else:
        output = ingest(args.path, args.target)

    print(stringify_document(output))


if __name__ == "__main__":
    # python src/examples/cli-html.py ingest src/ingestum/tests/data/test.html body
    # python src/examples/cli-html.py ingest tests/data/image.html body
    main()
