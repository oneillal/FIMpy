#!/bin/bash
gitbook build
cd _book
git init
git remote add upstream git@github.com:oneillal/FIMpy.git
git fetch upstream
git reset upstream/gh-pages
touch .
rev=$(git rev-parse --short HEAD)
echo $rev
git add -A .
git commit -a -m "Rebuild gitbook pages at ${rev}"
git push -q upstream HEAD:gh-pages
