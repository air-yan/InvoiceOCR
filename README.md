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

# PDF text extraction tool -> not required for now
pip install pdfminer.six

```
### Environments
- Microsoft Visual C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Tesseract: https://github.com/tesseract-ocr/tesseract/wiki
- imagemagik: https://imagemagick.org/script/download.php
- python 3 +

If you are using windows, you should set PATH for imagemagik and tesseract.

## TODO

- Add testing codes
- Core Functions:
  - amount
  - invoice #
  - bill date vs due date
  - address
  - vendor name
- Optimize your rating process
