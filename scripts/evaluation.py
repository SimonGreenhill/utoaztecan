from lingpy import Wordlist
from lingpy.evaluate.acd import bcubes, diff

wl = Wordlist('autocognates.tsv')
bcubes(wl, 'cogid', 'lexstatid')

diff(wl, "cogid", "lexstatid", filename="comparison", pprint=False)
