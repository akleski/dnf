import os

def rename_and_replace(root_dir, mode, old_str, new_str):
	# Determine the final replacement string based on mode
	if mode == 1:
		# Legacy behavior: simple replacement
		final_new_str = new_str
	elif mode == 2:
		# New behavior: add 's' prefix and 'y' suffix
		final_new_str = 's' + new_str + 'y'
	else:
		raise ValueError(f"Invalid mode: {mode}. Mode must be 1 or 2.")
	
	# First, rename files and directories
	for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
		# Rename files
		for filename in filenames:
			if old_str in filename:
				old_path = os.path.join(dirpath, filename)
				new_filename = filename.replace(old_str, final_new_str)
				new_path = os.path.join(dirpath, new_filename)
				os.rename(old_path, new_path)
		# Rename directories
		for dirname in dirnames:
			if old_str in dirname:
				old_dir = os.path.join(dirpath, dirname)
				new_dir = os.path.join(dirpath, dirname.replace(old_str, final_new_str))
				os.rename(old_dir, new_dir)

	# Now, replace in file contents
	for dirpath, dirnames, filenames in os.walk(root_dir):
		for filename in filenames:
			file_path = os.path.join(dirpath, filename)
			try:
				with open(file_path, 'r', encoding='utf-8') as f:
					content = f.read()
				if old_str in content:
					new_content = content.replace(old_str, final_new_str)
					with open(file_path, 'w', encoding='utf-8') as f:
						f.write(new_content)
			except Exception as e:
				# Skip binary or unreadable files
				pass

if __name__ == "__main__":
	import sys
	
	# Check if command line arguments are provided
	if len(sys.argv) != 4:
		print("Usage: python dnf_renamer.py <mode> <old_string> <new_string>")
		print("Mode 1: Legacy behavior (simple replacement)")
		print("Mode 2: Add 's' prefix and 'y' suffix to replacement")
		sys.exit(1)
	
	try:
		mode = int(sys.argv[1])
	except ValueError:
		print("Error: mode must be an integer (1 or 2)")
		sys.exit(1)
	
	old = sys.argv[2]
	new = sys.argv[3]
	
	# Validate that old_string is not empty
	if not old.strip():
		print("Error: old_string cannot be empty")
		sys.exit(1)
	
	# Validate mode
	if mode not in [1, 2]:
		print("Error: mode must be 1 or 2")
		sys.exit(1)
	
	root = os.path.dirname(os.path.abspath(__file__))
	
	if mode == 1:
		print(f"Mode 1: Replacing '{old}' with '{new}' in directory: {root}")
	else:
		print(f"Mode 2: Replacing '{old}' with 's{new}y' in directory: {root}")
	
	rename_and_replace(root, mode, old, new)
	print("Replacement complete!")
