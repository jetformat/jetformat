# Practical Jetformat workflows

[Home](../README.md) · [中文](../README.zh-CN.md) · [Full command reference](https://jetformat.com/docs/models)

Examples assume the input files exist. Quote paths with spaces. Use `-o` to choose the output; add `--force` only when you intend to overwrite an existing file. Converting, rendering, and writing require sign-in and credits.

## Convert Office documents

```bash
jetformat word to-pdf "contract.docx" -o "output/contract.pdf"
jetformat excel to-pdf "workbook.xlsx" -o "output/workbook.pdf"
jetformat ppt to-pdf "slides.pptx" -o "output/slides.pdf"
```

Excel includes visible worksheets in workbook order. For consistent layout, provide the fonts your document uses.

## Convert PDF back to Word

```bash
jetformat pdf to-word report.pdf -o report.docx
```

`to-word` is an alias of `to-docx`. It reconstructs an editable document from a PDF text layer. Scans need OCR elsewhere; complex layouts may not reconstruct exactly.

## Read documents as text, Markdown, or JSON

```bash
jetformat text report.docx -o report.txt
jetformat text report.docx --format markdown
jetformat text workbook.xlsx --format json
jetformat text slides.pptx --format markdown
jetformat text report.pdf --format markdown
```

Markdown is useful for an agent's context; JSON is useful for scripts. Extraction does not perform OCR. Reading is free and does not require login.

## Inspect and validate before processing

```bash
jetformat validate report.docx
jetformat word inspect report.docx --json
jetformat excel inspect workbook.xlsx --json
jetformat ppt inspect slides.pptx --json
jetformat pdf info report.pdf --json
```

## Fill a Word template

```bash
# Match a content control by Tag or Alias.
jetformat word template template.docx --set customer="Acme Corp" -o contract.docx

# Fill a MERGEFIELD by name.
jetformat word mail-merge letter.docx --set Customer="Acme Corp" -o filled-letter.docx
```

These commands operate on an existing document prepared with the corresponding content controls or merge fields.

## Read or change a spreadsheet cell

```bash
jetformat excel get finance.xlsx --sheet Summary --cell B12
jetformat excel set finance.xlsx --sheet Summary --cell A1 --value 5 -o updated.xlsx
jetformat excel to-pdf updated.xlsx -o updated.pdf
```

## Reorder a slide

```bash
jetformat ppt reorder slides.pptx --from 1 --to 3 -o reordered.pptx
jetformat ppt to-pdf reordered.pptx -o reordered.pdf
```

## Merge, extract, and preview PDFs

```bash
jetformat pdf merge cover.pdf report.pdf -o combined.pdf
jetformat pdf extract combined.pdf --pages 2-5 -o chapter.pdf
jetformat pdf render combined.pdf --pages 1,3-5,last --width 1600 -o preview
```

Page numbers start at 1. `pdf extract` accepts a contiguous range (`2-5`, `5-last`, or `all`). `pdf render` also accepts lists and writes images such as `preview/page-0001.png`.

## Batch conversion in a shell

```bash
mkdir -p output
for file in ./*.docx; do
  [ -f "$file" ] || continue
  name=$(basename "$file" .docx)
  jetformat word to-pdf "$file" -o "output/$name.pdf" || break
done
```

This runs one document per command and stops on the first conversion error. Each conversion uses credits.

## Discover more commands

```bash
jetformat --help
jetformat word --help
jetformat excel --help
jetformat ppt --help
jetformat pdf --help
jetformat word to-pdf --help
```

Advanced commands and HTML renderer configuration are covered in the [full command reference](https://jetformat.com/docs/models).
