import Vision
import CoreImage
import AppKit
// swift frei.swift <eingabe> <ausgabe.png>: Hauptmotiv freistellen (Vision, auf dem Rechner, ohne Netz)
let a = CommandLine.arguments
let ci = CIImage(contentsOf: URL(fileURLWithPath: a[1]))!
let req = VNGenerateForegroundInstanceMaskRequest()
let h = VNImageRequestHandler(ciImage: ci)
try! h.perform([req])
guard let r = req.results?.first else { print("keins"); exit(1) }
let buf = try! r.generateMaskedImage(ofInstances: r.allInstances, from: h, croppedToInstancesExtent: false)
let out = CIImage(cvPixelBuffer: buf)
let ctx = CIContext()
try! ctx.writePNGRepresentation(of: out, to: URL(fileURLWithPath: a[2]), format: .RGBA8, colorSpace: CGColorSpaceCreateDeviceRGB())
print("ok", r.allInstances.count)
