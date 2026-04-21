import json
import xml.etree.ElementTree as ET

class State:
    def __init__(self, name, is_initial=False, is_final=False):
        self.name = name
        self.is_initial = is_initial
        self.is_final = is_final

    def __repr__(self):
        return self.name

class AFD:
    def __init__(self):
        self.states = []
        self.alphabet = set()
        self.initial_state = None
        self.final_states = []
        self.transitions = {}

    def add_state(self, name, is_initial=False, is_final=False):
        if any(s.name == name for s in self.states):
            return None
        new_state = State(name, is_initial, is_final)
        self.states.append(new_state)
        if is_initial:
            self.initial_state = new_state
        if is_final:
            self.final_states.append(new_state)
        return new_state

    def add_transition(self, from_state_name, symbol, to_state_name):
        from_s = self.get_state_by_name(from_state_name)
        to_s = self.get_state_by_name(to_state_name)
        
        if from_s and to_s:
            if symbol != '':
                self.alphabet.add(symbol)
            self.transitions[(from_s, symbol)] = to_s
            return True
        return False

    def get_state_by_name(self, name):
        for state in self.states:
            if state.name == name:
                return state
        return None

    def validate_string(self, input_string):
        if not self.initial_state:
            return False, "No hay estado inicial"

        current_state = self.initial_state
        path = [current_state.name]

        for symbol in input_string:
            if (current_state, symbol) not in self.transitions:
                return False, f"Bloqueado en {current_state.name} con '{symbol}'"
            current_state = self.transitions[(current_state, symbol)]
            path.append(current_state.name)

        es_valido = current_state in self.final_states
        return es_valido, " -> ".join(path)
 
    def minimizar_y_reportar(self):
        reporte = "=== PROCESO DE MINIMIZACIÓN ===\n\n"
        finales = [s.name for s in self.final_states]
        no_finales = [s.name for s in self.states if s not in self.final_states]
        grupos = []
        if no_finales: grupos.append(no_finales)
        if finales: grupos.append(finales)
        reporte += f"Paso 0: Partición inicial (Finales vs No Finales)\n"
        reporte += f"  Grupos: {grupos}\n\n"
        cambio = True
        paso = 1
        while cambio:
            nuevos_grupos = []
            cambio = False
            reporte += f"=== Refinamiento Paso {paso} ===\n"
            for grupo in grupos:
                if len(grupo) <= 1:
                    nuevos_grupos.append(grupo)
                    continue
                comportamiento = {}
                for s_name in grupo:
                    clave = []
                    for simbolo in sorted(list(self.alphabet)):
                        destino = self.transitions.get((self.get_state_by_name(s_name), simbolo))
                        if destino:
                            for idx, g in enumerate(grupos):
                                if destino.name in g:
                                    clave.append(idx)
                                    break
                                else:
                                    clave.append(-1) # No hay transición
                                    clave_tuple = tuple(clave)
                                    if clave_tuple not in comportamiento:
                                        comportamiento[clave_tuple] = []
                                        comportamiento[clave_tuple].append(s_name)
                                        if len(comportamiento) > 1:
                                            cambio = True
                                            for g_div in comportamiento.values():
                                                nuevos_grupos.append(g_div)
                                                reporte += f"  Estado(s) {g_div} forman nuevo subgrupo por transiciones idénticas.\n"

                                            else:
                                                nuevos_grupos.append(grupo)
                                                reporte += f"  Grupo {grupo} se mantiene estable.\n"
                                                grupos = nuevos_grupos
                                                reporte += f"  Partición actual: {grupos}\n\n"
                                                paso += 1
                                                if paso > 10: break
                                                reporte += "=== AFD MINIMIZADO ===\n"
                                                reporte += f"Estados finales combinados: {grupos}\n"
                                                return reporte

    def to_dict(self):
        return {
            "states": [{"name": s.name, "is_initial": s.is_initial, "is_final": s.is_final} for s in self.states],
            "transitions": [
                {"from": f.name, "symbol": s, "to": t.name} 
                for (f, s), t in self.transitions.items()
            ]
        }
    

    @classmethod
    def from_dict(cls, data):
        nuevo_afd = cls()
        for s in data["states"]:
            nuevo_afd.add_state(s["name"], s["is_initial"], s["is_final"])
        for t in data["transitions"]:
            nuevo_afd.add_transition(t["from"], t["symbol"], t["to"])
        return nuevo_afd

    @classmethod
    def from_jff_format(cls, jff_content):
        afd = cls()
        root = ET.fromstring(jff_content)
        id_to_state = {}
        for state_elem in root.findall(".//state"):
            s_id = state_elem.get("id")
            s_name = state_elem.get("name", f"q{s_id}")
            is_initial = state_elem.find("initial") is not None
            is_final = state_elem.find("final") is not None
            nuevo_estado = afd.add_state(s_name, is_initial, is_final)
            id_to_state[s_id] = nuevo_estado

        for trans_elem in root.findall(".//transition"):
            from_id = trans_elem.find("from").text
            to_id = trans_elem.find("to").text
            read_elem = trans_elem.find("read")
            symbol = read_elem.text if read_elem is not None and read_elem.text else ""
            from_state = id_to_state.get(from_id)
            to_state = id_to_state.get(to_id)
            if from_state and to_state:
                afd.add_transition(from_state.name, symbol, to_state.name)
        return afd