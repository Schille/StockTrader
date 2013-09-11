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
            
    def execute_calc(self, data):
        run = []
        if not self.__is_sequence(data):
            raise Exception('Data is no array!')
        for alg in self._pluginManager.getAllPlugins():
            result, prop = alg.plugin_object.calc(data)
            run.append({alg.name : (result, prop)})
        return run

    
    def __is_sequence(self, arg):
        return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))
            
            
    
                 
    
        