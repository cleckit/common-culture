import subprocess
import argparse
import yaml
import os
import re
from datetime import datetime
from pathlib import Path

def get_git_info():
    """Get current git commit hash and author info."""
    try:
        commit_hash = subprocess.run(['git', 'rev-parse', 'HEAD'], 
                                   capture_output=True, text=True, check=True).stdout.strip()
        commit_author = subprocess.run(['git', 'log', '-1', '--format=%an'], 
                                     capture_output=True, text=True, check=True).stdout.strip()
        commit_date = subprocess.run(['git', 'log', '-1', '--format=%ci'], 
                                   capture_output=True, text=True, check=True).stdout.strip()
        return commit_hash, commit_author, commit_date
    except subprocess.CalledProcessError:
        return "unknown", "unknown", "unknown"

def get_changed_files(common_dir, since_commit='HEAD~1'):
    """
    Returns a list of files changed in the common directory since the specified commit.
    """
    cmd = ['git', 'diff', '--name-only', since_commit, 'HEAD', '--', common_dir]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        changed_files = [line for line in result.stdout.strip().split('\n') if line]
        return changed_files
    except subprocess.CalledProcessError:
        print(f"Warning: Could not get git diff for {common_dir}")
        return []

def analyze_imports_in_file(file_path):
    """
    Analyze Python imports in a file and return structured information.
    """
    imports = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find import statements
        import_patterns = [
            r'^from\s+([^\s]+)\s+import\s+(.+)$',  # from module import something
            r'^import\s+([^\s]+)$'                  # import module
        ]
        
        for line_num, line in enumerate(content.split('\n'), 1):
            line = line.strip()
            for pattern in import_patterns:
                match = re.match(pattern, line)
                if match:
                    if 'from' in pattern:
                        module = match.group(1)
                        items = [item.strip() for item in match.group(2).split(',')]
                        imports.append({
                            'type': 'from_import',
                            'module': module,
                            'items': items,
                            'line': line_num,
                            'raw_line': line
                        })
                    else:
                        module = match.group(1)
                        imports.append({
                            'type': 'import',
                            'module': module,
                            'line': line_num,
                            'raw_line': line
                        })
    except Exception as e:
        print(f"Warning: Could not analyze {file_path}: {e}")
    
    return imports

def scan_common_directory(common_dir):
    """
    Scan the common directory for Python files and analyze their structure.
    """
    common_files = {}
    common_path = Path(common_dir)
    
    if not common_path.exists():
        print(f"Warning: Common directory {common_dir} does not exist")
        return common_files
    
    for python_file in common_path.rglob("*.py"):
        relative_path = str(python_file.relative_to(common_path))
        imports = analyze_imports_in_file(python_file)
        
        common_files[relative_path] = {
            'full_path': str(python_file),
            'size_bytes': python_file.stat().st_size,
            'imports': imports,
            'last_modified': datetime.fromtimestamp(python_file.stat().st_mtime).isoformat()
        }
    
    return common_files

def find_usage_across_codebase(common_dir):
    """
    Search for usage of common modules across the entire codebase.
    """
    usage_data = {}
    
    # Get all Python files in the project (excluding common_dir to avoid self-references)
    try:
        cmd = ['find', '.', '-name', '*.py', '-not', '-path', f'./{common_dir}/*']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        all_python_files = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        
        # Look for imports that reference the common directory
        for file_path in all_python_files:
            if not os.path.exists(file_path):
                continue
                
            imports = analyze_imports_in_file(file_path)
            common_imports = []
            
            for imp in imports:
                # Check if import references common directory
                module = imp.get('module', '')
                if common_dir.replace('/', '.') in module or common_dir.replace('\\', '.') in module:
                    common_imports.append(imp)
            
            if common_imports:
                usage_data[file_path] = {
                    'common_imports': common_imports,
                    'import_count': len(common_imports)
                }
    
    except subprocess.CalledProcessError:
        print("Warning: Could not scan codebase for usage patterns")
    
    return usage_data

def load_existing_tracking(tracking_file):
    """Load existing tracking data if it exists."""
    if os.path.exists(tracking_file):
        try:
            with open(tracking_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not load existing tracking file: {e}")
    return {}

def update_tracking_file(common_dir, tracking_file):
    """
    Update the tracking YAML file with current state of common code usage.
    """
    print(f"Analyzing common directory: {common_dir}")
    print(f"Updating tracking file: {tracking_file}")
    
    # Get git information
    commit_hash, commit_author, commit_date = get_git_info()
    
    # Get changed files in common directory
    changed_files = get_changed_files(common_dir)
    
    # Scan common directory structure
    common_files = scan_common_directory(common_dir)
    
    # Find usage across codebase
    usage_data = find_usage_across_codebase(common_dir)
    
    # Load existing tracking data
    existing_data = load_existing_tracking(tracking_file)
    
    # Create new tracking entry
    tracking_entry = {
        'timestamp': datetime.now().isoformat(),
        'commit_info': {
            'hash': commit_hash,
            'author': commit_author,
            'date': commit_date
        },
        'analysis': {
            'common_directory': common_dir,
            'changed_files_in_common': changed_files,
            'total_common_files': len(common_files),
            'common_files_detail': common_files,
            'usage_across_codebase': usage_data,
            'total_files_using_common': len(usage_data)
        }
    }
    
    # Update tracking data structure
    if 'tracking_history' not in existing_data:
        existing_data['tracking_history'] = []
    
    existing_data['tracking_history'].append(tracking_entry)
    existing_data['last_updated'] = datetime.now().isoformat()
    existing_data['common_directory'] = common_dir
    
    # Keep only last 50 entries to prevent file from growing too large
    if len(existing_data['tracking_history']) > 50:
        existing_data['tracking_history'] = existing_data['tracking_history'][-50:]
    
    # Create summary statistics
    existing_data['summary'] = {
        'total_tracking_entries': len(existing_data['tracking_history']),
        'current_common_files': len(common_files),
        'current_usage_count': len(usage_data),
        'most_recent_changes': changed_files[:10] if changed_files else []
    }
    
    # Write updated tracking file
    try:
        with open(tracking_file, 'w', encoding='utf-8') as f:
            yaml.dump(existing_data, f, default_flow_style=False, sort_keys=False, indent=2)
        print(f"Successfully updated tracking file: {tracking_file}")
        print(f"Found {len(common_files)} files in common directory")
        print(f"Found {len(usage_data)} files using common code")
        if changed_files:
            print(f"Detected {len(changed_files)} changed files in common directory")
    except Exception as e:
        print(f"Error writing tracking file: {e}")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Track common code usage and imports')
    parser.add_argument('--common_dir', required=True, 
                       help='Directory containing common code to track')
    parser.add_argument('--tracking_file', required=True,
                       help='YAML file to store tracking information')
    
    args = parser.parse_args()
    
    # Ensure we're in the right directory (where .git exists)
    if not os.path.exists('.git'):
        print("Error: This script must be run from the root of a git repository")
        return 1
    
    success = update_tracking_file(args.common_dir, args.tracking_file)
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())