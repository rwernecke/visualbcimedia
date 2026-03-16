from __future__ import annotations

TOPIC = "What is EEG?"

SEGMENTS = [
    {
        "id": "hook",
        "title": "Hook",
        "target_seconds": 10,
        "text": (
            "What if we could watch the brain think in real time? "
            "Electroencephalography, or EEG, gives us a window into the "
            "electrical rhythms of the brain."
        ),
        "visual": "Open with a dark background, glowing head outline, and animated waveform pulses.",
    },
    {
        "id": "measurements",
        "title": "What EEG Measures",
        "target_seconds": 20,
        "text": (
            "EEG measures tiny voltage changes at the scalp caused by large groups "
            "of neurons firing together. Electrodes do not read thoughts directly. "
            "They detect synchronized electrical activity."
        ),
        "visual": "Show scalp electrodes, cortex activity, and signal lines traveling to a monitor.",
    },
    {
        "id": "brain_waves",
        "title": "Brain Waves Overview",
        "target_seconds": 20,
        "text": (
            "These signals are often grouped into brain wave bands like delta, theta, "
            "alpha, beta, and gamma. Each band is linked with different states such as "
            "sleep, relaxation, focus, and active processing."
        ),
        "visual": "Introduce five glowing wave bands with labels and frequency ranges.",
    },
    {
        "id": "importance",
        "title": "Why EEG Matters",
        "target_seconds": 20,
        "text": (
            "EEG matters because it is noninvasive, fast, and useful in medicine, "
            "research, and brain-computer interfaces. It helps us study attention, "
            "detect seizures, and build systems that respond to brain activity."
        ),
        "visual": "End with split panels for clinic, research lab, and BCI interface.",
    },
]

REELS = [
    {
        "id": "reel_01",
        "title": "EEG Hook",
        "segment_ids": ["hook"],
    },
    {
        "id": "reel_02",
        "title": "What EEG Measures",
        "segment_ids": ["measurements"],
    },
    {
        "id": "reel_03",
        "title": "Why EEG Matters",
        "segment_ids": ["importance"],
    },
]
