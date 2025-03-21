# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-03-21

### Added
- Enhanced variable parsing with automatic type conversion
- Better support for key-value pairs format in the `variables` input
- Verbose logging for easier debugging
- Improved error handling and reporting
- Validation of template paths before processing

### Fixed
- Fixed parsing errors for key-value variables format
- Corrected file pattern handling for template discovery
- Resolved issue with directory structure preservation when rendering templates
- Fixed handling of relative paths in multi-directory setups

## [1.0.0] - 2025-03-19

### Added
- Initial release of the Jinja2 Renderer GitHub Action
- Support for rendering single template files or entire directories
- Variable loading from JSON or YAML files
- Direct variable passing as JSON string
- Recursive directory processing capability
- Custom file extension support
- Multi-architecture Docker image (amd64 and arm64)
- Comprehensive error handling and logging
- Testing workflow for GitHub Actions