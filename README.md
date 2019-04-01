# git工具

## 写在前面
> python3 -m venv .venv  
> source .venv/bin/activate  
> pip install -r requirements.txt  

## 目录
* [别名](#别名)
* [仓库迁移](#仓库迁移)

## 别名
> $ ./script/git_alias.py 

等价于下面的配置:  
> $ git config --global alias.br branch  
$ git config --global alias.ci commit  
$ git config --global alias.co checkout  
$ git config --global alias.df diff  
$ git config --global alias.last 'log -1 HEAD'  
$ git config --global alias.st status  
$ git config --global alias.unstage 'reset HEAD --'

## 仓库迁移
> $ ./script/git_transfer.py  
> Source Git URL: `self.source.repo.url`  
> Target Git URL: `self.target.repo.url`  
> Preparing  
> Clone from `self.source.repo.url`  
> Push to `self.target.repo.url`  
> Finishing  
> Done
