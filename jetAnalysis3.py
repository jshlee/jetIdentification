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
events = Events("/cms/scratch/jlee/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext3-v1/0064B539-803A-E611-BDEA-002590D0B060.root")


def deltaPhi(phi1, phi2):
	dphi = phi2 - phi1
	if dphi > pi:
		dphi -= 2.0*pi
	if dphi <= -pi:
		dphi += 2.0*pi
	return dphi



# histogram
tfile = ROOT.TFile("jets.root","RECREATE")

jets_Parton = ROOT.TH1D("jets_Partron", "", 30, 0, 30)
gjets_PtD = ROOT.TH1D("gjet_PtD","",30,0,8)
gjets_PtD.SetLineColor(2)
qjets_PtD = ROOT.TH1D("qjet_PtD","",30,0,8)
qjets_PtD.SetLineColor(1)
gjets_eta = ROOT.TH1D("gjet_eta","",3,-6,6)
gjets_eta.SetLineColor(2)
qjets_eta = ROOT.TH1D("qjet_eta","",3,-6,6)
qjets_eta.SetLineColor(1)
gjets_axis2 = ROOT.TH1D("gjet_axis2","",30,0,0.2)
gjets_axis2.SetLineColor(2)
qjets_axis2 = ROOT.TH1D("qjet_axis2","",30,0,0.2)
qjets_axis2.SetLineColor(1)
g_useQC_mult = ROOT.TH1D("g_useQC_mult","",10,-5,20)
g_useQC_mult.SetLineColor(1)
g_mult = ROOT.TH1D("g_mult","",30,0,30)
g_mult.SetLineColor(2)
q_useQC_mult = ROOT.TH1D("q_useQC_mult","",10,-5,20)
q_useQC_mult.SetLineColor(3)
q_mult = ROOT.TH1D("q_mult","",30,0,30)
q_mult.SetLineColor(4)




for iev,event in enumerate(events):


	event.getByLabel(jetLabel, jets)
	print "\nEvent %d: run %6d, lumi %4d, event %12d" % (iev,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())
    #https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/DataFormats/PatCandidates/interface/Jet.h
	for i,jet in enumerate(jets.product()):
		print "jet %3d: pt %5.1f, eta %+4.2f, mass %5.1f, partonFlavour %3d" % (
			i, jet.pt(), jet.eta(), jet.mass(), jet.partonFlavour())

#        print "jet.bDiscriminator()", jet.bDiscriminator()
#        print "jet.chargedHadronEnergyFraction()", jet.chargedHadronEnergyFraction(),
#        print "jet.neutralHadronEnergyFraction()", jet.neutralHadronEnergyFraction(),
#        print "jet.chargedEmEnergyFraction()", jet.chargedEmEnergyFraction(),
#        print "jet.neutralEmEnergyFraction()", jet.neutralEmEnergyFraction()
        
#        print "jet.photonEnergyFraction()", jet.photonEnergyFraction(),
#        print "jet.electronEnergyFraction()", jet.electronEnergyFraction(),
#        print "jet.muonEnergyFraction()", jet.muonEnergyFraction(),
#        print "jet.HFHadronEnergyFraction()", jet.HFHadronEnergyFraction()



		if ROOT.TMath.Abs(jet.partonFlavour()) == 21:

			#initialize
			gjet_mult = 0
			gjet_useQC_mult = 0
			g_sum_weight = 0
			g_sum_pt = 0
			g_sum_deta = 0
			g_sum_dphi = 0
			g_sum_deta2 = 0
			g_sum_detadphi = 0
			g_sum_dphi2 = 0


			for d in range(jet.numberOfDaughters()):
                # https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/DataFormats/PatCandidates/interface/PackedCandidate.h
				dau = jet.daughter(d)
#				print "daughter: pt %5.1f, eta %+4.2f, phi %+4.2f, pdgId %3d" % (dau.pt(), dau.eta(), dau.phi(), dau.pdgId())
            	

				# calculate mult
				if dau.charge():
					if not (dau.fromPV() > 1 and dau.trackHighPurity()):
						continue
					if dau.dzError() != 0:
						if ((dau.dz()*dau.dz())/(dau.dzError()*dau.dzError()) > 25.):
							continue
						if ((dau.dxy()*dau.dxy())/(dau.dxyError()*dau.dxyError()) < 25.):
							gjet_useQC_mult = gjet_useQC_mult + 1
						else: 
							gjet_useQC_mult = gjet_useQC_mult + 1

					if (dau.pt() < 1.0): 
						gjet_mult = gjet_mult + 1
					else:
						gjet_mult = gjet_mult + 1

                #calculate valiabe
				g_partPt = dau.pt()
				g_weight = g_partPt*g_partPt
				g_deta = dau.eta() - jet.eta()
				g_dphi = deltaPhi(dau.phi(), jet.phi())

				g_sum_weight += g_weight
				g_sum_pt += g_partPt
				g_sum_deta += g_deta*g_weight
				g_sum_dphi += g_dphi*g_weight
				g_sum_deta2 += g_deta*g_deta*g_weight
				g_sum_detadphi += g_deta*g_dphi*g_weight
				g_sum_dphi2 += g_dphi*g_dphi*g_weight



                #calculate axis2, ptD
				g_a = 0
				g_b = 0
				g_c = 0
				g_ave_deta = 0
				g_ave_dphi = 0
				g_ave_deta2 = 0
				g_ave_dphi2 = 0
                
				if g_sum_weight > 0:
					g_ave_deta  = g_sum_deta/g_sum_weight
					g_ave_dphi  = g_sum_dphi/g_sum_weight
					g_ave_deta2 = g_sum_deta2/g_sum_weight
					g_ave_dphi2 = g_sum_dphi2/g_sum_weight
					g_a         = g_ave_deta2 - g_ave_deta*g_ave_deta
					g_b         = g_ave_dphi2 - g_ave_dphi*g_ave_dphi
					g_c         = -(g_sum_detadphi/g_sum_weight - g_ave_deta*g_ave_dphi)

					g_ptD = sqrt(g_sum_weight/g_sum_pt)

				g_delta = sqrt(fabs((g_a-g_b)*(g_a-g_b)+4*g_c*g_c))

				if g_a+g_b-g_delta > 0:
					g_axis2 = sqrt(0.5*(g_a+g_b-g_delta))

				else:
					g_axis2 = 0
					g_ptD = 0

				gjets_PtD.Fill(g_ptD) 
				gjets_axis2.Fill(g_axis2)

			# 1 daughter mult
			g_mult.Fill(gjet_mult)
			g_useQC_mult.Fill(gjet_useQC_mult)


            # Gluon partonFlavour Histogram
			jets_Parton.Fill(ROOT.TMath.Abs(jet.partonFlavour()))


        if ROOT.TMath.Abs(jet.partonFlavour()) != 21 and jet.partonFlavour() != 0:

			#initialize
			qjet_mult = 0
			qjet_useQC_mult = 0
			q_sum_weight = 0
			q_sum_pt = 0
			q_sum_deta = 0
			q_sum_dphi = 0
			q_sum_deta2 = 0
			q_sum_detadphi = 0
			q_sum_dphi2 = 0

			for d in range(jet.numberOfDaughters()):
                # https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/DataFormats/PatCandidates/interface/PackedCandidate.h
				dau = jet.daughter(d)
#				print "daughter: pt %5.1f, eta %+4.2f, phi %+4.2f, pdgId %3d" % (dau.pt(), dau.eta(), dau.phi(), dau.pdgId())


				#calculate mult
				if dau.charge():
					if not (dau.fromPV() > 1 and dau.trackHighPurity()):
						continue
					if dau.dzError() != 0:
						if ((dau.dz()*dau.dz())/(dau.dzError()*dau.dzError()) > 25.):
							continue
						if ((dau.dxy()*dau.dxy())/(dau.dxyError()*dau.dxyError()) < 25.):
							qjet_useQC_mult = qjet_useQC_mult + 1
						else:
							qjet_mult = qjet_mult + 1

					if dau.pt() < 1.0: 
						continue
					else:
						qjet_mult = qjet_mult + 1
				


                #calculate valiabe
				q_partPt = dau.pt()
				q_weight = q_partPt*q_partPt
				q_deta = dau.eta() - jet.eta()
				q_dphi = deltaPhi(dau.phi(), jet.phi())

				q_sum_weight += q_weight
				q_sum_pt += q_partPt
				q_sum_deta += q_deta*q_weight
				q_sum_dphi += q_dphi*q_weight
				q_sum_deta2 += q_deta*q_deta*q_weight
				q_sum_detadphi += q_deta*q_dphi*q_weight
				q_sum_dphi2 += q_dphi*q_dphi*q_weight



                #calculate axis2, ptD
				q_a = 0
				q_b = 0
				q_c = 0
				q_ave_deta = 0
				q_ave_dphi = 0
				q_ave_deta2 = 0
				q_ave_dphi2 = 0
                
				if q_sum_weight > 0:
					q_ave_deta  = q_sum_deta/q_sum_weight
					q_ave_dphi  = q_sum_dphi/q_sum_weight
					q_ave_deta2 = q_sum_deta2/q_sum_weight
					q_ave_dphi2 = q_sum_dphi2/q_sum_weight
					q_a         = q_ave_deta2 - q_ave_deta*q_ave_deta
					q_b         = q_ave_dphi2 - q_ave_dphi*q_ave_dphi
					q_c         = -(q_sum_detadphi/q_sum_weight - q_ave_deta*q_ave_dphi)

					q_ptD = sqrt(q_sum_weight/q_sum_pt)

				q_delta = sqrt(fabs((q_a-q_b)*(q_a-q_b)+4*q_c*q_c))

				if q_a+q_b-q_delta > 0:
				    q_axis2 = sqrt(0.5*(q_a+q_b-q_delta))

				else:
				    q_axis2 = 0
				    q_ptD = 0

				qjets_PtD.Fill(q_ptD) 
				qjets_axis2.Fill(q_axis2)

			# 1 daughter mult
			q_mult.Fill(qjet_mult)
			q_useQC_mult.Fill(qjet_useQC_mult)
            # quark  partonFlavour Histogram
			jets_Parton.Fill(ROOT.TMath.Abs(jet.partonFlavour()))

			
	#print "q_ptD: %f g_ptD: %f q_axis2: %f  g_axis2: %f " % (q_ptD, g_ptD, q_axis2, g_axis2)
#	print "------------------------------------------------------"


#normalized PtD
c1 = ROOT.TCanvas() 
qjets_PtD_norm = qjets_PtD.Clone()
qjets_PtD_norm.Scale(1/qjets_PtD_norm.GetEntries())
qjets_PtD_norm.Draw()
gjets_PtD_norm = gjets_PtD.Clone()
gjets_PtD_norm.Scale(1/gjets_PtD_norm.GetEntries())
gjets_PtD_norm.Draw("same")
leg1 = ROOT.TLegend(0.9,0.8,0.6,0.9)
leg1.SetHeader("jet ptD")
leg1.AddEntry(gjets_PtD,"gloun jets ptD", "F")
leg1.AddEntry(qjets_PtD,"quark jets ptD", "F")
leg1.Draw()
c1.SaveAs("jet_PtD.png")

#normalized axis2
c2 = ROOT.TCanvas()
qjets_axis2_norm = qjets_axis2.Clone()
qjets_axis2_norm.Scale(1/qjets_axis2_norm.GetEntries())
qjets_axis2_norm.Draw()
gjets_axis2_norm = gjets_axis2.Clone()
gjets_axis2_norm.Scale(1/gjets_axis2_norm.GetEntries())
gjets_axis2_norm.Draw("same")
leg2 = ROOT.TLegend(0.9,0.8,0.6,0.9)
leg2.SetHeader("jet axis2")
leg2.AddEntry(gjets_eta, "gloun jets axis2","F")
leg2.AddEntry(qjets_eta, "quark jets axis2","F")
leg2.Draw()
c2.SaveAs("jet_axis2.png")

#normalized mult
c3 = ROOT.TCanvas()
q_useQC_mult_norm = q_useQC_mult.Clone()
q_useQC_mult_norm.Scale(1/q_useQC_mult_norm.GetEntries())
q_useQC_mult_norm.Draw()
g_useQC_mult_norm = g_useQC_mult.Clone()
g_useQC_mult_norm.Scale(1/g_useQC_mult_norm.GetEntries())
g_useQC_mult_norm.Draw("same")
q_mult_norm = q_mult.Clone()
q_mult_norm.Scale(1/q_mult_norm.GetEntries())
q_mult_norm.Draw("same")
g_mult_norm = g_mult.Clone()
g_mult_norm.Scale(1/g_mult_norm.GetEntries())
g_mult_norm.Draw("same")
leg3 = ROOT.TLegend(0.9,0.8,0.6,0.9)
leg3.SetHeader("jets mult")
leg3.AddEntry(g_useQC_mult, "gluon_useQC_mult","F")
leg3.AddEntry(q_useQC_mult, "quark_useQC_mult","F")
leg3.AddEntry(g_mult, "gluon_mult","F")
leg3.AddEntry(q_mult, "quark_mult","F")
leg3.Draw()
c3.SaveAs("jet_mult.png")



tfile.Write()
tfile.Close()


print "-----------------------------------------------------"
