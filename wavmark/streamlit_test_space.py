import time
import wavmark
import streamlit as st
import os
import torch
import datetime
import numpy as np
import soundfile
from wavmark.utils import file_reader
import subprocess
import sys
import time



def my_read_file(audio_path, max_second):
    signal, sr, audio_length_second = file_reader.read_as_single_channel_16k(audio_path, default_sr)
    if audio_length_second > max_second:
        signal = signal[0:default_sr * max_second]
        audio_length_second = max_second

    return signal, sr, audio_length_second


def add_watermark(audio_path, watermark_text):
    #t1 = time.time()
    assert len(watermark_text) == 16
    watermark_npy = np.array([int(i) for i in watermark_text])
    signal, sr, audio_length_second = my_read_file(audio_path, max_second_encode)
    watermarked_signal, _ = wavmark.encode_watermark(model, signal, watermark_npy, show_progress=False)

    tmp_file_name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + "_" + watermark_text + ".wav"
    tmp_file_path = '/tmp/' + tmp_file_name
    soundfile.write(tmp_file_path, watermarked_signal, sr)
    #encode_time_cost = time.time() - t1
    return tmp_file_path

#def encode_water()
    
def decode_watermark(audio_path):
    assert os.path.exists(audio_path)

    #t1 = time.time()
    signal, sr, audio_length_second = my_read_file(audio_path, max_second_decode)
    payload_decoded, _ = wavmark.decode_watermark(model, signal, show_progress=False)
    #decode_cost = time.time() - t1

    if payload_decoded is None:
       #return "No Watermark" , decode_cost
       return "No Watermark"

    payload_decoded_str = "".join([str(i) for i in payload_decoded])
    st.write("Result:", payload_decoded_str)
    #st.write("Time Cost:%d seconds" % (decode_cost))


def create_default_value():
    if "def_value" not in st.session_state:
        def_val_npy = np.random.choice([0, 1], size=32 - len_start_bit)
        def_val_str = "".join([str(i) for i in def_val_npy])
        st.session_state.def_value = def_val_str



def main():
    create_default_value()

    st.title("AudioWaterMarking")
    markdown_text = """
    # Audio WaterMarking
    You can upload an audio file and encode a custom 16-bit watermark or perform decoding from a watermarked audio.
    
    See [WaveMarktoolkit](https://github.com/wavmark/wavmark) for further details.
    """

    st.markdown(markdown_text)

    audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3"], accept_multiple_files=False)

    if audio_file:
        
        tmp_input_audio_file = os.path.join("/tmp/", audio_file.name)
        with open(tmp_input_audio_file, "wb") as f:
            f.write(audio_file.getbuffer())

        
        # st.audio(tmp_input_audio_file, format="audio/wav")

        action = st.selectbox("Select Action", ["Add Watermark", "Decode Watermark"])

        if action == "Add Watermark":
            watermark_text = st.text_input("The watermark (0, 1 list of length-16):", value=st.session_state.def_value)
            add_watermark_button = st.button("Add Watermark", key="add_watermark_btn")
            if add_watermark_button:  
                if audio_file and watermark_text:
                    with st.spinner("Adding Watermark..."):
                        #watermarked_audio, encode_time_cost = add_watermark(tmp_input_audio_file, watermark_text)
                        watermarked_audio = add_watermark(tmp_input_audio_file, watermark_text)
                        st.write("Watermarked Audio:")
                        print("watermarked_audio:", watermarked_audio)
                        st.audio(watermarked_audio, format="audio/wav")
                        #st.write("Time Cost: %d seconds" % encode_time_cost)

        elif action == "Decode Watermark":
            if st.button("Decode"):
                with st.spinner("Decoding..."):
                    decode_watermark(tmp_input_audio_file)


if __name__ == "__main__":
    default_sr = 16000
    max_second_encode = 60
    max_second_decode = 30
    len_start_bit = 16
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    model = wavmark.load_model().to(device)
    main()

   