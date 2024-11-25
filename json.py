import json

class Soiskatel:
    def __init__(self, fam, imya, otchestvo, kvalifikaciya, professiya, data_rozhdeniya, telefon, adres):
        self.fam = Validator.validate_name(fam, "Фамилия")
        self.imya = Validator.validate_name(imya, "Имя")
        self.otchestvo = otchestvo
        self.kvalifikaciya = Validator.validate_non_empty(kvalifikaciya, "Квалификация")
        self.professiya = Validator.validate_non_empty(professiya, "Профессия")
        self.data_rozhdeniya = Validator.validate_date(data_rozhdeniya)
        self.telefon = Validator.validate_phone(telefon)
        self.adres = adres

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(
            fam=data["fam"],
            imya=data["imya"],
            otchestvo=data.get("otchestvo", ""),
            kvalifikaciya=data["kvalifikaciya"],
            professiya=data["professiya"],
            data_rozhdeniya=date.fromisoformat(data["data_rozhdeniya"]),
            telefon=data["telefon"],
            adres=data["adres"]
        )
