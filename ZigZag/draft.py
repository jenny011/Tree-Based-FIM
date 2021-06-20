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
