# Tree-Based-FIM
CS Independent Studies (Capstone) on frequent itemset mining algorithms

## FP-Growth
Centralized non-incremental algorithm. <br>
Comprised of two phases: <br>
<li>FP-Tree building: project the frequent itemsets in the database onto a compact tree following a descending frequency order.</li>
<li>FP-Growth: mine the FP-Tree to retrieve all the frequent itemsets</li>

## CanTree
Centralized incremental algorithm. <br>
Its tree-building phase is similar to FP-Growth. <br>
It deals with incremental database updates by storing all the frequent and infrequent itemsets in its CanTree following a canonical order. <br>
CanTree can be mined using existing FP-Growth-like mining algorithms.

## Freno
A primitive design of an incremental algorithm that is suitable for distributed computing.
