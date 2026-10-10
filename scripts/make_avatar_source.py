"""Download the GitHub avatar and prepare a grayscale portrait source."""
import io
import os
from urllib.request import Request, urlopen

import numpy as np
from PIL import Image, ImageOps

from common import ROOT
from config import USERNAME


def main():
    request = Request(f"https://github.com/{USERNAME}.png?size=460", headers={"User-Agent": "profile-readme"})
    with urlopen(request, timeout=30) as response:
        image = Image.open(io.BytesIO(response.read())).convert("RGB")
    grayscale = ImageOps.autocontrast(ImageOps.grayscale(image))
    grayscale.save(os.path.join(ROOT, "source-prepped.png"))
    print("wrote source-prepped.png", grayscale.size)


if __name__ == "__main__":
    main()
