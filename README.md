# UOM 培训助手

**v1.2 · Chrome / Edge 扩展 · 本地验证码识别**

在 UOM 视频培训页面提供课程选择、验证码识别及提交控制。所有操作集中在网页悬浮面板中。

## 功能

- 普通模式：识别并提交，等待响应，失败后冷却 300ms 再继续。
- 高并发模式：以 **200ms** 间隔推进提交，限制未完成请求的数量。
- 插件主动打开弹窗、刷新验证码及提交操作，共用不小于 **200ms** 的操作间隔。
- 支持课程选择、验证码刷新和手动提交。
- 切换课程或模式时停止当前任务；关闭面板时停止并释放页面绑定。
- 本地双模型识别，提供浏览器备用识别和成功提示音。

200ms 是插件主动调用页面操作的最小间隔；等待响应、识别及冷却可能让实际间隔更长。平台页面方法内部产生的请求由平台自身实现决定。

## 环境要求

| 项目 | 要求 |
| --- | --- |
| 系统 | Windows 64 位 |
| 浏览器 | Chrome 或 Microsoft Edge，支持 Manifest V3 |
| Python | Python 3.12，加入 PATH |
| 本地服务 | `127.0.0.1:8899` 端口可用 |
| 首次安装 | 能访问 PyPI 下载依赖 |

## 安装

### 1. 下载并解压

从本仓库 Releases 下载 `UOM-Helper-v1.2.zip`，解压到固定位置。下面的安装与启动脚本均位于 `extension/` 文件夹。

### 2. 安装本地识别服务

双击 `extension/INSTALL_AI_SERVER.bat`。脚本会在扩展目录内创建 `.venv`，按 `requirements.lock.txt` 安装固定依赖。

安装只需进行一次。安装失败时检查 Python 版本、PATH 与 PyPI 网络连接。

### 3. 启动识别服务

双击 `extension/START_AI_SERVER.bat`，等待模型加载完成。保持窗口运行。

服务地址：`http://127.0.0.1:8899`。浏览器访问 `/health` 可查看状态；正常状态为 `status: "ok"`，版本为 `1.2.0`。

### 4. 加载浏览器扩展

1. Edge 打开 `edge://extensions/`，Chrome 打开 `chrome://extensions/`。
2. 开启开发者模式。
3. 选择“加载解压缩的扩展程序”，定位到 `extension/`，该目录内应有 `manifest.json`。
4. 进入 [UOM 平台](https://uom.caac.gov.cn/)，登录并打开视频培训课程列表。

## 使用

1. 等待面板提示连接到课程列表。
2. 在下拉框中确认目标课程，也可直接点击页面课程来同步选择。
3. 选择普通模式或高并发模式。
4. 点击“开始任务”。
5. 点击“停止任务”结束自动操作。关闭面板也会停止，刷新页面可重新显示。

切换课程或模式会停止任务，确认选择后重新开始。手动提交与自动任务互斥；连续手动操作也受 200ms 间隔限制。

已经由平台页面发出的请求无法通过关闭弹窗撤回。提交超过 10 秒没有响应时，插件停止新增操作，请先确认页面结果。

## 常见问题

**没有面板或开始按钮不可用？** 重新加载扩展并刷新网页，确认进入的是视频培训课程列表。

**AI 离线？** 检查本地服务窗口、安装依赖与 8899 端口。备用识别需要下载 CDN 脚本和语言资源，也可能受页面安全策略限制。

**提示上一轮提交尚未结束？** 等待页面返回结果后再开始；长期无响应时先确认课程状态，必要时刷新页面。

**验证码识别失败？** 使用刷新验证码操作。识别结果不是准确率保证；课程结果以平台反馈为准。

**页面升级后无法使用？** 本插件依赖培训页面适配。平台改版可能影响使用，可提交不包含账号数据的故障描述。

## 文件

```text
extension/
  manifest.json
  content.js / content_bridge.js / injector.js / background.js
  popup.html / popup.js
  uom_ai_server.py / uom_engine.py
  requirements.txt / requirements.lock.txt
  INSTALL_AI_SERVER.bat / START_AI_SERVER.bat
```

权限与数据处理说明见 [PRIVACY.md](PRIVACY.md)。第三方依赖见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。发布内容见 [RELEASE_NOTES.md](RELEASE_NOTES.md)。`SHA256SUMS.txt` 提供文件校验值。
