from collections import defaultdict

import matplotlib.pyplot as plt

from hrv.classical import time_domain
from hrv.rri import RRi


__all__ = ["time_varying"]


class TimeVarying:
    def __init__(self, results, rri_segments):
        self.results = results
        self.transponsed = self._transform_results(results)
        self.rri_segments = rri_segments

    def _transform_results(self, results):
        return {
            key: [item[key] for item in results] for key in results[0].keys()
        }

    def ylabel_mapper(self, index):
        mapper = {
            "rmssd": "RMSSD (ms)",
            "sdnn": "SDNN (ms²)",
            "sdsd": "SDSD (ms²)",
            "nn50": "nn50 (count)",
            "pnn50": "pnn50 (%)",
            "mrri": "mean RRi (ms)",
            "mhr": "mean HR (bpm)",
        }
        return mapper.get(index)

    def __getattr__(self, index):
        try:
            return self.transponsed[index]
        except KeyError:
            raise ValueError(f"index `{index}` does not exist.")

    def plot(self, ax=None, index="rmssd", *args, **kwargs):
        fig = None
        if ax is None:
            fig, ax = plt.subplots(1, 1)

        ax.plot(self.__getattr__(index), *args, **kwargs)
        ax.set(xlabel="Time Interval (s)", ylabel=self.ylabel_mapper(index))
        plt.show(block=False)

        return fig, ax


def time_varying(rri, seg_size, overlap, keep_last=False):
    if not isinstance(rri, RRi):
        rri = RRi(rri)

    segments = rri.time_split(
        seg_size=seg_size,
        overlap=overlap,
        keep_last=keep_last
    )
    results = []
    for segment in segments:
        results.append(time_domain(segment))

    return TimeVarying(results, segments)
