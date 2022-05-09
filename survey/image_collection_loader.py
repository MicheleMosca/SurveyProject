import sys
import yaml

if __name__ == '__main__':
    print("Image Collection Loader\n")

    if len(sys.argv) != 2:
        print(f"Error: incorrect parameters! Usage: {sys.argv[0]} file.yaml")
        exit(1)

    print(f"Load: {sys.argv[1]}")
    file = open(sys.argv[1], "r")
    data = yaml.load(file, Loader=yaml.FullLoader)
    print(data)
