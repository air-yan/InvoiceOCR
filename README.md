# Invoice-Receipt-OCR
This project aims to automate the receipt/invoice parsing process.


## Installation and Prerequisite

### Python Modules
```python
# to add rating for text extraction process
pip install python-Levenshtein

# images and preprocessing
pip install Wand
pip install opencv-python

# ocr engine
pip install pytesseract

# PDF text extraction tool
pip install pdfminer.six

# other modules for testing purposes
pip install pandas
pip install tabulate
```
### Environments
- Microsoft Visual C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Tesseract: https://github.com/tesseract-ocr/tesseract/wiki
- imagemagik: https://imagemagick.org/script/download.php

If you are using windows, you should set PATH for imagemagik and tesseract.

## TODO

- Reconstruct the codes into py files √
- Make the codes clean √
- Add testing codes
  - add txt log output
  - add pandas Excel output
  - read the correct result
- Add License √
- Functions to add:
  - amount √
  - invoice #
  - bill date vs due date
  - address
  - vendor name
- Add three OCR loops for diff parameters
- Optimize your rating process
