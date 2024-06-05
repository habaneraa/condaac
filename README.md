# condaac

condaac is a CLI application that helps you to list and switch between your conda environments easily.

<video width="85%" src="docs/terminal_demo.mp4" controls></video>


> [!NOTE]  
> condaac currently does not support Windows as it relies on Linux shell script.

## Installation

Step 1. Install Python application via [pipx](https://pipx.pypa.io/latest/)

```bash
pipx install https://github.com/habaneraa/condaac.git
```

Step 2. Install script.

```bash
condaac-cli --install
```

Step 3. Add `condaac` alias to your shell profile script.

Step 4. Run `condaac` !

## How does this work

由于切换环境的 `conda activate` 命令必须要在当前 shell 执行（一般的运行脚本只能在子进程运行不会影响用户的 shell），所以必须使用 `source` 命令来实现对当前 shell 切换环境。因此，本工具实际上分为两个部分：工具本体 `condaac-cli` 和辅助脚本 `condaac.sh`。安装时，用户需要在自己的配置文件中添加 `alias condaac="source ~/.local/bin/condaac.sh"`，也就是为使用脚本设置别名。否则，直接执行 `condaac-cli` 或者 `condaac.sh` 都不能起到在当前 shell 切换 conda 环境的作用！

本工具的工作流程如下：

1. 在命令行安装 `condaac-cli`，它基于 Python 所以应使用 pipx 安装
2. 使用 `condaac-cli --install`，这一命令应当正确完成以下任务：
    - 通过命令 `conda info` 得知用户的 conda 信息
    - 将 conda 信息缓存至文件 ~/.conda/conda_info.json 以便后续使用
    - 将辅助脚本 `condaac.sh` 放置于 `~/.local/bin/`
    - 帮助用户正确设置脚本 `source ~/.local/bin/condaac.sh` 的别名
3. 用户在 conda shell 下启动 `condaac`，该工具读取缓存的 conda info 并寻找所有 conda 环境
4. 用户在 UI 中选择一个并按下回车，成功激活 conda 环境

**Q**: 为什么要事先执行 `conda info` 并缓存结果？

**A**: 因为 `conda` 本身非常慢。我们并不依赖该命令获取用户的环境列表，而该命令的主要作用是得知用户的 base 环境位置和虚拟环境所在目录。实际运行 `condaac` 时，脚本会主动遍历目录来寻找可能的 conda 环境，这比临时执行 `conda info` 要快十倍以上。

## Dependencies

[textual](https://github.com/Textualize/textual): a Rapid Application Development framework for Python.

[typer](https://github.com/tiangolo/typer): a library for building CLI applications based on Python type hints.

[natsort](https://github.com/SethMMorton/natsort): simple yet flexible natural sorting in Python.

## Trivia

When I was creating this tool I completely do not know "conda-zsh-completion" which is obviously better than this.
