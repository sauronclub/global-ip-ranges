#!/usr/bin/env python3
"""
上传data目录到R2存储桶
"""
import boto3
from pathlib import Path
import os
import sys

def get_s3_client():
    """创建R2 S3客户端"""
    account_id = os.getenv('R2_ACCOUNT_ID')
    access_key = os.getenv('R2_ACCESS_KEY_ID')
    secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
    
    if not all([account_id, access_key, secret_key]):
        print("❌ 缺少R2环境变量", file=sys.stderr)
        sys.exit(1)
    
    endpoint = f"https://{account_id}.r2.cloudflarestorage.com"
    
    return boto3.client(
        's3',
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name='auto'
    )

def upload_directory(s3_client, bucket_name, local_dir, prefix=''):
    """递归上传目录"""
    local_path = Path(local_dir)
    
    for file_path in local_path.rglob('*'):
        if not file_path.is_file():
            continue
        
        # 计算R2中的key
        relative_path = file_path.relative_to(local_path)
        key = f"{prefix}{relative_path}"
        
        # 设置Content-Type
        content_type = 'application/json' if file_path.suffix == '.json' else 'text/plain'
        
        try:
            s3_client.upload_file(
                str(file_path),
                bucket_name,
                str(key),
                ExtraArgs={
                    'ContentType': content_type,
                    'CacheControl': 'public, max-age=86400'  # 缓存24小时
                }
            )
            print(f"✅ 上传: {key}")
        except Exception as e:
            print(f"❌ 上传失败 {key}: {e}", file=sys.stderr)

def main():
    print("🚀 开始上传到R2...")
    
    s3_client = get_s3_client()
    bucket_name = os.getenv('R2_BUCKET')
    
    if not bucket_name:
        print("❌ 缺少R2_BUCKET环境变量", file=sys.stderr)
        sys.exit(1)
    
    # 检查bucket是否存在
    try:
        s3_client.head_bucket(Bucket=bucket_name)
    except Exception as e:
        print(f"❌ Bucket不存在或权限错误: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 上传data目录
    data_dir = Path('data')
    if not data_dir.exists():
        print("❌ data目录不存在", file=sys.stderr)
        sys.exit(1)
    
    print(f"📤 正在上传 {bucket_name}...")
    upload_directory(s3_client, bucket_name, data_dir)
    
    print("\n🎉 全部上传完成！")

if __name__ == '__main__':
    main()