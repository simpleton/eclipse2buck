from eclipse2buck.generator.res import Resource
from eclipse2buck.util import util
if __name__ == "__main__":
    print util.find_all_folder_contains_file_with_suffix("./libsupport", "*.java")

