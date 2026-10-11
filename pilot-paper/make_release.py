import json, os, re, zipfile
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
tex = open("pilot-paper/main.tex", encoding="utf-8").read()
ab = tex.split(r"\begin{abstract}")[1].split(r"\end{abstract}")[0].strip()
ab = ab.replace(r"$\eps$", "ε").replace(r"\emph{", "").replace("}", "").replace("~", " ").replace(r"\%", "%").replace(r"\$", "$").replace("$", "")
meta = {"metadata": {
    "title": "Interfaces or Bodies? A 24-Instance Pilot Measurement of ε-Sufficient Context for Language-Model Code Editing in Go",
    "upload_type": "publication", "publication_type": "report", "publication_date": "2026-10-11", "description": "<p>" + ab + "</p>",
    "creators": [{"name": "Johansen, Jude Castiel", "affiliation": "Shockware Limited, independent researcher", "orcid": "0009-0002-5644-3073"}],
    "access_right": "open", "license": "cc-by-4.0",
    "keywords": ["context sufficiency", "language model code editing", "SuffBench", "Go", "prompt length", "interfaces", "pilot study"],
    "related_identifiers": [{"identifier": "10.5281/zenodo.23282195", "relation": "isSupplementTo", "scheme": "doi"},
                            {"identifier": "10.5281/zenodo.23282863", "relation": "references", "scheme": "doi"},
                            {"identifier": "https://github.com/Shockware-Limited/suffbench", "relation": "isSupplementedBy", "resource_type": "software", "scheme": "url"}],
    "version": "0.1.1-pilot", "language": "eng", "contributors": [{"name": "Shockware Limited", "type": "HostingInstitution"}],
    "notes": "Exploratory pilot on one repository and two models; it fixes the design of a preregistered study and makes no confirmatory claim. The data zip includes instances, the mining log, the harness and all verdict records."}}
json.dump(meta, open("pilot-paper/zenodo-metadata.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
import shutil; shutil.copy("pilot-paper/main.pdf", "pilot-release/paper/main.pdf"); shutil.copy("pilot-paper/main.tex", "pilot-release/paper/main.tex")
z = "pilot-paper/suffbench-pilot-v0.1.1.zip"
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, _, files in os.walk("pilot-release"):
        for f in files: zf.write(os.path.join(root, f), os.path.relpath(os.path.join(root, f), "."))
print("metadata + zip ok", round(os.path.getsize(z) / 1e6, 2), "MB")
