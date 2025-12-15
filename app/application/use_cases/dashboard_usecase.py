from datetime import datetime
from collections import defaultdict
from app.infrastructure.mongodb.donation_repository_impl import DonationRepositoryImpl


class DashboardUseCase:
    def __init__(self):
        self.repo = DonationRepositoryImpl()

    async def execute(self) -> dict:
        donations = await self.repo.list_all()

        now = datetime.now()
        mes_atual = now.month
        ano_atual = now.year

        total_arrecadado = 0.0
        total_aplicado = 0.0
        doacoes_positivas = []
        doacoes_mes = 0
        doadores_unicos = set()

        for d in donations:
            value = float(d["value"])
            date = d.get("date")

            if not date:
                continue

            if value > 0:
                total_arrecadado += value
                doacoes_positivas.append(value)
                doadores_unicos.add(d["donor_email"])

                if date.month == mes_atual and date.year == ano_atual:
                    doacoes_mes += 1

            elif value < 0:
                total_aplicado += abs(value)

        doacao_media = (
            sum(doacoes_positivas) / len(doacoes_positivas)
            if doacoes_positivas else 0.0
        )

        saldo_disponivel = total_arrecadado - total_aplicado

        return {
            "total_arrecadado": total_arrecadado,
            "total_aplicado": total_aplicado,
            "saldo_disponivel": saldo_disponivel,
            "total_doadores": len(doadores_unicos),
            "doacao_media": doacao_media,
            "doacoes_mes": doacoes_mes
        }

    async def get_charts(self) -> dict:
        donations = await self.repo.list_all()

        line_data = defaultdict(float)
        pie_data = defaultdict(float)

        for d in donations:
            value = float(d.get("value", 0))
            date = d.get("date")
            categoria = d.get("type")

            # SOMENTE DOAÇÕES
            if value <= 0 or not date:
                continue

            # chave cronológica REAL
            key = (date.year, date.month)
            line_data[key] += value

            categoria_final = categoria if categoria else "Outros"
            pie_data[categoria_final] += value

        # ✅ ORDENAÇÃO CRONOLÓGICA
        sorted_keys = sorted(line_data.keys())

        labels = []
        values = []

        for year, month in sorted_keys:
            labels.append(datetime(year, month, 1).strftime("%b"))
            values.append(line_data[(year, month)])

        return {
            "line": {
                "labels": labels,
                "data": values
            },
            "pie": {
                "labels": list(pie_data.keys()),
                "data": list(pie_data.values())
            }
        }

