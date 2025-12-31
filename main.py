import json
import os
from pathlib import Path

#
# This file is unrelated to the library.  It provides macro definitions to MkDocs
#

def define_env(env):
    """
    This is the hook for defining variables, macros and filters
    """

    @env.macro
    def load_form_data(revision: str, form_id: str):
        """
        Loads the JSON asset for a specific form_id and returns it as a dict.
        """
        # env.project_dir is provided by the plugin to help locate files
        project_root = Path(env.project_dir)
        json_path = project_root / "src" / "regional_observer_workbook" / "assets" / revision / form_id / "form-fields.json"

        if not json_path.exists():
            return {"error": f"File not found: {json_path}"}

        with open(json_path, 'r') as f:
            data = json.load(f)
        
        return data