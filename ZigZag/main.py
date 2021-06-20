import sys, os, argparse
import json, csv
from time import time
from utils import *
from objects import *
import numpy as np


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='argparse')
    # parser.add_argument('--expnum', '-n', help='experiment number', required=True)
    # parser.add_argument('--perf', '-p', help='performance output', required=True)
    # parser.add_argument('--result', '-r', help='result output', required=True)
    parser.add_argument('--dbdir', '-b', help='database directory', required=True)
    parser.add_argument('--db', '-d', help='database name', required=True)
    parser.add_argument('--minsup', '-m', type=float, help='minimum support X%', required=True)
    parser.add_argument('--inc_number', '-i', type=int, help='number of increments', required=False, default=3)
    parser.add_argument('--granularity', '-g', type=int, help='size of increment', required=False, default=10000)
    args = parser.parse_args()

    totalDB = get_DB(args.dbdir, args.db)
    db_size = len(totalDB)
    minsup = args.minsup / 100 * db_size

    inc_number = args.inc_number
    granularity = args.granularity
    inc_split = db_size - inc_number * granularity
    assert(inc_split >= 0)

    baseDB = totalDB[:inc_split]
    zigzag = ZigZag(minsup, baseDB)
    zigzag.prep()
    zigzag.run()
    zigzag.updateRetainedFIs()

    for i in range(inc_number):
        incDB = totalDB[inc_split + granularity * i : inc_split + granularity * (i+1)]
        zigzag.update_incDB(incDB, inc_split)
        zigzag.runInc()
        zigzag.updateRetainedFIs()
