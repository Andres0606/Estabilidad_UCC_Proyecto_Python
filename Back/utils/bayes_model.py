import xml.etree.ElementTree as ET


class BayesModel:

    def __init__(self, xml_path, target):
        self.tree = ET.parse(xml_path)
        self.root = self.tree.getroot()
        self.target = target

        self.variables = {}
        self.probabilities = {}

        self._load_variables()
        self._load_probabilities()

    # -----------------------------
    # Cargar variables
    # -----------------------------
    def _load_variables(self):
        for var in self.root.iter("VARIABLE"):
            name = var.find("NAME").text.strip()

            outcomes = []
            for outcome in var.findall("OUTCOME"):
                outcomes.append(outcome.text.strip())

            self.variables[name] = outcomes

    # -----------------------------
    # Cargar probabilidades
    # -----------------------------
    def _load_probabilities(self):
        for definition in self.root.iter("DEFINITION"):
            var = definition.find("FOR").text.strip()

            given = []
            for g in definition.findall("GIVEN"):
                given.append(g.text.strip())

            table = definition.find("TABLE").text.strip()
            probs = list(map(float, table.split()))

            self.probabilities[var] = {
                "given": given,
                "table": probs
            }

    # -----------------------------
    # LIMPIAR claves (MUY IMPORTANTE)
    # -----------------------------
    def _clean_key(self, key):
        return key.strip().replace("  ", " ").replace("\xa0", " ")

    # -----------------------------
    # QUERY (AQUÍ ESTÁ LA MAGIA)
    # -----------------------------
    def query(self, evidence):

        print("\n===== EVIDENCIA ORIGINAL =====")
        print(evidence)

        # limpiar claves
        evidence_clean = {}
        for k, v in evidence.items():
            new_key = self._clean_key(k)
            evidence_clean[new_key] = v

        print("\n===== EVIDENCIA LIMPIA =====")
        for k, v in evidence_clean.items():
            print(f"{k} = {v}")

        target_probs = self.probabilities[self.target]["table"]
        target_states = self.variables[self.target]

        result = {}

        # cálculo simple tipo Naive Bayes
        for i, state in enumerate(target_states):

            prob = target_probs[i]

            for var, value in evidence_clean.items():

                if var not in self.probabilities:
                    continue

                definition = self.probabilities[var]

                # solo variables que dependen del target
                if self.target not in definition["given"]:
                    continue

                outcomes = self.variables[var]

                if value not in outcomes:
                    print(f"⚠️ VALOR NO ENCONTRADO: {var} = {value}")
                    continue

                index_value = outcomes.index(value)

                # calcular posición en tabla
                index = i * len(outcomes) + index_value

                prob *= definition["table"][index]

            result[state] = prob

        # normalizar
        total = sum(result.values())
        if total > 0:
            for k in result:
                result[k] /= total

        print("\n===== RESULTADO FINAL =====")
        print(result)

        return result