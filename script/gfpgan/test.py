# streamlit run test.py

import streamlit as st
from numpysocket import NumpySocket
import cv2
from narutils import *
import numpy as np
from PIL import Image
from face_detection.face_detector import FaceDetector
from gfpgan import GFPGANer


def main():
    face_detector = FaceDetector(upscale_factor=4, face_size=128)
    # wget https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth
    restorer = GFPGANer(
        model_path="pretrained/GFPGANv1.3.pth",
        upscale=4,
        arch="clean",
        channel_multiplier=2
    )

    print("start")
    st.markdown("# Camera")
    np_sock = NumpySocket()
    np_sock.startServer(41234)
    start = now()
    time_loc = st.empty()
    detect_image_loc = st.empty()
    crop_image_loc = st.empty()

    while True:
        image_raw = np_sock.recieve()
        time_loc.text(str(now(start)))
        cropped_faces, bboxes = face_detector.crop_faces(image_raw)
        if len(cropped_faces) > 0:
            _, restored_faces, _ = restorer.enhance(cropped_faces[0], has_aligned=True)
            restored_face = restored_faces[0]
            # restored_face = (srgan.eval(cropped_faces[0]) * 255).astype(np.uint8)
            detect_img = cv2.drawContours(image_raw, bboxes, -1, (0, 255, 0), thickness=2)
            detect_image_rgb = Image.fromarray(cv2.cvtColor(detect_img, cv2.COLOR_BGR2RGB))
            sr_image_rgb = Image.fromarray(cv2.cvtColor(restored_face, cv2.COLOR_BGR2RGB))
            detect_image_loc.image(detect_image_rgb)
            crop_image_loc.image(sr_image_rgb)

        if cv2.waitKey() & 0xFF == ord("q"):
            break

    np_sock.close()


if __name__ == "__main__":
    main()
