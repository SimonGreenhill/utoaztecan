# Analyzing Cognate Decisions

In order to carry out the automated cognate detection analysis using LingPy, please make sure that you have installed the most recent version of LingPy, which you can install easily with the help of `pip`:

```
$ pip install lingpy
```

Make also sure to install [python-igraph](https://igraph.org), which will require to install the general igraph library first (igraph is used for clustering cognates).

In addition, you need `cltoolkit`, which you can install from GitHub:

```
$ git clone https://github.com/cldf/cltoolkit.git
$ pip install -e ./
```

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
* Precision:     0.9523 *
* Recall:        0.5831 *
* F-Scores:      0.7234 *
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
utoaztecan-Kawaiisu            	monojo      	   4	   4
utoaztecan-SouthernPaiute      	mano        	   4	   4
utoaztecan-SouthernUte         	pɑʔɑmɑnuni  	   4	   4
utoaztecan-SouthernPaiute      	manu        	   4	   4
utoaztecan-SouthernUte         	mɑnuni      	   4	   4
utoaztecan-SouthernUte         	pɑʔɑmɑnuktis	   4	  44
utoaztecan-Comanche            	ojɯ         	   6	   6
utoaztecan-ShoshoniGosiute     	ojoːn       	   6	   6
utoaztecan-Comanche            	ojo         	   6	   6
utoaztecan-Pannamint           	ojoːntɯ     	   6	   6
utoaztecan-Pannamint           	ojoːntɯsɯ   	   6	   6
utoaztecan-NorthernPaiute      	noːʔju      	   6	  19
utoaztecan-Cora                	heitse      	   7	   7
utoaztecan-Cupeno              	pətɑ̠ʔɑmɑ   	   8	   8
utoaztecan-Eudeve              	awona       	   9	   9
utoaztecan-Eudeve              	haona       	   9	   9
utoaztecan-Gabrielino          	owɑ̠̄ʔix    	  10	  10
utoaztecan-Guarijio            	joma        	  11	  11
utoaztecan-Hopi                	sosojɑm     	  12	  12
utoaztecan-Hopi                	sosoj       	  12	  12
utoaztecan-Huichol             	naitɯ       	  13	   1
utoaztecan-Huichol             	junaitɯ     	  13	   1
utoaztecan-Huichol             	nai         	  13	   1
utoaztecan-Kitanemuk           	puju        	  15	  15
utoaztecan-Serrano             	puju        	  15	  15
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
utoaztecan-SanJuanPuebloTewa   	tʲɛ̃hkih    	  26	  26
utoaztecan-Tarahumara          	omɑrwɑme    	  32	  32
utoaztecan-Tubatulabel         	piniju      	  34	  34
utoaztecan-ClassicalAztec      	iːxkitʃ     	  46	  46
utoaztecan-Pannamint           	sɯmɯsɯ      	  50	  18
```

The first column in this file is the language identifier, the second column gives the word form (without spaces segmenting sounds to make the output more compact), the third column provides the experts' judgments, which have been renumbered consecutively, and the fourth column provides the automated cognate judgments, which have also been renumbered, to allow for a quick comparison.

In this example, we can see that the experts identify the first five words as cognates, while the algorithm splits them into two sets, one representing words starting with `[`n`]` the other words starting with `[`m`]`. 

Cognate set 4 in the example only differs with respect to the word
`[`pɑʔɑmɑnuktis`]`, which the algorithm fails to assign to the group, as it
fails to detect the partial cognacy with the other words. 

