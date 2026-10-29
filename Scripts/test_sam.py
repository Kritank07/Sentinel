from sentinel.segment import segment, highlight

IMAGE = "samples/videocall.png"      # any image with a face (AI-generated preferred)
boxes = segment(IMAGE, "face")
print(f"Found {len(boxes)}:", boxes)
if boxes:
    print("Saved", highlight(IMAGE, boxes, "samples/videocall_highlighted.png"))