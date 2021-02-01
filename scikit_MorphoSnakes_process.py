from ikomia import core, dataprocess
import copy
# your imports below
from skimage.segmentation import (morphological_geodesic_active_contour, inverse_gaussian_gradient, morphological_chan_vese)
from skimage import img_as_float
import numpy as np
import cv2


# --------------------
# - Class to handle the process parameters
# - Inherits core.CProtocolTaskParam from Ikomia API
# --------------------
class scikit_MorphoSnakesParam(core.CProtocolTaskParam):

    def __init__(self):
        core.CProtocolTaskParam.__init__(self)
        
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

    def setParamMap(self, paramMap):
        # Set parameters values from Ikomia application
        self.method = int(paramMap["method"])
        self.mgac_amplification_contour = int(paramMap["mgac_amplification_contour"])
        self.mgac_iterations = int(paramMap["mgac_iterations"])
        self.mgac_smoothing = int(paramMap["mgac_smoothing"])
        self.mgac_threshold = int(paramMap["mgac_threshold"])
        self.mgac_balloon = int(paramMap["mgac_balloon"])
        self.mcv_iterations = int(paramMap["mcv_iterations"])
        self.mcv_smoothing = int(paramMap["mcv_smoothing"])
        self.mcv_lambda1 = int(paramMap["mcv_lambda1"])
        self.mcv_lambda2 = int(paramMap["mcv_lambda2"])

    def getParamMap(self):
        # Send parameters values to Ikomia application
        # Create the specific dict structure (string container)
        paramMap = core.ParamMap()
        paramMap["method"] = str(self.method)
        paramMap["mgac_amplification_contour"] = str(self.mgac_amplification_contour)
        paramMap["mgac_iterations"] = str(self.mgac_iterations)
        paramMap["mgac_smoothing"] = str(self.mgac_smoothing)
        paramMap["mgac_threshold"] = str(self.mgac_threshold)
        paramMap["mgac_balloon"] = str(self.mgac_balloon)
        paramMap["mcv_iterations"] = str(self.mcv_iterations)
        paramMap["mcv_smoothing"] = str(self.mcv_smoothing)
        paramMap["mcv_lambda1"] = str(self.mcv_lambda1)
        paramMap["mcv_lambda2"] = str(self.mcv_lambda2)
        return paramMap


# --------------------
# - Class which implements the process
# - Inherits core.CProtocolTask or derived from Ikomia API
# --------------------
class scikit_MorphoSnakesProcess(dataprocess.CImageProcess2d):

    def __init__(self, name, param):
        dataprocess.CImageProcess2d.__init__(self, name)

        #Create parameters class
        if param is None:
            self.setParam(scikit_MorphoSnakesParam())
        else:
            self.setParam(copy.deepcopy(param))
        
        # add input -> initial level set
        self.addInput(dataprocess.CImageProcessIO())

        # add output -> results image
        self.addOutput(dataprocess.CImageProcessIO())

        # set color mask
        self.setOutputColorMap(1,0,[[255,0,0]])

    def getProgressSteps(self, eltCount=1):
        # Function returning the number of progress steps for this process
        # This is handled by the main progress bar of Ikomia application
        param = self.getParam()
        if param.method == "mgac":
            nb_iter = param.mgac_iterations
        else :
            nb_iter = param.mcv_iterations
        
        return nb_iter

    def run(self):
        self.beginTaskRun()

        # Get input 0 :
        input = self.getInput(0)

        # Get output :
        output = self.getOutput(0)

        # Get parameters :
        param = self.getParam()

        # Get image from input/output (numpy array):
        srcImage = input.getImage()

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
        initlevelSetInput = self.getInput(2)
        if initlevelSetInput.isDataAvailable():
            initlevelSetBinary = initlevelSetInput.getImage()
            if param.method == "mgac":
                proc_img = morphological_geodesic_active_contour(gimage, param.mgac_iterations, init_level_set=initlevelSetBinary, smoothing=param.mgac_smoothing, threshold=param.mgac_threshold,balloon=param.mgac_balloon, iter_callback=(lambda callback: self.emitStepProgress())).astype(np.uint8) * 255
            else:
                proc_img = morphological_chan_vese(gimage, param.mcv_iterations, init_level_set=initlevelSetBinary, smoothing=param.mcv_smoothing, lambda1=param.mcv_lambda1, lambda2=param.mcv_lambda2, iter_callback=(lambda callback: self.emitStepProgress())).astype(np.uint8) * 255
        else :
            # input graph -> by user / by previous aoperation in worflow  
            graphInput = self.getInput(1)
            if graphInput.isDataAvailable():
                self.createGraphicsMask(imagef.shape[1], imagef.shape[0], graphInput)
                binImg = self.getGraphicsMask(0)
                if param.method == "mgac":
                    proc_img = morphological_geodesic_active_contour(gimage, param.mgac_iterations, init_level_set=binImg, smoothing=param.mgac_smoothing, threshold=param.mgac_threshold,balloon=param.mgac_balloon, iter_callback=(lambda callback: self.emitStepProgress())).astype(np.uint8) * 255
                else:
                    proc_img = morphological_chan_vese(gimage, param.mcv_iterations, init_level_set=binImg, smoothing=param.mcv_smoothing, lambda1=param.mcv_lambda1, lambda2=param.mcv_lambda2, iter_callback=(lambda callback: self.emitStepProgress())).astype(np.uint8) * 255
            else:
                raise Exception("No initial level-set given: it must be graphics input or binary image.")

        # set output mask binary image
        output.setImage(proc_img)

        # add foward input image
        self.forwardInputImage(0, 1)

        # Call endTaskRun to finalize process
        self.endTaskRun()


# --------------------
# - Factory class to build process object
# - Inherits dataprocess.CProcessFactory from Ikomia API
# --------------------
class scikit_MorphoSnakesProcessFactory(dataprocess.CProcessFactory):

    def __init__(self):
        dataprocess.CProcessFactory.__init__(self)
        # Set process information as string here
        self.info.name = "scikit_MorphoSnakes"
        self.info.shortDescription = "Morphological active contour segmentation from scikit-image library."
        self.info.description = "Morphological active contour segmentation from scikit-image library. " \
                                "Two algorithms are implemented: Morphological Geodesic Active Contour (MGAC) " \
                                "and Morphological Chan Vese (MCV). Users must give initial level-set as input, " \
                                "it can be graphics input drawn interactively or binary image. Process outputs " \
                                "segmented region in a binary image and overlays the mask on top of the original image."
        self.info.authors = "Ikomia team"
        # relative path -> as displayed in Ikomia application process tree
        self.info.path = "Plugins/Python/Segmentation/Active contour"
        self.info.article = ""
        self.info.journal = ""
        self.info.year = 2020
        self.info.license = "MIT License"
        self.info.version = "1.0.0"
        self.info.repo = "https://github.com/Ikomia-dev/IkomiaPluginsPython"
        self.info.documentationLink = "https://scikit-image.org/docs/stable/api/skimage.segmentation.html#morphological-geodesic-active-contour"
        # If you want to customize plugin icon
        self.info.iconPath = "icons/scikit.png"
        # Associated keywords, for search
        self.info.keywords = "sci-kit,image,morphological,geodesic,active,contour,segmentation,chan vese"

    def create(self, param=None):
        # Create process object
        return scikit_MorphoSnakesProcess(self.info.name, param)
