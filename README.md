全球IP段数据库 / Global IP Ranges
一个免费、自动更新、CDN加速的全球各国IP段API。数据直接来源于官方RIR（区域互联网注册机构）。
在线API: https://api.yourdomain.com/ipv4/CN.json (替换为你的域名)
🚀 特性 / Features
100%免费 / 100% Free: 完全基于GitHub Actions + Cloudflare R2 + CDN的免费额度构建
每周自动更新 / Weekly Updates: 每周一通过GitHub Actions自动更新数据
官方数据源 / Official Sources: 直接来自APNIC、ARIN、RIPE、LACNIC、AFRINIC
全球CDN加速 / Global CDN: 通过Cloudflare实现全球50ms内响应
零维护 / Zero Maintenance: 配置完成后无需人工干预
📁 数据结构 / Data Structure
复制
data/
├── ipv4/
│   ├── CN.json (中国IPv4段)
│   ├── US.json (美国IPv4段)
│   └── ... (200+个国家)
└── ipv6/
    ├── CN.json
    ├── US.json
    └── ...
JSON格式 / JSON Format
JSON
复制
// https://api.yourdomain.com/ipv4/CN.json
[
  "1.0.1.0/24",
  "1.0.2.0/23",
  "1.0.8.0/21",
  "... 中国约8000个CIDR段"
]
🔥 快速开始 / Quick Start
HTTP访问 / Access via HTTP
bash
复制
# 获取中国所有IPv4段
# Get all IPv4 ranges for China
curl https://api.yourdomain.com/ipv4/CN.json

# 获取日本所有IPv6段
# Get all IPv6 ranges for Japan
curl https://api.yourdomain.com/ipv6/JP.json
Python使用示例 / Use in Python
Python
复制
import requests

def get_country_ip_ranges(country_code, ip_version='ipv4'):
    """获取指定国家的IP段"""
    # Get IP ranges for a specific country
    url = f"https://api.yourdomain.com/{ip_version}/{country_code.upper()}.json"
    response = requests.get(url)
    return response.json()

# 示例 / Example
cn_ips = get_country_ip_ranges('CN')
print(f"中国共有 {len(cn_ips)} 个IPv4 CIDR段")
# China has 8000 IPv4 CIDR blocks
Node.js使用示例 / Use in Node.js
JavaScript
复制
async function getIPRanges(country, version = 'ipv4') {
    // 获取指定国家的IP段
    const response = await fetch(`https://api.yourdomain.com/${version}/${country.toUpperCase()}.json`);
    return response.json();
}

// 示例 / Example
const usIPs = await getIPRanges('US', 'ipv6');
console.log(usIPs.length); // 约3000个IPv6段 / ~3000 IPv6 ranges
🛠️ 技术栈 / Tech Stack
数据采集 / Data Collection: GitHub Actions (定时任务)
数据存储 / Storage: Cloudflare R2 (10GB免费存储)
分发网络 / Distribution: Cloudflare CDN (全球边缘缓存)
数据源 / Source: 官方RIR FTP服务器
APNIC: https://ftp.apnic.net/stats/apnic/
ARIN: https://ftp.arin.net/pub/stats/arin/
RIPE: https://ftp.ripe.net/pub/stats/ripencc/
LACNIC: https://ftp.lacnic.net/pub/stats/lacnic/
AFRINIC: https://ftp.afrinic.net/pub/stats/afrinic/
📅 更新计划 / Update Schedule
表格
复制
日期 / Day	时间 (UTC)	操作 / Action
周一 / Monday	00:00	GitHub Actions自动触发
按需 / On-demand	任意时间	手动运行Actions工作流
💰 成本分析 / Cost Breakdown
永久完全免费 (在免费额度内):
表格
复制
服务 / Service	免费额度 / Free Quota	本项目用量 / Usage	月费用 / Monthly Cost
GitHub Actions	2000分钟/月	~8分钟/月	¥0 / $0
Cloudflare R2存储	10GB	~50MB	¥0 / $0
Cloudflare R2操作	100万次B类操作	~800次写入/月	¥0 / $0
Cloudflare CDN流量	无限	缓存读取	¥0 / $0
总计 / Total	-	-	¥0 / $0
🚀 部署你的实例 / Deploy Your Own
前置条件 / Prerequisites
GitHub账号
Cloudflare账号
已接入Cloudflare的域名
1. Fork并克隆 / Fork & Clone
bash
复制
git clone https://github.com/sauronclub/global-ip-ranges.git
cd global-ip-ranges
2. 配置R2 / Configure R2
创建名为 ip-ranges 的R2存储桶
开启 Public Access
绑定自定义域名 (如 api.yourdomain.com)
3. 设置GitHub密钥 / Set GitHub Secrets
在仓库: Settings → Secrets → Actions
R2_ACCOUNT_ID
R2_ACCESS_KEY_ID
R2_SECRET_ACCESS_KEY
R2_BUCKET
4. 触发首次运行 / Trigger First Run
进入 Actions → Update IP Ranges → Run workflow
📜 许可证 / License
所有数据来自官方RIR，属于公有领域。
代码采用 MIT许可证 发布。
All data is sourced from official RIRs and is in the public domain.
Code released under MIT License.
🤝 贡献 / Contributing
欢迎提交Issue或PR：
优化解析逻辑
增加数据校验
改进文档
Feel free to open issues or PRs for:
Optimizing parsing logic
Adding data validation
Improving documentation
💬 支持 / Support
觉得有用？点个 ⭐ Star！
需要帮助？提交Issue或发起讨论。
Found this useful? Star ⭐ the repo!
Need help? Open an Issue or reach out via Discussions.
用心为开发者打造，由开发者创造。
Built with ❤️ for developers, by developers.
