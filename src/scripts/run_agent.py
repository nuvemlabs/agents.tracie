import typer
from agents.core import run

app = typer.Typer()

@app.command()
def run_agent(query: str):
    run(query)

if __name__ == "__main__":
    app()