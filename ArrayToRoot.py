from ROOT import TFile, TTree, TBranch
import numpy

class TwoDArrayToROOT:

#
# for saving 2-D array to ROOT file
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
# SetFileName : WGAN_data.root
# SetTreeName : RealData
# Tree 'RealData' Saved
# SetTreeName : FakeData
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
        print('SetFileName : {0}'.format(filename))

    def SetTreeName(self, treename, treehelp=''):
        self.ttree = TTree(treename,treehelp)
        print('SetTreeName : {0}'.format(treename))

    def Fill(self, arraytype, array, arrayname=None):
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

class ROOTToTwoDArray:

#
# for loading 2-D array form ROOT file
#
# ex)
#
# from ArrayToRoot import ROOTToTwoDArray
#
# loadroot = ROOTToTwoDArray('WGAN_data.root')
# loadroot.SetTreeName('FakeData')
# test_array = loadroot.ReadRow(['P1_pz','P1_px','TEST'])
#

    def __init__(self,filename=None):
        if filename != None:
            self.SetFileName(filename)

    def SetFileName(self, filename):
        self.tfile = TFile(filename, 'READ')
        print('SetFileName : {0}'.format(filename))

    def SetTreeName(self, treename):
        self.ttree = self.tfile.Get(treename) 
        print('SetTreeName : {0}'.format(treename))

    def Read(self, arraytype, arrayname=None):
        n_evt = self.ttree.GetEntries()
        l_val = []
        l_b = self.ttree.GetListOfBranches()
        for i_b in l_b:
            l_l = i_b.GetListOfLeaves()
            for i_l in l_l:
                leaftype = i_l.GetTypeName()
                if leaftype == 'Double_t' or leaftype == 'Float_t' or leaftype == 'Int_t':
                    if arrayname == None:
                        l_val.append(i_b.GetName())
                    else:
                        for i_array in arrayname:
                            if i_array == i_b.GetName():
                                l_val.append(i_b.GetName())

        if not arrayname == None:
            for j_array in arrayname:
                if not j_array in l_val:
                    arrayname.remove(j_array)
                    print('WARTING : Can not find \'{}\''.format(j_array))
            l_val = arrayname
      
        n_val = len(l_val)
        if arraytype == 'R':
            result_array = numpy.zeros((n_evt, n_val),dtype=numpy.float64)
        elif arraytype == 'C':
            result_array = numpy.zeros((n_val, n_evt),dtype=numpy.float64)
        else:
            print("ARRAY TYPE ERROR")
            exit()       

        for i_evt in range(n_evt):
            self.ttree.GetEntry(i_evt)
            for i_val in range(n_val):
                if arraytype == 'R':
                    result_array[i_evt, i_val] = self.ttree.GetLeaf(l_val[i_val]).GetValue()
                else:
                    result_array[i_val, i_evt] = self.ttree.GetLeaf(l_val[i_val]).GetValue()
       
        return result_array

    def ReadRow(self, arrayname=None):
        return self.Read('R',arrayname)

    def ReadColumn(self,  arrayname=None):
        return self.Read('C',arrayname)
