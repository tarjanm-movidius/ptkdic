
PREFIX := /usr
INSTDIR := $(PREFIX)/share/ptkdic
SRCS := dic.py \
	unichar.py
DBS := wlam_trie.pgz \
	wlma_trie.pgz \
	wlde_trie.pgz \
	wled_trie.pgz \
	wlmn_trie.pgz \
	wlnm_trie.pgz \

all:
	@echo -n "Python version: "
	@python3 -c 'import platform; print(platform.python_version())'
	python3 -OO -m compileall -b *.py

clean:
	@rm -fv *.pyc

install: all
	@mkdir -vp $(INSTDIR)/lang
	@for i in $(SRCS); do cp -fv $${i}c $(INSTDIR); done
	@cp -iv $(DBS) $(INSTDIR)/lang
	chmod -R a+w $(INSTDIR)/lang
	$(info Add to /etc/bash/bashrc.d/aliases or ~/.bashrc:)
	$(info alias am='python3 $(INSTDIR)/dic.pyc am')
	$(info alias ma='python3 $(INSTDIR)/dic.pyc ma')
	$(info alias de='python3 $(INSTDIR)/dic.pyc de')
	$(info alias ed='python3 $(INSTDIR)/dic.pyc ed')
	$(info alias mn='python3 $(INSTDIR)/dic.pyc mn')
	$(info alias nm='python3 $(INSTDIR)/dic.pyc nm')

uninstall:
	@for i in $(DBS); do rm -fv $(INSTDIR)/lang/$$i; done
	@for i in $(SRCS); do rm -fv $(INSTDIR)/$${i}c; done
	@rmdir -v $(INSTDIR)/lang $(INSTDIR) || true
