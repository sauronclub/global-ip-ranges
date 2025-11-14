
# global-ip-ranges

[![CI](https://github.com/your-username/global-ip-ranges/actions/workflows/update.yml/badge.svg)](https://github.com/your-username/global-ip-ranges/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

一个轻量级的工具集合，用于从五大区域性注册机构（RIR）下载 delegated 分配表，解析并按国家生成 IP 段（CIDR）JSON 文件，且可选择将生成的数据上传到 Cloudflare R2（兼容 S3 API）。

主要功能
- 从 APNIC / ARIN / RIPE / LACNIC / AFRINIC 拉取最新 delegated 数据
- 将 IPv4 / IPv6 分配解析为按国家分组的 CIDR 列表
- 输出 JSON 文件到 `data/ipv4/` 与 `data/ipv6/`
- 可选：将生成的 `data/` 上传到 Cloudflare R2
- 提供 GitHub Actions 工作流以自动定期更新

目录结构

```
global-ip-ranges/
├─ README.md
├─ .github/workflows/update.yml
├─ scripts/
│  ├─ update_ranges.py    # 下载 + 解析 -> data/
│  └─ upload_to_r2.py     # 上传 data/ -> R2 (S3 API)
└─ data/                  # 运行脚本后生成（通常不纳入版本控制）
```

快速开始

先决条件
- Python 3.8+（CI 使用 3.11）
- pip

安装依赖（推荐先添加 `requirements.txt`，可让我为你创建）

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

生成国家级 IP 列表（本地运行）

```powershell
python scripts/update_ranges.py
```

上传生成的数据到 Cloudflare R2

```powershell
$env:R2_ACCOUNT_ID = "<your-account-id>"
$env:R2_ACCESS_KEY_ID = "<your-access-key>"
$env:R2_SECRET_ACCESS_KEY = "<your-secret>"
$env:R2_BUCKET = "<your-bucket-name>"
python scripts/upload_to_r2.py
```

运行成功后，你会在 `data/ipv4/` 与 `data/ipv6/` 下看到以国家两字母代码命名的 JSON 文件（例如 `CN.json`），每个文件是一个 CIDR 字符串数组。

脚本说明

- `scripts/update_ranges.py`
	- 从 RIR 的 `delegated-*-latest` 文件下载并合并。
	- 跳过注释行以及保留/未知国家条目（例如 `ZZ`）。
	- IPv4：将数量（count）转换为 CIDR（当前实现用 log2 计算前缀，适用于 count 为 2 的幂的情况）。
	- IPv6：使用给定的前缀长度直接保存。
	- 输出为 `data/ipv4/<CC>.json` 与 `data/ipv6/<CC>.json`。

- `scripts/upload_to_r2.py`
	- 使用 `boto3` 创建兼容 S3 的客户端，endpoint 基于 `R2_ACCOUNT_ID` 拼接为 R2 地址。
	- 递归上传 `data/` 目录内容，按文件后缀设置 `ContentType` 并添加 `Cache-Control`。

配置与环境变量

上传脚本需要以下环境变量：

- `R2_ACCOUNT_ID`
- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_BUCKET`

切勿将密钥明文提交到仓库；在 GitHub Actions 中请使用仓库的 Secrets（Settings → Secrets & variables）。

GitHub Actions

仓库自带 `.github/workflows/update.yml`：

- 定期调度（每周）并支持手动触发（workflow_dispatch）。
- 工作流会安装依赖、运行 `scripts/update_ranges.py` 生成 `data/`、在有变更时提交到仓库，并调用 `scripts/upload_to_r2.py` 上传到 R2（需要在 Secrets 中配置凭据）。

请确保在仓库 Secrets 中设置：

- `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET`

已知限制与问题

- IPv4 转换目前假定 `count` 为 2 的幂并直接转换为单个 CIDR；对于非 2 的幂的分配，当前实现可能跳过或生成不准确的结果。建议实现更健壮的“拆分为最少CIDR列表”算法。
- 缺少网络请求重试和退避策略，临时网络故障会导致脚本中止。
