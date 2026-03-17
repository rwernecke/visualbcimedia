const phases = [
  {
    start: 0,
    end: 4000,
    lines: [
      { size: "sm", parts: [{ text: "YOUR " }, { text: "BRAIN", emphasis: true }] },
      { size: "md", parts: [{ text: "PRODUCES" }] },
      { size: "lg", parts: [{ text: "ELECTRICITY", glow: true }] }
    ],
    seed: 1
  },
  {
    start: 4000,
    end: 8000,
    lines: [
      { size: "sm", parts: [{ text: "EEG LETS US" }] },
      { size: "md", parts: [{ text: "SEE", emphasis: true }, { text: " THOSE" }] },
      { size: "lg", parts: [{ text: "SIGNALS", glow: true }] }
    ],
    seed: 2
  },
  {
    start: 8000,
    end: 12000,
    lines: [
      { size: "sm", parts: [{ text: "LEARN TO READ" }] },
      { size: "lg", parts: [{ text: "BRAIN WAVES", emphasis: true }] },
      { size: "md", parts: [{ text: "AT VISUALBCI", glow: true }] }
    ],
    seed: 3
  }
];

const durationMs = 12000;
const lines = [
  document.getElementById("line-1"),
  document.getElementById("line-2"),
  document.getElementById("line-3")
];
const signalLine = document.getElementById("signal-line");
const signalGlow = document.getElementById("signal-glow");
let activePhase = -1;

function buildSignalPath(seed) {
  const width = 900;
  const height = 600;
  const baseY = 330;
  const count = 18;
  const step = width / count;
  const points = [];

  for (let i = 0; i <= count; i += 1) {
    const x = i * step;
    const primary = Math.sin((i + seed * 0.8) * 0.82) * 38;
    const secondary = Math.cos((i + seed * 0.4) * 1.48) * 20;
    const spike = i % 6 === 0 ? Math.sin((i + seed) * 2) * 30 : 0;
    const y = baseY + primary + secondary + spike;
    points.push([x, Math.max(160, Math.min(height - 92, y))]);
  }

  let path = `M ${points[0][0]} ${points[0][1]}`;
  for (let i = 1; i < points.length; i += 1) {
    const previous = points[i - 1];
    const current = points[i];
    const cx1 = previous[0] + step * 0.34;
    const cx2 = current[0] - step * 0.34;
    path += ` C ${cx1} ${previous[1]}, ${cx2} ${current[1]}, ${current[0]} ${current[1]}`;
  }
  return path;
}

function renderLine(target, config) {
  target.className = `line is-visible size-${config.size}`;
  target.innerHTML = "";
  config.parts.forEach((part) => {
    const span = document.createElement("span");
    span.textContent = part.text;
    if (part.emphasis) span.classList.add("emphasis");
    if (part.glow) span.classList.add("glow");
    target.appendChild(span);
  });
}

function transitionOut() {
  lines.forEach((line) => {
    if (!line.textContent) return;
    line.classList.remove("is-visible");
    line.classList.add("is-exiting");
  });
}

function renderPhase(index) {
  const phase = phases[index];
  transitionOut();

  window.setTimeout(() => {
    phase.lines.forEach((line, i) => renderLine(lines[i], line));
  }, 140);

  const path = buildSignalPath(phase.seed);
  signalLine.setAttribute("d", path);
  signalGlow.setAttribute("d", path);
}

function tick(startTime) {
  const elapsed = (performance.now() - startTime) % durationMs;
  const next = phases.findIndex((phase) => elapsed >= phase.start && elapsed < phase.end);

  if (next !== -1 && next !== activePhase) {
    activePhase = next;
    renderPhase(next);
  }

  window.requestAnimationFrame(() => tick(startTime));
}

renderPhase(0);
activePhase = 0;
window.requestAnimationFrame(() => tick(performance.now()));
