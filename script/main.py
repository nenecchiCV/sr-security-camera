# streamlit run main.py

import streamlit as st
from numpysocket import NumpySocket
import cv2
import time
import numpy as np
from PIL import Image


def main():
    print("start")
    start = time.time()
    st.markdown("# Camera")
    np_sock = NumpySocket()
    np_sock.startServer(41234)
    time_loc = st.empty()
    image_loc = st.empty()

    while True:
        image_raw = np_sock.recieve()
        time_loc.text(str(time.time() - start))
        image_rgb = Image.fromarray(cv2.cvtColor(image_raw, cv2.COLOR_BGR2RGB))
        image_loc.image(image_rgb)

        if cv2.waitKey() & 0xFF == ord("q"):
            break

    np_sock.close()


if __name__ == "__main__":
    main()
