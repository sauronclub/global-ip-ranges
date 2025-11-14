#!/usr/bin/env python3
"""
下载RIR数据，按国家生成JSON文件
存入 data/ipv4/ 和 data/ipv6/ 目录
"""
import requests
from pathlib import Path
import json
import sys

# 五个RIR的FTP地址
RIR_URLS = {
    'apnic': 'https://ftp.apnic.net/stats/apnic/delegated-apnic-latest',
    'arin': 'https://ftp.arin.net/pub/stats/arin/delegated-arin-extended-latest',
    'ripe': 'https://ftp.ripe.net/pub/stats/ripencc/delegated-ripencc-latest',
    'lacnic': 'https://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest',
    'afrinic': 'https://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-latest'
}

def download_rir_data():
    """下载所有RIR数据"""
    all_lines = []
    for rir, url in RIR_URLS.items():
        print(f"📥 下载 {rir} 数据: {url}")
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            lines = resp.text.splitlines()
            all_lines.extend(lines)
            print(f"   获取 {len(lines)} 行")
        except Exception as e:
            print(f"❌ 下载失败: {e}", file=sys.stderr)
            sys.exit(1)
    return all_lines

def parse_and_group(lines):
    """按国家解析IP段"""
    country_data = {}
    
    for line in lines:
        if not line or line.startswith('#'):
            continue
        
        parts = line.split('|')
        if len(parts) < 7:
            continue
        
        registry, country, type_, start, value = parts[0], parts[1], parts[2], parts[3], parts[4]
        
        if type_ not in ['ipv4', 'ipv6']:
            continue
        
        # 跳过保留地址和未知国家
        if country in ['', '*', 'ZZ']:
            continue
        
        if country not in country_data:
            country_data[country] = {'ipv4': [], 'ipv6': []}
        
        if type_ == 'ipv4':
            # IPv4: value是IP数量，转CIDR
            try:
                ip_count = int(value)
                # 计算前缀长度: 2^(32-prefix) = ip_count
                import math
                prefix = 32 - int(math.log2(ip_count))
                cidr = f"{start}/{prefix}"
                country_data[country]['ipv4'].append(cidr)
            except ValueError:
                continue
        else:
            # IPv6: value直接是前缀长度
            cidr = f"{start}/{value}"
            country_data[country]['ipv6'].append(cidr)
    
    return country_data

def save_json_files(country_data):
    """保存到data目录"""
    data_dir = Path('data')
    ipv4_dir = data_dir / 'ipv4'
    ipv6_dir = data_dir / 'ipv6'
    
    # 创建目录
    ipv4_dir.mkdir(parents=True, exist_ok=True)
    ipv6_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存每个国家
    for country, ips in sorted(country_data.items()):
        # 保存IPv4
        if ips['ipv4']:
            ipv4_file = ipv4_dir / f'{country}.json'
            with open(ipv4_file, 'w') as f:
                json.dump(sorted(ips['ipv4']), f, indent=2)
        
        # 保存IPv6
        if ips['ipv6']:
            ipv6_file = ipv6_dir / f'{country}.json'
            with open(ipv6_file, 'w') as f:
                json.dump(sorted(ips['ipv6']), f, indent=2)
    
    print(f"✅ 生成完成: {len(country_data)} 个国家")
    print(f"   IPv4文件: {len(list(ipv4_dir.glob('*.json')))} 个")
    print(f"   IPv6文件: {len(list(ipv6_dir.glob('*.json')))} 个")

def main():
    print("🚀 开始更新IP段数据...")
    
    # 1. 下载
    lines = download_rir_data()
    
    # 2. 解析
    print("\n📝 解析数据中...")
    country_data = parse_and_group(lines)
    
    # 3. 保存
    print("\n💾 保存JSON文件...")
    save_json_files(country_data)
    
    print("\n🎉 全部完成！")

if __name__ == '__main__':
    main()