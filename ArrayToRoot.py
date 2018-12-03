from ROOT import TFile, TTree, TBranch
import numpy

class TwoDArrayToROOT:

# for savring 2-D array to ROOT file
#
# ex1) array = [ [a1, b1, c1, ...],
#                [a2, b2, c2, ...],
#                .................  ] => Row = Event : use 'FillRow'
# ex2) array = [ [a1, a2, a3, ...],
#                [b1, b2, b3, ...],
#                .................  ] => Column = Event : use 'FillColumn'
#
# ------------------------------------------------------------------------------------------------------------    
#
# code ex)
#
# from ArrayToRoot import TwoDArrayToROOT
#
# saveroot = TwoDArrayToROOT('WGAN_data.root')
# saveroot.SetTreeName('RealData','momentums of Real Data')
# namearray = ['P1_px','P1_py','P1_pz','P2_px','P2_py','P2_pz','b1_px','b1_py','b1_pz','b2_px','b2_py','b2_pz']
# saveroot.FillRow(input_data,namearray)
# saveroot.SaveTree()
# saveroot.SetTreeName('FakeData','momentums of Fake Data')
# saveroot.FillRow(fakedata,namearray)
# saveroot.SaveTree()
#
# output ex)
#
# SetFileNane : WGAN_data.root
# SetTreeNane : RealData
# Tree 'RealData' Saved
# SetTreeNane : FakeData
# Tree 'FakeData' Saved
#
# [output_path]$ root WGAN_data.root 
# root [0] 
# Attaching file WGAN_data.root as _file0...
# (TFile *) 0x17b92c0
# root [1] .ls
# TFile**		WGAN_data.root	
#  TFile*		WGAN_data.root	
#   KEY: TTree	RealData;1	momentums of Real Data
#   KEY: TTree	FakeData;1	momentums of Fake Data
#

    def __init__(self,filename=None):
        if filename != None:
            self.SetFileName(filename)

    def SetFileName(self, filename, filetype='RECREATE'):
        self.tfile = TFile(filename, filetype)
        print('SetFileNane : {0}'.format(filename))

    def SetTreeName(self, treename, treehelp=''):
        self.ttree = TTree(treename,treehelp)
        print('SetTreeNane : {0}'.format(treename))

    def Fill(self, arraytype, array, arrayname=None):
        #print('Array type : {0}'.format(arraytype))
        if arraytype=='R':
            n_evt = array.shape[0]
            n_val = array.shape[1]
        elif arraytype=='C':
            n_evt = array.shape[1]
            n_val = array.shape[0]
        else:
            print("ARRAY TYPE ERROR")
            exit()

        val = numpy.zeros((n_val,1),dtype=numpy.float64)
        for i_val in range(n_val):
            if arrayname == None:
                self.ttree.Branch('val_{0}'.format(i_val),val[i_val],'val_{0}/D'.format(i_val))
            else:
                self.ttree.Branch('{0}'.format(arrayname[i_val]),val[i_val],'{0}/D'.format(arrayname[i_val]))
        for i_evt in range(n_evt):
            for j_val in range(n_val):
                if arraytype=='R':
                    val[j_val] = array[i_evt,j_val]
                elif arraytype=='C':
                    val[j_val] = array[j_val,i_evt]
            self.ttree.Fill()

    def FillColumn(self, array, arrayname=None):
        self.Fill('C',array, arrayname)

    def FillRow(self, array, arrayname=None):
        self.Fill('R',array, arrayname)

    def SaveTree(self):
        if self.tfile == None:
            print('No ROOT File')
            exit()
        self.ttree.Write()
        print('Tree \'{0}\' Saved'.format(self.ttree.GetName()))
