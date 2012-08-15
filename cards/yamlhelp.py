"""Make PyYaml work the way we want."""

import re
import yaml

# Configure PyYaml

class quoted(str): pass
class literal(str): pass
class mapping(list): pass

yaml.add_representer(quoted,
    lambda dumper, data: dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
    )

yaml.add_representer(literal, 
    # PyYaml won't use literal blocks if there's trailing space, so trim trailing space from the data.
    lambda dumper, data: dumper.represent_scalar('tag:yaml.org,2002:str', re.sub(r"\s+\n", "\n", data), style='|')
    )

yaml.add_representer(mapping, 
    lambda dumper, data: dumper.represent_dict(data)
    )
