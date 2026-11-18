.PHONY: all examples cv clean
.DEFAULT_GOAL := cv

EXAMPLES_DIR = examples
CV_SRCS = $(wildcard $(EXAMPLES_DIR)/cv/*.tex)
CV_ASSETS = awesome-cv.cls fontawesome.sty $(wildcard fonts/*)
LATEXMK ?= latexmk

all examples: cv

cv: $(EXAMPLES_DIR)/cv.pdf

$(EXAMPLES_DIR)/cv.pdf: $(EXAMPLES_DIR)/cv.tex $(CV_SRCS) $(CV_ASSETS)
	cd $(EXAMPLES_DIR) && $(LATEXMK) -xelatex -file-line-error -halt-on-error -interaction=nonstopmode cv.tex

clean:
	cd $(EXAMPLES_DIR) && $(LATEXMK) -c cv.tex
