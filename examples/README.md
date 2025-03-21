# Jinja2 Renderer Examples

This directory contains example configurations and templates to demonstrate the usage of the Jinja2 Renderer GitHub Action.

## Basic Examples

### Single Template Rendering

**Template (`templates/config.conf.j2`):**
```jinja
# Configuration for {{ app_name }} v{{ version }}
debug = {{ debug }}
log_level = {{ log_level | default('info') }}
```

**Variables (`variables.json`):**
```json
{
  "app_name": "ExampleApp",
  "version": "1.0.0",
  "debug": true
}
```

**Workflow:**
```yaml
- name: Render Config
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: 'templates/config.conf.j2'
    output_path: 'output/config.conf'
    variables_file: 'variables.json'
```

**Result (`output/config.conf`):**
```
# Configuration for ExampleApp v1.0.0
debug = True
log_level = info
```

### Directory Processing

**Structure:**
```
templates/
├── app.conf.j2
├── nginx.conf.j2
└── logging.conf.j2
```

**Workflow:**
```yaml
- name: Process Template Directory
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: 'templates'
    output_path: 'output'
    variables_file: 'variables.json'
```

This will process all `.j2` files in the `templates` directory and save the rendered files to the `output` directory.

## Advanced Examples

### Using Key-Value Variables with Automatic Type Conversion

**Template (`templates/types.conf.j2`):**
```jinja
# Type demonstrations
boolean_true = {{ boolean_true }} (type: {{ boolean_true.__class__.__name__ }})
boolean_false = {{ boolean_false }} (type: {{ boolean_false.__class__.__name__ }})
integer = {{ integer }} (type: {{ integer.__class__.__name__ }})
float_number = {{ float_number }} (type: {{ float_number.__class__.__name__ }})
string = {{ string }} (type: {{ string.__class__.__name__ }})
```

**Workflow:**
```yaml
- name: Demonstrate Type Conversion
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: 'templates/types.conf.j2'
    output_path: 'output/types.conf'
    variables: |
      boolean_true=true
      boolean_false=false
      integer=42
      float_number=3.14
      string=hello
```

**Result (`output/types.conf`):**
```
# Type demonstrations
boolean_true = True (type: bool)
boolean_false = False (type: bool)
integer = 42 (type: int)
float_number = 3.14 (type: float)
string = hello (type: str)
```

### Using Environment Variables

**Template (`templates/env.conf.j2`):**
```jinja
# Environment Variables
GITHUB_ACTOR = {{ env.GITHUB_ACTOR }}
CUSTOM_VAR = {{ env.get('CUSTOM_VAR', 'not set') }}
```

**Workflow:**
```yaml
- name: Render with Environment Variables
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: 'templates/env.conf.j2'
    output_path: 'output/env.conf'
    environment_variables: 'true'
  env:
    CUSTOM_VAR: 'custom value'
```

### Using Nested Directory Structure

**Structure:**
```
templates/
├── configs/
│   ├── app.conf.j2
│   └── logging.conf.j2
└── nginx/
    └── site.conf.j2
```

**Workflow:**
```yaml
- name: Process Nested Directories
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: 'templates'
    output_path: 'output'
    variables_file: 'variables.json'
    recursive: 'true'
```

**Result:**
```
output/
├── configs/
│   ├── app.conf
│   └── logging.conf
└── nginx/
    └── site.conf
```

## Troubleshooting Examples

### Handling Missing Variables with Default Values

**Template (`templates/defaults.conf.j2`):**
```jinja
# Using default values
required_value = {{ required_value }}
optional_value = {{ optional_value | default('default value') }}
```

### Strict Mode Example

**Workflow:**
```yaml
- name: Render in Strict Mode
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: 'templates/config.j2'
    output_path: 'output/config'
    variables: 'required_value=exists'
    strict: 'true'  # This will fail if any variable is undefined
```

## Use Cases

### Kubernetes Manifests

**Template (`templates/deployment.yaml.j2`):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ app_name }}
  namespace: {{ namespace }}
spec:
  replicas: {{ replicas }}
  selector:
    matchLabels:
      app: {{ app_name }}
  template:
    metadata:
      labels:
        app: {{ app_name }}
    spec:
      containers:
      - name: {{ app_name }}
        image: {{ docker_image }}:{{ image_tag }}
        ports:
        - containerPort: {{ port }}
        env:
        {% for key, value in environment_variables.items() %}
        - name: {{ key }}
          value: "{{ value }}"
        {% endfor %}
```

### Docker Compose File

**Template (`templates/docker-compose.yml.j2`):**
```yaml
version: '3'
services:
  {{ service_name }}:
    image: {{ docker_image }}:{{ image_tag }}
    ports:
      - "{{ host_port }}:{{ container_port }}"
    environment:
      {% for key, value in env_vars.items() %}
      {{ key }}: {{ value }}
      {% endfor %}
    {% if volumes %}
    volumes:
      {% for volume in volumes %}
      - {{ volume }}
      {% endfor %}
    {% endif %}
```