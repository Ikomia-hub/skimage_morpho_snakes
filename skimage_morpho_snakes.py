from ikomia import dataprocess


# --------------------
# - Interface class to integrate the process with Ikomia application
# - Inherits dataprocess.CPluginProcessInterface from Ikomia API
# --------------------
class IkomiaPlugin(dataprocess.CPluginProcessInterface):

    def __init__(self):
        dataprocess.CPluginProcessInterface.__init__(self)

    def get_process_factory(self):
        from skimage_morpho_snakes.skimage_morpho_snakes_process import MorphoSnakesFactory
        # Instantiate process object
        return MorphoSnakesFactory()

    def get_widget_factory(self):
        from skimage_morpho_snakes.skimage_morpho_snakes_widget import MorphoSnakesWidgetFactory
        # Instantiate associated widget object
        return MorphoSnakesWidgetFactory()
