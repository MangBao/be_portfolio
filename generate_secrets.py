#!/usr/bin/env python3
"""
Script để tạo SECRET_KEY và JWT_SECRET_KEY ngẫu nhiên và an toàn
Chạy: python generate_secrets.py
"""

import secrets
import string

def generate_secret_key(length=64):
    """
    Tạo một secret key ngẫu nhiên và an toàn
    
    Args:
        length: Độ dài của key (mặc định 64 ký tự)
    
    Returns:
        String chứa secret key
    """
    # Sử dụng secrets module để tạo key ngẫu nhiên an toàn
    alphabet = string.ascii_letters + string.digits + string.punctuation
    # Loại bỏ các ký tự có thể gây vấn đề trong shell/env
    alphabet = alphabet.replace('"', '').replace("'", '').replace('\\', '').replace('$', '')
    
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_hex_key(length=64):
    """
    Tạo một secret key dạng hexadecimal (chỉ chứa 0-9, a-f)
    An toàn hơn cho việc sử dụng trong environment variables
    
    Args:
        length: Độ dài của key (mặc định 64 ký tự)
    
    Returns:
        String chứa secret key dạng hex
    """
    return secrets.token_hex(length // 2)

if __name__ == '__main__':
    print("=" * 60)
    print("TẠO SECRET KEYS CHO DỰ ÁN BE PORTFOLIO")
    print("=" * 60)
    print()
    
    # Tạo SECRET_KEY
    secret_key = generate_hex_key(64)
    print("SECRET_KEY (cho Flask):")
    print(f"SECRET_KEY={secret_key}")
    print()
    
    # Tạo JWT_SECRET_KEY
    jwt_secret_key = generate_hex_key(64)
    print("JWT_SECRET_KEY (cho JWT tokens):")
    print(f"JWT_SECRET_KEY={jwt_secret_key}")
    print()
    
    print("=" * 60)
    print("HƯỚNG DẪN SỬ DỤNG:")
    print("=" * 60)
    print("1. Copy các giá trị trên vào file .env")
    print("2. Hoặc export trực tiếp trong terminal:")
    print(f"   export SECRET_KEY={secret_key}")
    print(f"   export JWT_SECRET_KEY={jwt_secret_key}")
    print()
    print("⚠️  LƯU Ý: KHÔNG BAO GIỜ commit các key này lên Git!")
    print("=" * 60)

