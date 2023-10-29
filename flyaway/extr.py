import wave
from tqdm import tqdm

def extract_bin_from_morse():
    ret = b''

    with open("morse", "r") as morse_f:
        morse = morse_f.readline()

        for i in range(len(morse)//8):
            curr = 0

            for j in range(8):
                curr |= ((0 if morse[i*8+j]=='-' else 1) << (j))

            ret += curr.to_bytes()

    print(ret)

    with open("test", "wb") as out_f:
        out_f.write(ret)


def extract_duration():
    msg = ''
    prev_up = True
    curr_signal = ''

    for frm in tqdm(range(audio_file.getnframes()//5)):
        frames = audio_file.readframes(5)

        # Low
        if frames[:2] == b'\x01\x80':

            # First low
            if prev_up:
                msg += curr_signal
                curr_signal = '.'

            # Second low
            else:
                curr_signal = '-'

            prev_up = False

        # High
        else:

            # First high
            if not prev_up:
                msg += curr_signal
                curr_signal = '.'

            # Second high
            else:
                curr_signal = '-'

            prev_up = True

    print(msg)
    print(len(msg))

#extract_duration()
extract_bin_from_morse()
