# Contributing to Resume ATS Analyzer

First off, thank you for considering contributing to Resume ATS Analyzer! It's people like you that make this tool better for job seekers everywhere.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if applicable**
- **Include your environment details** (OS, Python version, Node version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and expected behavior**
- **Explain why this enhancement would be useful**

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. Ensure the test suite passes
4. Make sure your code follows the existing style
5. Write a clear commit message
6. Open a pull request!

## Development Setup

See the README.md for detailed setup instructions.

## Code Style

### Python (Backend)
- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and small

### TypeScript/React (Frontend)
- Use functional components with hooks
- Follow the existing component structure
- Use TypeScript interfaces for props
- Keep components focused and reusable

## Project Structure

```
Resume-Analyser/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/     # API routes
│   │   ├── core/    # Core config
│   │   ├── models/  # Data models
│   │   └── services/# Business logic
│   └── main.py
├── frontend/         # React frontend
│   └── src/
│       ├── components/
│       ├── services/
│       └── types/
└── docs/
```

## Testing

- Write tests for new features
- Ensure existing tests pass
- Add integration tests for API endpoints
- Test UI components with various inputs

## Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests

## Questions?

Feel free to open an issue with your question!

Thank you! ❤️
