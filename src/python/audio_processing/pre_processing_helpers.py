import glob
import math
import numpy as np
import os
import pathlib
from spectrogram_helpers import AudioFile
import time


class LibriSpeechReader:
    """
    This class accepts a directory and parses all of the found audio files into
    a single structure.
    """
    def __init__(self, directory, debug=False):
        # Determine how many files we are actually processing for debug 
        # purposes.
        all_files = []
        text_files = []
        audio_files = []
        for (root, _, files) in os.walk(directory):
            if files:
                if glob.glob(root + "/*.trans.txt") and glob.glob(root + "/*.flac"):
                    all_files += files
                    text_files += glob.glob(root + "/*.trans.txt")
                    audio_files += glob.glob(root + "/*.flac")
        total_text_files = len(text_files)
        if debug:
            print(
                f"Pre-processing the LibriSpeech dataset located at: {directory}\n"
                f" -- Processing {len(all_files)} total files...\n"
                f" -- Processing {len(text_files)} text files...\n"
                f" -- Processing {len(audio_files)} audio files..."
            )
            
        data = []
        total_time = time.time()
        progress = 0
        for (root, _, files) in os.walk(directory):
            if files:
                # If the directory we are in contains both a text file and a series
                # of audio files, continue.
                if glob.glob(root + "/*.trans.txt") and glob.glob(root + "/*.flac"):
                    
                    # Get the text file containing all of the transcribed vocal 
                    # lines.
                    text_file = open(
                        glob.glob(root + "/*.trans.txt")[0], 
                        mode='r'
                    )
                    lines = text_file.readlines()
                    
                    # Get the audio files and parse them into the data struct.
                    audio_files = glob.glob(root + "/*.flac")
                    for idx in range(len(audio_files)):
                        # Remove the first word (the audio identifier) and 
                        # remove the newline character from the end of the 
                        # string.
                        transcription = lines[idx].split(' ', 1)[1][:-1]

                        # Append the data.
                        #spect_time = time.time()
                        data.append(
                            [AudioFile(audio_files[idx]), transcription]
                        )

                    # Print the progress regardless if debugging.
                    progress += 1
                    print_progress(progress, total_text_files)

        # Find the max audio length in the data.
        lengths = []
        for entry in data:
            lengths.append(entry[0].audio.duration_seconds)
        max_length = max(lengths)

        # Using this max duration, pad the shorter segments of audio with
        # silence.
        progress = 0
        for entry in data:
            # We will run into an error if we try to append silence to the
            # audio whose duration IS the max duration, so skip it.
            if entry[0].audio.duration_seconds != max_length:
                entry[0].pad_silence(max_length)
            progress += 1
            print_progress(progress, len(data))

        spectrogram_lengths = []
        for entry in data:
            spectrogram_lengths.append(entry[0].spectrogram.shape[1])
        max_spectrogram_length = max(spectrogram_lengths)

        for entry in data:
            assert entry[0].spectrogram.shape[1] == max_spectrogram_length, "EH"

        

        # Set the data to a class member.
        print("Total time: " + str(time.time() - total_time))
        self.data = data


def print_progress(current, total):
    end = '\r' if current != total else '\n'
    print(f"Progress: {100 * round(current / total, 2):.2f}", end='\r')



if __name__=='__main__':
    directory = "data/speech/LibriSpeech"
    reader = LibriSpeechReader(directory, debug=True)
    reader.data[0][0].play()
    reader.data[0][0].merge_audio(reader.data[1][0].audio)
    reader.data[0][0].play()




    print ('--------------------------------') 
