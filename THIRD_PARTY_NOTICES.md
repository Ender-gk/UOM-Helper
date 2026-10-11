# 第三方依赖

本地服务通过安装脚本从 PyPI 下载依赖；本发布包不包含这些依赖的安装文件或模型文件。实际版本以 `extension/requirements.lock.txt` 为准。

| 组件 | 用途 | 项目页面 |
| --- | --- | --- |
| Flask | 本地 HTTP API | https://pypi.org/project/Flask/ |
| flask-cors | 跨域响应处理 | https://pypi.org/project/flask-cors/ |
| ddddocr | 验证码识别模型 | https://pypi.org/project/ddddocr/ |
| NumPy | 图像数据处理 | https://pypi.org/project/numpy/ |
| ONNX Runtime | 模型推理 | https://pypi.org/project/onnxruntime/ |
| OpenCV | 图像增强 | https://pypi.org/project/opencv-python/ |
| Pillow | 图片格式校验 | https://pypi.org/project/Pillow/ |
| Tesseract.js | 浏览器备用识别 | https://github.com/naptha/tesseract.js |

传递依赖也列在依赖锁定文件中。各第三方组件的版权、许可和模型说明以其发布包及项目文档为准。
