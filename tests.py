from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def main():
    working_directory = "calculator"
    
    # Test get_files_info with various directories
    # root_contents = get_files_info(working_directory)
    # print(f"Contents of {working_directory}:\n{root_contents}")
    # pkg_contents = get_files_info(working_directory, "pkg")
    # print(f"Contents of {working_directory}/pkg:\n{pkg_contents}")
    # pkg_contents = get_files_info(working_directory, "/bin")
    # print(f"Contents of {working_directory}/bin:\n{pkg_contents}")
    # pkg_contents = get_files_info(working_directory, "../")
    # print(f"Contents of {working_directory}/../:\n{pkg_contents}")  
    
    # # Test get_file_content with various files
    # print(get_file_content(working_directory, "lorem.txt"))
    # print(get_file_content(working_directory, "main.py"))
    # print(get_file_content(working_directory, "pkg/calculator.py"))
    # print(get_file_content(working_directory, "/bin/cat"))
    # print(get_file_content(working_directory, "pkg/nonexistent.py"))
    
    # Test write_file with various file paths and content
    # print(write_file(working_directory, "new_file.txt", "This is a new file."))
    # print(write_file(working_directory, "pkg/new_file.txt", "This is a new file in pkg."))
    # print(write_file(working_directory, "../new_file.txt", "This should fail."))
    # print(write_file(working_directory, "/bin/new_file.txt", "This should also fail."))
    
    # Test run_python_file with various file paths
    # print(run_python_file(working_directory, "main.py"))
    # print(run_python_file(working_directory, "tests.py"))
    # print(run_python_file(working_directory, "nonexistent.py"))
    # print(run_python_file(working_directory, "../main.py"))
    # print(run_python_file(working_directory, "main.py", ["3 + 5"]))
    
main()