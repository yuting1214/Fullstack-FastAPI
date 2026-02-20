import sys
import argparse
from src.backend.core.config import get_settings

parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["dev", "prod"], default="dev", help="Set the running mode")
parser.add_argument("--host", type=str, default="127.0.0.1", help="Set the host")

is_testing = "pytest" in sys.argv[0]

if is_testing:
    args = argparse.Namespace(mode="dev", host="127.0.0.1")
else:
    args = parser.parse_args()

settings = get_settings(args.mode)
global_settings = settings
