import io
import sys
import os
import pickle
import base64
import torch
import torchvision
from generator import Generator

### GLOBALS ###

num_gpu: int = 0  # Number of GPUs available. Set to 0 for CPU mode.

# Define device (use CPU by default)
device: torch.device = torch.device("cpu")

# Initialize the generator model and move it to the appropriate device
Generator(num_gpu=0).to(device)

# Define the directory for model files
model_dir: str = "model"
g_path: str = os.path.join(model_dir, "G.pkl")


class DeviceUnpickler(pickle.Unpickler):
    """
    A custom Unpickler that ensures models are loaded onto the current device
    (CPU or GPU), independent of the device on which the model was originally trained.
    """

    def find_class(self, module: str, name: str):
        if module == "torch.storage" and name == "_load_from_bytes":
            # Load the model onto the current device
            return lambda b: torch.load(
                io.BytesIO(b), map_location=device, weights_only=True
            )
        else:
            return super().find_class(module, name)


def gen_tater(model: torch.nn.Module) -> str:
    """
    Generate four random fake images using the given model and return the 0th image as a base64-encoded string.

    Args:
        model (torch.nn.Module): The generator model used to produce the images.

    Returns:
        str: A base64-encoded string.
    """
    # Generate random noise to feed into the generator
    noise = torch.randn(4, 100, 1, 1, device=device)

    # Generate fake images
    fakes = model(noise).detach().cpu()
    fake_img = fakes[0]

    # Create an image grid and convert to PIL Image format
    grid = torchvision.utils.make_grid(fake_img, padding=2, normalize=True)
    img = torchvision.transforms.ToPILImage()(grid)

    # Save the image to a buffer and encode it in base64
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_str = base64.b64encode(img_buffer.getvalue()).decode()

    return img_str


def make_tater() -> str:
    """
    Load the generator model from file, move it to the appropriate device, and generate a potato image.

    Returns:
        str: A base64-encoded string.
    """
    # Load the generator model from the pickle file
    with open(g_path, "rb") as g_file:
        netG = DeviceUnpickler(g_file).load()

    # Ensure the model is using the CPU
    netG = netG.module.to(device)

    return gen_tater(netG)


# Generate potato image and write base64 string to stdout
tater: str = make_tater()
sys.stdout.write(tater)
