from common.unify_audio import audioUnify
from common.prep_working_dir import prepareDir
from common.rename_by_idx import rename



def main():
    audio_formats = ['.wav', '.mp3', '.flac', '.ogg', '.m4a', '.aiff']
    export_sample_rate = 44100
    audio_origin = 'audio_copy'
    audio_dir = 'AudioExport'
 
    prep_working_dir = prepareDir(audio_origin, audio_formats)
    prep_working_dir.create()

    processor = audioUnify(audio_formats, audio_dir, export_sample_rate)
    processor.format_check()
    processor.get_stats()
    processor.file_to_int16()
    processor.unify_samplerate()
    processor.split_channels()
    rename()

if __name__ == '__main__':
    main()