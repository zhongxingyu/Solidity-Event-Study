import os.path
import sys
from gas_reducer import function

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("missing path to solidity file")

    path = sys.argv[1]

    if os.path.isdir(path):
        compile_success = []
        compile_error = []
        for root, dirs, files in os.walk(path):
            for item in files:
                absolute_path = os.path.join(root, item)
                if os.path.splitext(absolute_path)[1] == '.sol':
                    returnValue = function.scan(absolute_path)
                    if returnValue == -1:
                        compile_error.append(absolute_path)
                    else:
                        compile_success.append(absolute_path)
        # for item in compile_success:
        #     print("Compiled successfully " + item)
        for item in compile_error:
            print("Compiled unsuccessfully " + item)
    elif os.path.isfile(path):
        returnValue = function.scan(path)
        if returnValue == -1:
            print("Compilation unsuccessfully " + path + "\n")
        # else:
        #     print("Compilation successful " + path + "\n")
    else:
        print(path + " is not the path to solidity file")