import configparser


def get_config():
    try:
        cfg = configparser.ConfigParser()
        cfg.read("config.ini", encoding="utf-8")
        return cfg
    except IOError:
        return {}
