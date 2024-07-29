# use pybp submodule

## 引用子模块

```shell
git submodule add https://github.com/chengzhang/pybp.git pybp
```

同步子模块的更新
```shell
git submodule update --init --recursive
```

提交本地修改到子模块
```shell
git add .gitmodules pybp
git commit -m "change from daily repo"
git push
```

## 同步子模块的更新 

```shell
#!/bin/bash

# 初始化子模块
git submodule init

# 更新子模块
git submodule update

# 获取子模块的最新更改
git submodule update --remote

# 提交和推送更新
git add .
git commit -m "Update submodule to latest version"
git push origin main  # 或者你的分支名称
```
