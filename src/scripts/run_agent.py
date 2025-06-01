"""Command-line interface for running the agent with queries."""

import sys

from agent.core import run


def main():
    """Run the agent with a command-line query."""
    if len(sys.argv) < 2:
        print("Usage: python run_agent.py <query>")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    response = run(query)
    print(response)


if __name__ == "__main__":
    main()
