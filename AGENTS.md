# AGENTS.md - Key Learnings from Lektor Shortcodes Modernization

## Project Overview
Successfully modernized a legacy Lektor shortcodes package from setup.py/setup.cfg to modern pyproject.toml with uv dependency management.

## Key Learnings

### 1. UV Package Management
- **Fast Installation**: UV provides extremely fast package installation compared to pip
- **PyPI Focus**: UV works directly with PyPI packages, eliminating conda/pip compatibility issues
- **PyProject.toml Integration**: UV respects standard `[project]` and `[project.optional-dependencies]` sections
- **Virtual Environments**: UV manages virtual environments efficiently with `uv venv`
- **Runtime Dependencies**: Place runtime dependencies in `[project]` section, development dependencies in `[project.optional-dependencies]`
- **Plugin Dependencies**: For Lektor plugins, keep Lektor as a dev/test dependency, not a runtime dependency. The plugin is installed in Lektor's environment, so Lektor doesn't need to be a dependency of the plugin itself.

### 2. Modern Python Tooling
- **Ruff**: Replaces flake8, isort, and black for linting and formatting
- **MyPy**: Essential for type checking in modern Python projects
- **Pytest**: Standard testing framework with coverage support
- **Pre-commit hooks**: Automate code quality checks
- **Hatch**: Modern build system (replaces setuptools)

### 3. Lektor Dependency Compatibility Issues
- **GitHub Issue #1156**: Lektor has an open issue for mistune 3.x support (not resolved as of 2024)
- **Werkzeug 3.x Breaking Changes**: `werkzeug.urls.url_parse` was removed in Werkzeug 3.x
- **Mistune 3.x Breaking Changes**: `mistune.Renderer` became `mistune.HTMLRenderer` in 3.x
- **Proper Solution**: Pin to compatible versions (`mistune<2.0.0`, `werkzeug<3.0.0`) instead of compatibility layers
- **Avoid Compatibility Layers**: They are band-aid solutions that mask the real problem
- **Check GitHub Issues**: Always check for open issues before assuming latest versions work

### 4. Code Modernization
- **Type Hints**: Add comprehensive type hints throughout the codebase
- **F-strings**: Use f-strings instead of % formatting
- **Exception Handling**: Use proper exception chaining with `raise ... from`
- **Import Organization**: Use ruff for automatic import sorting
- **Test Style**: Use pytest function-style tests, not unittest class-style
- **Single Configuration**: Use `pyproject.toml` for all project configuration

### 5. Testing and CI
- **GitHub Actions**: Set up CI/CD with multiple Python versions
- **Coverage**: Include test coverage reporting
- **Linting Pipeline**: Ensure lint, type-check, and test all pass

### 6. Documentation
- **README Updates**: Include modern installation instructions
- **Development Setup**: Document uv usage and development workflow
- **Pre-commit Setup**: Include pre-commit hook installation instructions

## Best Practices Established

1. **Always test the full pipeline** (lint, type-check, test) after modernization
2. **Use uv for dependency management** for fast, reliable Python package management
3. **Pin dependency versions** when compatibility issues arise
4. **Modernize incrementally** - don't try to update everything at once
5. **Check GitHub issues** before assuming latest dependency versions work
6. **Avoid compatibility layers** - they are band-aid solutions that mask real problems
7. **Pin to compatible versions** instead of creating workarounds

## Common Pitfalls Avoided

- Don't skip compatibility testing with latest dependency versions
- Don't forget to update CI/CD configurations
- Don't ignore type checking in modern Python projects
- Don't use deprecated packaging methods (setup.py/setup.cfg)
- Don't create compatibility layers without checking GitHub issues first
- Don't assume latest dependency versions work with older packages
- Don't use compatibility layers as a permanent solution

## Tools and Commands

```bash
# Set up virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -e .[dev]

# Run linting
ruff check .

# Run type checking
mypy lektor_shortcodes

# Run tests
pytest

# Build package
hatch build

# Format code
ruff format .
```

## Future Considerations

- Monitor for Lektor updates that support Werkzeug 3.x and Mistune 3.x
- Update documentation as new versions become available
- Maintain backward compatibility where possible
