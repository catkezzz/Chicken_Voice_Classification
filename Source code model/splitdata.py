from pydub import AudioSegment
import os


def split_audio_with_overlap(audio_path, segment_length, overlap, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    audio = AudioSegment.from_file(audio_path)
    audio_length = len(audio)

    segment_length_ms = segment_length * 1000
    overlap_ms = overlap * 1000
    step = segment_length_ms - overlap_ms

    segment_start = 0
    segment_index = 0

    while segment_start < audio_length:
        segment_end = segment_start + segment_length_ms
        if segment_end > audio_length:
            segment_end = audio_length

        segment = audio[segment_start:segment_end]
        segment.export(f"{output_folder}/suarasetelahbertelur_{segment_index}.wav", format="wav")

        segment_index += 1
        segment_start += step

audio_path = "E:\Kezia\Kuliah\\ta\Suara ayam\\suara setelah bertelur\\suarasetelahbertelurgabung.wav"
segment_length = 4
overlap = 1
output_folder = "E:\Kezia\Kuliah\\ta\Suara ayam\\suara setelah bertelur\potongan1"

split_audio_with_overlap(audio_path, segment_length, overlap, output_folder)
