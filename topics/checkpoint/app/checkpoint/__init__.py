"""Checkpoint research companion. Expression cues are never treated as mood labels."""

# Disable the problematic MSMF hardware transform path before importing OpenCV.
# Applies only to this process; DirectShow is still our first Windows camera API.
import os
import sys
if sys.platform == 'win32':
    os.environ.setdefault('OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS', '0')
