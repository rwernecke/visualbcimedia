from __future__ import annotations

TOPIC = "Viral Brain Reels"

SEGMENTS = [
    {
        "id": "beginner_mistake",
        "title": "Your Brain Can Fake a Signal",
        "target_seconds": 8,
        "hook": "This is why fake brain signals fool people.",
        "text": (
            "Your brain can fake a signal that looks intense, dramatic, and completely real. "
            "Sometimes the most exciting brain wave on screen is just noise wearing a costume."
        ),
        "visual": (
            "Start with a cinematic sci-fi brain in a storm of neon signal lines, then strip away the chaos until only one clean golden pulse remains."
        ),
        "image_prompt": (
            "A hyper-detailed cinematic sci-fi human brain floating in darkness, neon cyan and emerald electrical storms, "
            "gold signal thread, glossy biomechanical texture, volumetric glow, premium Instagram reel background, no text, vertical composition"
        ),
    },
    {
        "id": "brain_electricity",
        "title": "Your Brain Produces Electricity",
        "target_seconds": 8,
        "hook": "Your thoughts run on electricity.",
        "text": (
            "Your thoughts run on electricity. Tiny flashes race across your brain every second, like a living city lighting up from the inside."
        ),
        "visual": (
            "Show a luminous sci-fi brain igniting from the inside with branching neurons, glowing synapses, and waves racing through a dark futuristic void."
        ),
        "image_prompt": (
            "An epic futuristic brain made of light, glowing neural pathways, bright cyan and green electricity, gold highlights, "
            "deep dark background, cinematic science fiction style, ultra detailed, premium social media artwork, vertical"
        ),
    },
    {
        "id": "no_phd",
        "title": "You Do Not Need a PhD",
        "target_seconds": 8,
        "hook": "Reading brain patterns is easier than people think.",
        "text": (
            "Reading brain patterns is easier than people think. You do not need a genius IQ, you just need to notice what changes, what repeats, and what lights up."
        ),
        "visual": (
            "Show an elegant sci-fi brain interface where glowing regions activate and patterns snap together like a futuristic puzzle."
        ),
        "image_prompt": (
            "A stunning futuristic brain interface with glowing regions, floating data patterns, neon cyan green and gold lighting, "
            "cinematic sci-fi medical visualization, beautiful for viral reels, no text, vertical aspect ratio"
        ),
    },
]

REELS = [
    {
        "id": "reel_01",
        "title": "One EEG Mistake Almost Every Beginner Makes",
        "segment_ids": ["beginner_mistake"],
    },
    {
        "id": "reel_02",
        "title": "Your Brain Produces Electricity",
        "segment_ids": ["brain_electricity"],
    },
    {
        "id": "reel_03",
        "title": "You Don't Need a PhD to Analyze EEG",
        "segment_ids": ["no_phd"],
    },
]
