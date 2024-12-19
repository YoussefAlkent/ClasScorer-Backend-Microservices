import torch
from gazelle.model import get_gazelle_model
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load Gaze-LLE Model
model, transform = get_gazelle_model("gazelle_dinov2_vitl14_inaout")
model.eval()
model.to(device)

def perform_inference(image: Image.Image, bbox: list[float]):
    """
    Perform inference using the Gaze-LLE model.
    """
    input_data = {
        "images": transform(image).unsqueeze(dim=0).to(device),
        "bboxes": [[tuple(bbox)]] if bbox else [[None]]
    }

    with torch.no_grad():
        output = model(input_data)

    heatmap = output["heatmap"][0][0]
    inout_score = output["inout"][0][0].item()
    is_looking = inout_score > 0.5
    return is_looking, heatmap
