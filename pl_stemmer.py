#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
import optparse

def main(argv):
    parser = optparse.OptionParser()
    black_list_file_location = ''
    blacklist = []
    expected_stem_location = ''
    debug = False
    evaluate = False
    parser.add_option('-f', action="store_true", dest="debug", default=False, help="Debug mode")
    parser.add_option('-e', action="store", dest="expected_stem_location", help="Location of file containing document stemmed by user")
    parser.add_option('-b', action="store", dest="black_list_file_location", help="Location of file containing words not to stem")
    print parser.parse_args()
    options, args = parser.parse_args()
    debug = options.debug
    black_list_file_location = options.black_list_file_location
    expected_stem_location = options.expected_stem_location
    if expected_stem_location:
        evaluate = True
    print "Debug:", debug
    print "Blacklist:", black_list_file_location
    print "ExpectedFile:", expected_stem_location
    expected = None
    lines_parsed = 0
    if black_list_file_location:
        blacklist = get_blacklist(black_list_file_location)
    if evaluate:
        stemmed_good = 0 
        stemmed_bad = 0
        true_positives = 0
        true_negatives = 0
        false_positives = 0
        false_negatives = 0
        expected = get_expected_stem_file(expected_stem_location)
        for line in sys.stdin:
            lines_parsed = lines_parsed + 1
            i = 0
            expected_line = ''
            if expected:
                expected_line = expected.readline()
                
            expected_words = expected_line.split()
            if len(expected_words) != len(line.split()):
                print "Number of words in expected line and stemmed line is different" \
                 "- skipping (line " + str(lines_parsed) + ")"
                print "Skipped line: ", expected_line
                continue
            stemmed_line = ''
            for word in line.split():
                blacklisted = False
                word = word.lower()
                word = word.decode('utf-8')
                if is_in_blacklist(word, blacklist):
                    blacklisted = True
                    """
                    if debug and evaluate:
                        print word + '|' + word + '|' + expected_words[i].lower().decode('utf-8'),
                    elif debug:
                        print word + '|' + word,
                    else:
                        print word,
                    """
                stem = word[:]
                stem = remove_nouns(stem)
                stem = remove_diminutive(stem)
                stem = remove_adjective_ends(stem)
                stem = remove_verbs_ends(stem)
                stem = remove_adverbs_ends(stem)
                stem = remove_plural_forms(stem)
                stem = remove_general_ends(stem)
                if blacklisted:
                    stem = word[:]
                #print stem
                if debug and evaluate:
                    print word + '|' + stem + '|' + expected_words[i].lower().decode('utf-8'),
                elif debug:
                    print word + '|' + stem,
                else:
                    print stem,
                #print '!!!' + stem + ' ' + expected_words[i].decode('utf-8') + '!!!'
                expected_word = expected_words[i].lower().decode('utf-8')
                    
                if expected_word == stem:
                    stemmed_good += 1
                    true_positives += 1
                else:
                    stemmed_bad += 1
                    #false positives - stemmed words which shouldn't be stemmed
                    if expected_word == word:
                        false_positives += 1
                    #false negatives - words not stemmed but should be
                    elif stem == word:
                        false_negatives += 1    
                    else:
                        true_negatives += 1
                i = i + 1
            print ''
        print ''
        print "Good:", stemmed_good, ", bad:", stemmed_bad
        accuracy = float(stemmed_good) / float(stemmed_good + stemmed_bad)
        print "Good / Bad:", accuracy
        print ''
        print "True positives:", true_positives
        print "True negatives:", true_negatives
        print "False positives:", false_positives
        print "False negatives:", false_negatives
        precision = float(true_positives) / float(true_positives + false_positives)
        recall = float(true_positives) / float(true_positives + false_negatives)
        print "Precision:", true_positives, "/ (", true_positives, "+", false_positives, ") =", precision
        print "Recall:", true_positives, "/ (", true_positives, "+", false_negatives, ") =", recall
        accuracy = float(true_positives + true_negatives) / \
            float(true_positives + true_negatives + false_negatives + false_positives)
        print "Accuracy: (", true_positives, '+', true_negatives, ") / (", \
            true_positives, "+", false_negatives, "+", true_negatives, '+', false_positives, ") =", accuracy
    else:
        for line in sys.stdin:
            stemmed_line = ''
            for word in line.split():
                blacklisted = False
                word = word.lower()
                word = word.decode('utf-8')
                if is_in_blacklist(word, blacklist):
                    blacklisted = True
                    """
                    if debug and evaluate:
                        print word + '|' + stem + '|' + expected_words[i].lower().decode('utf-8'),
                    elif debug:
                        print word + '|' + stem,
                    else:
                        print word,
                    """
                stem = word[:]
                stem = remove_nouns(stem)
                stem = remove_diminutive(stem)
                stem = remove_adjective_ends(stem)
                stem = remove_verbs_ends(stem)
                stem = remove_adverbs_ends(stem)
                stem = remove_plural_forms(stem)
                stem = remove_general_ends(stem)
                if blacklisted:
                    stem = word[:]
                #print stem
                if debug:
                    print word + '|' + stem,
                else:
                    print stem,
            print '' 

def get_expected_stem_file(location):
    print 'The file with the prepared stems is located in: ', location
    expected_file = open(location, 'r')
    return expected_file
            
def get_blacklist(location):
    print 'The file with list of words not to stem was named: ' + location
    blacklist_file = open(location, 'r')
    blacklist_list = []
    for line in blacklist_file:
        blacklist_list.append(line.decode('utf-8').strip(' \t\n\r'))
    return blacklist_list
    
def remove_general_ends(word):
    #print "DEBUG: END", word[-1:]
    if len(word) > 4 and word[-2:] in {"ia", "ie"}:
        return word[:-2]
    if len(word) > 4 and word[-1:] in {"u", u"ą", "i", "a", u"ę", "y", u"ę", u"ł"}:
        return word[:-1]
    return word
    
def remove_diminutive(word):
    if len(word) > 6:
        if word[-5:] in {"eczek", "iczek", "iszek", "aszek", "uszek"}:
            return word[:-5]
        if word[-4:] in {"enek", "ejek", "erek"}:
            return word[:-2]
    if len(word) > 4:
        if word[-2:] in {"ek", "ak"}:
            return word[:-2]
    return word
    
def remove_verbs_ends(word):
    if len(word) > 5 and word.endswith("bym"):
        return word[:-3]
    if len(word) > 5 and word[-3:] in {"esz", "asz", "cie", u"eść", u"aść", u"łem", "amy", "emy"}:
        return word[:-3]
    if len(word) > 3 and word[-3:] in {"esz", "asz", u"eść", u"aść", u"eć", u"ać"}:
        return word[:-2]
    if len(word) > 3 and word[-3:] in {"aj"}:
        return word[:-1]
    if len(word) > 3 and word[-2:] in {u"ać", "em", "am", u"ał", u"ił", u"ić", u"ąc"}:
        return word[:-2]
    return word

def remove_nouns(word):
    if len(word) > 7 and word[-5:] in {"zacja", u"zacją", "zacji"}:
        return word[:-4]
    if len(word) > 6 and word[-4:] in {"acja", "acji", u"acją", "tach", "anie", "enie",
    "eniu", "aniu"}:
        return word[:-4]
    if len(word) > 6 and word.endswith("tyka"):
        return word[:-2]
    if len(word) > 5 and word[-3:] in {"ach", "ami", "nia", "niu", "cia", "ciu"}:
        return word[:-3]
    if len(word) > 5 and word[-3:] in {"cji", "cja", u"cją"}:
        return word[:-2]
    if len(word) > 5 and word[-2:] in {"ce", "ta"}:
        return word[:-2]
    return word
    
def remove_adjective_ends(word):
    if len(word) > 7 and word.startswith("naj") and (word.endswith("sze")
    or word.endswith("szy")):
        return word[3:-3]
    if len(word) > 7 and word.startswith("naj") and word.endswith("szych"):
        return word[3:-5]
    if len(word) > 6 and word.endswith("czny"):
        return word[:-4]
    if len(word) > 5 and word[-3:] in {"owy", "owa", "owe", "ych", "ego"}:
        return word[:-3]
    if len(word) > 5 and word[-2:] in {"ej"}:
        return word[:-2]
    return word
    
def remove_adverbs_ends(word):
    if len(word) > 4 and word[:-3] in {"nie", "wie"}:
        return word[:-2]
    if len(word) > 4 and word.endswith("rze"):
        return word[:-2]
    return word

def remove_plural_forms(word):
    if len(word) > 4 and (word.endswith(u"ów") or word.endswith("om")):
        return word[:-2]
    if len(word) > 4 and word.endswith("ami"):
        return word[:-3]
    return word
    
def is_in_blacklist(word, blacklist):
    if word in blacklist:
        return True
    return False
    
        
if __name__ == "__main__":
    main(sys.argv[1:])

