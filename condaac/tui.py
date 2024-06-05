from pathlib import Path

from textual.app import App
from textual.widgets import Header, OptionList


class CondaEnvSel(App):
    """Show a list of conda environments and allow the user to select one."""

    BINDINGS = [("q", "quit", "Quit")]
    CSS_PATH = "condaac.tcss"
    TITLE = "condaac"
    SUB_TITLE = "select a conda environment and activate it!"

    def __init__(self, conda_info: dict, **kwargs):
        super().__init__(**kwargs)
        self.conda_info = conda_info
        self.env_paths = conda_info['envs']
        self.env_names = [self.parse_env_name(env) for env in self.env_paths]
        
    def parse_env_name(self, env_path):
        if env_path == self.conda_info['root_prefix']:
            return 'base'
        else:
            return Path(env_path).name
    
    def current_env_mark(self, env_name):
        if self.conda_info['active_prefix_name'] == env_name:
            return '|>'
        else:
            return '  '

    def on_mount(self) -> None:
        max_env_name_len = max([len(n) for n in self.env_names])
        option_names = [self.current_env_mark(name) + name.ljust(max_env_name_len + 8) + path
                        for path, name in zip(self.env_paths, self.env_names)]

        self.options.add_options(option_names)

    def compose(self):
        yield Header()
        self.options = OptionList()
        yield self.options
    
    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        target_env_name = event.option.prompt.split()[1]
        self.exit(target_env_name)
    
    def action_quit(self):
        self.exit(result=None, return_code=0)
