# Since this is copy-pasted wrongly(mostly) at a lot of places across the web, i'm putting the fixed, updated version here, mainly for self-reference

## Add this to the first block in your note book
import uuid
from IPython.core.display import display, HTML

import json

class RenderJSON(object):
    def __init__(self, json_data):
        if isinstance(json_data, dict):
            self.json_str = json.dumps(json_data)
        else:
            self.json_str = json_data
        self.uuid = str(uuid.uuid4())
        # This line is missed out in most of the versions of this script across the web, it is essential for this to work interleaved with print statements
        self._ipython_display_()

    def _ipython_display_(self):
        display(HTML('<div id="{}" style="height: auto; width:100%;"></div>'.format(self.uuid)))
        display(HTML("""<script>
        require(["https://rawgit.com/caldwell/renderjson/master/renderjson.js"], function() {
          renderjson.set_show_to_level(1)
          document.getElementById('%s').appendChild(renderjson(%s))
        });</script>
        """ % (self.uuid, self.json_str)))



## To use this function, call this, this now works even when you have a print statement before or after the RenderJSON call
