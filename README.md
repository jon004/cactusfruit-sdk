# Cactusfruit SDK

A Python SDK for interacting with Cactusfruit model services, including text embeddings, token counting, and text generation.

## Features

- Generate text using a configured language model.
- Create document embeddings.
- Create query embeddings.
- Count embedding tokens.
- Configure the server URL and model paths.
- Run the configuration loader explicitly when needed.

## Installation

Install from PyPI:

```bash
pip install cactusfruit-sdk
```

## Quick Start

Import the client:

```python
from cactusfruit.sdk import LlmServerClient

client = LlmServerClient()
```

### Generate Text

```python
response = client.generate(
    role="user",
    content="Explain what a Python SDK is.",
)

print(response)
```

You can also provide generation parameters:

```python
response = client.generate(
    role="user",
    content="Write a short introduction to machine learning.",
    params={
        "temperature": 0.7,
        "max_tokens": 200,
    },
)

print(response)
```

The parameters accepted depend on the underlying Cactusfruit model service.

### Generate Document Embeddings

```python
embedding = client.embed_document(
    "This is a document to embed."
)

print(embedding)
```

### Generate Query Embeddings

```python
embedding = client.embed_query(
    "How does semantic search work?"
)

print(embedding)
```

### Count Embedding Tokens

```python
token_count = client.embed_token_count(
    "Count the tokens in this text."
)

print(token_count)
```

## Configuration

The `LlmServerClient` supports configuration through constructor arguments.

```python
from cactusfruit.sdk import LlmServerClient

client = LlmServerClient(
    base_url="http://localhost:8000",
    embedder_model_path="models/all-MiniLM-L6-v2",
    generator_model_path="models/your-generator-model",
)
```

| Argument | Description |
|---|---|
| `base_url` | Base URL of the Cactusfruit model service |
| `embedder_model_path` | Model path used for document embeddings, query embeddings, and embedding token counts |
| `generator_model_path` | Model path used for text generation |

The default server URL is `http://localhost:8000`. The default embedding model path is `models/all-MiniLM-L6-v2`.

The default generator model path in the current client implementation is also `models/all-MiniLM-L6-v2`. For text generation, explicitly configure a suitable generator model path.

## Configuration Loader

Cactusfruit SDK includes a configuration loader intended for environments such as Docker.

The configuration loader is **not executed automatically** when the package is installed or imported. Run it explicitly when you want to generate `/app/.env`.

### Run the loader

Set `MODEL_CONFIG_ARG` to a JSON configuration and invoke the module:

```bash
export MODEL_CONFIG_ARG='{
  "type": "generative",
  "system_prompt": "You are a helpful assistant.",
  "params": {
    "threads": 8,
    "parallel": 4
  }
}'

python -m cactusfruit.dockerscripts.configloader
```

The loader writes configuration values to `/app/.env`.

### Example Docker usage

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir cactusfruit-sdk

ENV MODEL_CONFIG_ARG='{"type":"generative","system_prompt":"You are a helpful assistant.","params":{"threads":8,"parallel":4}}'

RUN python -m cactusfruit.dockerscripts.configloader
```

**Note:** The loader writes to `/app/.env`, so the process must have permission to create or modify that file. The loader's environment variables are used to generate the file; writing a `.env` file does not automatically load its values into every running process. Your application must load the file or otherwise configure its environment.

Avoid putting secrets in Docker build arguments or image environment variables, as they may be exposed through image metadata or build history.

## Model Service Endpoints

The client communicates with the configured model service using these endpoints:

| Operation | Endpoint |
|---|---|
| Document embeddings | `/m/embed/doc` |
| Query embeddings | `/m/embed/query` |
| Embedding token count | `/m/embed/token/count` |
| Text generation | `/m/prompt` |

The model service must be running and accessible at the configured `base_url`.

## Requirements

- Python 3.10 or later
- `requests`
- `python-dotenv`

These dependencies are installed automatically when you install `cactusfruit-sdk` from PyPI.

## Development

Clone the repository:

```bash
git clone https://github.com/jon004/cactusfruit-sdk.git
cd cactusfruit-sdk
```

Install the package in editable mode:

```bash
python -m pip install -e .
```

Build the distribution:

```bash
python -m pip install --upgrade build
python -m build
```

## Contributing

Contributions, bug reports, and feature requests are welcome. Please open an issue or pull request in the [GitHub repository](https://github.com/jon004/cactusfruit-sdk).

## License

Add your project's chosen license here before publishing. If you intend others to use, modify, and redistribute this SDK, include an appropriate license file in the repository.
