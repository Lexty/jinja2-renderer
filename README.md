# Jinja2 Renderer GitHub Action

[![GitHub release](https://img.shields.io/github/v/release/lexty/jinja2-renderer?style=flat-square)](https://github.com/lexty/jinja2-renderer/releases/latest)
[![GitHub marketplace](https://img.shields.io/badge/marketplace-jinja2--renderer-blue?logo=github&style=flat-square)](https://github.com/marketplace/actions/jinja2-renderer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This GitHub Action allows you to render [Jinja2](https://jinja.palletsprojects.com/) templates with custom variables. AMD64 and ARM64 architectures are supported.

## Features

- ✅ Render single templates or process entire directories
- ✅ Load variables from JSON or YAML files
- ✅ Pass variables directly as JSON string or key-value pairs
- ✅ Automatic type conversion for key-value pairs
- ✅ Recursive directory processing
- ✅ Custom file extension support
- ✅ Multi-architecture support (amd64 and arm64)
- ✅ Docker-based for consistent execution
- ✅ Detailed error reporting with strict mode support

## Usage

### Basic Examples

### Using Variables from a File

#### JSON/YAML Variables File

```yaml
name: Render Templates
on:
  push:
    branches: [ main ]

jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Render Jinja2 Templates
        uses: lexty/jinja2-renderer@v1
        with:
          template_path: './templates'
          output_path: './output'
          variables_file: './variables.json'
```

#### Using .env Files

```yaml
- name: Render Jinja2 Templates with .env
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: './templates'
    output_path: './output'
    variables_file: '.env'
```

Your `.env` file:
```bash
APP_NAME=MyApplication
VERSION=1.2.3
DEBUG=true
PORT=8080
```

### Using JSON Inline Variables

```yaml
- name: Render Jinja2 Templates
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: './templates/config.conf.j2'
    output_path: './output/config.conf'
    variables: '{"app_name": "MyApp", "version": "1.2.3", "debug": true}'
```

### Using Key-Value Inline Variables

The action supports three formats for key-value variables:

#### Multi-line format (with pipe character)

```yaml
- name: Render Config
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: 'templates/nginx.conf.j2'
    output_path: 'output/nginx.conf'
    variables: |
      server_name=example.com
      port=80
      max_connections=1024
```

#### Single-line format (space-separated)

```yaml
- name: Render Config
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: 'templates/nginx.conf.j2'
    output_path: 'output/nginx.conf'
    variables: 'server_name=example.com port=80 max_connections=1024'
```

#### Using YAML block scalar (>-)

```yaml
- name: Render Config
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: 'templates/nginx.conf.j2'
    output_path: 'output/nginx.conf'
    variables: >-
      server_name=example.com 
      port=80 
      max_connections=1024
```

### Data Type Conversion

When using key-value pairs format, the action automatically converts values to appropriate types:

- `true`, `True`, `yes`, `y`, `1` → boolean `true`
- `false`, `False`, `no`, `n`, `0` → boolean `false`
- Numbers (e.g., `123`) → integers
- Decimal numbers (e.g., `12.34`) → floats
- All other values → strings

### Using Environment Variables

```yaml
- name: Render with Environment Variables
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: 'templates/app.conf.j2'
    output_path: 'output/app.conf'
  env:
    APP_NAME: MyAwesomeApp
    APP_VERSION: 1.0.0
    DEBUG_MODE: true
```

Then in your template file:
```
# Configuration for {{ env.APP_NAME }}
version = {{ env.get('APP_VERSION') }}
debug = {{ env.get('DEBUG_MODE', 'false') }}
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `template_path` | Path to the Jinja2 template file or directory | Yes | - |
| `output_path` | Path where rendered files will be saved | Yes | - |
| `variables_file` | Path to a JSON, YAML, or .env file with variables | No | - |
| `variables_file_format` | Explicit format specification for variables_file (`json`, `yaml`, `env`). If not specified, format is auto-detected by file extension | No | auto-detect |
| `variables` | JSON string or key=value pairs for variables | No | - |
| `environment_variables` | Use environment variables in templates | No | `true` |
| `recursive` | Process templates in subdirectories recursively | No | `false` |
| `file_pattern` | Glob pattern for finding template files | No | `*.j2` |
| `strict` | Enable strict undefined variable checking | No | `false` |
| `trim_blocks` | Configure Jinja2 to trim blocks | No | `true` |
| `lstrip_blocks` | Configure Jinja2 to strip blocks | No | `true` |

## Outputs

| Output | Description |
|--------|-------------|
| `rendered_files` | JSON list of rendered template files |

## Examples

For more detailed examples with template files and configurations, check out the [examples documentation](examples/README.md).

### Rendering a Single Template

```yaml
- name: Render Config Template
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: './templates/nginx.conf.j2'
    output_path: './output/nginx.conf'
    variables_file: './variables.yaml'
```

### Processing a Directory of Templates

```yaml
- name: Process Template Directory
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: './templates'
    output_path: './output'
    variables_file: './variables.json'
    recursive: 'true'
```

### Using Strict Mode (Fail on Undefined Variables)

```yaml
- name: Render in Strict Mode
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: './templates/config.j2'
    output_path: './output/config'
    variables_file: './variables.json'
    strict: 'true'
```

### Processing Templates with Custom File Pattern

```yaml
- name: Process Template Files
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: './templates'
    output_path: './output'
    variables_file: './variables.json'
    file_pattern: '*.template'
```

### Using Explicit Format Specification

If your variables file has a non-standard extension, you can explicitly specify the format:

```yaml
- name: Render with Explicit Format
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: './templates'
    output_path: './output'
    variables_file: './my-vars.txt'
    variables_file_format: 'env'  # Force treating as .env file
```

### Using the Output

```yaml
- name: Render Templates
  id: render
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: './templates'
    output_path: './output'
    variables_file: './variables.json'

- name: Use Rendered Files
  run: |
    echo "Rendered files: ${{ steps.render.outputs.rendered_files }}"
    # Do something with the rendered files
```

## Troubleshooting

### Common Issues

#### Variable Parsing Errors

If you're seeing parsing errors with your variables:

1. For JSON format, ensure your JSON is valid with properly quoted keys and values
2. For key-value pairs, use the format `key=value` with spaces between pairs
3. Try using a variables file instead of inline variables for complex data

#### No Templates Found

If no templates are being rendered:

1. Check that your template files match the `file_pattern` (default is `*.j2`)
2. Verify the `template_path` is correct
3. If using `recursive: true`, ensure templates are in the expected subdirectories

#### Strict Mode Failures

When using `strict: true`, all variables used in templates must be defined. If you get errors:

1. Make sure all variables referenced in your templates are provided
2. Use `{{ variable | default('fallback') }}` in templates for optional variables
3. Consider setting `strict: false` during development

## File Format Support

### Variables File

You can provide variables in JSON, YAML, or .env format:

#### JSON (variables.json)

```json
{
  "app_name": "MyApp",
  "version": "1.2.3",
  "features": ["auth", "api", "admin"],
  "database": {
    "host": "localhost",
    "port": 5432
  }
}
```

#### YAML (variables.yaml)

```yaml
app_name: MyApp
version: 1.2.3
features:
  - auth
  - api
  - admin
database:
  host: localhost
  port: 5432
```

#### .env (variables.env or .env)

```bash
# Application configuration
APP_NAME=MyApp
VERSION=1.2.3
DEBUG=true
PORT=8080

# Database settings
DB_HOST=localhost
DB_PORT=5432
DB_NAME="my database"

# Multiline values (quoted)
DESCRIPTION="This is a
multiline
description"
```

**Note**: .env files support:
- Comments (lines starting with `#`)
- Quoted values with spaces (`KEY="value with spaces"`)
- Single and double quotes
- Multiline values (in quoted strings)
- Escape sequences (`\n`, `\t`, etc.)
- Automatic type conversion (booleans, integers, floats)

### Template Example

```jinja
# Configuration for {{ app_name }} v{{ version }}

app:
  name: {{ app_name }}
  version: {{ version }}
  
features:
{% for feature in features %}
  - {{ feature }}
{% endfor %}

database:
  host: {{ database.host }}
  port: {{ database.port }}
```

## Local Development

If you want to test the action locally or contribute to development, you'll need to install the required Python dependencies:

```bash
pip3 install jinja2 pyyaml python-dotenv
```

Then you can run the entrypoint script directly:

```bash
# Set required environment variables
export INPUT_TEMPLATE_PATH="./templates/test.j2"
export INPUT_OUTPUT_PATH="./output/test.conf"
export INPUT_VARIABLES_FILE="./variables.env"

# Run the script
python3 entrypoint.py
```

For testing with inline variables:

```bash
export INPUT_TEMPLATE_PATH="./templates/test.j2"
export INPUT_OUTPUT_PATH="./output/test.conf"
export INPUT_VARIABLES='{"key": "value"}'

python3 entrypoint.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Changelog

All notable changes to this project will be documented in the [CHANGELOG.md](CHANGELOG.md) file.

## License

This project is licensed under the MIT License - see the LICENSE file for details.