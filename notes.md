# use pybp submodule

引用子模块

```shell
git submodule add https://$GITHUB_TOKEN@github.com/chengzhang/pybp.git pybp
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
