import glob
import os

def main():
    output_dir = "/app/output"
    files = glob.glob(os.path.join(output_dir, "*"))
    for file in files:
        try:
            os.remove(file)
            print(f"Deleted file: {file}")
        except Exception as e:
            print(f"Error deleting file {file}: {e}")

if __name__ == "__main__":
    main()