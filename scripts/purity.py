from lingpy import *
from lingrex.copar import CoPaR
from lingrex.util import add_structure
from tabulate import tabulate
from collections import defaultdict

almsA = Alignments('autocognates.tsv', ref="cogid")
almsB = Alignments('autocognates.tsv', ref="lexstatid")
almsA.align()
almsB.align()

add_structure(almsA)
add_structure(almsB)

copA = CoPaR(almsA, ref="cogid")
copB = CoPaR(almsB, ref="lexstatid")

copA.get_sites()
copA.cluster_sites()
purA = copA.purity()
copA.sites_to_pattern()


copB.get_sites()
copB.cluster_sites()
purB = copB.purity()
copB.sites_to_pattern()

lenA, lenB = len(copA.clusters), len(copB.clusters)

regA, regB = (
        len([c for c, vals in copA.clusters.items() if len(vals) > 1]),
        len([c for c, vals in copB.clusters.items() if len(vals) > 1])
        )

sitesA = [tuple(p) for _, p in copA.sites.items()]
sitesB = [tuple(p) for _, p in copB.sites.items()]

propA = [p for p in sitesA if p in copA.clusters]
propB = [p for p in sitesB if p in copB.clusters]

fullA = defaultdict(list)
patA = defaultdict(list)
for s, v in copA.sites.items():
    v = tuple(v)
    if v in copA.clusters:
        if len(copA.clusters[v]) > 1:
            fullA[s[0]] += [1]
        else:
            fullA[s[0]] += [0]
        patA[s[0]] += [1]
    else:
        fullA[s[0]] += [0]
cogsA = [1 if sum(val) > 1 else 0 for _, val in fullA.items()]

fullB = defaultdict(list)
patB = defaultdict(list)
for s, v in copB.sites.items():
    v = tuple(v)
    if v in copB.clusters:
        if len(copB.clusters[v]) > 1:
            fullB[s[0]] += [1]
        else:
            fullB[s[0]] += [0]
        patB[s[0]] += [1]
    else:
        fullB[s[0]] += [0]
cogsB = [1 if sum(val) > 1 else 0 for _, val in fullB.items()]

singleA = []
for cogid, row in copA.etd["cogid"].items():
    if sum([1 for x in row if x]) > 1:
        singleA += [1]
    else:
        singleA += [0]



singleB = []
for cogid, row in copB.etd["lexstatid"].items():
    if sum([1 for x in row if x]) > 1:
        singleB += [1]
    else:
        singleB += [0]


covA = [len(copA.msa["cogid"][x]["taxa"]) for x, y in fullA.items() if sum(y) >
        1]
covB = [len(copB.msa["lexstatid"][x]["taxa"]) for x, y in fullB.items() if sum(y) >
        1]


table = [
        ["singletons", singleA.count(0), singleB.count(0)],
        ["cognates", sum(singleA), sum(singleB)],
        ["patterns", lenA, lenB],
        ["regular patterns", regA, regB],
        ["pattern proportion", regA/lenA, regB/lenB],
        ["sites", len(sitesA), len(sitesB)],
        ["clustered sites", len(propA), len(propB)], 
        ["sites proportion", len(propA)/len(sitesA), len(propB)/len(sitesB)],
        ["purity", purA, purB],
        ["cognates with patterns", len(patA), len(patB)], 
        ["regular cognates", sum(cogsA), sum(cogsB)],
        ["regularity", sum(cogsA)/len(patA), sum(cogsB)/len(patB)],
        ["coverage", sum(covA), sum(covB)],
        ["coverage proportion", sum(covA)/len(copA), sum(covB)/len(copB)]
        ]
print(tabulate(table, headers=["", "Expert", "LexStat"]))
