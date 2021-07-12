from cltoolkit import Wordlist
from cltoolkit.util import lingpy_columns
from pycldf import Dataset
from lingpy.evaluate.acd import bcubes
from lingpy import LexStat

clwl = Wordlist(datasets=[Dataset.from_metadata("../cldf/cldf-metadata.json")])
clwl.load_cognates()
# get languages with good coverage
selected = []
for language in clwl.languages:
    if len(language.concepts) >= 100:
        selected += [language.id]

language_filter = lambda x: x.id in selected

print("[i] wordlist has {0} languages, filtered {1}".format(len(clwl.languages),
    len(selected)))
wl = clwl.as_lingpy(
        language_filter=language_filter, 
        columns=lingpy_columns(cognates="default"))
print("[i] loaded wordlist with {0} languages".format(wl.width))
# renumber cognates
C = {}
cognates = {}
cogid = 1
for idx, cog in wl.iter_rows("cognacy"):
    if cog.strip():
        if cog in cognates:
            C[idx] = cognates[cog]
        else:
            C[idx] = cogid
            cognates[cog] = cogid
            cogid += 1
    else:
        C[idx] = cogid
        cogid += 1
wl.add_entries("cogid", C, lambda x: x)
print("[i] start lexstat analysis")
lex = LexStat(wl)
lex.get_scorer(runs=10000)
lex.cluster(method="lexstat", threshold=0.55, ref="lexstatid")
lex.output("tsv", filename="lexstat-analysis")
lex.output('tsv', filename="autocognates", ignore="all", prettify=False)

bcubes(lex, "cogid", "lexstatid")



