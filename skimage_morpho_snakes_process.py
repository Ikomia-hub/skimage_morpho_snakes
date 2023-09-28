from ikomia import core, dataprocess
import copy
from skimage.segmentation import (morphological_geodesic_active_contour, inverse_gaussian_gradient, morphological_chan_vese)
from skimage import img_as_float
import numpy as np
import cv2


# --------------------
# - Class to handle the process parameters
# - Inherits core.CProtocolTaskParam from Ikomia API
# --------------------
class MorphoSnakesParam(core.CWorkflowTaskParam):

    def __init__(self):
        core.CWorkflowTaskParam.__init__(self)
        # parameters
        self.method = "mgac"
        self.mgac_amplification_contour = "Inverse gaussian gradient"
        self.mgac_iterations = 100
        self.mgac_smoothing = 1
        self.mgac_threshold = 'auto'
        self.mgac_balloon = 0
        self.mcv_iterations = 100
        self.mcv_smoothing = 1
        self.mcv_lambda1 = 1
        self.mcv_lambda2 = 1

    def set_values(self, params):
        # Set parameters values from Ikomia application
        self.method = params["method"]
        self.mgac_amplification_contour = params["mgac_amplification_contour"]
        self.mgac_iterations = int(params["mgac_iterations"])
        self.mgac_smoothing = int(params["mgac_smoothing"])
        self.mgac_threshold = params["mgac_threshold"]
        self.mgac_balloon = float(params["mgac_balloon"])
        self.mcv_iterations = int(params["mcv_iterations"])
        self.mcv_smoothing = int(params["mcv_smoothing"])
        self.mcv_lambda1 = float(params["mcv_lambda1"])
        self.mcv_lambda2 = float(params["mcv_lambda2"])

    def get_values(self):
        # Send parameters values to Ikomia application
        # Create the specific dict structure (string container)
        params = {"method": str(self.method),
                  "mgac_amplification_contour": str(self.mgac_amplification_contour),
                  "mgac_iterations": str(self.mgac_iterations),
                  "mgac_smoothing": str(self.mgac_smoothing),
                  "mgac_threshold": str(self.mgac_threshold),
                  "mgac_balloon": str(self.mgac_balloon),
                  "mcv_iterations": str(self.mcv_iterations),
                  "mcv_smoothing" : str(self.mcv_smoothing),
                  "mcv_lambda1": str(self.mcv_lambda1),
                  "mcv_lambda2": str(self.mcv_lambda2)}
        return params


# --------------------
# - Class which implements the process
# - Inherits core.CProtocolTask or derived from Ikomia API
# --------------------
class MorphoSnakes(dataprocess.C2dImageTask):

    def __init__(self, name, param):
        dataprocess.C2dImageTask.__init__(self, name)

        # Create parameters class
        if param is None:
            self.set_param_object(MorphoSnakesParam())
        else:
            self.set_param_object(copy.deepcopy(param))

        # add input -> initial level set
        self.add_input(dataprocess.CImageIO())

        # add output -> results image
        self.add_output(dataprocess.CImageIO())


    def get_progress_steps(self):
        # Function returning the number of progress steps for this process
        # This is handled by the main progress bar of Ikomia application
        param = self.get_param_object()
        if param.method == "mgac":
            nb_iter = param.mgac_iterations
        else :
            nb_iter = param.mcv_iterations

        return nb_iter

    def run(self):
        self.begin_task_run()

        # Get input 0 :
        input = self.get_input(0)

        # Get output :
        output = self.get_output(0)

        # Get parameters :
        param = self.get_param_object()

        # Get image from input/output (numpy array):
        srcImage = input.get_image()

        # Convert to grey Image if RGB
        if len(srcImage.shape) == 3:
            image = cv2.cvtColor(srcImage, cv2.COLOR_RGB2GRAY)
        else:
            image = srcImage
        
        # Convert to float
        imagef = img_as_float(image)

        # enhances borders
        if param.mgac_amplification_contour == "Inverse gaussian gradient":
           gimage = inverse_gaussian_gradient(imagef)
        else:
           gimage = imagef

        # initial level set
        initlevelSetInput = self.get_input(2)
        if initlevelSetInput.is_data_available():
            initlevelSetBinary = initlevelSetInput.get_image()
            if param.method == "mgac":
                proc_img = morphological_geodesic_active_contour(
                                                        gimage, param.mgac_iterations,
                                                        init_level_set=initlevelSetBinary,
                                                        smoothing=param.mgac_smoothing,
                                                        threshold=param.mgac_threshold,
                                                        balloon=param.mgac_balloon, 
                                                        iter_callback=(lambda callback: self.emit_step_progress())
                                                                ).astype(np.uint8) * 255
            else:
                proc_img = morphological_chan_vese(
                                    gimage,
                                    param.mcv_iterations,
                                    init_level_set=initlevelSetBinary,
                                    smoothing=param.mcv_smoothing,
                                    lambda1=param.mcv_lambda1,
                                    lambda2=param.mcv_lambda2,
                                    iter_callback=(lambda callback: self.emit_step_progress())
                                                    ).astype(np.uint8) * 255
        else :
            # input graph -> by user / by previous aoperation in worflow  
            graphInput = self.get_input(1)
            if graphInput.is_data_available():
                self.create_graphics_mask(imagef.shape[1], imagef.shape[0], graphInput)
                binImg = self.get_graphics_mask(0)
                if param.method == "mgac":
                    proc_img = morphological_geodesic_active_contour(
                                            gimage,
                                            param.mgac_iterations,
                                            init_level_set=binImg,
                                            smoothing=param.mgac_smoothing,
                                            threshold=param.mgac_threshold,
                                            balloon=param.mgac_balloon,
                                            iter_callback=(lambda callback: self.emit_step_progress())
                                                                    ).astype(np.uint8) * 255
                else:
                    proc_img = morphological_chan_vese(
                                        gimage,
                                        param.mcv_iterations,
                                        init_level_set=binImg,
                                        smoothing=param.mcv_smoothing,
                                        lambda1=param.mcv_lambda1,
                                        lambda2=param.mcv_lambda2,
                                        iter_callback=(lambda callback: self.emit_step_progress())
                                                    ).astype(np.uint8) * 255
            else:
                raise Exception("No initial level-set given: it must be graphics input or binary image.")

        # set output mask binary image
        output.set_image(proc_img)

        # add foward input image
        self.forward_input_image(0, 1)

        # Call end_task_run to finalize process
        self.end_task_run()


# --------------------
# - Factory class to build process object
# - Inherits dataprocess.CProcessFactory from Ikomia API
# --------------------
class MorphoSnakesFactory(dataprocess.CTaskFactory):

    def __init__(self):
        dataprocess.CTaskFactory.__init__(self)
        # Set process information as string here
        self.info.name = "skimage_morpho_snakes"
        self.info.short_description = "Morphological active contour segmentation from scikit-image library."
        self.info.authors = "Ikomia team"
        # relative path -> as displayed in Ikomia application process tree
        self.info.path = "Plugins/Python/Segmentation/Active contour"
        self.info.article = ""
        self.info.journal = ""
        self.info.year = 2020
        self.info.license = "MIT License"
        self.info.version = "1.1.1"
        self.info.repository = "https://github.com/Ikomia-hub/skimage_morpho_snakes"
        self.info.original_repository = "https://github.com/scikit-image/scikit-image"
        self.info.documentation_link = "https://scikit-image.org/docs/stable/api/skimage.segmentation.html#morphological-geodesic-active-contour"
        # If you want to customize plugin icon
        self.info.icon_path = "icons/scikit.png"
        # Associated keywords, for search
        self.info.keywords = "sci-kit,image,morphological,geodesic,active,contour,segmentation,chan vese"

    def create(self, param=None):
        # Create process object
        return MorphoSnakes(self.info.name, param)
