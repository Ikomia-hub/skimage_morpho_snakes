from ikomia.core import task
import cv2
from ikomia.utils.tests import run_for_test
import logging
logger = logging.getLogger(__name__)


def test(t, data_dict):
    logger.info("===== Test::infer skimage morpho snakes =====")
    img = cv2.imread(data_dict["images"]["detection"]["coco"])[::-1]
    bin_mask = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    input_img = t.getInput(0)
    input_img.setImage(img)
    input_mask = t.getInput(2)
    input_mask.setImage(bin_mask)

    for method in ["mgac", "mcv"]:
        params = task.get_parameters(t)
        params["method"] = method
        # without update = 1, model is not updated between 2 test
        task.set_parameters(t, params)
        yield run_for_test(t)

