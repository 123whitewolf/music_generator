import mido
from pydub import AudioSegment
from pydub.generators import Sine
import asyncio

async def process_note_on(msg, current_time, notes):
    frequency = 440 * (2 ** ((msg.note - 69) / 12))
    sine_wave = Sine(frequency).to_audio_segment(duration=int(current_time * 1000), volume=-20)
    if msg.note in notes:
        notes[msg.note] += sine_wave
    else:
        notes[msg.note] = sine_wave

async def process_note_off(msg, notes, audio_segments):
    if msg.note in notes:
        audio_segments.append(notes.pop(msg.note))

async def midi_to_mp3(midi_file_path, mp3_file_path):
    mid = mido.MidiFile(midi_file_path)
    tempo = 500000 
    for msg in mid.tracks[0]:
        if msg.type == 'set_tempo':
            tempo = msg.tempo
    sample_rate = 44100
    audio_segments = []
    notes = {}
    current_time = 0

    tasks = []
    for track in mid.tracks:
        for msg in track:
            current_time += mido.tick2second(msg.time, mid.ticks_per_beat, tempo)
            if msg.type == 'note_on' and msg.velocity > 0:
                tasks.append(process_note_on(msg, current_time, notes))
            elif msg.type in ('note_off', 'note_on') and msg.velocity == 0:
                tasks.append(process_note_off(msg, notes, audio_segments))

    await asyncio.gather(*tasks)

    combined_audio = AudioSegment.silent(duration=0)
    combined_audio = combined_audio.set_frame_rate(sample_rate)
    combined_audio += sum(audio_segments, AudioSegment.silent(duration=0))
    combined_audio.export(mp3_file_path, format="mp3")

if __name__ == "__main__":
    print("正在运行")
    midi_path = "midi_songs\\AT.mid"
    mp3_path  = "资料\\music\\AT.mp3"
    asyncio.run(midi_to_mp3(midi_path, mp3_path))
    print("运行结束")