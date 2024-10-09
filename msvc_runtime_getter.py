
from dumpbin import Dumpbin


class MSVCRuntimeGetter:
    
    VC_VERSION_LIST = {
        '1997': ['msvcrt.dll'],
        '2001': ['msvcr20.dll'],
        '2003': ['msvcr70.dll','msvcr71.dll'],
        '2005': ['msvcp80.dll','vcruntime80.dll'],
        '2010': ['msvcp100.dll','vcruntime100.dll'],
        '2013': ['msvcp120.dll','vcruntime120.dll'],
        '2015': ['msvcp140.dll','vcruntime140.dll'],
        '2017': ['msvcp141.dll','vcruntime141.dll'],
        '2019': ['msvcp142.dll','vcruntime142.dll'],
        '2022': ['msvcp143.dll','vcruntime143.dll'],
    }

    def __init__(self):
        self.dumpbin = Dumpbin()

    def get_msvc_runtime(self, file_path: str):
        # Get the dependencies of the executable
        dependents_info = self.dumpbin.run_dependents(file_path)

        # Get the VC runtime version
        msvc_version = self.__get_msvc_runtime(dependents_info)

        return msvc_version
    
    def __get_msvc_runtime(self, dependents_info: str) -> str:
        """ Return the version of the VC runtime used by the executable from the dumpbin output """
        dependents_info = dependents_info.lower()

        for vc_runtime_version, msvc_runtime_files in self.VC_VERSION_LIST.items():
            # Search runtime from the output
            for msvc_runtime_file in msvc_runtime_files:
                # Check if the runtime is in the output
                if msvc_runtime_file in dependents_info:
                    return vc_runtime_version
        
        return None
