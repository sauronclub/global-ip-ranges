
# global-ip-ranges

[![CI](https://github.com/your-username/global-ip-ranges/actions/workflows/update.yml/badge.svg)](https://github.com/your-username/global-ip-ranges/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

Lightweight tools to download delegated IP allocations from the five Regional Internet Registries (RIRs), parse them into per-country CIDR lists and optionally upload the generated data to Cloudflare R2 (S3-compatible).

Features
- Download the latest delegated data from APNIC, ARIN, RIPE, LACNIC and AFRINIC
- Parse IPv4/IPv6 allocations into country-level CIDR lists
- Output JSON files under `data/ipv4/` and `data/ipv6/`
- Optional upload to Cloudflare R2 using the S3 API
- GitHub Actions workflow to update on schedule and push results

Table of contents
- Quick start
- Scripts
- Configuration & environment
- GitHub Actions
- Contributing
- License

Project layout
```
global-ip-ranges/
├─ README.md
├─ RIR_URLS.txt
├─ .github/workflows/update.yml
├─ scripts/
│  ├─ update_ranges.py    # download + parse -> data/
│  └─ upload_to_r2.py     # upload data/ -> R2 (S3 API)
└─ data/                  # generated output (not checked in by default)
```

Quick start

Requirements
- Python 3.8+ (CI uses 3.11)
- pip

Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Generate the per-country IP lists locally

```powershell
python scripts/update_ranges.py
```

Upload generated data to Cloudflare R2

```powershell
$env:R2_ACCOUNT_ID = "<your-account-id>"
$env:R2_ACCESS_KEY_ID = "<your-access-key>"
$env:R2_SECRET_ACCESS_KEY = "<your-secret>"
$env:R2_BUCKET = "<your-bucket-name>"
python scripts/upload_to_r2.py
```

After success you will find files like `data/ipv4/CN.json` and `data/ipv6/CN.json` containing arrays of CIDR strings for each country.

Scripts

- scripts/update_ranges.py
	- Downloads RIR delegated files and merges them.
	- Parses lines for `ipv4` and `ipv6` entries, filters out comments and reserved/unknown country codes (`ZZ`).
	- IPv4 entries currently convert `count` to a single CIDR using log2 (works when count is a power of two).
	- IPv6 entries use the provided prefix length.
	- Writes JSON arrays to `data/ipv4/<CC>.json` and `data/ipv6/<CC>.json`.

- scripts/upload_to_r2.py
	- Creates a boto3 S3 client pointed at Cloudflare R2 (endpoint uses account id).
	- Recursively uploads `data/` files to a target bucket and sets `ContentType` and `CacheControl`.

Configuration & environment

The upload script requires the following environment variables:
- `R2_ACCOUNT_ID`
- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_BUCKET`

Never commit secrets to the repository. Use GitHub Secrets for CI.

GitHub Actions

The repository includes `.github/workflows/update.yml` which:
- Runs weekly (cron) and can be manually triggered.
- Installs dependencies, runs `update_ranges.py`, commits the `data/` folder (if changed) and uploads to R2.

Make sure to populate the repository secrets:
- `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET`.

Limitations & known issues

- IPv4 conversion assumes `count` is a power of two and converts it to one CIDR; for non-power-of-two allocations the current script may produce incorrect results or skip entries. Consider implementing a CIDR-splitting routine to cover arbitrary counts.
- No retry/backoff on network errors; transient failures may abort the run.

Recommended next steps

1. Add `requirements.txt` (I can add this for you).
2. Implement IPv4 splitting so arbitrary allocation sizes become a minimal set of CIDRs.
3. Add unit tests (pytest) for parsing and conversion logic and mock `boto3` for upload tests.

Contributing

Contributions are welcome. Please open an issue for discussion or submit a pull request. If you plan to make breaking changes, open an issue first so we can coordinate.

Security

- Do not commit credentials. If credentials were committed accidentally, rotate them immediately and remove them from git history.
- Use GitHub Secrets for CI environment variables.

License

This repository does not contain a license file by default. If you want to publish this project as open source, add a `LICENSE` file (MIT or Apache-2.0 recommended).

中文说明（简短）

这是一个用于从五大 RIR 下载并按国家生成 IPv4/IPv6 CIDR 列表的工具，支持将结果上传到 Cloudflare R2。更多用法请参见上文英文说明。

---

If you'd like, I can now:

- add a `requirements.txt` and update the CI to use it (recommended),
- implement robust IPv4 splitting and unit tests (more work), or
- add an `LICENSE` file (MIT) and update README badges/links.

Tell me which task to do next and I'll implement it.
