from yapsy.PluginManager import PluginManager
import config


class AlgorithmManager():
    def __init__(self):
        self._pluginManager = PluginManager()
        self._pluginManager.setPluginPlaces(config.PLUGIN_DIR)
        self._pluginManager.collectPlugins()
        for pluginInfo in self._pluginManager.getAllPlugins():
            self._pluginManager.activatePluginByName(pluginInfo.name)
            
    def get_alg_names(self):
        for plugin in self._pluginManager.getAllPlugins():
            plugin.plugin_object.print_name()