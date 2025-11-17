# az-fa-formatops

FormatOps provides Azure Functions for fast, reliable content transformations and validation. Includes JSON↔YAML converters, HTML→DOCX generation, and format validators built with consistent standards for use in automation, SOAR workflows, and cloud-native pipelines.

## Features

### HTML to DOCX Conversion

Convert HTML content to Microsoft Word DOCX format with base64-encoded output for easy JSON transport.

**Endpoint:** `POST /api/html_to_docx/convert`

**Example:**

```bash
curl -X POST http://localhost:7071/api/html_to_docx/convert \
  -H "Content-Type: application/json" \
  -d '{"html": "<html><body><h1>Hello World</h1></body></html>"}'
```

**Documentation:**
- [Module Reference](docs/modules/html_to_docx.md)
- [Usage Examples](docs/examples/html_to_docx-curl.md)
- [Implementation Details](docs/implementation/html_to_docx.md)

## Requirements

- Python 3.11+
- Azure Functions Core Tools 4.x
- Pandoc (required for HTML to DOCX conversion)

## Installation

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/kevinflint-cs2/az-fa-formatops.git
   cd az-fa-formatops
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. Install Pandoc:
   ```bash
   # Linux/Debian
   apt-get install pandoc

   # macOS
   brew install pandoc

   # Windows
   choco install pandoc
   ```

5. Start the function app:
   ```bash
   func start
   ```

## Testing

Run tests with pytest:

```bash
# Unit tests (fast, mocked)
pytest -m mock -vv

# Endpoint tests (requires running function app)
pytest -m endpoint -vv

# All tests
pytest -vv
```

## Code Quality

This project uses automated code quality tools:

```bash
# Linting
ruff check .
ruff check . --fix

# Formatting
ruff format .

# Type checking
mypy . --config-file mypy.ini
```

## Deployment

### Azure Staging

```bash
./scripts/deploy_staging.sh
```

**Note:** Ensure Pandoc is installed in the Azure Functions runtime environment (requires custom container or Premium plan).

## Project Structure

```
az-fa-formatops/
├── function_app.py              # HTTP route definitions
├── functions/                   # Business logic modules
│   └── html_to_docx.py
├── tests/                       # Test suites
│   ├── test_html_to_docx.py
│   └── test_html_to_docx_endpoint.py
├── docs/                        # Documentation
│   ├── modules/                 # Module references
│   ├── examples/                # Usage examples
│   └── implementation/          # Implementation notes
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
└── scripts/                     # Deployment scripts
```

## Contributing

1. Create a feature branch: `git checkout -b feat/my-feature`
2. Follow the [development process](docs/development/development-process.prompt.md)
3. Ensure all tests pass and code quality checks succeed
4. Submit a pull request

## License

See [LICENSE](LICENSE) for details.
