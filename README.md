# Python Logic Minimizer

This is a script that minimizes boolean algebra expressions using the minterms/maxterms (and any don't cares) of a given expression.

To run, install python 3.6 (may work on older version of 3.x, but untested), and run `python minimizer.py` in a console window.

Currently, the minimizer only supports minimization from minterms and maxterms, but I'd like to implement an expression parser that can parse and minimize, at the very least, expressions in sum of products form.

Other TODOs include printing K-maps for up to 6 variable instructions.

The algorithms used in this script are the  [Quine-McCluskey algorithm](https://en.wikipedia.org/wiki/Quine%E2%80%93McCluskey_algorithm) to get essential prime implicants, and [Petrick's method](https://en.wikipedia.org/wiki/Petrick%27s_method) in order to find possible minimizations to cover the rest of the function.
