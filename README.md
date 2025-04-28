# 食品标签后端API服务

这是一个基于Flask的食品标签相关API服务

## 项目结构

```
.
├── app/                    # 应用主目录
│   ├── __init__.py         # 应用初始化
│   ├── api/                # API模块
│   │   ├── __init__.py
│   │   ├── label.py        # 标签审核API
│   │   ├── ocr.py          # OCR图像识别API
│   │   ├── translation.py  # 图像翻译API
│   │   ├── comparison.py   # 图像对比API
│   │   └── laws.py         # 法规相关API
│   ├── config/             # 配置模块
│   │   ├── __init__.py
│   │   └── config.py       # 配置类
│   └── utils/              # 工具函数
│       ├── __init__.py
│       └── helpers.py      # 辅助函数
├── uploads/                # 上传文件存储目录
├── laws/                   # 法规文件存储目录
├── .env                    # 环境变量
├── run.py                  # 应用入口
└── requirements.txt        # 项目依赖
```

## 功能列表

1. 标签审核接口
2. OCR图像识别接口
3. 图像翻译接口
4. 图像对比接口
5. 法规检索接口
6. 法规文件上传接口
7. 法规文件下载接口

## 安装与运行

### 前置需求

- Python 3.8+

### 安装依赖

```bash
pip install -r requirements.txt
```

### 环境配置

1. 复制环境变量示例文件并按需修改
```bash
cp .env.example .env
```

2. 修改.env文件中的配置

### 运行服务

```bash
python run.py
```

服务默认在 `http://localhost:5000` 启动

## 接口说明

### 1. 标签审核接口

- 路径: `/LabelCheck/TextAndSheet`
- 方法: POST
- 请求体: JSON格式，包含文本和表格数据

### 2. OCR图像识别接口

- 路径: `/TextAndSheet`
- 方法: POST
- 请求体: form-data，包含图片文件

### 3. 图像翻译接口

- 路径: `/Translation`
- 方法: POST
- 请求体: form-data，包含图片文件

### 4. 图像对比接口

- 路径: `/TextComparison`
- 方法: POST
- 请求体: form-data，包含两个图片文件

### 5. 法规检索接口

- 路径: `/LawsSearch`
- 方法: POST
- 请求体: JSON格式，包含检索关键词

### 6. 法规文件上传接口

- 路径: `/zsk-api/open/prepack/addFoodRegula`
- 方法: POST
- 请求体: form-data，包含法规文件和相关信息

### 7. 法规文件下载接口

- 路径: `/hn/fileDownload`
- 方法: GET
- 查询参数: fileid和appid

