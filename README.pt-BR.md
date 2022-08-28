# Ingestum Workshop

## Requisitos
- Linux (OS ou VM)
- Docker
- Conda ou Mamba
- VSCode (recomendado) por causar da funcionalidade "Developing inside a Container"

## Iniciando

1. Clone esse repositório
2. Clone ingestum para repositório `src` e instale
    ```
    $ git clone https://gitlab.com/sorcero/community/ingestum src/ingestum
    $ pip install -e src/ingestum
    ```

## Usando

### Modo Declarativo
```
$ cd src/ingestum
$ ingestum-manifest tests/pipelines/manifest_text.json --pipelines=tests/pipelines --workspace=workspace
```