import os
import yaml

def fix_yaml_files():
    docs_dir = 'src/docs'
    directories = ['auth', 'menu', 'about', 'project', 'skill', 'experience', 'contact']
    
    for dir_name in directories:
        dir_path = os.path.join(docs_dir, dir_name)
        if not os.path.exists(dir_path):
            continue
            
        yaml_files = [f for f in os.listdir(dir_path) if f.endswith('.yaml')]
        
        for yaml_file in yaml_files:
            file_path = os.path.join(dir_path, yaml_file)
            
            try:
                # Đọc toàn bộ nội dung file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Xóa các dấu --- và tất cả khoảng trắng/xuống dòng thừa
                content = content.replace('---', '').strip()
                
                # Parse YAML content
                doc = yaml.safe_load(content)
                
                # Ghi lại file với format chuẩn
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(doc, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
                
                print(f"✅ Fixed: {file_path}")
                
            except Exception as e:
                print(f"❌ Error fixing {file_path}: {str(e)}")

if __name__ == "__main__":
    print("=== Fixing YAML Files ===\n")
    fix_yaml_files()
