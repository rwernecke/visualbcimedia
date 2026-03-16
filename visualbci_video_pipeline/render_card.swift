import AppKit
import Foundation
import CoreGraphics

struct Spec: Decodable {
    let mode: String
    let title: String?
    let body: String?
    let accent: String?
    let words: [String]?
    let highlightIndex: Int?

    enum CodingKeys: String, CodingKey {
        case mode
        case title
        case body
        case accent
        case words
        case highlightIndex = "highlight_index"
    }
}

func paragraph(alignment: NSTextAlignment, lineSpacing: CGFloat = 6) -> NSMutableParagraphStyle {
    let style = NSMutableParagraphStyle()
    style.alignment = alignment
    style.lineSpacing = lineSpacing
    style.lineBreakMode = .byWordWrapping
    return style
}

func fillRoundedRect(_ rect: NSRect, radius: CGFloat, color: NSColor) {
    let path = NSBezierPath(roundedRect: rect, xRadius: radius, yRadius: radius)
    color.setFill()
    path.fill()
}

func strokeRoundedRect(_ rect: NSRect, radius: CGFloat, color: NSColor, lineWidth: CGFloat) {
    let path = NSBezierPath(roundedRect: rect, xRadius: radius, yRadius: radius)
    path.lineWidth = lineWidth
    color.setStroke()
    path.stroke()
}

func drawWave(in rect: NSRect, color: NSColor, baseline: CGFloat, amplitude: CGFloat, cycles: CGFloat, lineWidth: CGFloat) {
    let path = NSBezierPath()
    path.lineWidth = lineWidth
    let steps = 80
    for step in 0...steps {
        let progress = CGFloat(step) / CGFloat(steps)
        let x = rect.minX + rect.width * progress
        let y = baseline + sin(progress * .pi * 2 * cycles) * amplitude
        if step == 0 {
            path.move(to: NSPoint(x: x, y: y))
        } else {
            path.line(to: NSPoint(x: x, y: y))
        }
    }
    color.setStroke()
    path.stroke()
}

func drawBarChart(in rect: NSRect, values: [CGFloat], colors: [NSColor]) {
    let gap: CGFloat = 14
    let totalGap = gap * CGFloat(max(values.count - 1, 0))
    let barWidth = (rect.width - totalGap) / CGFloat(max(values.count, 1))
    for (index, value) in values.enumerated() {
        let height = max(rect.height * value, 12)
        let x = rect.minX + CGFloat(index) * (barWidth + gap)
        let barRect = NSRect(x: x, y: rect.minY, width: barWidth, height: height)
        fillRoundedRect(barRect, radius: 10, color: colors[index % colors.count])
    }
}

func glow(color: NSColor, radius: CGFloat) -> NSShadow {
    let shadow = NSShadow()
    shadow.shadowBlurRadius = radius
    shadow.shadowOffset = .zero
    shadow.shadowColor = color
    return shadow
}

func drawNeuralMesh(in frame: NSRect) {
    let cyan = NSColor(calibratedRed: 0 / 255, green: 212 / 255, blue: 255 / 255, alpha: 1)
    let green = NSColor(calibratedRed: 80 / 255, green: 250 / 255, blue: 123 / 255, alpha: 1)
    let gold = NSColor(calibratedRed: 1.0, green: 215 / 255, blue: 0, alpha: 1)
    let mint = NSColor(calibratedRed: 94 / 255, green: 239 / 255, blue: 180 / 255, alpha: 1)
    let white = NSColor.white
    let panel = NSRect(x: 1110, y: 150, width: 650, height: 700)

    fillRoundedRect(panel, radius: 42, color: NSColor(calibratedWhite: 1, alpha: 0.04))
    strokeRoundedRect(panel, radius: 42, color: white.withAlphaComponent(0.08), lineWidth: 2)

    let headerAttrs: [NSAttributedString.Key: Any] = [
        .font: NSFont(name: "Avenir Next Demi Bold", size: 28) ?? NSFont.systemFont(ofSize: 28, weight: .semibold),
        .foregroundColor: white,
    ]
    let subAttrs: [NSAttributedString.Key: Any] = [
        .font: NSFont(name: "Avenir Next Medium", size: 18) ?? NSFont.systemFont(ofSize: 18, weight: .medium),
        .foregroundColor: cyan,
    ]
    let smallAttrs: [NSAttributedString.Key: Any] = [
        .font: NSFont(name: "Avenir Next Medium", size: 16) ?? NSFont.systemFont(ofSize: 16, weight: .medium),
        .foregroundColor: white.withAlphaComponent(0.72),
    ]

    NSString(string: "Neural Field").draw(in: NSRect(x: 1160, y: 760, width: 260, height: 30), withAttributes: headerAttrs)
    NSString(string: "Live electric patterns").draw(in: NSRect(x: 1160, y: 730, width: 260, height: 24), withAttributes: subAttrs)

    let chips = [
        (text: "Signal", color: green),
        (text: "Synapse", color: gold),
        (text: "Rhythm", color: cyan),
    ]
    for (index, chip) in chips.enumerated() {
        let chipRect = NSRect(x: 1160 + CGFloat(index) * 112, y: 686, width: 96, height: 34)
        fillRoundedRect(chipRect, radius: 17, color: chip.color.withAlphaComponent(0.16))
        NSString(string: chip.text).draw(in: chipRect.insetBy(dx: 10, dy: 7), withAttributes: smallAttrs)
    }

    let traceRect = NSRect(x: 1160, y: 470, width: 560, height: 180)
    fillRoundedRect(traceRect, radius: 24, color: NSColor(calibratedWhite: 0, alpha: 0.20))
    strokeRoundedRect(traceRect, radius: 24, color: white.withAlphaComponent(0.06), lineWidth: 1.5)
    NSString(string: "Electric waves").draw(in: NSRect(x: 1184, y: 618, width: 160, height: 22), withAttributes: smallAttrs)
    for idx in 0..<4 {
        let rowY = traceRect.minY + 28 + CGFloat(idx) * 34
        let lineRect = NSRect(x: traceRect.minX + 22, y: rowY - 8, width: traceRect.width - 44, height: 20)
        drawWave(
            in: lineRect,
            color: idx == 1 ? gold : cyan.withAlphaComponent(0.95),
            baseline: rowY,
            amplitude: idx == 1 ? 9 : 6,
            cycles: CGFloat(4 + idx),
            lineWidth: 2.4
        )
    }

    let brainRect = NSRect(x: 1165, y: 220, width: 285, height: 205)
    fillRoundedRect(brainRect, radius: 24, color: NSColor(calibratedWhite: 0, alpha: 0.20))
    strokeRoundedRect(brainRect, radius: 24, color: white.withAlphaComponent(0.06), lineWidth: 1.5)
    NSString(string: "Brain map").draw(in: NSRect(x: 1188, y: 390, width: 120, height: 22), withAttributes: smallAttrs)
    let lobes = [
        (rect: NSRect(x: 1212, y: 278, width: 78, height: 108), color: cyan.withAlphaComponent(0.22)),
        (rect: NSRect(x: 1284, y: 290, width: 88, height: 96), color: green.withAlphaComponent(0.20)),
        (rect: NSRect(x: 1358, y: 278, width: 52, height: 84), color: gold.withAlphaComponent(0.24)),
    ]
    for lobe in lobes {
        fillRoundedRect(lobe.rect, radius: 26, color: lobe.color)
    }
    for point in [
        NSPoint(x: 1240, y: 350), NSPoint(x: 1260, y: 310), NSPoint(x: 1310, y: 360),
        NSPoint(x: 1334, y: 322), NSPoint(x: 1378, y: 330)
    ] {
        let orb = NSRect(x: point.x, y: point.y, width: 12, height: 12)
        fillRoundedRect(orb, radius: 6, color: white)
    }

    let powerRect = NSRect(x: 1490, y: 250, width: 230, height: 180)
    fillRoundedRect(powerRect, radius: 24, color: NSColor(calibratedWhite: 0, alpha: 0.20))
    strokeRoundedRect(powerRect, radius: 24, color: white.withAlphaComponent(0.06), lineWidth: 1.5)
    NSString(string: "Pulse energy").draw(in: NSRect(x: 1514, y: 396, width: 120, height: 22), withAttributes: smallAttrs)
    drawBarChart(
        in: NSRect(x: 1514, y: 276, width: 180, height: 96),
        values: [0.45, 0.82, 0.64, 0.38],
        colors: [cyan.withAlphaComponent(0.85), gold.withAlphaComponent(0.85), mint.withAlphaComponent(0.85), white.withAlphaComponent(0.6)]
    )
}

func drawSlide(spec: Spec, in frame: NSRect) {
    let bg = NSColor(calibratedRed: 15 / 255, green: 15 / 255, blue: 26 / 255, alpha: 1)
    bg.setFill()
    frame.fill()

    let cyan = NSColor(calibratedRed: 0 / 255, green: 212 / 255, blue: 255 / 255, alpha: 1)
    let green = NSColor(calibratedRed: 80 / 255, green: 250 / 255, blue: 123 / 255, alpha: 1)
    let gold = NSColor(calibratedRed: 1.0, green: 215 / 255, blue: 0, alpha: 1)
    let white = NSColor.white

    fillRoundedRect(NSRect(x: 120, y: 110, width: 1680, height: 860), radius: 42, color: NSColor(calibratedWhite: 1, alpha: 0.03))
    fillRoundedRect(NSRect(x: 120, y: 870, width: 420, height: 8), radius: 4, color: cyan)
    fillRoundedRect(NSRect(x: 1360, y: 870, width: 320, height: 8), radius: 4, color: gold.withAlphaComponent(0.65))
    fillRoundedRect(NSRect(x: 1500, y: 170, width: 220, height: 220), radius: 110, color: cyan.withAlphaComponent(0.08))
    fillRoundedRect(NSRect(x: 1320, y: 600, width: 280, height: 280), radius: 140, color: green.withAlphaComponent(0.06))
    fillRoundedRect(NSRect(x: 1490, y: 500, width: 120, height: 120), radius: 60, color: gold.withAlphaComponent(0.08))
    drawNeuralMesh(in: frame)

    let titleAttrs: [NSAttributedString.Key: Any] = [
        .font: NSFont(name: "Avenir Next Demi Bold", size: 58) ?? NSFont.systemFont(ofSize: 58, weight: .semibold),
        .foregroundColor: white,
        .paragraphStyle: paragraph(alignment: .left, lineSpacing: 10),
    ]
    let bodyAttrs: [NSAttributedString.Key: Any] = [
        .font: NSFont(name: "Avenir Next Regular", size: 34) ?? NSFont.systemFont(ofSize: 34),
        .foregroundColor: white.withAlphaComponent(0.92),
        .paragraphStyle: paragraph(alignment: .left, lineSpacing: 10),
    ]
    let accentAttrs: [NSAttributedString.Key: Any] = [
        .font: NSFont(name: "Avenir Next Medium", size: 26) ?? NSFont.systemFont(ofSize: 26, weight: .medium),
        .foregroundColor: cyan,
        .paragraphStyle: paragraph(alignment: .left, lineSpacing: 8),
    ]
    let labelAttrs: [NSAttributedString.Key: Any] = [
        .font: NSFont(name: "Avenir Next Medium", size: 20) ?? NSFont.systemFont(ofSize: 20, weight: .medium),
        .foregroundColor: gold,
    ]

    NSString(string: "BRAIN SIGNALS").draw(in: NSRect(x: 160, y: 800, width: 600, height: 32), withAttributes: labelAttrs)
    NSString(string: spec.title ?? "").draw(in: NSRect(x: 160, y: 655, width: 960, height: 130), withAttributes: titleAttrs)
    NSString(string: spec.body ?? "").draw(in: NSRect(x: 160, y: 365, width: 940, height: 250), withAttributes: bodyAttrs)
    NSString(string: spec.accent ?? "").draw(in: NSRect(x: 160, y: 220, width: 940, height: 120), withAttributes: accentAttrs)
}

func drawCaption(spec: Spec, in frame: NSRect) {
    NSColor.clear.setFill()
    frame.fill()

    let cyan = NSColor(calibratedRed: 0 / 255, green: 212 / 255, blue: 255 / 255, alpha: 1)
    let white = NSColor.white
    let shadow = NSShadow()
    shadow.shadowBlurRadius = 10
    shadow.shadowOffset = NSSize(width: 0, height: -2)
    shadow.shadowColor = NSColor.black.withAlphaComponent(0.6)

    let box = NSRect(x: 40, y: 10, width: frame.width - 80, height: frame.height - 20)
    fillRoundedRect(box, radius: 26, color: NSColor(calibratedWhite: 0, alpha: 0.58))

    let words = spec.words ?? []
    let highlight = spec.highlightIndex ?? 0
    let attr = NSMutableAttributedString()
    for (index, word) in words.enumerated() {
        let color = index == highlight ? cyan : white
        let chunk = NSAttributedString(
            string: index == words.count - 1 ? word : "\(word) ",
            attributes: [
                .font: NSFont(name: "Gill Sans Bold", size: 48) ?? NSFont.systemFont(ofSize: 48, weight: .bold),
                .foregroundColor: color,
                .shadow: shadow,
            ]
        )
        attr.append(chunk)
    }

    let line = CTLineCreateWithAttributedString(attr)
    let bounds = CTLineGetBoundsWithOptions(line, .useOpticalBounds)
    let drawRect = NSRect(
        x: (frame.width - bounds.width) / 2,
        y: (frame.height - bounds.height) / 2 - 8,
        width: bounds.width,
        height: bounds.height + 16
    )
    attr.draw(in: drawRect)
}

let arguments = CommandLine.arguments
guard arguments.count == 3 else {
    fputs("usage: swift render_card.swift spec.json output.png\n", stderr)
    exit(1)
}

let specURL = URL(fileURLWithPath: arguments[1])
let outputURL = URL(fileURLWithPath: arguments[2])
let data = try Data(contentsOf: specURL)
let spec = try JSONDecoder().decode(Spec.self, from: data)

let size: NSSize = spec.mode == "caption" ? NSSize(width: 1200, height: 180) : NSSize(width: 1920, height: 1080)
let image = NSImage(size: size)
image.lockFocus()

let frame = NSRect(origin: .zero, size: size)
if spec.mode == "caption" {
    drawCaption(spec: spec, in: frame)
} else {
    drawSlide(spec: spec, in: frame)
}

image.unlockFocus()

guard
    let tiff = image.tiffRepresentation,
    let rep = NSBitmapImageRep(data: tiff),
    let png = rep.representation(using: .png, properties: [:])
else {
    fputs("failed to render png\n", stderr)
    exit(1)
}

try png.write(to: outputURL)
