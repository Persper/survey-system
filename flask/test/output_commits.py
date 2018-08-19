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


# In manual test, expect the following order if the first commit is always chosen:
# 1. yyx990803@gmail.com (#1-self): 0e53066 vs. 3d36a44
# 2. yyx990803@gmail.com (#2-self): 0e53066 (filled) vs. 48acf71
# 3. yyx990803@gmail.com (#3-self): 21112ec vs. 48acf71 (filled)
# [Quit]
# 4. 805037171@163.com (#1-self): 049f317 vs. 3a5432a
# 5. 805037171@163.com (#2-other compared): 0e53066 vs. 3d36a44
# 6. 805037171@163.com (#3-self): 049f317 (filled) vs. d8d4ca6
# 7. 805037171@163.com (#4-other compared): 0e53066 (filled) vs. 48acf71
# 8. 805037171@163.com (#5-self): 3a5432a (filled) vs. d8d4ca6 (filled)
# 9. 805037171@163.com (#6-other compared): 21112ec vs. 48acf71 (filled)
# 10. 805037171@163.com (#7-other comparison): 21112ec (filled) vs. 5a255d9
# 11. 805037171@163.com (#8-other comparison): 3d36a44 (filled) vs. 5a255d9 (filled)
# [Complete]
# 12. yyx990803@gmail.com (#4-other compared): 049f317 vs. d8d4ca6
# 13. yyx990803@gmail.com (#5-self): 21112ec (filled) vs. 5a255d9
# 14. yyx990803@gmail.com (#6-other compared): 049f317 (filled) vs. 3a5432a
# 15. yyx990803@gmail.com (#7-self): 3d36a44 (filled) vs. 5a255d9 (filled)
# 16. yyx990803@gmail.com (#8-other compared): 3a5432a (filled) vs. d8d4ca6 (filled)
# [Complete]


if __name__ == '__main__':
    main()
