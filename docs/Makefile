
GH_PAGES_SOURCES = source sphinx.make ../nautilus

gh-pages:
	git checkout gh-pages ; \
	git checkout master $(GH_PAGES_SOURCES) ; \
	git reset HEAD ; \
	make html -f ./sphinx.make ; \
	mv build/html/* .. ; \
	cd .. ; \
	git add -am "Updated documentation" ; \
	git push origin gh-pages;

	rm -rf $(GH_PAGES_SOURCES) build

all: gh-pages
