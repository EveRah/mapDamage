#!/usr/bin/env python

import mapdamage
import sys
import collections
from mapdamage.version import __version__


class recursivedefaultdict(collections.defaultdict):
  def __init__(self):
    self.default_factory = type(self) 



def initializeMut(tab, ref, lg):
    
  tab = recursivedefaultdict() 
  for contig in ref:
    for end in ('5p','3p'):
      for std in ('+','-'):
        for mut in mapdamage.seq.header:
          tab[contig][end][std][mut] = collections.defaultdict(int)
  
  return(tab)

def printMut(mut, op, out):
  # print header
  out.write("# table produced by mapDamage version %s\n" % __version__)
  out.write("# using mapped file %s and %s as reference file\n" % (op.filename, op.ref))
  out.write("# Chr: reference from sam/bam header, End: from which termini of DNA sequences, Std: strand of reads\n")
  out.write("Chr\tEnd\tStd\tPos\t%s\t%s\n" % ("\t".join(mapdamage.seq.letters),"\t".join(mapdamage.seq.mutations)))
  for ref in sorted(mut):
    for end in mut[ref].keys():
      for std in mut[ref][end].keys():
        for i in range(op.length):
          out.write("%s\t%s\t%s\t%d" % (ref, end, std, i+1))
          for mis in mapdamage.seq.header:
            out.write("\t%d" % mut[ref][end][std][mis][i])
          out.write("\n")


def initializeComp(tab, ref, around,lg):
    
  tab = recursivedefaultdict() 
  for contig in ref:
    for end in ('5p','3p'):
      for std in ('+','-'):
        for letters in mapdamage.seq.letters:
          tab[contig][end][std][letters] = collections.defaultdict(int)

  return(tab)


def printComp(comp, op, out):

  out.write("# table produced by mapDamage version %s\n" % __version__)
  out.write("# using mapped file %s and %s as reference file\n" % (op.filename, op.ref))
  out.write("# Chr: reference from sam/bam header, End: from which termini of DNA sequences, Std: strand of reads\n")
  out.write("Chr\tEnd\tStd\tPos\t%s\n" % ("\t".join(mapdamage.seq.letters)))
  for ref in sorted(comp):
    for end in comp[ref]:
      for std in comp[ref][end]:
        if end == '5p':
          for i in range((-1*op.around), (op.length+1)):
            if i == 0:
              continue
            out.write("%s\t%s\t%s\t%d" % (ref, end, std, i))
            for base in mapdamage.seq.letters:
              out.write("\t%d" % comp[ref][end][std][base][i])
            out.write("\n")
        else:
          for i in range((-1*op.length), (op.around+1)):
            if i == 0:
              continue
            out.write("%s\t%s\t%s\t%d" % (ref, end, std, i))
            for base in mapdamage.seq.letters:
              out.write("\t%d" % comp[ref][end][std][base][i])
            out.write("\n")

def initializeLg(tab):
  
  tab = recursivedefaultdict() 
  for std in ('+','-'):
    tab[std] = collections.defaultdict(int)

  return(tab)

def printLg(tab, op, out):

  out.write("# table produced by mapDamage version %s\n" % __version__)
  out.write("# using mapped file %s and %s as reference file\n" % (op.filename, op.ref))
  out.write("# Std: strand of reads\n")
  out.write("Std\tLength\tOccurences \n")
  for std in tab:
    for i in tab[std]:
      # write Length in 1-base offset
      out.write("%s\t%d\t%d\n" % (std, i+1, tab[std][i]))
