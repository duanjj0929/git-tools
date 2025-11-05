# git工具

## 写在前面

```sh
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

## 目录

-   [配置](#配置)
-   [别名](#别名)
-   [仓库迁移](#仓库迁移)
-   [跟踪空目录](#跟踪空目录)
-   [导出 Git Log 到 CSV](#导出-git-log-到-csv)
-   [规范化 commit-message](#规范化-commit-message)
-   [git-open](#git-open)

## 配置

```sh
$ ./script/git_config.py
```

等价于下面的配置:

```sh
$ git config --global color.ui auto
$ git config --global core.autocrlf false/true
$ git config --global core.editor vim
$ git config --global log.date iso
$ git config --global push.default simple
$ git config --global credential.helper store
```

## 别名

```sh
$ ./script/git_alias.py
```

等价于下面的配置:

```sh
$ git config --global alias.br branch
$ git config --global alias.ci commit
$ git config --global alias.co checkout
$ git config --global alias.df diff
$ git config --global alias.last 'log -1 HEAD'
$ git config --global alias.st status
$ git config --global alias.unstage 'reset HEAD --'
```

## 仓库迁移

```sh
$ ./script/git_transfer.py --from=<from_git_url> --to=<to_git_url>
Preparing
Clone from <from_git_url>
Push to <to_git_url>
Finishing
Done
```

## 跟踪空目录

```sh
$ ./script/git_keep.py -d <starting-point> [-f <keep-file>]
```

## 导出 Git Log 到 CSV

```sh
$ ./script/git_log_csv.py [选项]
```

将 Git 提交历史导出为 CSV 文件，包含以下信息：
- 缩写提交哈希（7位）
- 作者姓名
- 作者邮箱
- 作者日期
- 提交主题
- 变更的文件列表（包含变更类型：A=新增, D=删除, R=重命名, C=复制, M=修改）

**选项：**
- `-h, --help`: 显示帮助信息
- `-r, --repo PATH`: Git 仓库路径（默认为当前目录）
- `-o, --output FILE`: 输出 CSV 文件路径（默认为 git_log.csv）
- `-n, --number N`: 最多导出的提交数量（默认导出全部）

**示例：**
```sh
# 导出当前目录的 git log
$ ./script/git_log_csv.py

# 导出指定仓库的 git log
$ ./script/git_log_csv.py -r /path/to/repo

# 指定输出文件名
$ ./script/git_log_csv.py -o output.csv

# 只导出最近 100 个提交
$ ./script/git_log_csv.py -n 100

# 组合使用
$ ./script/git_log_csv.py -r /path/to/repo -o output.csv -n 50
```

## 规范化 commit-message

-   [Angular 规范](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#commit-message-format)

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

-   [Commitizen 工具](https://github.com/commitizen/cz-cli#conventional-commit-messages-as-a-global-utility)

```sh
$ sudo npm install -g commitizen
$ sudo npm install -g cz-conventional-changelog
$ echo '{ "path": "cz-conventional-changelog" }' > ~/.czrc
```

使用 `git cz` 代替 `git commit` 。

## git-open

Type [git open](https://github.com/paulirish/git-open) to open the repo website (GitHub, GitLab, Bitbucket) in your browser.

```bash
$ sudo npm install --global git-open
```

To configure [GitLab](https://github.com/paulirish/git-open/blob/master/git-open.1.md#gitlab-options) support (or other unique hosting situations) you may need to set some options.
