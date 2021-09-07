from ikomia import utils, core, dataprocess
from ikomia.utils import qtconversion
from scikit_MorphoSnakes.scikit_MorphoSnakes_process import scikit_MorphoSnakesParam
# PyQt GUI framework
from PyQt5.QtWidgets import *


# --------------------
# - Class which implements widget associated with the process
# - Inherits core.CProtocolTaskWidget from Ikomia API
# --------------------
class scikit_MorphoSnakesWidget(core.CWorkflowTaskWidget):

    def __init__(self, param, parent):
        core.CWorkflowTaskWidget.__init__(self, parent)

        if param is None:
            self.parameters = scikit_MorphoSnakesParam()
        else:
            self.parameters = param

        # variable
        self.MAX_SPINBOX = 10000000

        # Create layout : QGridLayout by default
        self.gridLayout = QGridLayout()

        # all parameters widgets
        # snacks methods avaiable
        self.mgac = QWidget()
        self.chanVese = QWidget()

        # set all parameters widgets
        self.methodWidget()
        self.mgacWidget()
        self.chanVeseWidget()

        # main widget
        self.stack = QStackedWidget()
        self.stack.addWidget(self.mgac)
        self.stack.addWidget(self.chanVese)
        self.gridLayout.addWidget(self.stack, 2, 0)
        self.gridLayout.setRowStretch(3, 3)

        # PyQt -> Qt wrapping
        layout_ptr = qtconversion.PyQtToQt(self.gridLayout)

        # Set widget layout
        self.setLayout(layout_ptr)

        # update left parameter panel
        if self.parameters.method != "mgac":
           self.comboMethod.setCurrentIndex(1)
           
    def methodWidget(self):
        label_method = QLabel("Methods :")
        self.comboMethod = QComboBox()
        self.comboMethod.addItem("Morphological Geodesic Active Contour")
        self.comboMethod.addItem("Morphological Chan Vese")
        self.comboMethod.currentIndexChanged.connect(self.OnMethodChange)

        self.gridLayout.setRowStretch(0,0)
        self.gridLayout.addWidget(label_method, 0, 0)
        self.gridLayout.setRowStretch(1,1)
        self.gridLayout.addWidget(self.comboMethod, 1, 0)
        self.gridLayout.setRowStretch(2,2)

    def mgacWidget(self):
        self.gridLayoutMgac = QGridLayout()
        self.mgac_coutour_check = QCheckBox("Default borders amplification");
        self.mgac_coutour_check.setChecked(True);

        self.mgac_coutour_check.stateChanged.connect(self.OnContourDefaultChange)
        self.mgac_stack_comboContour = QComboBox()
        self.mgac_stack_comboContour.addItem("Inverse gaussian gradient")
        
        # update parametre -> left widget
        if self.parameters.mgac_amplification_contour == None:
            self.mgac_coutour_check.setChecked(False)
            self.mgac_stack_comboContour.hide()

        label_iter = QLabel("Iterations :")
        self.mgac_spin_iterations = QSpinBox()
        self.mgac_spin_iterations.setMaximum(self.MAX_SPINBOX)
        self.mgac_spin_iterations.setValue(100)
        if self.parameters.mgac_iterations != 100:
            self.mgac_spin_iterations.setValue(self.parameters.mgac_iterations)

        label_smooth = QLabel("Smoothing :")
        self.mgac_spin_smooth = QSpinBox()
        self.mgac_spin_smooth.setMinimum(0)
        self.mgac_spin_smooth.setMaximum(100)
        self.mgac_spin_smooth.setValue(1)

        if self.parameters.mgac_smoothing != 1:
            self.mgac_spin_smooth.setValue(self.parameters.mgac_smoothing )

        self.mgac_threshold_check = QCheckBox("Default threshold");
        self.mgac_threshold_check.setChecked(True)
        self.mgac_threshold_check.stateChanged.connect(self.OnThresholdDefaultChange)
        self.mgac_spin_threshold = QDoubleSpinBox()
        self.mgac_spin_threshold.setMaximum(self.MAX_SPINBOX)
        self.mgac_spin_threshold.setSingleStep(0.1)
        self.mgac_spin_threshold.setValue(0.5)
        self.mgac_spin_threshold.hide()

        if self.parameters.mgac_threshold != "auto":
            self.mgac_threshold_check.setChecked(False)
            self.mgac_spin_threshold.setValue(self.parameters.mgac_threshold)
            self.mgac_spin_threshold.show()

        label_balloon = QLabel("Balloon :")
        self.mgac_spin_balloon = QDoubleSpinBox()
        self.mgac_spin_balloon.setMaximum(self.MAX_SPINBOX)
        self.mgac_spin_balloon.setMinimum(-self.MAX_SPINBOX)
        self.mgac_spin_balloon.setSingleStep(0.5)
        self.mgac_spin_balloon.setValue(0)

        if self.parameters.mgac_balloon != 0:
            self.mgac_spin_balloon.setValue(self.parameters.mgac_balloon)

        self.gridLayoutMgac.setRowStretch(0,0)
        self.gridLayoutMgac.addWidget(self.mgac_coutour_check, 0, 0)
        self.gridLayoutMgac.setRowStretch(1,1)
        self.gridLayoutMgac.addWidget(self.mgac_stack_comboContour, 1, 0)
        self.gridLayoutMgac.setRowStretch(2,2)
        self.gridLayoutMgac.addWidget(label_iter, 2, 0)
        self.gridLayoutMgac.addWidget(self.mgac_spin_iterations, 2, 1)
        self.gridLayoutMgac.setRowStretch(3,3)
        self.gridLayoutMgac.addWidget(label_smooth, 3, 0)
        self.gridLayoutMgac.addWidget(self.mgac_spin_smooth, 3, 1)
        self.gridLayoutMgac.setRowStretch(4,4)
        self.gridLayoutMgac.addWidget(self.mgac_threshold_check, 4, 0)
        self.gridLayoutMgac.addWidget(self.mgac_spin_threshold, 4, 1)
        self.gridLayoutMgac.setRowStretch(5,5)
        self.gridLayoutMgac.addWidget(label_balloon,5, 0)
        self.gridLayoutMgac.addWidget(self.mgac_spin_balloon, 5, 1)
        self.gridLayoutMgac.setRowStretch(6,6)

        self.mgac.setLayout(self.gridLayoutMgac)

    def chanVeseWidget(self):
        self.gridLayoutMcv = QGridLayout()

        label_iter = QLabel("Iterations :")
        self.mcv_spin_iterations = QSpinBox()
        self.mcv_spin_iterations.setMaximum(self.MAX_SPINBOX)
        self.mcv_spin_iterations.setValue(100)
        if self.parameters.mcv_iterations != 100:
            self.mcv_spin_iterations.setValue(self.parameters.mcv_iterations)

        label_smooth = QLabel("Smoothing :")
        self.mcv_spin_smooth = QSpinBox()
        self.mcv_spin_smooth.setMinimum(0)
        self.mcv_spin_smooth.setMaximum(100)
        self.mcv_spin_smooth.setValue(1)
        if self.parameters.mcv_smoothing != 1:
            self.mcv_spin_smooth.setValue(self.parameters.mcv_smoothing)

        label_lambda1 = QLabel("Lambda1 :")
        self.mcv_spin_lambda1 = QDoubleSpinBox()
        self.mcv_spin_lambda1.setMaximum(self.MAX_SPINBOX)
        self.mcv_spin_lambda1.setValue(1)
        self.mcv_spin_lambda1.setSingleStep(0.1)
        if self.parameters.mcv_lambda1 != 1:
            self.mcv_spin_lambda1.setValue(self.parameters.mcv_lambda1)

        label_lambda2 = QLabel("Lambda2 :")
        self.mcv_spin_lambda2 = QDoubleSpinBox()
        self.mcv_spin_lambda2.setMaximum(self.MAX_SPINBOX)
        self.mcv_spin_lambda2.setValue(1)
        self.mcv_spin_lambda2.setSingleStep(0.1)
        if self.parameters.mcv_lambda2 != 1:
            self.mcv_spin_lambda2.setValue(self.parameters.mcv_lambda2)

        self.gridLayoutMcv.setRowStretch(0,0)
        self.gridLayoutMcv.addWidget(label_iter, 0, 0)
        self.gridLayoutMcv.addWidget(self.mcv_spin_iterations, 0, 1)
        self.gridLayoutMcv.setRowStretch(1,1)
        self.gridLayoutMcv.addWidget(label_smooth, 1, 0)
        self.gridLayoutMcv.addWidget(self.mcv_spin_smooth, 1, 1)
        self.gridLayoutMcv.setRowStretch(2,2)
        self.gridLayoutMcv.addWidget(label_lambda1, 2, 0)
        self.gridLayoutMcv.addWidget(self.mcv_spin_lambda1, 2, 1)
        self.gridLayoutMcv.setRowStretch(3,3)
        self.gridLayoutMcv.addWidget(label_lambda2, 3, 0)
        self.gridLayoutMcv.addWidget(self.mcv_spin_lambda2, 3, 1)
        self.gridLayoutMcv.setRowStretch(4,4)

        self.chanVese.setLayout(self.gridLayoutMcv)

    # pySlot
    def OnContourDefaultChange(self):
        if not self.mgac_coutour_check.isChecked():
            self.mgac_stack_comboContour.hide()
        else :
            self.mgac_stack_comboContour.show()

    # pySlot
    def OnThresholdDefaultChange(self):
        if self.mgac_threshold_check.isChecked():
            self.mgac_spin_threshold.hide()
        else :
            self.mgac_spin_threshold.show()

    # pySlot
    def OnMethodChange(self):
        if self.comboMethod.currentText() == "Morphological Geodesic Active Contour":
            self.stack.setCurrentIndex(0)
        else :
            self.stack.setCurrentIndex(1)

    def onApply(self):
        # Apply button clicked slot
        if self.comboMethod.currentText() == "Morphological Geodesic Active Contour":
            self.parameters.method = "mgac"

            if self.mgac_coutour_check.isChecked():
                self.parameters.mgac_amplification_contour = self.mgac_stack_comboContour.currentText()
            else :
                self.parameters.mgac_amplification_contour = None

            self.parameters.mgac_iterations = self.mgac_spin_iterations.value()
            self.parameters.mgac_smoothing = self.mgac_spin_smooth.value()

            if self.mgac_threshold_check.isChecked():
                self.parameters.mgac_threshold = 'auto'
            else :
                self.parameters.mgac_threshold = self.mgac_spin_threshold.value()

            self.parameters.mgac_balloon = self.mgac_spin_balloon.value()
        else :
            self.parameters.method = "mcv"
            self.parameters.mcv_iterations = self.mcv_spin_iterations.value()
            self.parameters.mcv_smoothing = self.mcv_spin_smooth.value()
            self.parameters.mcv_lambda1 = self.mcv_spin_lambda1.value()
            self.parameters.mcv_lambda2 = self.mcv_spin_lambda2.value()

        # Send signal to launch the process
        self.emitApply(self.parameters)


# --------------------
# - Factory class to build process widget object
# - Inherits dataprocess.CWidgetFactory from Ikomia API
# --------------------
class scikit_MorphoSnakesWidgetFactory(dataprocess.CWidgetFactory):

    def __init__(self):
        dataprocess.CWidgetFactory.__init__(self)
        # Set the name of the process -> it must be the same as the one declared in the process factory class
        self.name = "scikit_MorphoSnakes"

    def create(self, param):
        # Create widget object
        return scikit_MorphoSnakesWidget(param, None)
