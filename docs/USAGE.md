# Usage Guide

## Quick Start

1. Set up environment:
   ```bash
   cp config/.env.example .env
   # Edit .env with your API keys
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Run interactively:
   ```bash
   make run
   ```

4. Run single query:
   ```bash
   make run-cli q="What is machine learning?"
   ```

## Configuration

Edit `config/settings.yaml` to customize:
- Model settings (name, temperature, max_tokens)
- Agent behavior (verbose mode)
- Memory configuration

## Environment Variables

Required:
- `OPENAI_API_KEY`: Your OpenAI API key

Optional:
- `SERPAPI_API_KEY`: For web search functionality
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)

## Docker Usage

```bash
# Build image
make docker-build

# Run interactively
make docker-interactive

# Run with query
docker run --env-file .env agents-tracie:latest
