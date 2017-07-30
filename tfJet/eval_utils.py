import os
import numpy as np
import pandas as pd
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import ROOT


class ROC(object):

    def __init__(self, dpath, step, title):
        self.dpath = dpath
        self.step = step
        self.title = title
        plot_fname = 'run-%s.png' % str(step).zfill(6)
        self.plot_path = os.path.join(self.dpath, plot_fname)
        # 
        self.labels = np.array([])
        self.preds = np.array([])  # predictions
        # not initialized attributes
        self.fpr = None
        self.tpr = None
        self.fnr = None
        self.auc = None

    def append_data(self, labels, preds):
        self.labels = np.append(self.labels, labels)
        self.preds = np.append(self.preds, preds)

    def eval_roc(self):
        self.fpr, self.tpr, _ = roc_curve(self.labels, self.preds)
        self.fnr = 1 - self.fpr
        self.auc = auc(self.fpr, self.tpr)

    def save_roc(self, roc_path):
        logs = np.vstack([self.tpr, self.fnr, self.fpr]).T
        np.savetxt(roc_path, logs, delimiter=',', header='tpr, fnr, fpr')

    def plot_n_save_roc_curve(self):
        # fig = plt.figure()
        plt.plot(self.tpr, self.fnr, color='darkorange',
                 lw=2, label='ROC curve (area = %0.3f)' % self.auc)
        plt.plot([0, 1], [1, 1], color='navy', lw=2, linestyle='--')
        plt.plot([1, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.1])
        plt.ylim([0.0, 1.1])
        plt.xlabel('Quark Jet Efficiency (TPR)')
        plt.ylabel('Gluon Jet Rejection (FNR)')
        plt.title('%s-%d / ROC curve' % (self.title, self.step))
        plt.legend(loc='lower left')
        plt.grid()
        plt.savefig(self.plot_path)
        plt.close()

    def finish(self):
        self.eval_roc()
        roc_path = os.path.join(self.dpath, 'roc-auc_%.3f.csv' % self.auc)
        self.save_roc(roc_path)
        self.plot_n_save_roc_curve()


class QGHisto(object):
    '''
      Gluon discriminator
      1 : gluon-like
      0 : quark-like
    '''
    def __init__(self, dpath, step, is_training_data):
        fname = 'histogram_%s.root' % str(step).zfill(6)
        which_data_set = 'training' if is_training_data else 'validation'
        self.root_path = os.path.join(dpath, fname)

        self.quark = ROOT.TH1F("Quark(%s)" % which_data_set,"", 100, 0, 1)
        self.gluon = ROOT.TH1F("Gluon(%s)" % which_data_set,"", 100, 0, 1)

    def fill(self, labels, preds):
        for n, i in enumerate(labels.argmax(axis=1)):
            # gluon
            if i:
                self.gluon.Fill(preds[n, 1])
            else:
                self.quark.Fill(preds[n, 1])

    def save(self):
        writer = ROOT.TFile(self.root_path, 'RECREATE')
        self.quark.Write('quark')  
        self.gluon.Write('gluon')
        writer.Close()

    def finish(self):
        # self.draw()
        self.save()


def draw_qg_histogram(tr_path, val_path, step, path):
    tr = ROOT.TFile(tr_path, "READ")
    val = ROOT.TFile(val_path, "READ")
    c = ROOT.TCanvas("c2", "", 800, 600)
    for p in [tr.quark, tr.gluon, val.quark, val.gluon]:
        p.Scale(1.0/p.GetEntries())
        p.SetFillStyle(3001)
    tr.quark.SetFillColorAlpha(2, 0.35)
    tr.gluon.SetFillColorAlpha(4, 0.35)
    val.quark.SetLineColor(2)
    val.gluon.SetLineColor(4)
    c.SetGrid()
    tr.quark.Draw('hist')
    tr.gluon.Draw('hist SAME')
    val.quark.Draw('SAME')
    val.gluon.Draw('SAME')
    tr.quark.GetYaxis().SetRangeUser(0, 0.5)
    c.BuildLegend( 0.75,  0.75,  0.88,  0.88).SetFillColor(0)
    # title, axis,
    ltx = ROOT.TLatex()
    ltx.SetNDC()
    title = '%d step' % step
    ltx.DrawLatex(0.40, 0.93, title)
    ltx.SetTextSize(0.025)
    ltx.DrawLatex(0.85, 0.03, 'gluon-like')
    ltx.DrawLatex(0.07, 0.03, 'quark-like')
    c.Draw()
    c.SaveAs(path)
    c.Close()


def parse_qg_histogram_fname(path):
    fname = os.path.split(path)[-1]
    without_extension = os.path.splitext(fname)[0]
    step = int(without_extension.split('_')[-1])
    return step
    

def draw_all_qg_histograms(qg_histogram_dir):
    tr_fname_list = os.listdir(qg_histogram_dir.training.path)
    val_fname_list = os.listdir(qg_histogram_dir.validation.path)
    tr_path_list = map(lambda fname: os.path.join(qg_histogram_dir.training.path, fname), tr_fname_list)
    val_path_list = map(lambda fname: os.path.join(qg_histogram_dir.validation.path, fname), val_fname_list)
    tr_path_list.sort()
    val_path_list.sort()

    for tr_path, val_path in zip(tr_path_list, val_path_list):
        step = parse_qg_histogram_fname(tr_path)
        if step != parse_qg_histogram_fname(val_path):
            raise ValueError(':p')
        fname = 'step_%d.png' % step
        output_path = os.path.join(qg_histogram_dir.path, fname)
        draw_qg_histogram(tr_path, val_path, step, output_path)





class Analyser(object):
    def __init__(self):
        self.data = pd.DataFrame(columns=['pdgid', 'pt', 'correct'])
        self.pdgid_dict = {
            1: 'Down', -1: 'Anti-Down',
            2: 'Up', -2: 'Anti-Up',
            3: 'Strange', -3: 'Anti-Strange',
            4: 'Charm', -4: 'Anti-Charm',
            5: 'Botton', -5: 'Anti-Botton',
            21: 'Gluon',
        }

    def append(self, step, datum):
        self.data[step] = datum

    def analyse(self):
        self.total = [self.data[self.data.pdgid == pdgid].correct.size for pdgid in self.pdgid_dict.keys()]
        self.correct = [self.data[self.data.pdgid == pdgid].correct.sum() for pdgid in self.pdgid_dict.keys()]
 
    def analyse_between(self, min_pt, max_pt):
        total = [self.data[self.data.pdgid == pdgid].pt.between(min_pt, max_pt).size for pdgid in self.pdgid_dict.keys() ]
        correct = [ self.data[self.data.pdgid == pdgid].pt.between(min_pt, max_pt).sum() for pdgid in self.pdgid_dict.keys() ]
        return total, correct

    def draw(self, path):
        fig = plt.figure()
        # total --> incorrect
        plt.bar(range(len(self.total)), self.total, color='red', edgecolor='black', hatch='\\\\', width=0.6)
        # correct
        plt.bar(range(len(self.correct)), self.correct, color='blue', edgecolor='black', hatch='//', width=0.6)
        plt.xticks(range(len(self.pdgid_dict)), self.pdgid_dict.values())
        plt.show()
        plt.savefig(path)

    def draw_over_pt_inverval(self):
        fig = plt.figure()
        pt_range = [(0, 200), (200, 400), (400, 600), (600, 800)]
        num = 100 + 10*len(pt_range)
        for i, (min_value, max_value) in enumerate(pt_range):
            num += 1
            total, correct = self.calc_between(min_value, max_value)
            ax = fig.add_subplot(num)
            ax.bar(range(len(total)), total, color='red', edgecolor='black', hatch='\\\\', width=0.6)
            ax.bar(range(len(correct)), correct, color='blue', hatch='//', width=0.6)
        plt.show()
