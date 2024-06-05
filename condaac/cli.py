import json
import os

import typer

from condaac.install import install_command
from condaac.list_envs import list_env_paths

cli = typer.Typer()


@cli.command(
        name='condaac-cli',
)
def condaac_cli(
    version: bool = typer.Option(None, "--version", "-v"),
    install: bool = typer.Option(None, "--install", "-i"),
    select:  bool = typer.Option(None, "--select"),
    list: bool = typer.Option(None, "--list"),
):
    if version:
        from condaac import __version__
        typer.echo(f"condaac {__version__}")
        exit(0)
    
    conda_info_path = os.environ.get('CONDA_INFO_PATH') or \
                      os.path.expanduser(os.path.join("~", ".conda", "conda_info.json"))

    if install:
        cmd = install_command(conda_info_path)
        typer.echo("Please add the following command to your shell profile script:")
        typer.echo(" ")
        typer.echo("  " + cmd)
        typer.echo(" ")
        exit(0)
    
    try:
        with open(conda_info_path, 'r') as f:
            conda_info_dict = json.loads(f.read().strip())
    except json.JSONDecodeError as e:
        typer.echo('JSON decode error:', e)
        exit(1)
    except FileNotFoundError as e:
        typer.echo(f'Not found: {conda_info_path}')
        exit(1)

    conda_info_dict['envs'] = list_env_paths(conda_info_dict)

    if list:
        from rich import print as richprint
        richprint(conda_info_dict['envs'])
        exit(0)

    if select:
        from condaac.tui import CondaEnvSel
        app = CondaEnvSel(conda_info_dict)
        ret = app.run(inline=True)
        if conda_info_dict.get('active_prefix') is None:
            typer.echo('Warning: conda base environment is not activated!', err=True)
        if ret:
            typer.echo(ret, nl=False)
        exit(0)
    
    typer.echo("Empty action.")


def main():
    cli()


if __name__ == '__main__':
    main()
