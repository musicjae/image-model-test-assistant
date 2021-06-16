import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--p', default=30009,
                    help='사용하고자 하는 port 번호를 입력하시오',
                    type=int)

args = parser.parse_args()