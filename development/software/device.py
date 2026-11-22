"""Public configuration v1. Contains no secret-layer export or authentication command."""
import json
from copy import deepcopy

def default_config():
    return {"version":1, "rgb":{"color":"#00ff00", "brightness":32, "enabled":False},
            "macros":[["" for _ in range(9)] for _ in range(2)]}

def validate(config):
    if not isinstance(config,dict) or set(config)!={"version","rgb","macros"}:
        raise ValueError("Campos de configuração inválidos")
    if type(config["version"]) is not int or config["version"]!=1:
        raise ValueError("Versão de configuração incompatível")
    rgb=config["rgb"]
    if not isinstance(rgb,dict) or set(rgb)!={"color","brightness","enabled"}:
        raise ValueError("RGB inválido")
    color=rgb["color"]
    if not isinstance(color,str) or len(color)!=7 or color[0]!="#" or any(c not in "0123456789abcdefABCDEF" for c in color[1:]):
        raise ValueError("Cor deve usar #RRGGBB")
    if type(rgb["brightness"]) is not int or not 0<=rgb["brightness"]<=255 or type(rgb["enabled"]) is not bool:
        raise ValueError("Brilho ou estado RGB inválido")
    layers=config["macros"]
    if not isinstance(layers,list) or len(layers)!=2:
        raise ValueError("Apenas as duas camadas comuns são configuráveis aqui")
    for layer in layers:
        if not isinstance(layer,list) or len(layer)!=9:
            raise ValueError("Cada camada deve conter nove teclas")
        for macro in layer:
            if not isinstance(macro,str) or len(macro)>256 or "\x00" in macro:
                raise ValueError("Texto deve conter até 256 caracteres, sem NUL")
            macro.encode("utf-8", errors="strict")
    return deepcopy(config)

class Simulator:
    def __init__(self): self.config=default_config()
    def request(self, request):
        if not isinstance(request,dict): raise ValueError("Comando inválido")
        if request.get("command")=="get_config" and set(request)=={"command"}:
            return deepcopy(self.config)
        if request.get("command")=="set_config" and set(request)=={"command","config"}:
            next_config=validate(request["config"])
            self.config=next_config
            return {"ok":True,"transport":"simulator"}
        raise ValueError("Comando não suportado")

def load(path):
    with open(path,encoding="utf-8") as stream: return validate(json.load(stream))
