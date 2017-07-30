import os
import random

def get_vstring(dpath="/xrootd/store/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/", num_files=10):
    """
    Args:
      - dpath

      - nfiles

    Return:
      - vstring
    """

    fnames = os.listdir(dpath)
    fnames = filter(lambda f: os.path.splitext(f)[1] == '.root', fnames)

    if num_files == -1:
        pass
    else:
         fnames = fnames[:num_files]

    vstring = map(lambda f: "file:" + os.path.join(dpath, f), fnames)

    random.shuffle(vstring)

    return vstring

