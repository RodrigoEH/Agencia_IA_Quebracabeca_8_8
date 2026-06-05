"""ETAPA 11: testes automatizados do módulo de estados com unittest."""

import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from estado import (
    eh_solucionavel,
    gerar_sucessores,
    localizar_vazio,
    validar_estado,
)


class TestEstado(unittest.TestCase):
    """Verifica a representação e as operações básicas dos estados."""

    def setUp(self):
        self.estado_valido = (1, 2, 3, 4, 0, 6, 7, 5, 8)
        self.estado_repetido = (1, 2, 3, 4, 0, 6, 7, 5, 5)
        self.estado_tamanho_incorreto = (1, 2, 3, 4, 0, 6, 7, 5)
        self.estado_solucionavel = (1, 2, 3, 4, 0, 6, 7, 5, 8)
        self.estado_nao_solucionavel = (1, 2, 3, 4, 5, 6, 8, 7, 0)

    def test_validacao_de_estado_correto(self):
        self.assertTrue(validar_estado(self.estado_valido))

    def test_rejeicao_de_estado_com_valores_repetidos(self):
        self.assertFalse(validar_estado(self.estado_repetido))

    def test_rejeicao_de_estado_com_tamanho_incorreto(self):
        self.assertFalse(validar_estado(self.estado_tamanho_incorreto))

    def test_localizacao_do_espaco_vazio(self):
        self.assertEqual(localizar_vazio(self.estado_valido), 4)

    def test_movimentos_validos_do_estado_inicial(self):
        sucessores = gerar_sucessores(self.estado_valido)
        acoes = [acao for acao, _ in sucessores]
        estados = [estado for _, estado in sucessores]

        self.assertEqual(len(sucessores), 4)
        self.assertIn("Mover vazio para cima", acoes)
        self.assertIn("Mover vazio para baixo", acoes)
        self.assertIn("Mover vazio para esquerda", acoes)
        self.assertIn("Mover vazio para direita", acoes)
        self.assertIn((1, 0, 3, 4, 2, 6, 7, 5, 8), estados)
        self.assertIn((1, 2, 3, 4, 5, 6, 7, 0, 8), estados)
        self.assertIn((1, 2, 3, 0, 4, 6, 7, 5, 8), estados)
        self.assertIn((1, 2, 3, 4, 6, 0, 7, 5, 8), estados)

    def test_deteccao_de_estado_solucionavel(self):
        self.assertTrue(eh_solucionavel(self.estado_solucionavel))

    def test_deteccao_de_estado_nao_solucionavel(self):
        self.assertFalse(eh_solucionavel(self.estado_nao_solucionavel))


if __name__ == "__main__":
    unittest.main()
