#!/usr/bin/env python3
import os

def combine_to_code_py(src_folder):
    """Combine Python files in the 'src' folder into 'code.py', ensuring dependency order."""
    output_folder = "bin"
    os.makedirs(output_folder, exist_ok=True)  # Ensure 'bin' folder exists
    output_file = os.path.join(output_folder, "code.py")

    try:
        # Collect Python files
        python_files = [os.path.join(src_folder, file) for file in os.listdir(src_folder) if file.endswith(".py")]

        # Separate main.py and other utility files
        main_file = None
        utility_files = []

        for file in python_files:
            if os.path.basename(file) == "main.py":
                main_file = file
            else:
                utility_files.append(file)

        if not main_file:
            raise FileNotFoundError("main.py not found in the source folder.")

        # Ensure utility files are ordered if needed
        dependency_order = ["imports.py","init.py","colors.py", "grid_utils.py", "chase_fill.py"]
        utility_files.sort(key=lambda f: dependency_order.index(os.path.basename(f)) if os.path.basename(f) in dependency_order else len(dependency_order))

        imports = []
        utility_content = []
        main_content = []

        # Process utility files
        for file in utility_files:
            with open(file, "r") as infile:
                lines = infile.readlines()
                for line in lines:
                    if line.strip().startswith("import ") or line.strip().startswith("from "):
                        imports.append(line)
                    else:
                        utility_content.append(line)

        # Process main.py
        with open(main_file, "r") as infile:
            lines = infile.readlines()
            for line in lines:
                if line.strip().startswith("import ") or line.strip().startswith("from "):
                    imports.append(line)
                else:
                    main_content.append(line)

        # Write combined output
        with open(output_file, "w") as outfile:
            for line in sorted(set(imports)):
                outfile.write(line)
            outfile.write("\n")
            outfile.writelines(utility_content)

            # Add main script at the end
            outfile.writelines(main_content)

        print(f"Combined file saved as '{output_file}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
src_folder = "src"  # Replace with your source folder
combine_to_code_py(src_folder)
