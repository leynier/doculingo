from typer import Typer

from .word import main as word_main

app = Typer(no_args_is_help=True)


@app.callback()
def callback() -> None:
    """Translate documents using LLMs."""


app.command(name="word")(word_main)
