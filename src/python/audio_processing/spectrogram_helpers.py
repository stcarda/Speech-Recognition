import matplotlib.pyplot as plt
import numpy as np
from pathlib import PurePath
from pydub import AudioSegment, playback
from scipy.fft import fft, fftshift
import scipy.signal as signal
from scipy.special import i0
import time

class InvalidExtensionError(Exception):
    pass


class AudioFile:
    """
    A class representing a sample of audio. Rather than inheriting from pydub's
    AudioSegment class, this class instead leverages that functionality into
    a class variable. 
    """
    def __init__(self, filepath):
        # Ensure that we have been given a string filepath.
        assert(type(filepath) == str)

        # Read the audio at the given filepath.
        self.filepath = PurePath(filepath)
        self.extension = self.filepath.suffix[1:]
        if self.extension:
            self.audio = AudioSegment.from_file(filepath, self.extension)
        else:
            raise InvalidExtensionError(
                "No file extension detected. "
                "Please ensure that you have provided a proper file name"
            )
        
        # Setup STFT computation parameters.
        self.segment_length = 512
        self.overlap = 128
        self.fft_length = 512
        
        # Get the normalized amplitudes of the audio as well as the time scale
        # of the signal.
        self._update_signal()
        self._compute_spectrogram()
        

    def pad_silence(self, desired_length_in_sec):
        # Determine how much padding is necessary.
        current_length = self.audio.duration_seconds
        needed_length = desired_length_in_sec - current_length
        if needed_length < 0:
            raise ValueError(
                "Desired length is shorter than the audio's current length"
            )
        
        # Append silence to the audio.
        silent_audio = AudioSegment.silent(needed_length * 10**3)
        self.audio = self.audio.append(silent_audio)

        # Update the returned signal.
        self._update_signal()
        self._compute_spectrogram()


    def merge_audio(self, audio):
        self.audio = self.audio.append(audio)
        self._update_signal()
        self._compute_spectrogram()


    def play(self):
        playback.play(self.audio)


    def _compute_spectrogram(self):
        t, f, S = compute_spectrogram(
            self.signal, 
            self.audio.frame_rate, 
            hanning_window(self.segment_length),
            self.segment_length,
            self.overlap,
            self.fft_length
        )

        self.spectrogram_time = t
        self.frequencies = f
        self.spectrogram = S


    def _update_signal(self):
        # Update the signal amplitude samples.
        samples = self.audio.get_array_of_samples()
        amplitudes = np.array(samples).T.astype(np.float32)
        amplitudes /= np.iinfo(samples.typecode).max
        self.signal = amplitudes

        # Update the time scale of the signal.
        duration = self.audio.duration_seconds
        rate = self.audio.frame_rate
        self.time = np.linspace(
            0, 
            duration, 
            int(duration * rate)
        )


def compute_spectrogram(
    signal, 
    sampling_rate, 
    window, 
    segment_length, 
    overlap, 
    fft_length
):
    # Ensure that the length of the window matches the segment length.
    assert window.size == segment_length, ""

    # Compute the frequencies corresponding to the FFT computations.
    n = fft_length
    num_of_freq = int(n / 2)
    frequencies = sampling_rate * np.array(range(num_of_freq)) / n

    # Get the total length of the signal, and assign the overlap and segment
    # length variables to short-hand names.
    L = signal.size
    R = overlap
    M = segment_length

    # Compute the time scalee for this spectrogram.
    spect_time = np.arange(
        M / 2, 
        int(signal.shape[-1] - (M / 2)), 
        M - R
    ) / sampling_rate

    # Initialize our spectrogram.
    spectrogram = np.zeros((num_of_freq, int(L / (M - R))))

    # For each segment of the audio, compute the FFT for that portion of the
    # spectrogram.
    r = 0
    while r * (M - R) < L - M:
        # Get the current segment of the signal and compute its Fourier 
        # Transform.
        str_idx = r * (M - R)
        end_idx = str_idx + M
        signal_segment = signal[str_idx:end_idx] * window
        fft_segment = fftshift(fft(signal_segment, fft_length))

        # For the portion of time for which we have computed the FFT, set that
        # spectrogram segment to the spectrum we have just calculated.
        spectrogram[:, r] = np.abs(
            fft_segment[num_of_freq:]
        )

        # Increment the start of the segment.
        r += 1

    # Return both the frequency spectrum and the resulting spectrogram.
    return spect_time, frequencies, spectrogram


def rectangular_window(N):
    """
    Generates a Rect window of size N.

    Args:
        N: a scalar integer denoting the length of the window.

    Returns:
        window: the resutling Rect window.

    Raises:
    """
    return np.ones(N)


def hanning_window(N):
    """
    Generates a Hanning window of size N.

    Args:
        N: a scalar integer denoting the length of the window.

    Returns:
        window: the resutling Hanning window.

    Raises:
    """
    n = np.arange(N)
    window = 0.5 - (0.5 * np.cos((2 * np.pi * n) / (N - 1)))
    return window


def hamming_window(N):
    """
    Generates a Hamming window of size N.

    Args:
        N: a scalar integer denoting the length of the window.

    Returns:
        window: the resutling Hamming window.

    Raises:
    """
    n = np.arange(N)
    window = 0.54 - (0.46 * np.cos((2 * np.pi * n) / (N - 1)))
    return window


def kaiser_window(N, A):
    """
    Generates a Kaiser window of size N.

    Args:
        N: a scalar integer denoting the length of the window.
        A: a scalar integer denoting a peak sidelobe level of A dB below
           the peak value

    Returns:
        window: the resutling Kaiser window.

    Raises:
    """
    # Calculate the value of beta based on the value of A.
    if A <= 21:
        B = 0
    elif 21 < A <= 50:
        B = (0.5842 * (A - 21)**0.4) + (0.07886 * (A - 21))
    elif A > 50:
        B = 0.1102 * (A - 8.7)
    else:
        raise ValueError("Value of A does not produce a valid value for beta")
    
    # Calculate the window.
    n = np.arange(N)
    print(B)
    window = i0(B * np.sqrt(1 - (1 - (2 * n / (N - 1)))**2)) / i0(B)
    return window



if __name__=='__main__':
    filename = "data/speech/LibriSpeech/dev-clean/84/121123/84-121123-0000.flac"
    sample = AudioFile(filename)
    M = 512
    R = 256

    start = time.time()
    f, t, Sxx = signal.spectrogram(
        sample.signal, 
        sample.audio.frame_rate, 'hamming', M, R, 1024)
    plt.figure()
    plt.pcolormesh(t, f, Sxx, shading='gouraud')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    print(time.time() - start)

    t, f, S = compute_spectrogram(
        sample.signal, 
        sample.audio.frame_rate, 
        hanning_window(M), 
        M, 
        R, 
        1024
    )
    plt.figure()
    plt.pcolormesh(t, f, S, shading='gouraud')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    print(time.time() - start)
    plt.show()

    """
    plt.figure()
    plt.plot(Fs/L*np.array(list(range(int(-L/2), int(L/2-1)))), np.abs(fftshift(Y)))
    plt.title("Complex Magnitude of fft Spectrum")
    plt.xlabel("f (Hz)")
    plt.ylabel("|fft(X)|")
    plt.show()

    n = 1024
    Fs = sample.audio.frame_rate
    test = fftshift(fft(normalized_signal, n))
    f = Fs * np.array(list(range(int(-n / 2), int(n / 2)))) / n

    plt.figure()
    plt.plot(f, np.abs(test))
    plt.show()
    """