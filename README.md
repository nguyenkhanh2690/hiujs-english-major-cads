# HIUJS English Major CADS Reproducibility Repository

This repository accompanies the study **“Promoting the English Major: Employability and Internationalisation on Vietnamese University Websites.”**

## Contents

- `code/` — executable Python analysis scripts.
- `lexicons/` — frozen multiword lexicon, stopwords, and thematic dictionaries.
- `metadata/` — institution-level source metadata, including the dominant source genre, page/section selections, source formats, URLs/archived-source identifiers, word/token counts, corpus statistics, and checksums/provenance fields.
- `derived_outputs/` — frequency, keyness, collocation, concordance, university-level thematic, and comparison outputs.
- `validation/` — revised statistical outputs, full leave-one-institution-out runs, document-length sensitivity analysis, OCR quality-control source data, and Figure 1 data.
- `supplementary/` — reviewer-support files, including the thematic dictionaries, sensitivity analyses, OCR quality control, and the former Appendix A institution table moved out of the manuscript to comply with the Journal's no-appendix requirement.
- `logs/` — execution log.
- `requirements.txt` — Python package requirements.

## Corpus profile

- 40 university documents: 20 public and 20 private.
- Corpus freeze date: 12 July 2026.
- 101,210 cleaned orthographic word forms.
- 79,295 analytical tokens after study-specific Vietnamese multiword processing.
- 54,530 filtered content tokens for the shared lexical-profile analysis.

## OCR

Nine image-based PDFs lacking usable embedded text layers were processed with Tesseract OCR 5.5.0 using Vietnamese recognition (`vie`), OEM 1, and PSM 3. A quality check used one manually verified passage from each OCR-derived document (824 reference characters total), yielding an overall normalised CER of 1.09% (document-level sample range 0.00%–3.52%). See `supplementary/Supplementary_Table_S3_OCR_Quality_Control.csv`.

## Statistical verification

Install Python 3.13 or a compatible Python 3 environment and the packages in `requirements.txt`, then run:

```bash
python code/reproduce_revision_statistics.py
```

The script reads `derived_outputs/theme_by_university.csv` and writes the revised Table 4, document-length-trimmed sensitivity results, leave-one-institution-out results, sensitivity summary, and Figure 1 source data to `validation/`.

## Source-text access

Complete copied institutional texts are not redistributed because the underlying documents remain the property of their respective universities. `metadata/institution_metadata.csv` provides all 40 institutions with ownership, dominant source genre, official source URLs, selected pages/sections, archived-source identifiers/paths, source formats, orthographic-word and analytical-token counts, and hashes for traceability. The concise five-column institution table that previously appeared as Appendix A is preserved verbatim as `supplementary/Former_Appendix_A_Sampled_Institutions_and_Corpus_Metadata.csv`.

## Supplementary tables

- `supplementary/Supplementary_Table_S1_Thematic_Dictionaries.csv`
- `supplementary/Supplementary_Table_S2_Sensitivity_Analyses.csv`
- `supplementary/Supplementary_Table_S3_OCR_Quality_Control.csv`
- `supplementary/Former_Appendix_A_Sampled_Institutions_and_Corpus_Metadata.csv` — former manuscript Appendix A, relocated to the repository under the Journal's no-appendix requirement.
