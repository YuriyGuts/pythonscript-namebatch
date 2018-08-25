#!/usr/bin/env python3
"""
Generates spells to summon Benedict Cumberbatch.

Usage:
pythonscript-namebatch.py [-h] [--count N] [--diversity D]

optional arguments:
  -h, --help     show this help message and exit
  --count N      Number of names to generate (default: 10)
  --diversity D  Name diversity (0 = low [default], 1 = high)
"""

import argparse
import sys

from generator import NameGenerator
from morphology import CMUDictMorphologyService


def parse_command_line_args(args):
    """
    Parse command-line arguments and organize them into a single structured object.
    """

    parser = argparse.ArgumentParser(description='Generates spells to summon Benedict Cumberbatch.')
    parser.add_argument(
        '--count',
        metavar='N',
        required=False,
        type=int,
        choices=range(1, 10000),
        default=10,
        help='Number of names to generate (default: 10)'
    )
    parser.add_argument(
        '--diversity',
        metavar='D',
        required=False,
        type=int,
        default=0,
        choices=[0, 1],
        help='Name diversity (0 = low [default], 1 = high)'
    )

    # Try parsing the arguments and fail properly if that didn't succeed.
    return parser.parse_args(args)


def main():
    args = parse_command_line_args(sys.argv[1:])

    morph_service = CMUDictMorphologyService()
    morph_service.bootstrap()

    generator = NameGenerator(morph_service, diversity_level=args.diversity)
    for i in range(args.count):
        print(generator.random_name())


if __name__ == '__main__':
    main()
