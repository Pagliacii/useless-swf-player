# useless-swf-player

<div style="display: flex; justify-contents: center; align-items: center;">
    <img src="/static/img/useless-logo.svg" alt="The useless logo">
</div>

基于 [Flask](https://github.com/pallets/flask) 和 [Ruffle](https://github.com/ruffle-rs/ruffle) 的 SWF 播放器。

## Usage

```shell
# 1. clone 仓库
$ git clone https://github.com/Pagliacii/useless-swf-player
# 2. 安装所有 nodejs 模块
$ yarn
# 3. 创建 Python 虚拟环境并安装相应模块（如果报无法编译 uwsgi 的错误，那么要先安装依赖）
$ pipenv install
# 4. 迁移和升级数据库
$ FLASK_APP=wsgi.py pipenv run flask db migrate
$ FLASK_APP=wsgi.py pipenv run flask db upgrade
# 5. 启动服务器，默认监听端口 9000
$ ./run.sh -p
```

## Development

### Commands

```shell
# 基于 css/tailwind.css 生成最终的 css 文件
$ yarn run build:css
# 监视 css/tailwind.css 并自动生成的最终 css 文件
$ yarn run watch:css
# 以开发模式启动服务器
$ ./run.sh -d
# 另一种启动开发模式服务器的方式
$ FLASK_APP=wsgi.py FLASK_ENV=development yarn run dev
```

### Structure

+ `app`: 主体
    - `__init__.py`: 构建 Flask App
    - `errors.py`: 所有异常类
    - `files.py`: `/files` Blueprint
    - `logging.py`: 集成 `loguru` 日志库
    - `models.py`: ORM 数据模型
    - `route.py`: 首页和错误页面
    - `swf_parser.py`: SWF 文件头解析器
    - `utils.py`: 工具函数集
    - `video.py`: `/video` Blueprint
+ `css/tailwind.css`: tailwindcss 文件
+ `static`: 静态文件目录
+ `swfs`: SWF 文件目录
+ `templates`: 模版目录
    - `404.html`: 404 页面
    - `500.html`: 500 页面
    - `base.html`: 基础模板
    - `error.html`: 错误页面的基础模板
    - `index.html`: 首页
    - `macros.html`: 自定义的 `Jinja` 宏
    - `video.html`: 播放页面
+ `config.py`: Flask App 的配置文件
+ `tailwind.config.js`: tailwindcss 的配置文件
+ `wsgi.py`: 程序入口文件

### API

+ `/`
    - 描述：首页
    - 方法：GET
    - 参数：无
    - 响应：HTML
+ `/files/update`
    - 描述：重新扫描所有 SWF 文件并更新数据库
    - 方法：GET
    - 参数：无
    - 响应：JSON `{ "status": "ok|failure", ["reason": "blablabla"]}`
+ `/files/<path:filename>`
    - 描述：获取文件内容
    - 方法：GET
    - 参数：无
    - 响应：文件流
+ `/video/<int:file_id>`
    - 描述：打开指定文件的播放页面
    - 方法：GET
    - 参数：无
    - 响应：HTML

### Utils

+ `get_file_created_time(file_stat: os:stat_result) -> str`: 获取 ISO 格式的文件创建时间
+ `get_file_accessed_time(file_stat: os:stat_result) -> str`: 获取 ISO 格式的文件访问时间
+ `get_file_infos(directory: str) -> Generator`: 遍历指定目录，并生成其下文件的相关信息
+ `scan_swfs_folder(database: SQLAlchemy, logger: logging.Logger)`: 扫描 `swfs` 目录并更新数据库
+ `swf_parser::Header(path: str)`: 获取 SWF 文件头

### Exceptions

+ `Error`: 异常类的父类
    - `FieldLacked`: 缺少字段
    - `NotExpected`: 参数类型不匹配
    - `InvalidHeader`: SWF 文件头无效

### Scripts

+ `build.sh`: 打包最小可用的 tar.gz 文件
+ `run.sh`: 启动程序

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)