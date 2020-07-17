#!/bin/bash

die () { echo "ERROR: $*" >&2; exit 2; }

for cmd in pdoc3; do
    command -v "$cmd" >/dev/null ||
        die "Missing $cmd; \`pip install $cmd\`"
done

PACKAGE="plottools"
PACKAGEROOT="$(dirname "$(realpath "$0")")"
BUILDROOT="$PACKAGEROOT/site"

echo
echo "Clean up documentation of $PACKAGE"
echo

mkdir -p "$BUILDROOT"
rm -r "$BUILDROOT/$PACKAGE" 2> /dev/null || true

echo
echo "Building general documentation for $PACKAGE"
echo

cd "$PACKAGEROOT"
mkdocs build --config-file .mkdocs.yml --site-dir "$BUILDROOT" 
cd - > /dev/null

echo
echo "Building API reference docs for $PACKAGE"
echo

cd "$PACKAGEROOT"
pdoc3 --html --output-dir "$BUILDROOT/api-tmp" $PACKAGE
mv "$BUILDROOT/api-tmp/$PACKAGE" "$BUILDROOT/api"
rmdir "$BUILDROOT/api-tmp"
cd - > /dev/null

echo
echo "Done. Docs in:"
echo
echo "    file://$BUILDROOT/index.html"
echo
