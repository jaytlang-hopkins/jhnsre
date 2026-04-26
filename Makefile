BUILDDIR := build
SRC := analysis.ipynb
TEX := $(BUILDDIR)/$(SRC:.ipynb=.tex)
PDF := $(SRC:.ipynb=.pdf)
ZIP := $(PDF:.pdf=.zip)

TITLE := $(shell basename "$(PWD)")

TEXFLAGS := -no-shell-escape -halt-on-error

.PHONY: all dist pdf clean
.DELETE_ON_ERROR:

all: dist
dist: $(ZIP)
pdf: $(PDF)

$(ZIP): $(PDF)
	zip -r $@ ./* -x "$(BUILDDIR)/*" "env/*" "$@"

$(PDF): $(TEX)
	pdflatex $(TEXFLAGS) -output-directory=$(BUILDDIR) $(TEX)
	mv $(BUILDDIR)/$@ .

$(TEX): $(SRC) | $(BUILDDIR)
	jupyter nbconvert --to latex $< --output-dir $(BUILDDIR)
	sed -i '' 's|\\title{.*}|\\title{$(TITLE)}\n\\author{Jay Lang}|' $(TEX)

$(BUILDDIR):
	mkdir -p $@

clean:
	rm -rf $(BUILDDIR) $(PDF) $(ZIP)

