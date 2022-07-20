# Analyzing Cognate Decisions

In order to carry out the automated cognate detection analysis using LingPy, please make sure that you have installed the most recent version of LingPy and the most recent version of LingRex and CL Toolkit, which you can install easily with the help of `pip`:

```
$ pip install lingpy
$ pip install lingrex
$ pip install cltoolkit
```

Then, make sure to install the pyclts package and to download the CLTS data, placing it into the `scripts` folder.

```
$ pip install pyclts
$ cd scripts
$ git clone https://github.com/cldf-clts/clts
$ cd clts
$ git checkout v2.2.0
$ cd ..
```

Make also sure to install [python-igraph](https://igraph.org), which will require to install the general igraph library first (igraph is used for clustering cognates).

Once this has been done, simply type:

```
$ python cognates.py
```

This may take quite some time, since we use 10000 iterations in the permutation test for the wordlists.

The results will be written to the file `autocognates.tsv`, which we also provide here.

To measure differences and inspect the results, we compute the B-Cubed scores (see [List et al. 2017](https://doi.org/10.1371/journal.pone.0170046) for details). 

```
$ python evaluation.py
```

The results are:

```
*************************
* B-Cubed-Scores        *
* --------------------- *
* Precision:     0.9496 *
* Recall:        0.5879 *
* F-Scores:      0.7262 *
*************************'
```

Detailed results are listed in the file `comparison.diff`, which lists differences in the cognate decisions for all concepts where differences could be observed.

Consider, for example, the following excerpt:

```
Concept: ALL, False Positives: yes, False Negatives: yes
utoaztecan-AztecTetelcingo     	notʃi       	   1	   1
utoaztecan-AztecZacapoaxtla    	notʃi       	   1	   1
utoaztecan-ClassicalAztec      	motʃ        	   1	   5
utoaztecan-Pipil               	mutʃi       	   1	   5
utoaztecan-ClassicalAztec      	motʃi       	   1	   5
utoaztecan-Cahuilla            	u̠mun       	   3	   3
utoaztecan-Chemehuevi          	mɑnːo       	   4	   4
utoaztecan-Kawaiisu            	monodʒo     	   4	   4
utoaztecan-SouthernPaiute      	mano        	   4	   4
utoaztecan-SouthernPaiute      	manu        	   4	   4
utoaztecan-SouthernUte         	pɑʔɑmɑnuni  	   4	  31
utoaztecan-SouthernUte         	pɑʔɑmɑnuktis	   4	  31
utoaztecan-SouthernUte         	mɑnuni      	   4	  31
utoaztecan-Comanche            	odʒɯ        	   6	   6
utoaztecan-ShoshoniGosiute     	odʒoːn      	   6	   6
utoaztecan-Comanche            	odʒo        	   6	   6
utoaztecan-Pannamint           	odʒoːntɯ    	   6	   6
utoaztecan-Pannamint           	odʒoːntɯsɯ  	   6	   6
utoaztecan-NorthernPaiute      	noːˀdʒu     	   6	  19
utoaztecan-Cora                	heitse      	   7	   7
utoaztecan-Cupeno              	pətɑ̠ʔɑmɑ   	   8	   8
utoaztecan-Eudeve              	awona       	   9	   9
utoaztecan-Eudeve              	haona       	   9	   9
utoaztecan-Gabrielino          	owɑ̠̄ʔix    	  10	  10
utoaztecan-Guarijio            	joma        	  11	  11
utoaztecan-Hopi                	sosodʒɑm    	  12	  12
utoaztecan-Hopi                	sosoj       	  12	  12
utoaztecan-Huichol             	naitɯ       	  13	   1
utoaztecan-Huichol             	dʒunaitɯ    	  13	   1
utoaztecan-Huichol             	nai         	  13	   1
utoaztecan-Kitanemuk           	pudʒu       	  15	  15
utoaztecan-Serrano             	pudʒu       	  15	  15
utoaztecan-Luiseno             	tʃoʔon      	  16	  16
utoaztecan-Mayo                	tsikti      	  17	  17
utoaztecan-Yaqui               	tsikti      	  17	  17
utoaztecan-Mono                	nasimi      	  18	  18
utoaztecan-NorthernTepehuan    	βɯʃi        	  20	  20
utoaztecan-Papago              	wɯs         	  20	  20
utoaztecan-PimaDeOnavas        	βɯʃ         	  20	  20
utoaztecan-SoutheasternTepehuan	vɯʃ         	  20	  20
utoaztecan-Papago              	wɯs         	  20	  20
utoaztecan-Tubar               	wetsɑ̠t     	  20	  33
utoaztecan-Tubar               	wesɑ̠t      	  20	  33
utoaztecan-Opata               	sə          	  21	  21
utoaztecan-Pannamint           	wɯmː        	  22	  22
utoaztecan-SanJuanPuebloTewa   	tʲɛ̃ʰkih    	  26	  26
utoaztecan-Tarahumara          	omɑrwɑme    	  32	  32
utoaztecan-Tubatulabel         	pinidʒu     	  34	  15
utoaztecan-ClassicalAztec      	iːxkitʃ     	  46	  46
utoaztecan-Pannamint           	sɯmɯsɯ      	  50	  18
```

The first column in this file is the language identifier, the second column gives the word form (without spaces segmenting sounds to make the output more compact), the third column provides the experts' judgments, which have been renumbered consecutively, and the fourth column provides the automated cognate judgments, which have also been renumbered, to allow for a quick comparison.

In this example, we can see that the experts identify the first five words as cognates, while the algorithm splits them into two sets, one representing words starting with `[`n`]` the other words starting with `[`m`]`. 

Cognate set 4 in the example only differs with respect to the words
`[`pɑʔɑmɑnuktis`]`, `[`pɑʔɑmɑnuni`]`, and `[`mɑnuni`]`, which the algorithm fails to assign to the group, as it
fails to detect the partial cognacy with the other words. 

In order to test further, how much the two cognate judgments differ, we make an analysis of the sound correspondence patterns, using the method for sound correspondence pattern detection provided by the LingRex package (described in [List 2019](http://doi.org/10.1162/coli_a_00344)).

Our basic assumption is that correspondence patterns should be more consistent
the better the cognate judgments.  In order to test this, we first align the
data automatically for both the automated and the expert cognate judgments and
then use the LingRex package to compute all correspondence patterns in the
data. 

Correspondence patterns are determined by assigning individual alignment sites (columns in an alignment) to the same cluster. In order to compare two correspondence pattern analyses, we cannot directly compare the number of clusters identified, or the size of the clusters, since the original number of cognate sets and their overall cover varies drastically. As a result, we need to compare the results of this analysis indirectly by computing several additional statistics.

These are provided in the following table, which can be computed by typing:

```
$ python purity.py
```

                             Expert       LexStat
----------------------  -----------  ------------
singletons              1175         1859
cognates                 588          869
patterns                1276          689
regular patterns         656          381
pattern proportion         0.514107     0.552975
sites                   3613         2726
clustered sites          751          404
sites proportion           0.207861     0.148202
purity                     0.534804     0.494849
cognates with patterns   270          229
regular cognates          40           24
regularity                 0.148148     0.104803
coverage                 615          154
coverage proportion        0.118474     0.0296667



The first value, "singletons" points to the number of orphaned words which cannot be assigned to a cognate set. The automated analysis here has a significant amount of those.

The second and third values show the cognate sets, that is, the number of non-singleton cognate sets, as well as the automatically inferred number of correspondence patterns.

We can see that the expert analysis cannot be reduced to as many patterns as the analysis made by the automated approach. When inspecting the proportion of regular patterns (patterns which appear more than once in the data), we can also see that the expert analysis has more different patterns than the automatic analysis, and that the automatic analysis has a slightly higher proportion with respect to "regular" patterns. 
 
This, however, does not mean that the automatic analysis is superior, since it may also indicate that the analysis just picks out those parts in the data which are easiest to explain and leaves the rest unanalyzed. 

This becomes obvious if we inspect number of individual alignment sites in the expert analysis (row "sites") in comparison with the automated analysis. If we furthermore compare the number of sites which qualify to be assigned to a cluster (clustered sites) and the proportion of them, we can see that the expert analysis covers much more data than the automated analsyis. 

The purity is a measure that tests how well the correspondence patterns are "filled", that is, how much evidence we find in the data for a given pattern. Here, the expert analysis shows a higher amount of purity (which ranges between 1 for completely filled patterns and 0). 

Finally, we provide an analysis of the number of cognate sets which are "regular", in the sense that they consist of at least two correspondence patterns which recur at least in one additional cognate set. Here, the number of regular cognate sets is slightly larger for the expert analysis (as well as the proportion), but what is remarkable is that the number of regular cognates covers a much larger proportion of words in the wordlist in the expert analysis than in the automated analysis.

We can thus -- at least for the time being -- conclude that the expert analysis covers more data and yields correspondence patterns which are all in all more regular, covering a higher proportion of words in the sample, than the automated analysis.
