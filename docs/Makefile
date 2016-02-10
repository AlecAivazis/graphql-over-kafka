
GH_PAGES_SOURCES = source sphinx.make ../nautilus

gh-pages:
	git checkout gh-pages ; \
	git checkout master $(GH_PAGES_SOURCES) ; \
	git reset HEAD ; \
	make html -f ./sphinx.make ; \
	rsync -av build/html/ .. ; \
	rm -rf $(GH_PAGES_SOURCES) build ; \
	git add .. ; \
	git commit -m "Updated documentation"
	git push origin gh-pages; \
	git checkout master

local: clean
	make html -f ./sphinx.make

clean:
	make clean -f ./sphinx.make

all: gh-pages
