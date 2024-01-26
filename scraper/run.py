import argparse
import subprocess
import sys
import os


def run_main(args):
    main_py_path = os.path.join(os.path.dirname(__file__), "src", "main.py")
    subprocess.run(["python", main_py_path] + args, check=True)


def run_read_db():
    import src.read_db

    src.read_db.main()


if __name__ == "__main__":
    mode_parser = argparse.ArgumentParser(description="Control script", add_help=False)
    mode_parser.add_argument("--mode", required=True)
    args, remaining_args = mode_parser.parse_known_args()

    if args.mode == "main":
        run_main(remaining_args)
    elif args.mode == "read_db":
        run_read_db()
        pass
    else:
        print("Invalid mode selected.")
        sys.exit(1)
