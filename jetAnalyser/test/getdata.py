#!/usr/bin/env python

from math import *

# import ROOT in batch mode
import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv


# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

jets, jetLabel = Handle("std::vector<pat::Jet>"), "slimmedJets"

# open file
## QCD jets pythia
events = Events("/pnfs/user/jlee/data/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM/02E23E7E-71BE-E611-8258-FA163E8B40DC.root")

## QCD jets herwigpp
#events = Events("/pnfs/user/jlee/data/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM/0401C3EE-60D2-E611-BBB0-1866DAEA7E28.root")

## ttbar jets
#events = Events("/pnfs/user/jlee/data/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM/0693E0E7-97BE-E611-B32F-0CC47A78A3D8.root")

def deltaPhi(phi1, phi2):
	dphi = phi2 - phi1
	if dphi > pi:
		dphi -= 2.0*pi
	if dphi <= -pi:
		dphi += 2.0*pi
	return dphi

from array import array

# TTree
#tfile = ROOT.TFile("jets.root","RECREATE")

jet_ptD = array("d",[0])
jet_axis2 = array("d",[0])
jet_useQC_mult = array("i",[0])
jet_mult = array("i",[0])
jet_neutral_Multi = array("i",[0])
jet_charged_Multi = array("i",[0])

q_ttree = ROOT.TTree("quark","tree")
q_ttree.Branch("jet_ptD",jet_ptD,"jet_ptD/D")
q_ttree.Branch("jet_axis2",jet_axis2,"jet_axis2/D")
q_ttree.Branch("jet_useQC_mult",jet_useQC_mult,"jet_useQC_mult/I")
q_ttree.Branch("jet_mult",jet_mult,"jet_mult/I")
q_ttree.Branch("jet_neutral_Multi",jet_neutral_Multi,"jet_neutral_Multi/I")
q_ttree.Branch("jet_charged_Multi",jet_charged_Multi,"jet_charged_Multi/I")

g_ttree = ROOT.TTree("gluon","tree")
g_ttree.Branch("jet_ptD",jet_ptD,"jet_ptD/D")
g_ttree.Branch("jet_axis2",jet_axis2,"jet_axis2/D")
g_ttree.Branch("jet_useQC_mult",jet_useQC_mult,"jet_useQC_mult/I")
g_ttree.Branch("jet_mult",jet_mult,"jet_mult/I")
g_ttree.Branch("jet_neutral_Multi",jet_neutral_Multi,"jet_neutral_Multi/I")
g_ttree.Branch("jet_charged_Multi",jet_charged_Multi,"jet_charged_Multi/I")

# Histogram
#jets_Parton = ROOT.TH1D("jets_Partron", "", 30, 0, 30)
#gjets_PtD = ROOT.TH1D("gjet_PtD","",30,0,8)
#gjets_PtD.SetLineColor(2)
#qjets_PtD = ROOT.TH1D("qjet_PtD","",30,0,8)
#qjets_PtD.SetLineColor(1)
#gjets_axis2 = ROOT.TH1D("gjet_axis2","",30,0,0.2)
#gjets_axis2.SetLineColor(2)
#qjets_axis2 = ROOT.TH1D("qjet_axis2","",30,0,0.2)
#qjets_axis2.SetLineColor(1)
#g_useQC_mult = ROOT.TH1D("g_useQC_mult","",10,-5,20)
#g_useQC_mult.SetLineColor(1)
#g_mult = ROOT.TH1D("g_mult","",30,0,30)
#g_mult.SetLineColor(2)
#q_useQC_mult = ROOT.TH1D("q_useQC_mult","",10,-5,20)
#q_useQC_mult.SetLineColor(3)
#q_mult = ROOT.TH1D("q_mult","",30,0,30)
#q_mult.SetLineColor(4)
box=[]
num=0
ke=0
for iev,event in enumerate(events):
	if(iev>10):break
	box.append([])
	event.getByLabel(jetLabel, jets)
	print "\nEvent %d: run %6d, lumi %4d, event %12d" % (ke,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())
    #https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/DataFormats/PatCandidates/interface/Jet.h
	kj=0
	for i,jet in enumerate(jets.product()):
		if(i>10):break
		print "jet %3d: pt %5.1f, eta %+4.2f, mass %5.1f, partonFlavour %3d" % (i, jet.pt(), jet.eta(), jet.mass(), jet.partonFlavour())
		if(jet.partonFlavour()==0):continue
		box[ke].append([jet.partonFlavour()])
#        print "jet.bDiscriminator()", jet.bDiscriminator()
#        print "jet.chargedHadronEnergyFraction()", jet.chargedHadronEnergyFraction(),
#        print "jet.neutralHadronEnergyFraction()", jet.neutralHadronEnergyFraction(),
#        print "jet.chargedEmEnergyFraction()", jet.chargedEmEnergyFraction(),
#        print "jet.neutralEmEnergyFraction()", jet.neutralEmEnergyFraction()
        
#        print "jet.photonEnergyFraction()", jet.photonEnergyFraction(),
#        print "jet.electronEnergyFraction()", jet.electronEnergyFraction(),
#        print "jet.muonEnergyFraction()", jet.muonEnergyFraction(),
#        print "jet.HFHadronEnergyFraction()", jet.HFHadronEnergyFraction()



		#initialize
		mult = 0
		useQC_mult = 0
		sum_weight = 0
		sum_pt = 0
		sum_deta = 0
		sum_dphi = 0
		sum_deta2 = 0
		sum_detadphi = 0
		sum_dphi2 = 0


        #axis2, ptD valiables
		a = 0
		b = 0
		c = 0
		ave_deta = 0
		ave_dphi = 0
		ave_deta2 = 0
		ave_dphi2 = 0
		

		neutral_Multi = 0
		charged_Multi = 0


		for d in range(jet.numberOfDaughters()):
			
            # https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/DataFormats/PatCandidates/interface/PackedCandidate.h
			dau = jet.daughter(d)
		#	print "daughter: pt %5.1f, eta %+4.2f, phi %+4.2f, pdgId %3d" % (dau.pt(), dau.eta(), dau.phi(), dau.pdgId())
        	

			# calculate mult
			if dau.charge():
				if not (dau.fromPV() > 1 and dau.trackHighPurity()):
					continue
				mult = mult + 1

				if dau.dzError() != 0:
					if ((dau.dz()*dau.dz())/(dau.dzError()*dau.dzError()) > 25.):
						continue
					if ((dau.dxy()*dau.dxy())/(dau.dxyError()*dau.dxyError()) < 25.):
						useQC_mult = useQC_mult + 1

			#calculate Multiplicity
			if dau.charge() == 0:
				neutral_Multi = neutral_Multi + 1
			if dau.charge() != 0:
				charged_Multi = charged_Multi + 1

			else:
				if (dau.pt() < 1.0): 
					continue
				mult = mult + 1
				useQC_mult = useQC_mult + 1

			#calculate valiables
			partPt = dau.pt()
			weight = partPt*partPt
			deta = dau.eta() - jet.eta()
			dphi = deltaPhi(dau.phi(), jet.phi())

		#	print "daughter: pt %5.1f, deta %+4.2f, dphi %+4.2f, charge %3d" % (dau.pt(), deta, dphi, dau.charge())
			daub=[dau.pt(),deta,dphi,dau.charge()]
			box[ke][kj].append([dau.pt(),deta,dphi,dau.charge()])
		 # box[iev][i].append(daub)

			sum_weight += weight
			sum_pt += partPt
			sum_deta += deta*weight
			sum_dphi += dphi*weight
			sum_deta2 += deta*deta*weight
			sum_detadphi += deta*dphi*weight
			sum_dphi2 += dphi*dphi*weight
 	    
		#calculate ptD, axis2
		if sum_weight > 0:
			ave_deta  = sum_deta/sum_weight
			ave_dphi  = sum_dphi/sum_weight
			ave_deta2 = sum_deta2/sum_weight
			ave_dphi2 = sum_dphi2/sum_weight
			a         = ave_deta2 - ave_deta*ave_deta
			b         = ave_dphi2 - ave_dphi*ave_dphi
			c         = -(sum_detadphi/sum_weight - ave_deta*ave_dphi)

			ptD = sqrt(sum_weight)/sum_pt

		if not (sum_weight > 0):
			ptD = 0

		delta = sqrt(fabs((a-b)*(a-b)+4*c*c))

		if a+b-delta > 0:
			axis2 = sqrt(0.5*(a+b-delta))

		if not (a+b-delta > 0):
			axis2 = 0



		if ROOT.TMath.Abs(jet.partonFlavour()) == 21:
			jet_ptD[0] = ptD
			jet_axis2[0] = axis2
			jet_useQC_mult[0] = useQC_mult
			jet_mult[0] = mult
			jet_neutral_Multi[0] = neutral_Multi
			jet_charged_Multi[0] = charged_Multi

			g_ttree.Fill()
			#gjets_PtD.Fill(ptD)
			#gjets_axis2.Fill(axis2)
			#g_useQC_mult.Fill(jet_useQC_mult)
			#g_mult.Fill(jet_mult)

		if ROOT.TMath.Abs(jet.partonFlavour()) != 21 and jet.partonFlavour() != 0:
			jet_ptD[0] = ptD
			jet_axis2[0] = axis2
			jet_useQC_mult[0] = useQC_mult
			jet_mult[0] = mult
			jet_neutral_Multi[0] = neutral_Multi
			jet_charged_Multi[0] = charged_Multi

			q_ttree.Fill()
			#qjets_PtD.Fill(ptD)
			#qjets_axis2.Fill(axis2)
			#q_useQC_mult.Fill(jet_useQC_mult)
			#q_mult.Fill(jet_mult)
		kj+=1
	ke+=1

#			else:
#				axis2 = 0
#				ptD = 0

			
        # Gluon partonFlavour Histogram
#		jets_Parton.Fill(ROOT.TMath.Abs(jet.partonFlavour()))



			
	#print "q_ptD: %f g_ptD: %f q_axis2: %f  g_axis2: %f " % (q_ptD, g_ptD, q_axis2, g_axis2)
#	print "------------------------------------------------------"


f = open("array.txt",'w')
f.write("//number jetflavour deta dphi pt charge 0 0 0 0 0 0 line is dummy\n")
			#box[iev][i].append([dau.pt(),deta,dphi,dau.charge()])
for i in range(len(box)):
	for j in range(len(box[i])):
		f.write(str(num)+'\t0\t-1\t-1\t-1\t0\n')
		line=str(num)+'\t'+str(box[i][j][0])+'\t'
		num+=1;
		#print box[i][j][0]
		for k in range(len(box[i][j])):
			if k!=0:
				line1=line+str(box[i][j][k][1])+'\t'+str(box[i][j][k][2])+'\t'+str(box[i][j][k][0])+'\t'+str(box[i][j][k][3])+'\n'
				f.write(line1)
#				print box[i][j][1]
#				print box[i][j][2]
#				print box[i][j][0]
#				print box[i][j][k][3]
f.write('-1\t-1\t-1\t-1\t-1\t-1\n')
f.close()
#print box
#print len(box)
#print len(box[i])
#print len(box[i][j])
#print box[0][0][0]
#print box[0][0][1][1]
#tfile.Write()
#tfile.Close()


print "-----------------------------------------------------"
