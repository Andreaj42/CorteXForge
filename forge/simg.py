import numpy as np
import sigmf
from sigmf import SigMFFile
from sigmf.utils import get_data_type_str
import os

num_samples = 100_000
sample_rate = 1e6
center_freq = 2.45e9

data_filename = "/cortexlab/homes/andrea_joly/random_sigmf/random.sigmf-data"
meta_filename = "/cortexlab/homes/andrea_joly/random_sigmf/random.sigmf-meta"

iq = (np.random.randn(num_samples) + 1j * np.random.randn(num_samples)).astype(np.complex64)

iq.tofile(data_filename)

sigmf_obj = SigMFFile(
    data_file=data_filename,
    global_info={
        SigMFFile.DATATYPE_KEY: get_data_type_str(iq),  # ex: 'cf32_le'
        SigMFFile.SAMPLE_RATE_KEY: sample_rate,
        SigMFFile.AUTHOR_KEY: "andrea_joly",
        SigMFFile.DESCRIPTION_KEY: "Random IQ test for SigMF (bruit complexe)",
        SigMFFile.VERSION_KEY: sigmf.__version__,
    },
)

sigmf_obj.add_capture(
    0,
    metadata={
        SigMFFile.FREQUENCY_KEY: center_freq,
    },
)

sigmf_obj.add_annotation(
    start_index=0,
    length=num_samples,
    metadata={
        "test:modulation": "random_noise",
        "test:snr_db": 10,
    },
)

sigmf_obj.tofile(meta_filename)

print(f"Écrit : {data_filename} et {meta_filename}")
