import os
from pocketsphinx import LiveSpeech, get_model_path

model_path = get_model_path()
print(model_path)

def main():
    speech = LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        hmm= os.path.join(model_path, 'es-Mx'),
        lm= os.path.join(model_path, 'es-Mx.lm.bin'),
        dict= os.path.join(model_path, 'bocina.dic')
    )

    for phrase in speech:
        print(phrase)
        return 0

