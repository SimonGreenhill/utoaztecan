import json
from pathlib import Path

import attr
from clldutils.misc import slug

import pylexibank
from pylexibank import Dataset as BaseDataset
from pylexibank import Language as BaseLanguage
from pylexibank import Lexeme as BaseLexeme

# Cognacy details:
#
# 1) ? means missing data
#
# 2) SL means Spanish loan which should always be treated as unique
#
# 3) EL means English loan which should always be treated as unique
#
# 4) 1? Means the cognate 1 is speculative and should be treated as unique for most analyses (or,
# in all likelihood, all analyses)
#
# 5) L1, L1 means “loan” such that the common ancestor of these two languages borrowed the word, so
# should be treated as cognate. (When recoding don’t accidentally recode “1” and “L1” as being
# cognate with each other)
#
# 6) L1, L2 means “loan” such that the word was loaned independently, so should not be treated as
# cognate
#
# 7) L is an old code for “loan” and is an error. Please let me know if you find an L and I will
# correct it


@attr.s
class Language(BaseLanguage):
    DatabaseID = attr.ib(default=None)


@attr.s
class Lexeme(BaseLexeme):
    Annotation = attr.ib(default=None)
    Loan = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "utoaztecan"
    writer_options = dict(keep_languages=False, keep_parameters=False)
    language_class = Language
    lexeme_class = Lexeme

    # define the way in which forms should be handled
    form_spec = pylexibank.FormSpec(
        brackets={"(": ")"},  # characters that function as brackets
        separators=";/,",  # characters that split forms e.g. "a, b".
        missing_data=("?", "-"),  # characters that denote missing data.
        replacements=[("*", ""), ("$", "s")],  # characters to replace
        strip_inside_brackets=True,  # do you want data removed in brackets or not?
    )

    def cmd_download(self, args):
        pass

    def cmd_makecldf(self, args):
        
        args.writer.add_sources()
        
        languages = args.writer.add_languages(lookup_factory=lambda l: l["DatabaseID"])
        
        concepts = args.writer.add_concepts(
            id_factory=lambda w: '%s_%s' % (w.id.split("-")[-1], slug(w.english)),
            lookup_factory=lambda w: w["ID"].split("_")[0],
        )
        
        sources = {s["ID"]: s["Key"] for s in self.etc_dir.read_csv("sources.csv", dicts=True)}

        jsonfiles = [j for j in self.raw_dir.iterdir() if j.suffix == ".json"]
        for jsonfile in sorted(jsonfiles):
            data = json.loads(jsonfile.read_text("utf8"))
            language = languages[data["language"]["id"]]

            for d in data["lexicon"]:
                if d["item"] == "?":
                    continue
                
                # patch concepts as original dataset is missing item 109 and this is not in 
                # the concepticon list ...which means that if the word_id value in the dataset
                # is 109+, then it needs to be decreased by one to match the concepts in
                # concepticon
                word_id = int(d['word_id'])
                if word_id >= 109:
                    parameter_id = concepts[str(word_id - 1)]
                else:
                    parameter_id = concepts[str(word_id)]

                # handle cognacy and loan markers in cognacy column
                loan = d["loan"] if d["loan"] else False
                cogid = None
                if d["cognacy"]:
                    # handle missing data
                    if d["cognacy"] == "?":
                        cogid = None
                    # handle loans
                    elif d["cognacy"] in ("SL", "EL", "L1", "L2", "L?"):
                        loan, cogid = True, None
                    # remove speculative cognates
                    elif "?" in d["cognacy"]:
                        cogid = None
                    # everything else
                    else:
                        cogid = "%s-%s" % (parameter_id, d["cognacy"])

                bibkey = sources.get(d["source_id"], None)
                
                lex = args.writer.add_forms_from_value(
                    ID=d["id"],
                    Local_ID=d["id"],
                    Language_ID=language,
                    Parameter_ID=parameter_id,
                    Value=d["item"],
                    Source=bibkey,
                    Annotation=d["annotation"],
                    Loan=loan,
                    Cognacy=cogid,
                )
                for l in lex:
                    args.writer.add_cognate(lexeme=l, Cognateset_ID=cogid)
