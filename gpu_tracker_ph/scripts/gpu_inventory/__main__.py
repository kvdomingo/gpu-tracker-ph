import sys
from .clean.clean_lazada_data import clean_data as clean_lazada
from .clean.clean_shopee_data import clean_data as clean_shopee
from .push_to_db import push


def main(op: str):
    if op == "clean":
        clean_lazada()
        clean_shopee()
    elif op == "push":
        push()
    else:
        raise ValueError("Unrecognized argument")


if __name__ == "__main__":
    main(sys.argv[1])
