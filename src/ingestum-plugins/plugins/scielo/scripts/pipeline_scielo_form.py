import argparse
import tempfile

from ingestum import engine
from ingestum import manifests
from ingestum import pipelines
from ingestum import transformers
from ingestum.utils import stringify_document


def generate_pipeline():
    pipeline = pipelines.base.Pipeline(
        name="default",
        pipes=[
            pipelines.base.Pipe(
                name="default",
                sources=[pipelines.sources.Manifest(source="scielo")],
                steps=[
                    transformers.ScieloSourceCreateFormCollectionDocument(
                        query=""
                    )
                ],
            )
        ],
    )
    return pipeline


def ingest(query):
    destination = tempfile.TemporaryDirectory()

    manifest = manifests.base.Manifest(
        sources=[
            manifests.sources.Scielo(
                id="id",
                pipeline="default",
                query=query,
                destination=manifests.sources.destinations.Local(
                    directory=destination.name,
                ),
            )
        ]
    )

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
    subparser = parser.add_subparsers(dest="command", required=True)
    subparser.add_parser("export")
    ingest_parser = subparser.add_parser("ingest")
    ingest_parser.add_argument("query", type=str)
    args = parser.parse_args()

    if args.command == "export":
        output = generate_pipeline()
    else:
        output = ingest(args.query)

    print(stringify_document(output))


if __name__ == "__main__":
    main()
