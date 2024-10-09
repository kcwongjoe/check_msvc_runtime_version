import os
import subprocess

# Class to run dumpbin on the specified file
class Dumpbin:
    def __init__(self, dumpbin_path: str = None):
        """ Initialize the dumpbin class
        Args:
            dumpbin_path (str, optional): The path to the dumpbin.exe file. Defaults to None.
        """
        self.__search_dumpbin(dumpbin_path)

    def __search_dumpbin(self, dumpbin_path: str = None):
        """ Search for the dumpbin.exe file in the default locations if not provided
        Args:
            dumpbin_path (str, optional): The path to the dumpbin.exe file. Defaults to None.
        Raises:
            FileNotFoundError: If dumpbin.exe is not found
        """

        # Set the dumpbin path if provided
        if dumpbin_path is not None:

            # Make sure dumpbin.exe is at the end of the path
            if not dumpbin_path.lower().endswith(r'dumpbin.exe'):
                dumpbin_path = os.path.join(dumpbin_path, r'dumpbin.exe')

            # Check if dumpbin.exe exists
            if os.path.exists(dumpbin_path):
                self.dumpbin_path = dumpbin_path
                return
            else:
                print(f'{dumpbin_path} not found, searching for dumpbin.exe in the default locations')

        # Searching dumpbin.exe under the Microsoft Visual Studio folders
        possible_parent_dirs = [
            r'C:\Program Files\Microsoft Visual Studio',
            r'C:\Program Files (x86)\Microsoft Visual Studio',
        ]

        for parent_dir in possible_parent_dirs:
            for dirpath, _, filenames in os.walk(parent_dir):

                # Set the dumpbin path if found
                if r'dumpbin.exe' in filenames:
                    self.dumpbin_path = os.path.join(dirpath, r'dumpbin.exe')

                    # Dumpbin found, exit the function
                    return
            
        # Dumpbin not found
        raise FileNotFoundError('dumpbin.exe not found, Please provide the path to dumpbin.exe')

    def __get_dumpbin_cmd(self, file_path: str, options: str = None) -> str:
        """ Return the command to run dumpbin on the specified executable 
        Args:
            file_path (str): The path to the file
            options (str, optional): The options to be passed to dumpbin. Defaults to None. It can be /all, /dependents, /summary, etc.
        Returns:
            str: The dumpbin command
        """
        if options is None:
            return f'"{self.dumpbin_path}" {file_path}'
        else:
            return f'"{self.dumpbin_path}" {options} {file_path}'
    
    def run(self, file_path: str, options: str = None) -> str:
        """ Run the dumpbin command on the specified file
        Args:
            file_path (str): The path to the file
            options (str, optional): The options to be passed to dumpbin. Defaults to None. It can be /all, /dependents, /summary, etc.
        Returns:
            str: The output of the dumpbin command
        """
        # Get the dumpbin command
        dumpbin_cmd = self.__get_dumpbin_cmd(file_path, options)

        # Run the command
        out_txt = subprocess.run(dumpbin_cmd, capture_output=True).stdout
        return str(out_txt)
    
    def run_dependents(self, file_path: str) -> str:
        """ Get the dependents information of the file 
        Args:
            file_path (str): The path to the file
        Returns:
            str: The dependents information
        """
        return self.run(file_path, r'/dependents')
