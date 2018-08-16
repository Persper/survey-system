#!/usr/bin/env python3.6

import argparse
import json


def main():
    parser = argparse.ArgumentParser(
        description='Generate test input for the input_db.py script')
    parser.add_argument('-f', '--file', required=True, help='file to generate')
    args = parser.parse_args()

    selected = dict()
    selected['vue'] = dict()

    selected['vue']['yyx990803@gmail.com'] = []
    selected['vue']['yyx990803@gmail.com'].append(['3d36a443c755bf16f2656a8595dda9076f021a4a',
                                                   '5a255d946c6c70218f6ebc0ddbf31029db696813'])
    selected['vue']['yyx990803@gmail.com'].append(['21112ecc691e25fc13b40985c0f0381e3911efa5',
                                                   '5a255d946c6c70218f6ebc0ddbf31029db696813'])
    selected['vue']['yyx990803@gmail.com'].append(['21112ecc691e25fc13b40985c0f0381e3911efa5',
                                                   '48acf71a01e5665f72696d44aa5a8d8f1d137172'])
    selected['vue']['yyx990803@gmail.com'].append(['0e5306658ad7b83c553a6a3eeedb15f9066ab063',
                                                   '48acf71a01e5665f72696d44aa5a8d8f1d137172'])
    selected['vue']['yyx990803@gmail.com'].append(['0e5306658ad7b83c553a6a3eeedb15f9066ab063',
                                                   '3d36a443c755bf16f2656a8595dda9076f021a4a'])

    selected['vue']['805037171@163.com'] = []
    selected['vue']['805037171@163.com'].append(['3a5432a9e3f470ebafcef905281b830537897037',
                                                 'd8d4ca6763af55e1715bbc1e0fadd10e5be41db3'])
    selected['vue']['805037171@163.com'].append(['049f3171a9d2e97f62c209a4b78a71ec9dae810f',
                                                 'd8d4ca6763af55e1715bbc1e0fadd10e5be41db3'])
    selected['vue']['805037171@163.com'].append(['049f3171a9d2e97f62c209a4b78a71ec9dae810f',
                                                 '3a5432a9e3f470ebafcef905281b830537897037'])

    with open(args.file, 'w') as f:
        json.dump(selected, f)


if __name__ == '__main__':
    main()
