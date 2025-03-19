# Jinja2 Template Renderer Examples

This directory contains example templates and configurations to demonstrate the usage of the Jinja2 Template Renderer GitHub Action.

## Basic Examples

### Configuration Template

**Template File: `config.conf.j2`**

```jinja
# Configuration for {{ app_name }} v{{ version }}

[app]
name = {{ app_name }}
version = {{ version }}
debug = {{ debug }}

[features]
{% for feature in features %}
{{ feature }} = enabled
{% endfor %}

[database]
host = {{ database.host }}
port = {{ database.port }}
```

**Variables File: `variables.json`**

```json
{
  "app_name": "MyApp",
  "version": "1.2.3",
  "debug": true,
  "features": ["auth", "api", "admin"],
  "database": {
    "host": "localhost",
    "port": 5432
  }
}
```

**Usage:**

```yaml
- name: Render Config
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: './examples/config.conf.j2'
    output_path: './output/config.conf'
    variables_file: './examples/variables.json'
```

### Nginx Configuration

**Template File: `nginx.conf.j2`**

```jinja
# Nginx configuration for {{ server_name }}

server {
    listen {{ port }};
    server_name {{ server_name }};
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    {% if ssl_enabled %}
    listen 443 ssl;
    ssl_certificate /etc/nginx/ssl/{{ server_name }}.crt;
    ssl_certificate_key /etc/nginx/ssl/{{ server_name }}.key;
    {% endif %}
}

upstream backend {
    {% for server in backend_servers %}
    server {{ server.host }}:{{ server.port }};
    {% endfor %}
}
```

**Variables File: `nginx-variables.yaml`**

```yaml
server_name: example.com
port: 80
ssl_enabled: true
backend_servers:
  - host: app1.internal
    port: 8080
  - host: app2.internal
    port: 8080
```

**Usage:**

```yaml
- name: Render Nginx Config
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: './examples/nginx.conf.j2'
    output_path: './output/nginx.conf'
    variables_file: './examples/nginx-variables.yaml'
```

## Advanced Examples

### Environment Variables

**Template File: `env-example.conf.j2`**

```jinja
# Configuration using environment variables
HOSTNAME={{ env.HOSTNAME }}
GITHUB_WORKSPACE={{ env.GITHUB_WORKSPACE }}
CURRENT_BRANCH={{ env.GITHUB_REF_NAME }}
DEPLOYMENT_ENV={{ env.get('DEPLOYMENT_ENV', 'development') }}
```

**Usage:**

```yaml
- name: Render Environment Config
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: './examples/env-example.conf.j2'
    output_path: './output/env-config.conf'
  env:
    DEPLOYMENT_ENV: production
```

### Multiple Templates with Custom Pattern

**Directory Structure:**
```
templates/
  ├── app.yaml.template
  ├── service.yaml.template
  └── deployment.yaml.template
```

**Usage:**

```yaml
- name: Render Kubernetes Templates
  uses: lexty/jinja2-renderer@v1
  with:
    template_path: './templates'
    output_path: './k8s'
    variables_file: './k8s-variables.yaml'
    file_pattern: '*.yaml.template'
    recursive: 'true'
```