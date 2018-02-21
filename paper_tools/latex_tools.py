import os
import paper_tools
import bibtexparser
from paper_tools import general_tools as gt


def build_base_folders(base_path, root_folder_name, initials, author=""):
    # Create folder for latex work
    latex_path = "%s%s_paper/" % (base_path, initials)
    gt.build_folder(latex_path, "Latex")
    # Create images folder and figures folder
    images_path = "%s%s-images/" % (latex_path, initials)
    gt.build_folder(images_path, "Images")
    figures_path = "%s%s-figures/" % (latex_path, initials)
    gt.build_folder(figures_path, "Figures")
    # Copy base .svg file into image folder

    # Copy latex file into location

    template_ffp = gt.get_template_ffp('base-paper.tex')
    a = open(template_ffp)
    f_str = a.read()
    a.close()
    f_str = f_str.replace("###TITLE###", root_folder_name)
    f_str = f_str.replace("###AUTHOR###", author)
    # Add example .svg file into latex
    latex_file_name = "%s-paper.tex" % initials
    out_ffp = latex_path + latex_file_name
    ofile = open(out_ffp, "w")
    ofile.write(f_str)
    ofile.close()


def find_references(fn):
    """
    Creates a cite key based on a function, or object or method.
    :param fn: function, object or method
    :return:
    """
    full_docstring = fn.__doc__
    ds_lines = full_docstring.split("\n")
    for line in ds_lines:
        if ".. [1]" in line:
            print(line)


def find_equations(fn):
    """
    Creates a latex equation based on a function, or object or method.
    :param fn: function, object or method
    :return:
    """
    full_docstring = fn.__doc__
    ds_lines = full_docstring.split("\n")
    for line in ds_lines:
        if ".. math" in line:
            print(line)


def combine_bibtex(bibtex_ffp1, bibtex_ffp2):
    """
    Reads a latex file and extracts the cite keys then finds
     the references in a large bibtex file and writes a new bibtex file
     with just the required references.
    :param ffp:
    :return:
    """

    with open(bibtex_ffp1) as bibtex_file:
        bibtex_database = bibtexparser.load(bibtex_file)

    with open(bibtex_ffp2) as org_bibtex_file:
        org_bibtex_database = bibtexparser.load(org_bibtex_file)

    for entry in bibtex_database.entries_dict:
        if entry not in org_bibtex_database.entries_dict:
            print("Not found: ", entry)
        # else:
        #     print('found')
        # print(entry, bibtex_database.entries_dict[entry])


def compile_bibtex(citations, big_bibtex_ffp):
    """
     finds the bibtex entries that correspond to a list of cite keys,
     from a large bibtex file and writes a new bibtex file
     with just the required references.
     :param citations: a list of citation keys.
    :param big_bibtex_ffp: full file path to bibtex file
    :return:
    """

    remove_keys = ["annote", "date-added", "date-modified", "local-url", "file", "rating", "month", "uri", "read"
                   "abstract"]

    with open(big_bibtex_ffp) as org_bibtex_file:
        org_bibtex_database = bibtexparser.load(org_bibtex_file)

    new_bibtex_db = bibtexparser.loads("")  # create a new bibtex DB obj
    for entry in citations:
        if entry not in org_bibtex_database.entries_dict:
            print("Not found: ", entry)
        else:
            new_bibtex_db.entries.append(org_bibtex_database.entries_dict[entry])
            # new_bibtex_db.entries_dict[entry['ID']] = org_bibtex_database.entries_dict[entry]

    # new_bibtex_db = copy.deepcopy(org_bibtex_database)
    # for entry in org_bibtex_database.entries_dict:
    #     if entry not in citations:
    #         print("Not found: ", entry)
    #         del new_bibtex_db.entries_dict[entry]
    #     else:
    #         print("adding: ", entry)
    #         new_bibtex_db.entries_dict[entry] = org_bibtex_database.entries_dict[entry]

    # print(new_bibtex_db.entries)

    for entry in new_bibtex_db.entries_dict:
        for r_key in remove_keys:
            if r_key in new_bibtex_db.entries_dict[entry]:
                del new_bibtex_db.entries_dict[entry][r_key]
    bibtex_str = bibtexparser.dumps(new_bibtex_db)
    return bibtex_str


def extract_citation_keys_from_latex(latex_ffp, chicago=True):
    """
    Reads a latex file and returns a list of cite keys used.
    :param latex_ffp: full file path to latex file
    :return:
    """
    citations = []
    import regex
    import re
    a = open(latex_ffp)
    lines = a.readlines()
    matches = []
    for line in lines:

        matches += re.findall('\\cite\{([^\},]+)(?:,\s*([^\},]+))*\}', line)
        matches += re.findall('\\citep\{([^\},]+)(?:,\s*([^\},]+))*\}', line)
        matches += re.findall('\\citet\{([^\},]+)(?:,\s*([^\},]+))*\}', line)
        if chicago:
            matches += re.findall('\\citeN\{([^\},]+)(?:,\s*([^\},]+))*\}', line)
            matches += re.findall('\\citeNP\{([^\},]+)(?:,\s*([^\},]+))*\}', line)
            matches += re.findall('\\shortcite\{([^\},]+)(?:,\s*([^\},]+))*\}', line)
            matches += re.findall('\\shortciteN\{([^\},]+)(?:,\s*([^\},]+))*\}', line)
            matches += re.findall('\\shortciteNP\{([^\},]+)(?:,\s*([^\},]+))*\}', line)

    for m in matches:
        new_cite = m[0]
        if new_cite not in citations:
            citations.append(new_cite)

    return citations


if __name__ == '__main__':
    ffp = "../tests/test_data_files/sample_latex.tex"
    full_bibtex_ffp = "../tests/test_data_files/sample.bib"
    citations = extract_citation_keys_from_latex(latex_ffp=ffp)
    print(citations)

    bstr = compile_bibtex(citations, full_bibtex_ffp)
    print(bstr)

