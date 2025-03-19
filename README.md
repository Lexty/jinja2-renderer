# Jinja2 Renderer GitHub Action

[![GitHub release](https://img.shields.io/github/v/release/lexty/jinja2-renderer?style=flat-square)](https://github.com/lexty/jinja2-renderer/releases/latest)
[![GitHub marketplace](https://img.shields.io/badge/marketplace-jinja2--renderer-blue?logo=github&style=flat-square)](https://github.com/marketplace/actions/jinja2-renderer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This GitHub Action allows you to render [Jinja2](https://jinja.palletsprojects.com/) templates with custom variables. AMD64 and ARM64 architectures are supported.

## Features

- ✅ Render single templates or process entire directories
- ✅ Load variables from JSON or YAML files
- ✅ Pass variables directly as a JSON string
- ✅ Recursive directory processing
- ✅ Custom file extension support
- ✅ Multi-architecture support (amd64 and arm64)
- ✅ Docker-based for consistent execution

## Usage

### Basic Examples

### Using Variables from a File

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
| `variables_file` | Path to a JSON or YAML file with variables | No | - |
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

## File Format Support

### Variables File

You can provide variables in either JSON or YAML format:

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Changelog

All notable changes to this project will be documented in the [CHANGELOG.md](CHANGELOG.md) file.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
