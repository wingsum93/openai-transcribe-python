import os
import sys

def list_files_with_extension(folder_path, extension, output_file):
    """
    Lists all files in the given folder with the specified extension and writes the results to a file.

    :param folder_path: Path to the folder to search.
    :param extension: File extension to filter by.
    :param output_file: File to write the results to.
    """
    if not os.path.exists(folder_path):
        print("Folder path does not exist.")
        return

    with open(output_file, 'w',encoding='utf8') as file:
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith('.' + extension):
                    file_path = os.path.join(root, file_name)
                    file.write(file_path + '\n')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py [folder_path] [extension]")
    else:
        folder_path = sys.argv[1]
        extension = sys.argv[2]
        output_file = "result.txt"
        list_files_with_extension(folder_path, extension, output_file)
        print(f"Results written to {output_file}")
