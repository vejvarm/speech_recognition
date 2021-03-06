import os
import numpy as np
# noinspection PyPackageRequirements

from matplotlib import pyplot as plt

from FeatureExtraction import FeatureExtractor
from DataLoader import PDTSCLoader


def plot_signal(time, signal, title=''):
    plt.plot(time, signal)
    plt.title(title)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True, 'major')


def plot_spectrum(frmspan, fspan, spectrum, title=''):
    # normalize spectrum to (0,1)
    spectrum_normal = spectrum / spectrum.max(axis=0)

    plt.pcolormesh(frmspan, fspan, spectrum_normal.T, cmap='inferno')
    plt.title(title)
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')


def plot_filters(fspan, filterbanks, title=''):
    plt.plot(fspan, filterbanks.T)
    plt.title(title)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude (1)')


def plot_logsum(framespan, nbanks, logsum, title=''):
    bankspan = np.arange(nbanks)
    plt.title(title)
    plt.pcolormesh(framespan, bankspan, logsum.T)
    plt.xlabel('Time (s)')
    plt.ylabel('Bank (1)')


def samples_for_svk(sample=0, folder='./private/images/', format='png', dpi=None):
    pdtsc = PDTSCLoader(['../data/pdtsc_003.ogg'], ['../data/pdtsc_003.wdata'])
    labels = pdtsc.transcripts_to_labels()
    audio, fs = pdtsc.load_audio()

    audio = audio[0]
    fs = fs[0]

    mfcc = FeatureExtractor([audio[sample]], fs, feature_type="MFSC")
    cepstra = mfcc.transform_data()
    stft = mfcc.stft[0].astype(np.float32)
    power_stft = mfcc.power_stft[0]
    log_sum = mfcc.log_sum[0]

    timespan = np.arange(len(audio[sample]))/fs
    framespan = np.arange(np.shape(power_stft)[0]) * mfcc.framestride
    freqspan = np.arange(np.shape(power_stft)[1]) / mfcc.nfft * fs

    # plot audio signal
    plt.figure()
    plot_signal(timespan, audio[sample], title='Audio signal sample no. {}'.format(sample))
    plt.savefig('{}audiosignal.{}'.format(folder, format), dpi=dpi, transparent=True)  # save the figure

    # plot stft spectrum of audio signal
    plt.figure()
    plot_spectrum(framespan, freqspan, stft, title='Spectrogram of sample no. {}'.format(sample))
    plt.savefig('{}spectrum.{}'.format(folder, format), dpi=dpi, transparent=True)  # save the figure

    # plot power spectral density of audio signal
    plt.figure()
    plot_spectrum(framespan, freqspan, power_stft, title='Periodogram of sample no. {}'.format(sample))
    plt.savefig('{}power_spectrum.{}'.format(folder, format), dpi=dpi, transparent=True)  # save the figure

    # plot mel scaled filterbanks
    plt.figure()
    plot_filters(freqspan, mfcc.filterbanks, title='Mel-scaled frequency filter bank'.format(sample))
    plt.savefig('{}filterbank.{}'.format(folder, format), dpi=dpi, transparent=True)  # save the figure

    # plot log10 of mel scaled filterbanks
    plt.figure()
    plot_logsum(framespan, mfcc.nbanks, log_sum, title='log10 of matmul(P,F) for sample no. {}'.format(sample))
    plt.savefig('{}logsum.{}'.format(folder, format), dpi=dpi, transparent=True)  # save the figure

    # plot final mfcc
    mfcc.plot_cepstra(cepstra, nplots=1)
    plt.savefig('{}mfcc.{}'.format(folder, format), dpi=dpi, transparent=True)  # save the figure

    print('transcript: ' + pdtsc.tokens[0][sample])
    print('labels: {}'.format(labels[0][sample]))

    plt.show()


if __name__ == '__main__':
    samples_for_svk(sample=3, folder='../private/images/mfcc/new/', format='png', dpi=300)
