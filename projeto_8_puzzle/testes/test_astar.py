"""ETAPA 11: testes automatizados do algoritmo A* com unittest."""

import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from agente_astar import resolver_astar
from estado import ESTADO_OBJETIVO
from heuristicas import distancia_manhattan, distancia_manhattan_nao_admissivel


class TestAStar(unittest.TestCase):
    """Verifica a execução do A* com as duas heurísticas disponíveis."""

    def setUp(self):
        self.estado_inicial = (1, 2, 3, 4, 0, 6, 7, 5, 8)

    def test_solucao_do_estado_inicial_exemplo_com_heuristica_admissivel(self):
        resultado = resolver_astar(
            estado_inicial=self.estado_inicial,
            estado_objetivo=ESTADO_OBJETIVO,
            funcao_heuristica=distancia_manhattan,
            registrar_historico=True,
        )

        self.assertTrue(resultado["encontrou_solucao"])
        self.assertEqual(resultado["custo_total"], 2)
        self.assertEqual(resultado["caminho"][-1]["estado"], ESTADO_OBJETIVO)
        self.assertGreaterEqual(resultado["estados_expandidos"], 1)
        self.assertGreaterEqual(len(resultado["historico"]), 1)

    def test_execucao_da_heuristica_admissivel(self):
        resultado = resolver_astar(
            estado_inicial=self.estado_inicial,
            estado_objetivo=ESTADO_OBJETIVO,
            funcao_heuristica=distancia_manhattan,
            registrar_historico=False,
        )

        self.assertTrue(resultado["encontrou_solucao"])
        self.assertEqual(resultado["custo_total"], 2)
        self.assertEqual(resultado["caminho"][-1]["estado"], ESTADO_OBJETIVO)

    def test_execucao_da_heuristica_nao_admissivel(self):
        resultado = resolver_astar(
            estado_inicial=self.estado_inicial,
            estado_objetivo=ESTADO_OBJETIVO,
            funcao_heuristica=distancia_manhattan_nao_admissivel,
            registrar_historico=False,
        )

        self.assertTrue(resultado["encontrou_solucao"])
        self.assertEqual(resultado["caminho"][-1]["estado"], ESTADO_OBJETIVO)
        self.assertEqual(resultado["custo_total"], 2)


if __name__ == "__main__":
    unittest.main()
