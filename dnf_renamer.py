import os

def rename_and_replace(root_dir, old_str, new_str):
	# First, rename files and directories
	for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
		# Rename files
		for filename in filenames:
			if old_str in filename:
				old_path = os.path.join(dirpath, filename)
				new_filename = filename.replace(old_str, new_str)
				new_path = os.path.join(dirpath, new_filename)
				os.rename(old_path, new_path)
		# Rename directories
		for dirname in dirnames:
			if old_str in dirname:
				old_dir = os.path.join(dirpath, dirname)
				new_dir = os.path.join(dirpath, dirname.replace(old_str, new_str))
				os.rename(old_dir, new_dir)

	# Now, replace in file contents
	for dirpath, dirnames, filenames in os.walk(root_dir):
		for filename in filenames:
			file_path = os.path.join(dirpath, filename)
			try:
				with open(file_path, 'r', encoding='utf-8') as f:
					content = f.read()
				if old_str in content:
					new_content = content.replace(old_str, new_str)
					with open(file_path, 'w', encoding='utf-8') as f:
						f.write(new_content)
			except Exception as e:
				# Skip binary or unreadable files
				pass

if __name__ == "__main__":
	import sys
	
	# Check if command line arguments are provided
	if len(sys.argv) != 3:
		print("Usage: python dnf_renamer.py <old_string> <new_string>")
		sys.exit(1)
	
	old = sys.argv[1]
	new = sys.argv[2]
	
	# Validate that old_string is not empty
	if not old.strip():
		print("Error: old_string cannot be empty")
		sys.exit(1)
	
	root = os.path.dirname(os.path.abspath(__file__))
	
	print(f"Replacing '{old}' with '{new}' in directory: {root}")
	rename_and_replace(root, old, new)
	print("Replacement complete!")
