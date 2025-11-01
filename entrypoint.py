#!/usr/bin/env python3

import os
import sys
import json
import yaml
import glob
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from dotenv import dotenv_values

def get_env_bool(var_name, default=False):
    """Convert environment variable to boolean."""
    val = os.environ.get(var_name, str(default)).lower()
    return val in ('true', 't', 'yes', 'y', '1')

def convert_value_type(value):
    """Convert string value to appropriate type (bool, int, float, or str)."""
    if not isinstance(value, str):
        return value

    # Try boolean conversion
    if value.lower() in ('true', 't', 'yes', 'y', '1'):
        return True
    elif value.lower() in ('false', 'f', 'no', 'n', '0'):
        return False

    # Try integer conversion
    if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
        return int(value)

    # Try float conversion
    try:
        if '.' in value:
            return float(value)
    except ValueError:
        pass

    # Return as string
    return value

def load_env_file(file_path):
    """Load variables from .env file using python-dotenv."""
    if not os.path.exists(file_path):
        print(f"Error: Variables file '{file_path}' not found", file=sys.stderr)
        sys.exit(1)

    try:
        # dotenv_values returns a dict with all values as strings
        env_vars = dotenv_values(file_path)

        # Convert values to appropriate types
        converted_vars = {}
        for key, value in env_vars.items():
            if value is not None:
                converted_vars[key] = convert_value_type(value)

        return converted_vars
    except Exception as e:
        print(f"Error parsing .env file: {e}", file=sys.stderr)
        sys.exit(1)

def detect_file_format(file_path, explicit_format=None):
    """Detect the format of the variables file."""
    if explicit_format:
        return explicit_format.lower()

    # Auto-detect by extension
    if file_path.endswith('.env'):
        return 'env'
    elif file_path.endswith(('.yaml', '.yml')):
        return 'yaml'
    elif file_path.endswith('.json'):
        return 'json'
    else:
        # Default to JSON for unknown extensions
        return 'json'

def load_variables_from_file(file_path, file_format=None):
    """Load variables from JSON, YAML, or .env file."""
    if not os.path.exists(file_path):
        print(f"Error: Variables file '{file_path}' not found", file=sys.stderr)
        sys.exit(1)

    format_type = detect_file_format(file_path, file_format)

    if format_type == 'env':
        return load_env_file(file_path)

    with open(file_path, 'r') as f:
        if format_type == 'yaml':
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError as e:
                print(f"Error parsing YAML file: {e}", file=sys.stderr)
                sys.exit(1)
        else:  # json
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON file: {e}", file=sys.stderr)
                sys.exit(1)

def load_variables_from_string(vars_str):
    """Try to load variables from string, attempting multiple formats."""
    # First, try parsing as JSON
    try:
        return json.loads(vars_str)
    except json.JSONDecodeError:
        pass  # Not JSON, continue to other formats

    # Try parsing as key=value pairs
    variables = {}
    # Split by whitespace or newlines
    pairs = re.split(r'[\s\n]+', vars_str.strip())

    for pair in pairs:
        if not pair:  # Skip empty strings
            continue

        if '=' in pair:
            key, value = pair.split('=', 1)
            # Try to convert value to appropriate type
            try:
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                elif value.isdigit():
                    value = int(value)
                elif value.replace('.', '', 1).isdigit() and value.count('.') == 1:
                    value = float(value)
            except (ValueError, AttributeError):
                pass  # Keep as string if conversion fails

            variables[key] = value
        else:
            print(f"Warning: Ignoring invalid key-value pair: {pair}", file=sys.stderr)

    if variables:
        return variables

    # If all parsing methods failed
    print(f"Error: Could not parse variables string. Expected JSON or key=value format.", file=sys.stderr)
    sys.exit(1)

def find_template_files(template_path, file_pattern, recursive):
    """Find all template files in the given path matching the pattern."""
    if os.path.isfile(template_path):
        return [template_path]

    search_pattern = os.path.join(template_path, "**", file_pattern) if recursive else os.path.join(template_path, file_pattern)
    return glob.glob(search_pattern, recursive=recursive)

# Add a filter to format booleans consistently as lowercase
def format_bool(value):
    if isinstance(value, bool):
        return str(value).lower()
    return value

def render_template(template_file, template_dir, output_path, variables, env):
    """Render a single template file."""
    try:
        # Set up jinja environment
        loader = FileSystemLoader(template_dir)
        jinja_env_params = {
            'loader': loader,
            'autoescape': select_autoescape(['html', 'xml']),
            'trim_blocks': env['trim_blocks'],
            'lstrip_blocks': env['lstrip_blocks'],
        }

        # Add StrictUndefined only if strict mode is enabled
        if env['strict']:
            jinja_env_params['undefined'] = StrictUndefined

        template_env = Environment(**jinja_env_params)

        # Add filters
        template_env.filters['bool'] = format_bool

        # Add environment variables if requested
        if env['use_env_vars']:
            variables['env'] = os.environ

        # Get the template name relative to the loader
        template_name = os.path.relpath(template_file, template_dir)
        template = template_env.get_template(template_name)

        # Determine output file path
        file_name = os.path.basename(template_file)
        file_pattern = env['file_pattern']

        # Remove file pattern suffix if present
        if file_pattern.startswith('*'):
            pattern_suffix = file_pattern[1:]  # Remove the * wildcard
            if file_name.endswith(pattern_suffix):
                file_name = file_name[:-len(pattern_suffix)]

        if os.path.isdir(output_path):
            # If both template_path and output_path are directories, preserve the directory structure
            rel_path = os.path.relpath(os.path.dirname(template_file), template_dir)
            output_dir = os.path.join(output_path, rel_path) if rel_path != '.' else output_path
            output_file = os.path.join(output_dir, file_name)
        else:
            # If output_path is a specific file path
            output_file = output_path

        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Render and write the template
        rendered_content = template.render(**variables)

        with open(output_file, 'w') as f:
            f.write(rendered_content)

        print(f"Rendered: {template_file} -> {output_file}")
        return output_file

    except Exception as e:
        print(f"Error rendering template {template_file}: {e}", file=sys.stderr)
        if env['strict']:
            sys.exit(1)
        return None

def main():
    # Get inputs from environment variables
    template_path = os.environ.get('INPUT_TEMPLATE_PATH')
    output_path = os.environ.get('INPUT_OUTPUT_PATH')
    variables_file = os.environ.get('INPUT_VARIABLES_FILE')
    variables_file_format = os.environ.get('INPUT_VARIABLES_FILE_FORMAT')
    variables_string = os.environ.get('INPUT_VARIABLES')

    use_env_vars = get_env_bool('INPUT_ENVIRONMENT_VARIABLES', True)
    recursive = get_env_bool('INPUT_RECURSIVE', False)
    file_pattern = os.environ.get('INPUT_FILE_PATTERN', '*.j2')
    strict = get_env_bool('INPUT_STRICT', False)
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
        format_info = f" (format: {variables_file_format})" if variables_file_format else " (auto-detect)"
        print(f"Loading variables from file: {variables_file}{format_info}")
        variables.update(load_variables_from_file(variables_file, variables_file_format))

    if variables_string:
        print(f"Loading variables from input string")
        try:
            parsed_vars = load_variables_from_string(variables_string)
            variables.update(parsed_vars)
            print(f"Loaded {len(parsed_vars)} variable(s) from input string")
        except Exception as e:
            print(f"Error parsing variables: {e}", file=sys.stderr)
            sys.exit(1)

    # Print configuration
    print(f"Configuration:")
    print(f"  Template Path: {template_path}")
    print(f"  Output Path: {output_path}")
    print(f"  File Pattern: {file_pattern}")
    print(f"  Recursive: {recursive}")
    print(f"  Strict Mode: {strict}")
    print(f"  Using Environment Variables: {use_env_vars}")

    # Create output directory if it doesn't exist and is a directory path
    if not os.path.splitext(output_path)[1]:  # No file extension, assumed to be a directory
        os.makedirs(output_path, exist_ok=True)

    # Configure environment
    env = {
        'file_pattern': file_pattern,
        'trim_blocks': trim_blocks,
        'lstrip_blocks': lstrip_blocks,
        'strict': strict,
        'use_env_vars': use_env_vars
    }

    # Process templates
    rendered_files = []

    if os.path.isfile(template_path):
        # Single file processing
        template_dir = os.path.dirname(template_path) or '.'
        rendered_file = render_template(template_path, template_dir, output_path, variables, env)
        if rendered_file:
            rendered_files.append(rendered_file)
    else:
        # Directory processing
        template_files = find_template_files(template_path, file_pattern, recursive)

        if not template_files:
            print(f"Warning: No template files found matching pattern '{file_pattern}' in '{template_path}'", file=sys.stderr)

        for template_file in template_files:
            rendered_file = render_template(template_file, template_path, output_path, variables, env)
            if rendered_file:
                rendered_files.append(rendered_file)

    # Set output for GitHub Actions
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ.get('GITHUB_OUTPUT'), 'a') as f:
            f.write(f"rendered_files={json.dumps(rendered_files)}\n")

    print(f"Successfully rendered {len(rendered_files)} template(s)")

if __name__ == "__main__":
    main()