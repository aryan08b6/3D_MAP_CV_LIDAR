import yaml
from pathlib import Path

class ConfigManager:
    def __init__(self, path=""):
        if path == "":
            self.CONFIG_DIR = Path(__file__).resolve().parent.parent / "configs" / "config.yaml"
        else:
            self.CONFIG_DIR = Path(path).resolve()
        with open(self.CONFIG_DIR, "r") as f:
            self.config = yaml.safe_load(f)

        
    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value

    def save(self):
        def represent_inline_list(dumper, data):
            return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)

        yaml.add_representer(list, represent_inline_list)

        with open(self.CONFIG_DIR, "w") as f:
            yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)


    def get_config(self):
        return self.config
    

if __name__ == "__main__":
    config_manager = ConfigManager()
    print(config_manager.get("PORT"))
    print(config_manager.get("CALIBRATION")[0]['angles'])
    config_manager.save()
