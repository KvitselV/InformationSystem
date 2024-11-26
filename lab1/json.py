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
        )
