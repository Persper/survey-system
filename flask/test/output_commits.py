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

    selected['vue']['kawakazu80@gmail.com'] = []
    selected['vue']['kawakazu80@gmail.com'].append(['9478fde8c92d225661dcb4c949d0035284600fff',
                                                   'd80eff8eb61e48ac184536a159a0e96c4613e7d6'])

    selected['jquery'] = dict()

    selected['jquery']['dave.methvin@gmail.com'] = []
    selected['jquery']['dave.methvin@gmail.com'].append(['67fa2eab6ef323b1d894e9e7f054c6e8c844d304',
                                                         '4bf1a09522955eb52de1fafb4ee1ecc5982b7a3e'])

    with open(args.file, 'w') as f:
        json.dump(selected, f)


# In manual test, expect the following order (* is chosen):
# 1. kawakazu80@gmail.com (#1-self): 9478fde* vs. d80eff8
# 2. kawakazu80@gmail.com (#1-other comparison): d8d4ca6 vs. 049f317*
# [Quit]
# 3. yyx990803@gmail.com (#1-self): 0e53066* vs. 3d36a44
# 4  yyx990803@gmail.com (#2-other compared-0): 9478fde vs. d80eff8*
# 5. yyx990803@gmail.com (#3-self): 0e53066* (filled) vs. 48acf71
# 6. yyx990803@gmail.com (#4-self): 21112ec vs. 48acf71* (filled)
# [Quit]
# 7. 805037171@163.com (#1-self): 049f317 vs. 3a5432a*
# 8. 805037171@163.com (#2-other compared-0): 0e53066* vs. 48acf71
# 9. 805037171@163.com (#3-self): 049f317* (filled) vs. d8d4ca6
# 10. 805037171@163.com (#4-other compared-0): 0e53066 (filled) vs. 3d36a44*
# 11. 805037171@163.com (#5-self): 3a5432a* (filled) vs. d8d4ca6 (filled)
# 12. 805037171@163.com (#6-other compared-0): 48acf71* (filled) vs. 21112ec
# 10. 805037171@163.com (#7-other compared-1): 9478fde* vs. d80eff8
# 11 805037171@163.com (#8-other comparison): 5a255d9 vs. 21112ec* (filled)
# 12. 805037171@163.com (#9-other comparison): 3d36a44* (filled) vs. 5a255d9 (filled)
# [Complete]
# 13. yyx990803@gmail.com (#5-self): 21112ec (filled) vs. 5a255d9*
# 14. yyx990803@gmail.com (#6-other compared-0): 3a5432a* vs. d8d4ca6
# 15. yyx990803@gmail.com (#7-self): 3d36a44 (filled) vs. 5a255d9* (filled)
# 16. yyx990803@gmail.com (#8-other compared-0): 3a5432a* (filled) vs. 049f317
# 17. yyx990803@gmail.com (#9-other compared-1): 049f317 (filled) vs. d8d4ca6* (filled)
# [Complete]


if __name__ == '__main__':
    main()
