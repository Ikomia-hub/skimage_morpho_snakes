from ikomia import dataprocess


# --------------------
# - Interface class to integrate the process with Ikomia application
# - Inherits dataprocess.CPluginProcessInterface from Ikomia API
# --------------------
class scikit_MorphoSnakes(dataprocess.CPluginProcessInterface):

    def __init__(self):
        dataprocess.CPluginProcessInterface.__init__(self)

    def getProcessFactory(self):
        from scikit_MorphoSnakes.scikit_MorphoSnakes_process import scikit_MorphoSnakesProcessFactory
        # Instantiate process object
        return scikit_MorphoSnakesProcessFactory()

    def getWidgetFactory(self):
        from scikit_MorphoSnakes.scikit_MorphoSnakes_widget import scikit_MorphoSnakesWidgetFactory
        # Instantiate associated widget object
        return scikit_MorphoSnakesWidgetFactory()
