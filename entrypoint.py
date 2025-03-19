#!/usr/bin/env python3

import os
import sys
import json
import yaml
import glob
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

def get_env_bool(var_name, default=False):
    """Convert environment variable to boolean."""
    val = os.environ.get(var_name, str(default)).lower()
    return val in ('true', 't', 'yes', 'y', '1')

def load_variables_from_file(file_path):
    """Load variables from JSON or YAML file."""
    if not os.path.exists(file_path):
        print(f"Error: Variables file '{file_path}' not found", file=sys.stderr)
        sys.exit(1)

    with open(file_path, 'r') as f:
        if file_path.endswith(('.yaml', '.yml')):
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError as e:
                print(f"Error parsing YAML file: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON file: {e}", file=sys.stderr)
                sys.exit(1)

def load_variables_from_json_string(json_str):
    """Load variables from JSON string."""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON string: {e}", file=sys.stderr)
        sys.exit(1)

def find_template_files(template_path, file_extension, recursive):
    """Find all template files in the given path."""
    if os.path.isfile(template_path):
        return [template_path]

    search_pattern = f"**/*{file_extension}" if recursive else f"*{file_extension}"
    return glob.glob(os.path.join(template_path, search_pattern), recursive=recursive)

def render_template(template_path, output_path, variables, env):
    """Render a single template file."""
    try:
        # Get relative path from template directory
        template_dir = os.path.dirname(template_path) if os.path.isfile(template_path) else template_path
        loader = FileSystemLoader(template_dir)
        template_env = Environment(
            loader=loader,
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=env['trim_blocks'],
            lstrip_blocks=env['lstrip_blocks']
        )

        relative_path = os.path.basename(template_path) if os.path.isfile(template_path) else os.path.relpath(template_path, template_dir)
        template = template_env.get_template(relative_path)

        # Determine output file path
        if os.path.isfile(template_path):
            # If input is a single file
            output_file = output_path
            if os.path.isdir(output_path):
                # If output is a directory, write to a file inside it
                base_name = os.path.basename(template_path)
                output_name = base_name[:-len(env['file_extension'])] if base_name.endswith(env['file_extension']) else base_name
                output_file = os.path.join(output_path, output_name)
        else:
            # If input is a directory
            rel_path = os.path.relpath(template_path, template_dir)
            output_name = rel_path[:-len(env['file_extension'])] if rel_path.endswith(env['file_extension']) else rel_path
            output_file = os.path.join(output_path, output_name)

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Render and write the template
        rendered_content = template.render(**variables)
        with open(output_file, 'w') as f:
            f.write(rendered_content)

        return output_file

    except Exception as e:
        print(f"Error rendering template {template_path}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    # Get inputs from environment variables
    template_path = os.environ.get('INPUT_TEMPLATE_PATH')
    output_path = os.environ.get('INPUT_OUTPUT_PATH')
    variables_file = os.environ.get('INPUT_VARIABLES_FILE')
    variables_json = os.environ.get('INPUT_VARIABLES')
    recursive = get_env_bool('INPUT_RECURSIVE', False)
    file_extension = os.environ.get('INPUT_FILE_EXTENSION', '.j2')
    trim_blocks = get_env_bool('INPUT_TRIM_BLOCKS', True)
    lstrip_blocks = get_env_bool('INPUT_LSTRIP_BLOCKS', True)

    # Validate required inputs
    if not template_path:
        print("Error: template_path is required", file=sys.stderr)
        sys.exit(1)

    if not output_path:
        print("Error: output_path is required", file=sys.stderr)
        sys.exit(1)

    # Load variables
    variables = {}
    if variables_file:
        variables.update(load_variables_from_file(variables_file))

    if variables_json:
        variables.update(load_variables_from_json_string(variables_json))

    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Configure environment
    env = {
        'file_extension': file_extension,
        'trim_blocks': trim_blocks,
        'lstrip_blocks': lstrip_blocks
    }

    # Process templates
    rendered_files = []
    if os.path.isfile(template_path):
        # Single file processing
        rendered_file = render_template(template_path, output_path, variables, env)
        rendered_files.append(rendered_file)
    else:
        # Directory processing
        template_files = find_template_files(template_path, file_extension, recursive)
        for template_file in template_files:
            rendered_file = render_template(template_file, output_path, variables, env)
            rendered_files.append(rendered_file)

    # Set output for GitHub Actions
    with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
        f.write(f"rendered_files={json.dumps(rendered_files)}\n")

    print(f"Successfully rendered {len(rendered_files)} template(s)")
    for file in rendered_files:
        print(f"  - {file}")

if __name__ == "__main__":
    main()