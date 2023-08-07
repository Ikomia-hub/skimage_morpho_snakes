import cv2
from ikomia.utils.tests import run_for_test
import logging
logger = logging.getLogger(__name__)


def test(t, data_dict):
    logger.info("===== Test::infer skimage morpho snakes =====")
    img = cv2.imread(data_dict["images"]["detection"]["coco"])[::-1]
    bin_mask = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    input_img = t.get_input(0)
    input_img.set_image(img)
    input_mask = t.get_input(2)
    input_mask.set_image(bin_mask)

    for method in ["mgac", "mcv"]:
        params = t.get_parameters()
        params["method"] = method
        # without update = 1, model is not updated between 2 test
        t.set_parameters(params)
        yield run_for_test(t)

