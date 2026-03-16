import AppKit
import Foundation

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

func drawSlide(spec: Spec, in frame: NSRect) {
    let bg = NSColor(calibratedRed: 15 / 255, green: 15 / 255, blue: 26 / 255, alpha: 1)
    bg.setFill()
    frame.fill()

    let cyan = NSColor(calibratedRed: 0 / 255, green: 212 / 255, blue: 255 / 255, alpha: 1)
    let gold = NSColor(calibratedRed: 1.0, green: 215 / 255, blue: 0, alpha: 1)
    let white = NSColor.white

    fillRoundedRect(NSRect(x: 120, y: 110, width: 1680, height: 860), radius: 42, color: NSColor(calibratedWhite: 1, alpha: 0.03))
    fillRoundedRect(NSRect(x: 120, y: 870, width: 420, height: 8), radius: 4, color: cyan)
    fillRoundedRect(NSRect(x: 1360, y: 870, width: 320, height: 8), radius: 4, color: gold.withAlphaComponent(0.65))
    fillRoundedRect(NSRect(x: 1480, y: 150, width: 240, height: 240), radius: 32, color: cyan.withAlphaComponent(0.08))

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

    NSString(string: "VISUALBCI LESSON").draw(in: NSRect(x: 160, y: 800, width: 600, height: 32), withAttributes: labelAttrs)
    NSString(string: spec.title ?? "").draw(in: NSRect(x: 160, y: 655, width: 1240, height: 130), withAttributes: titleAttrs)
    NSString(string: spec.body ?? "").draw(in: NSRect(x: 160, y: 365, width: 1220, height: 250), withAttributes: bodyAttrs)
    NSString(string: spec.accent ?? "").draw(in: NSRect(x: 160, y: 250, width: 1220, height: 80), withAttributes: accentAttrs)
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
