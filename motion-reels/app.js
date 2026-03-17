const phases = [
  {
    start: 0,
    end: 2500,
    lines: [
      {
        size: "sm",
        parts: [
          { text: "YOUR " },
          { text: "BRAIN", emphasis: true }
        ]
      },
      {
        size: "md",
        parts: [{ text: "PRODUCES" }]
      },
      {
        size: "lg",
        parts: [{ text: "ELECTRICITY", glow: true }]
      }
    ],
    signalSeed: 1
  },
  {
    start: 2500,
    end: 5500,
    lines: [
      {
        size: "sm",
        parts: [{ text: "EEG LETS US" }]
      },
      {
        size: "md",
        parts: [
          { text: "SEE", emphasis: true },
          { text: " THOSE" }
        ]
      },
      {
        size: "lg",
        parts: [{ text: "SIGNALS", glow: true }]
      }
    ],
    signalSeed: 2
  },
  {
    start: 5500,
    end: 8000,
    lines: [
      {
        size: "sm",
        parts: [{ text: "LEARN TO READ" }]
      },
      {
        size: "lg",
        parts: [{ text: "BRAIN WAVES", emphasis: true }]
      },
      {
        size: "md",
        parts: [{ text: "AT VISUALBCI", glow: true }]
      }
    ],
    signalSeed: 3
  }
];

const reelDurationMs = 8000;
const lineElements = [
  document.getElementById("line-1"),
  document.getElementById("line-2"),
  document.getElementById("line-3")
];
const copyStack = document.getElementById("copy-stack");
const signalLine = document.getElementById("signal-line");
const signalGlow = document.getElementById("signal-glow");
let activePhaseIndex = -1;

function buildSignalPath(seed) {
  const width = 900;
  const height = 540;
  const baseY = 280;
  const segmentCount = 18;
  const step = width / segmentCount;
  const points = [];

  for (let i = 0; i <= segmentCount; i += 1) {
    const x = i * step;
    const primary = Math.sin((i + seed) * 0.82) * 52;
    const secondary = Math.cos((i + seed * 0.6) * 1.54) * 18;
    const spike = i % 5 === 0 ? Math.sin((i + seed) * 2.2) * 32 : 0;
    const y = baseY + primary + secondary + spike;
    points.push([x, Math.max(80, Math.min(height - 70, y))]);
  }

  let path = `M ${points[0][0]} ${points[0][1]}`;

  for (let i = 1; i < points.length; i += 1) {
    const prev = points[i - 1];
    const current = points[i];
    const cx1 = prev[0] + step * 0.35;
    const cy1 = prev[1];
    const cx2 = current[0] - step * 0.35;
    const cy2 = current[1];
    path += ` C ${cx1} ${cy1}, ${cx2} ${cy2}, ${current[0]} ${current[1]}`;
  }

  return path;
}

function renderLine(target, config) {
  const classNames = ["copy-line", "is-visible", `size-${config.size || "md"}`];

  target.className = classNames.join(" ");
  target.innerHTML = "";

  config.parts.forEach((part) => {
    const span = document.createElement("span");
    span.textContent = part.text;

    if (part.emphasis) {
      span.classList.add("emphasis");
    }

    if (part.glow) {
      span.classList.add("glow-word");
    }

    target.appendChild(span);
  });
}

function exitCurrentLines() {
  lineElements.forEach((line) => {
    if (!line.textContent) {
      return;
    }

    line.classList.remove("is-visible");
    line.classList.add("is-exiting");
  });
}

function renderPhase(phaseIndex) {
  const phase = phases[phaseIndex];

  exitCurrentLines();

  window.setTimeout(() => {
    phase.lines.forEach((line, index) => {
      renderLine(lineElements[index], line);
    });
  }, 120);

  copyStack.dataset.phase = String(phaseIndex);

  const path = buildSignalPath(phase.signalSeed);
  signalLine.setAttribute("d", path);
  signalGlow.setAttribute("d", path);
}

function getPhaseIndex(elapsedMs) {
  return phases.findIndex((phase) => elapsedMs >= phase.start && elapsedMs < phase.end);
}

function tick(startTime) {
  const elapsedMs = (performance.now() - startTime) % reelDurationMs;
  const nextPhaseIndex = getPhaseIndex(elapsedMs);

  if (nextPhaseIndex !== activePhaseIndex && nextPhaseIndex !== -1) {
    activePhaseIndex = nextPhaseIndex;
    renderPhase(activePhaseIndex);
  }

  window.requestAnimationFrame(() => tick(startTime));
}

renderPhase(0);
activePhaseIndex = 0;
window.requestAnimationFrame(() => tick(performance.now()));
