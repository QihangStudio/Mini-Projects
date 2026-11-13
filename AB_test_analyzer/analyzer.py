from scipy.stats import norm
import numpy as np


class ABAnalyzer:
    def __init__(self, data: list[dict[str, str | int]]) -> None:
        self.data: list[dict[str, str | int]] = data
        self.A: list[int] = [
            int(row["converted"]) for row in data if row["group"] == "A"
        ]
        self.B: list[int] = [
            int(row["converted"]) for row in data if row["group"] == "B"
        ]

    def conversion_rates(self) -> tuple[float, float]:
        p_A = float(np.mean(self.A))
        p_B = float(np.mean(self.B))
        return p_A, p_B

    def pool_prop(self) -> float:
        return float(np.mean(self.A + self.B))

    def standard_error(self) -> float:
        p = self.pool_prop()
        return float(np.sqrt(
            p * (1 - p) *
            (1 / len(self.A) + 1 / len(self.B))
        ))

    def z_test(self) -> tuple[float, float]:
        p_A, p_B = self.conversion_rates()
        se = self.standard_error()

        z = (p_B - p_A) / se
        p_value = 2 * norm.sf(abs(z))

        return z, float(p_value)

    def interpret(self, alpha: float = 0.05) -> str:
        """
        REQUIRES: 0 < alpha < 1 and standard error > 0.
        EFFECTS:  Returns the statistical conclusion based on
                the two-sided p-value and significance level.
        """
        _, p_value = self.z_test()

        if p_value < alpha:
            return (
                "Reject H0. "
                "Statistically significant difference between A and B."
            )

        return (
            "Fail to reject H0. "
            "No statistically significant difference between A and B."
        )
