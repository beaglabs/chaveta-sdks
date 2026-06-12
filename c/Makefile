CC ?= gcc
CFLAGS = -Wall -Wextra -std=c11 -O2
LDFLAGS = -lcurl

INCDIR = include
SRCDIR = src
BUILDDIR = build

all: $(BUILDDIR)/librobolytics.a

$(BUILDDIR)/client.o: $(SRCDIR)/client.c
	@mkdir -p $(BUILDDIR)
	$(CC) $(CFLAGS) -I$(INCDIR) -c $< -o $@

$(BUILDDIR)/librobolytics.a: $(BUILDDIR)/client.o
	ar rcs $@ $^

install: $(BUILDDIR)/librobolytics.a
	cp $(BUILDDIR)/librobolytics.a /usr/local/lib/
	cp $(INCDIR)/robolytics/client.h /usr/local/include/robolytics/

clean:
	rm -rf $(BUILDDIR)

.PHONY: all install clean
