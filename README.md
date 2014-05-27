pl_stemmer
==========

A very simple python stemmer for Polish language based on Porter's Algorithm

The result is the stemmed text od user's given input

It is possible to give a path to a file which contains a text manually stemmed by the user in order to evaluate the algorithm.

Usage: python find_abbreviations.py [-f file_with_list_of_abbreviations] [-s]

    -e    Path to the file which contains text which users expects to be the result of algorithm. Also evaluates the algorithm.
          Every abbreviation should be placed in a new line
    -b    Path to the file which contains words which should not be stemmed by the algorithm.
    -f    Debug mode - shows output with original word. If '-e' flag is given, prints texts in format: original|stemmed|expected
