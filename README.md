<div align="center">
  <img src="https://raw.githubusercontent.com/Ikomia-hub/skimage_morpho_snakes/main/icons/scikit.png" alt="Algorithm icon">
  <h1 align="center">skimage_morpho_snakes</h1>
</div>
<br />
<p align="center">
    <a href="https://github.com/Ikomia-hub/skimage_morpho_snakes">
        <img alt="Stars" src="https://img.shields.io/github/stars/Ikomia-hub/skimage_morpho_snakes">
    </a>
    <a href="https://app.ikomia.ai/hub/">
        <img alt="Website" src="https://img.shields.io/website/http/app.ikomia.ai/en.svg?down_color=red&down_message=offline&up_message=online">
    </a>
    <a href="https://github.com/Ikomia-hub/skimage_morpho_snakes/blob/main/LICENSE.md">
        <img alt="GitHub" src="https://img.shields.io/github/license/Ikomia-hub/skimage_morpho_snakes.svg?color=blue">
    </a>    
    <br>
    <a href="https://discord.com/invite/82Tnw9UGGc">
        <img alt="Discord community" src="https://img.shields.io/badge/Discord-white?style=social&logo=discord">
    </a> 
</p>

Morphological active contour segmentation from scikit-image library. Two methods are implemented: Morphological Geodesic Active Contour (MGAC) and Morphological Chan Vese (MCV). Users must give initial level-set as input, it can be graphics input drawn interactively (Ikomia Studio only) or binary image. Algorithm creates segmented region in a binary image.

![Example image](https://raw.githubusercontent.com/Ikomia-hub/infer_mmlab_text_recognition/feat/new_readme/images/coins-result.jpg)

## :rocket: Use with Ikomia API

#### 1. Install Ikomia API

We strongly recommend using a virtual environment. If you're not sure where to start, we offer a tutorial [here](https://www.ikomia.ai/blog/a-step-by-step-guide-to-creating-virtual-environments-in-python).

```sh
pip install ikomia
```

#### 2. Create your workflow

```python
from ikomia.dataprocess.workflow import Workflow
from ikomia.utils.displayIO import display

# Init your workflow
wf = Workflow()

# Set input image
wf.set_image_input(url="https://raw.githubusercontent.com/Ikomia-hub/skimage_morpho_snakes/main/images/coins.png", index=0)

# Set seed image (binary)
wf.set_image_input(url="https://raw.githubusercontent.com/Ikomia-hub/skimage_morpho_snakes/main/images/seed.png", index=1)

# Add snake algorithm
snake = wf.add_task(name="skimage_morpho_snakes", auto_connect=True)

# Adjust parameters
snake.set_parameters({
    "mgac_iterations": "500",
    "mgac_balloon": "-1.0",
})

# Run the workflow
wf.run()

# Display results
binary_output = snake.get_output(0)
original_img_output = snake.get_output(1)
display(original_img_output.get_image_with_mask(binary_output), title="Morpho snake")
```

## :sunny: Use with Ikomia Studio

Ikomia Studio offers a friendly UI with the same features as the API.

- If you haven't started using Ikomia Studio yet, download and install it from [this page](https://www.ikomia.ai/studio).

- For additional guidance on getting started with Ikomia Studio, check out [this blog post](https://www.ikomia.ai/blog/how-to-get-started-with-ikomia-studio).

## :pencil: Set algorithm parameters

```python
from ikomia.dataprocess.workflow import Workflow
from ikomia.utils.displayIO import display

# Init your workflow
wf = Workflow()

# Set input image
wf.set_image_input(url="https://raw.githubusercontent.com/Ikomia-hub/skimage_morpho_snakes/main/images/coins.png", index=0)

# Set seed image (binary)
wf.set_image_input(url="https://raw.githubusercontent.com/Ikomia-hub/skimage_morpho_snakes/main/images/seed.png", index=1)

# Add snake algorithm
snake = wf.add_task(name="skimage_morpho_snakes", auto_connect=True)

# Adjust parameters
snake.set_parameters({
    "method": "mgac",
    "mgac_amplification_contour": "Inverse gaussian gradient",
    "mgac_iterations": "100",
    "mgac_smoothing": "1",
    "mgac_threshold": "auto",
    "mgac_balloon": "0",
    "mcv_iterations": "100",
    "mcv_smoothing": "1",
    "mcv_lambda1": "1.0",
    "mcv_lambda2": "1.0",
})

# Run the workflow
wf.run()
```

- **method** (str, default="mgac"): choose either *"mgac"* (Morphological Geodesic Active Contour) or *"mcv"* (Morphological Chan Vese)
- **mgac_amplification_contour** (str, default="Inverse gaussian gradient"): pre-processing method. For MGAC method only.
- **mgac_iterations** (int, default=100): iteration count. For MGAC method only.
- **mgac_smoothing** (int, default=1): number of times the smoothing operator is applied per iteration. For MGAC method only.
- **mgac_threshold** (float, default="auto"): Areas of the image with a value smaller than this threshold will be considered borders. The evolution of the contour will stop in this areas. For MGAC method only.
- **mgac_balloon** (float, default=0): Balloon force to guide the contour in non-informative areas of the image, i.e., areas where the gradient of the image is too small to push the contour towards a border. A negative value will shrink the contour, while a positive value will expand the contour in these areas. Setting this to zero will disable the balloon force. For MGAC method only.
- **mcv_iterations** (int, default=100): iteration count. For MCV method only.
- **mcv_smoothing** (int, default=1): number of times the smoothing operator is applied per iteration. For MCV method only.
- **mcv_lambda1** (float, default=1): Weight parameter for the outer region. If lambda1 is larger than lambda2, the outer region will contain a larger range of values than the inner region. For MCV method only.
- **mcv_lambda2** (float, default=1): Weight parameter for the inner region. If lambda2 is larger than lambda1, the inner region will contain a larger range of values than the outer region. For MCV method only.

***Note***: parameter key and value should be in **string format** when added to the dictionary.

## :mag: Explore algorithm outputs

Every algorithm produces specific outputs, yet they can be explored them the same way using the Ikomia API. For a more in-depth understanding of managing algorithm outputs, please refer to the [documentation](https://ikomia-dev.github.io/python-api-documentation/advanced_guide/IO_management.html).

```python
from ikomia.dataprocess.workflow import Workflow
from ikomia.utils.displayIO import display

# Init your workflow
wf = Workflow()

# Set input image
wf.set_image_input(url="https://raw.githubusercontent.com/Ikomia-hub/skimage_morpho_snakes/main/images/coins.png", index=0)

# Set seed image (binary)
wf.set_image_input(url="https://raw.githubusercontent.com/Ikomia-hub/skimage_morpho_snakes/main/images/seed.png", index=1)

# Add snake algorithm
snake = wf.add_task(name="skimage_morpho_snakes", auto_connect=True)

# Adjust parameters
snake.set_parameters({
    "mgac_iterations": "500",
    "mgac_balloon": "-1.0",
})

# Run the workflow
wf.run()

# Iterate over outputs
for output in algo.get_outputs()
    # Print information
    print(output)
    # Export it to JSON
    output.to_json()
```

Scikit-image morphological active contour algorithm generates 2 outputs:

1. Binary segmentation output (CImageIO)
2. Original image output (CImageIO)