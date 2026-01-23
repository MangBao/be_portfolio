#!/usr/bin/env python3
"""
Portfolio Backend - Docker Setup Script
Hỗ trợ đa nền tảng: Windows, Linux, macOS
Chạy: python setup.py
"""

import os
import sys
import subprocess
import secrets
import shutil
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print colored header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.END}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def check_command(command):
    """Check if a command exists"""
    return shutil.which(command) is not None


def generate_secret_key():
    """Generate a secure random secret key"""
    return secrets.token_urlsafe(32)


def check_prerequisites():
    """Check if required tools are installed"""
    print_header("Kiểm Tra Prerequisites")
    
    required_tools = {
        'docker': 'Docker',
        'docker-compose': 'Docker Compose'
    }
    
    all_ok = True
    for cmd, name in required_tools.items():
        if check_command(cmd):
            print_success(f"{name} đã được cài đặt")
        else:
            print_error(f"{name} CHƯA được cài đặt")
            all_ok = False
    
    if not all_ok:
        print_error("\nVui lòng cài đặt các công cụ còn thiếu!")
        print_info("Docker Desktop: https://www.docker.com/products/docker-desktop")
        sys.exit(1)
    
    print_success("\nTất cả prerequisites đã sẵn sàng!\n")


def create_env_file():
    """Create .env file from .env.example"""
    print_header("Tạo File Environment Variables")
    
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if env_file.exists():
        response = input(f"{Colors.YELLOW}File .env đã tồn tại. Bạn có muốn ghi đè? (y/N): {Colors.END}").lower()
        if response != 'y':
            print_info("Giữ nguyên file .env hiện tại")
            return False
    
    if not env_example.exists():
        print_error("File .env.example không tồn tại!")
        sys.exit(1)
    
    # Read template
    with open(env_example, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Generate secrets
    print_info("Đang tạo secret keys...")
    secret_key = generate_secret_key()
    jwt_secret = generate_secret_key()
    
    # Replace placeholders
    env_content = template.replace(
        'your-secret-key-change-this-in-production', 
        secret_key
    ).replace(
        'your-jwt-secret-key-change-this-in-production',
        jwt_secret
    )
    
    # Write to .env
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print_success("File .env đã được tạo với secret keys tự động")
    print_info(f"SECRET_KEY: {secret_key[:20]}...")
    print_info(f"JWT_SECRET_KEY: {jwt_secret[:20]}...")
    print_warning("\n⚠ QUAN TRỌNG: KHÔNG CHIA SẺ hoặc COMMIT file .env lên git!\n")
    
    return True


def check_docker_running():
    """Check if Docker daemon is running"""
    print_header("Kiểm Tra Docker Service")
    
    try:
        result = subprocess.run(
            ['docker', 'info'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print_success("Docker service đang chạy")
            return True
        else:
            print_error("Docker service không chạy hoặc không có quyền truy cập")
            return False
    except FileNotFoundError:
        print_error("Docker không được tìm thấy trong PATH")
        return False
    except subprocess.TimeoutExpired:
        print_error("Docker không phản hồi (timeout)")
        return False
    except Exception as e:
        print_error(f"Lỗi khi kiểm tra Docker: {e}")
        return False


def docker_compose_build():
    """Build Docker images"""
    print_header("Build Docker Images")
    
    try:
        print_info("Đang build images... (có thể mất vài phút)")
        
        result = subprocess.run(
            ['docker-compose', 'build'],
            check=False
        )
        
        if result.returncode == 0:
            print_success("Build thành công!")
            return True
        else:
            print_error("Build thất bại!")
            return False
            
    except Exception as e:
        print_error(f"Lỗi khi build: {e}")
        return False


def docker_compose_up(detached=True):
    """Start Docker containers"""
    print_header("Start Docker Containers")
    
    try:
        cmd = ['docker-compose', 'up']
        if detached:
            cmd.append('-d')
        
        print_info(f"Đang start containers{'(background mode)' if detached else ''}...")
        
        result = subprocess.run(cmd, check=False)
        
        if result.returncode == 0:
            print_success("Containers đã được start thành công!")
            return True
        else:
            print_error("Start containers thất bại!")
            return False
            
    except Exception as e:
        print_error(f"Lỗi khi start: {e}")
        return False


def show_status():
    """Show Docker containers status"""
    print_header("Container Status")
    
    try:
        subprocess.run(['docker-compose', 'ps'], check=False)
    except Exception as e:
        print_error(f"Không thể hiển thị status: {e}")


def show_logs():
    """Show recent logs"""
    print_header("Recent Logs")
    
    try:
        subprocess.run(
            ['docker-compose', 'logs', '--tail=50'],
            check=False
        )
    except Exception as e:
        print_error(f"Không thể hiển thị logs: {e}")


def cleanup():
    """Clean up Docker resources"""
    print_header("Cleanup Docker Resources")
    
    response = input(f"{Colors.YELLOW}Bạn có chắc chắn muốn dọn dẹp? (y/N): {Colors.END}").lower()
    if response != 'y':
        print_info("Hủy cleanup")
        return
    
    print_warning("⚠ Đang dừng và xóa containers...")
    
    try:
        subprocess.run(['docker-compose', 'down'], check=False)
        print_success("Cleanup hoàn tất!")
        
        response_volumes = input(f"{Colors.RED}Bạn có muốn XÓA LUÔN DATABASE VOLUMES? (y/N): {Colors.END}").lower()
        if response_volumes == 'y':
            subprocess.run(['docker-compose', 'down', '-v'], check=False)
            print_warning("Database volumes đã bị xóa!")
        
    except Exception as e:
        print_error(f"Lỗi khi cleanup: {e}")


def print_access_info():
    """Print access information"""
    print_header("Thông Tin Truy Cập")
    print(f"{Colors.CYAN}📡 API Endpoint:{Colors.END} http://localhost:5000")
    print(f"{Colors.CYAN}🗄️  Database:{Colors.END}    localhost:5432")
    print(f"{Colors.CYAN}👤 DB User:{Colors.END}       portfolio_user")
    print(f"{Colors.CYAN}🔑 DB Password:{Colors.END}   portfolio_password")
    print(f"{Colors.CYAN}💾 DB Name:{Colors.END}       portfolio_db")
    print()


def print_useful_commands():
    """Print useful Docker commands"""
    print_header("Các Lệnh Hữu Ích")
    
    commands = {
        "Xem logs realtime": "docker-compose logs -f",
        "Xem logs của web service": "docker-compose logs web",
        "Xem logs của database": "docker-compose logs db",
        "Restart services": "docker-compose restart",
        "Stop services": "docker-compose down",
        "Vào shell của web container": "docker-compose exec web bash",
        "Vào PostgreSQL shell": "docker-compose exec db psql -U portfolio_user -d portfolio_db",
        "Xem container status": "docker-compose ps",
    }
    
    for desc, cmd in commands.items():
        print(f"{Colors.CYAN}{desc:.<35}{Colors.END} {Colors.GREEN}{cmd}{Colors.END}")
    print()


def main_menu():
    """Display main menu và xử lý lựa chọn"""
    while True:
        print_header("Portfolio Backend - Docker Setup")
        print(f"{Colors.CYAN}1.{Colors.END} 🚀 Quick Start (Setup + Build + Run)")
        print(f"{Colors.CYAN}2.{Colors.END} 📝 Tạo file .env")
        print(f"{Colors.CYAN}3.{Colors.END} 🔨 Build Docker images")
        print(f"{Colors.CYAN}4.{Colors.END} ▶️  Start containers (background)")
        print(f"{Colors.CYAN}5.{Colors.END} ▶️  Start containers (foreground)")
        print(f"{Colors.CYAN}6.{Colors.END} 📊 Xem container status")
        print(f"{Colors.CYAN}7.{Colors.END} 📜 Xem logs")
        print(f"{Colors.CYAN}8.{Colors.END} 🧹 Cleanup (stop & remove)")
        print(f"{Colors.CYAN}9.{Colors.END} ℹ️  Thông tin truy cập")
        print(f"{Colors.CYAN}0.{Colors.END} 🚪 Thoát")
        print()
        
        choice = input(f"{Colors.BOLD}Chọn một tùy chọn (0-9): {Colors.END}")
        
        if choice == '1':
            # Quick Start
            check_prerequisites()
            create_env_file()
            if check_docker_running():
                if docker_compose_build():
                    if docker_compose_up(detached=True):
                        import time
                        print_info("Đợi containers khởi động...")
                        time.sleep(5)
                        show_status()
                        print_access_info()
                        print_useful_commands()
        
        elif choice == '2':
            create_env_file()
        
        elif choice == '3':
            check_prerequisites()
            check_docker_running()
            docker_compose_build()
        
        elif choice == '4':
            check_prerequisites()
            check_docker_running()
            docker_compose_up(detached=True)
            show_status()
            print_access_info()
        
        elif choice == '5':
            check_prerequisites()
            check_docker_running()
            docker_compose_up(detached=False)
        
        elif choice == '6':
            show_status()
        
        elif choice == '7':
            show_logs()
        
        elif choice == '8':
            cleanup()
        
        elif choice == '9':
            print_access_info()
            print_useful_commands()
        
        elif choice == '0':
            print_success("\nTạm biệt! 👋\n")
            sys.exit(0)
        
        else:
            print_error("Lựa chọn không hợp lệ!")
        
        input(f"\n{Colors.YELLOW}Nhấn Enter để tiếp tục...{Colors.END}")


def main():
    """Main entry point"""
    try:
        # Change to script directory
        os.chdir(Path(__file__).parent)
        
        # Run menu
        main_menu()
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Đã dừng bởi người dùng{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Lỗi không mong đợi: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
