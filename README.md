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

Morphological active contour segmentation from scikit-image library. Two algorithms are implemented: Morphological Geodesic Active Contour (MGAC) and Morphological Chan Vese (MCV). Users must give initial level-set as input, it can be graphics input drawn interactively or binary image. Process outputs segmented region in a binary image and overlays the mask on top of the original image.

[Insert illustrative image here. Image must be accessible publicly, in algorithm Github repository for example.
<img src="images/illustration.png"  alt="Illustrative image" width="30%" height="30%">]

## :rocket: Use with Ikomia API

#### 1. Install Ikomia API

We strongly recommend using a virtual environment. If you're not sure where to start, we offer a tutorial [here](https://www.ikomia.ai/blog/a-step-by-step-guide-to-creating-virtual-environments-in-python).

```sh
pip install ikomia
```

#### 2. Create your workflow

[Change the sample image URL to fit algorithm purpose]

```python
import ikomia
from ikomia.dataprocess.workflow import Workflow

# Init your workflow
wf = Workflow()

# Add algorithm
algo = wf.add_task(name="skimage_morpho_snakes", auto_connect=True)

# Run on your image  
wf.run_on(url="example_image.png")
```

## :sunny: Use with Ikomia Studio

Ikomia Studio offers a friendly UI with the same features as the API.

- If you haven't started using Ikomia Studio yet, download and install it from [this page](https://www.ikomia.ai/studio).

- For additional guidance on getting started with Ikomia Studio, check out [this blog post](https://www.ikomia.ai/blog/how-to-get-started-with-ikomia-studio).

## :pencil: Set algorithm parameters

[Explain each algorithm parameters]

[Change the sample image URL to fit algorithm purpose]

```python
import ikomia
from ikomia.dataprocess.workflow import Workflow

# Init your workflow
wf = Workflow()

# Add algorithm
algo = wf.add_task(name="skimage_morpho_snakes", auto_connect=True)

algo.set_parameters({
    "param1": "value1",
    "param2": "value2",
    ...
})

# Run on your image  
wf.run_on(url="example_image.png")

```

## :mag: Explore algorithm outputs

Every algorithm produces specific outputs, yet they can be explored them the same way using the Ikomia API. For a more in-depth understanding of managing algorithm outputs, please refer to the [documentation](https://ikomia-dev.github.io/python-api-documentation/advanced_guide/IO_management.html).

```python
import ikomia
from ikomia.dataprocess.workflow import Workflow

# Init your workflow
wf = Workflow()

# Add algorithm
algo = wf.add_task(name="skimage_morpho_snakes", auto_connect=True)

# Run on your image  
wf.run_on(url="example_image.png")

# Iterate over outputs
for output in algo.get_outputs()
    # Print information
    print(output)
    # Export it to JSON
    output.to_json()
```

## :fast_forward: Advanced usage 

[optional]
