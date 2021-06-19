import sys, os, argparse
import json, csv
from time import time
from utils import *
from objects import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='argparse')
    # parser.add_argument('--expnum', '-n', help='experiment number', required=True)
    parser.add_argument('--dbdir', '-b', help='database directory', required=True)
    parser.add_argument('--db', '-d', help='database name', required=True)
    parser.add_argument('--minsup', '-m', help='minimum support X%', required=True)
    # parser.add_argument('--perf', '-p', help='performance output', required=True)
    # parser.add_argument('--result', '-r', help='result output', required=True)
    args = parser.parse_args()

    totalDB = get_DB(args.dbdir, args.db)
    db_size = len(totalDB)
    minsup = int(args.minsup) / 100 * db_size
    split = 0.4

    inc_split = int(db_size * split)
    baseDB = totalDB[:inc_split]

    zigzag = ZigZag(minsup, baseDB)
    zigzag.run()
    zigzag.updateRetainedFIs()

    incDB = totalDB[inc_split:]
    s = time()
    zigzag.update_incDB(incDB, inc_split)
    zigzag.runInc()
    e = time()
    print(e-s)
    zigzag.updateRetainedFIs()

    # incDB = totalDB[inc_split + int(db_size * 0.2):]
    # zigzag.update_incDB(incDB, inc_split + int(db_size * 0.2))
    # zigzag.runInc()
    # print(zigzag.mfis)
    # zigzag.updateRetainedFIs()


# ------------------------------------------------------------------
# -----------------------------Draft--------------------------------
# ------------------------------------------------------------------

    # ----------GenMax----------
    # freqDBItems = getFreqDBItems(baseDB, minsup)
    # freqDBItemList = list(freqDBItems.keys())
    # f = ascOrderedList(freqDBItems)
    # vdb = transposeDB(baseDB)
    # itemset_support = {}
    # for k, v in vdb.items():
    #     itemset_support[k] = len(v)
    # ---call---
    # mfis = []
    # s = time()
    # mfiBackTrack([], f, mfis, minsup, vdb, [])
    # e = time()
    # print(e-s)
    # print(mfis)
    # --- gen FI ---
    # fis = set()
    # for mfi in mfis:
    #     fis = fis.union(mypowerset(mfi))
    # fis.discard('')
    # --- count FI---
    # retained = {}
    # for fi in fis:
    #     if fi in retained:
    #         retained[fi] = len(vdb[fi])
    #     else:
    #         retained[fi] = countItemset(fi, vdb)
    #
    #
    # #------- Inc: D+ only, no D- -------
    # scan inc db
    # incDB = db[inc_split:]
    # vIncDB = transposeDB(incDB, inc_split)
    # # update db and support
    # newDB = baseDB + incDB
    # inc_itemset_support = {}
    # for k, v in vIncDB.items():
    #     vdb[k] = vdb.get(k,set()).union(v)
    #     # inc_itemset_support[k] = len(v)
    #     # itemset_support[k] = itemset_support.get(k, 0) + len(v)
    #
    # # freq items in new db
    # newFreqDBItems = getFreqDBItems(newDB, minsup)
    # newF = ascOrderedList(newFreqDBItems)
    #
    # mfiBackTrack([], newF, mfis, minsup, vdb, vIncDB, retained)
    # print(mfis)
