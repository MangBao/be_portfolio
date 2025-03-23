import yaml
import os

def validate_yaml_files():
    # Thư mục gốc chứa các file YAML
    docs_dir = 'src/docs'
    
    # Dictionary lưu kết quả kiểm tra
    validation_results = {
        'valid_files': [],
        'invalid_files': [],
        'not_found_files': []
    }
    
    # Danh sách các thư mục cần kiểm tra
    directories = ['auth', 'menu', 'about', 'project', 'skill', 'experience', 'contact']
    
    for dir_name in directories:
        dir_path = os.path.join(docs_dir, dir_name)
        
        # Kiểm tra thư mục có tồn tại không
        if not os.path.exists(dir_path):
            print(f"Directory not found: {dir_path}")
            continue
            
        # Lấy tất cả file .yaml trong thư mục
        yaml_files = [f for f in os.listdir(dir_path) if f.endswith('.yaml')]
        
        for yaml_file in yaml_files:
            file_path = os.path.join(dir_path, yaml_file)
            
            try:
                # Thử mở và parse file YAML
                with open(file_path, 'r', encoding='utf-8') as f:
                    yaml.safe_load(f)
                validation_results['valid_files'].append(file_path)
                print(f"✅ Valid YAML: {file_path}")
                
            except FileNotFoundError:
                validation_results['not_found_files'].append(file_path)
                print(f"❌ File not found: {file_path}")
                
            except yaml.YAMLError as e:
                validation_results['invalid_files'].append({
                    'file': file_path,
                    'error': str(e)
                })
                print(f"❌ Invalid YAML in {file_path}")
                print(f"Error: {str(e)}")
                
            except Exception as e:
                validation_results['invalid_files'].append({
                    'file': file_path,
                    'error': str(e)
                })
                print(f"❌ Unexpected error in {file_path}")
                print(f"Error: {str(e)}")
    
    # In tổng kết
    print("\n=== Validation Summary ===")
    print(f"Total valid files: {len(validation_results['valid_files'])}")
    print(f"Total invalid files: {len(validation_results['invalid_files'])}")
    print(f"Total not found files: {len(validation_results['not_found_files'])}")
    
    # In chi tiết các file không hợp lệ
    if validation_results['invalid_files']:
        print("\nDetailed errors in invalid files:")
        for invalid_file in validation_results['invalid_files']:
            print(f"\nFile: {invalid_file['file']}")
            print(f"Error: {invalid_file['error']}")
    
    return validation_results

def check_swagger_references():
    """Kiểm tra các đường dẫn trong decorator @swag_from"""
    blueprint_files = {
        'auth': ['register', 'login'],
        'menu': ['get_menus', 'get_menu', 'create_menu', 'update_menu', 'delete_menu', 'toggle_menu_active'],
        'about': ['get_about', 'create_about', 'update_about', 'delete_about'],
        'project': ['get_projects', 'get_project', 'create_project', 'update_project', 'delete_project', 'get_latest_projects'],
        'skill': ['get_skills', 'get_skill', 'create_skill', 'update_skill', 'delete_skill', 'batch_create_skills', 'get_categories'],
        'experience': ['get_experiences', 'get_experience', 'create_experience', 'update_experience', 'delete_experience', 'get_current_experience'],
        'contact': ['get_contacts', 'create_contact', 'update_contact_status', 'delete_contact', 'get_contact_stats', 'get_latest_contacts']
    }
    
    missing_files = []
    
    for blueprint, endpoints in blueprint_files.items():
        for endpoint in endpoints:
            yaml_path = f'src/docs/{blueprint}/{endpoint}.yaml'
            if not os.path.exists(yaml_path):
                missing_files.append(yaml_path)
                print(f"❌ Missing YAML file: {yaml_path}")
            else:
                print(f"✅ Found YAML file: {yaml_path}")
    
    if missing_files:
        print("\nMissing YAML files:")
        for file in missing_files:
            print(f"- {file}")
    else:
        print("\nAll expected YAML files are present!")
    
    return missing_files

if __name__ == "__main__":
    print("=== Validating YAML Files ===\n")
    validate_yaml_files()
    
    print("\n=== Checking Swagger References ===\n")
    check_swagger_references()
