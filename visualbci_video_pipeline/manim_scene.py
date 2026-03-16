from __future__ import annotations

import math

from manim import (
    AnimationGroup,
    Circle,
    Create,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    Group,
    LaggedStart,
    LEFT,
    Line,
    MovingCameraScene,
    ReplacementTransform,
    Succession,
    Text,
    TracedPath,
    UP,
    ValueTracker,
    VGroup,
    always_redraw,
    config,
    rate_functions,
)


config.background_color = "#0f0f1a"
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

CYAN = "#00d4ff"
GREEN = "#50fa7b"
GOLD = "#ffd700"
WHITE = "#f8fbff"

SAFE_TOP = 2.9
SAFE_WIDTH = 5.2


def headline_block(title: str, kicker: str) -> VGroup:
    title_text = Text(
        title,
        color=WHITE,
        font_size=42,
        weight="BOLD",
        line_spacing=0.9,
    )
    title_text.set_max_width(SAFE_WIDTH)
    kicker_text = Text(
        kicker,
        color=GOLD,
        font_size=24,
        weight="MEDIUM",
        line_spacing=0.9,
    )
    kicker_text.set_max_width(SAFE_WIDTH)
    block = VGroup(title_text, kicker_text).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    block.to_edge(UP, buff=0.55)
    block.shift(LEFT * 0.6)
    return block


def glow_dot(x: float, y: float, color: str, radius: float = 0.08) -> Dot:
    return Dot(point=[x, y, 0], radius=radius, color=color, fill_opacity=1.0, stroke_width=0)


def wave_group(width: float, baseline: float, amplitude: float, color: str, phase: float = 0.0) -> VGroup:
    samples = []
    for idx in range(80):
        progress = idx / 79
        x = -width / 2 + progress * width
        y = baseline + math.sin(progress * math.tau * 3 + phase) * amplitude
        samples.append([x, y, 0])
    lines = VGroup()
    for start, end in zip(samples, samples[1:]):
        segment = Line(start, end, stroke_color=color, stroke_width=4)
        lines.add(segment)
    return lines


def neuron_cluster() -> VGroup:
    nodes = [
        glow_dot(-1.3, 1.0, CYAN, 0.12),
        glow_dot(-0.5, 1.6, GREEN, 0.11),
        glow_dot(0.6, 1.1, CYAN, 0.10),
        glow_dot(-1.0, 0.0, GOLD, 0.10),
        glow_dot(0.2, 0.3, GREEN, 0.12),
        glow_dot(1.0, -0.4, CYAN, 0.12),
        glow_dot(-0.2, -1.1, GOLD, 0.09),
        glow_dot(1.2, -1.2, GREEN, 0.10),
    ]
    edges = [(0, 1), (1, 2), (0, 3), (3, 4), (4, 5), (4, 6), (5, 7), (6, 7), (2, 4)]
    lines = VGroup()
    for a, b in edges:
        line = Line(nodes[a].get_center(), nodes[b].get_center(), stroke_color=CYAN, stroke_opacity=0.45, stroke_width=2.5)
        lines.add(line)
    return VGroup(lines, *nodes)


def brain_shell() -> VGroup:
    left = Circle(radius=1.6, color=CYAN, stroke_width=5).stretch(1.2, 1).shift([-0.75, 0.0, 0])
    right = Circle(radius=1.55, color=GREEN, stroke_width=5).stretch(1.15, 1).shift([0.8, 0.0, 0])
    bridge = Line([-0.05, -1.6, 0], [0.05, 1.6, 0], stroke_color=GOLD, stroke_width=3, stroke_opacity=0.5)
    return VGroup(left, right, bridge).scale(0.85)


class BrainBaseScene(MovingCameraScene):
    def intro_title(self, title: str, kicker: str) -> VGroup:
        block = headline_block(title, kicker)
        title_text = block[0]
        kicker_text = block[1]
        self.play(FadeIn(title_text, shift=UP * 0.2), FadeIn(kicker_text, shift=UP * 0.15), run_time=0.6)
        return block


class BeginnerMistakeScene(BrainBaseScene):
    def construct(self) -> None:
        labels = self.intro_title("The EEG Mistake Beginners Always Make", "Noise can look convincing")

        shell = brain_shell().scale(0.92).shift([0.3, -0.2, 0])
        noisy_wave = wave_group(4.8, 0.0, 0.65, CYAN, 0.0).shift([0.0, 0.75, 0])
        clean_wave = wave_group(4.8, 0.0, 0.18, GOLD, 0.9).shift([0.0, -2.05, 0])
        burst = VGroup(
            glow_dot(-2.0, 0.8, CYAN, 0.12),
            glow_dot(0.2, 1.25, GREEN, 0.12),
            glow_dot(-0.9, -0.2, GOLD, 0.12),
        )

        self.play(LaggedStart(*[FadeIn(mob, scale=0.8) for mob in [shell, noisy_wave, clean_wave]], lag_ratio=0.15), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(dot, scale=0.5) for dot in burst], lag_ratio=0.1), run_time=0.5)
        self.play(noisy_wave.animate.set_stroke(opacity=0.25), clean_wave.animate.set_stroke(width=6, opacity=1.0), run_time=1.0)
        self.play(FadeOut(burst), run_time=0.4)
        self.wait(5.0)
        self.play(FadeOut(VGroup(labels, shell, noisy_wave, clean_wave)), run_time=0.6)


class BrainElectricityScene(BrainBaseScene):
    def construct(self) -> None:
        labels = self.intro_title("Your Brain Produces Electricity", "Tiny pulses. Constant motion.")
        mesh = neuron_cluster().scale(0.9).shift([0.15, -0.05, 0])

        pulse = ValueTracker(-2.5)
        runner = always_redraw(lambda: glow_dot(pulse.get_value(), -2.5, GOLD, 0.11))
        path = Line([-2.5, -2.5, 0], [2.2, -2.5, 0], stroke_color=CYAN, stroke_width=3, stroke_opacity=0.35)
        trace = TracedPath(runner.get_center, stroke_color=GOLD, stroke_width=5, dissipating_time=0.4)
        waves = VGroup(
            wave_group(4.6, 0.7, 0.22, CYAN, 0.0).shift([0.0, 0.0, 0]),
            wave_group(4.6, 0.0, 0.18, GREEN, 1.2).shift([0.0, 0.0, 0]),
            wave_group(4.6, -0.7, 0.26, GOLD, 2.2).shift([0.0, 0.0, 0]),
        )

        self.add(trace)
        self.play(FadeIn(mesh), FadeIn(path), FadeIn(waves), FadeIn(runner), run_time=1.0)
        self.play(pulse.animate.set_value(2.2), run_time=2.0, rate_func=rate_functions.linear)
        self.play(LaggedStart(*[mob.animate.scale(1.02) for mob in mesh[1:]], lag_ratio=0.06), run_time=1.0)
        self.wait(4.5)
        self.play(FadeOut(VGroup(labels, mesh, path, waves, runner, trace)), run_time=0.6)


class NoPhDScene(BrainBaseScene):
    def construct(self) -> None:
        labels = self.intro_title("You Don't Need a PhD", "Patterns first. Complexity later.")

        shell = brain_shell().scale(0.82).shift([0.3, 0.25, 0])
        raw = wave_group(4.6, 0.75, 0.35, CYAN, 0.2).shift([0.0, -0.25, 0])
        refined = wave_group(4.6, -0.05, 0.20, GREEN, 1.3).shift([0.0, -0.25, 0])
        insight = wave_group(4.6, -0.85, 0.12, GOLD, 2.4).shift([0.0, -0.25, 0])
        symbols = VGroup(
            Text("ALPHA", color=CYAN, font_size=28, weight="BOLD").move_to([0.0, 0.95, 0]),
            Text("BETA", color=GREEN, font_size=28, weight="BOLD").move_to([1.35, 0.05, 0]),
            Text("GAMMA", color=GOLD, font_size=28, weight="BOLD").move_to([0.55, -1.0, 0]),
        )

        self.play(FadeIn(shell), FadeIn(raw), FadeIn(refined), run_time=1.0)
        self.play(FadeIn(symbols), run_time=0.8)
        self.play(ReplacementTransform(raw.copy(), insight), run_time=1.0)
        self.wait(5.2)
        self.play(FadeOut(VGroup(labels, shell, raw, refined, insight, symbols)), run_time=0.6)
