from ikomia import dataprocess
import scikit_MorphoSnakes_process as processMod
import scikit_MorphoSnakes_widget as widgetMod


# --------------------
# - Interface class to integrate the process with Ikomia application
# - Inherits dataprocess.CPluginProcessInterface from Ikomia API
# --------------------
class scikit_MorphoSnakes(dataprocess.CPluginProcessInterface):

    def __init__(self):
        dataprocess.CPluginProcessInterface.__init__(self)

    def getProcessFactory(self):
        # Instantiate process object
        return processMod.scikit_MorphoSnakesProcessFactory()

    def getWidgetFactory(self):
        # Instantiate associated widget object
        return widgetMod.scikit_MorphoSnakesWidgetFactory()
