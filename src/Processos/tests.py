import datetime
import json
from unittest.mock import MagicMock, patch

from django.test import TestCase
from django.utils import timezone

from Processos.models import ProcessoLegislativo
from Processos.services import (
    _coerce_list,
    _extract_ano_camara,
    _mapear_processo_senado_da_listagem,
    _parse_date,
    _parse_datetime,
    atualizar_detalhes_camara,
    atualizar_detalhes_senado,
    buscar_todas_proposicoes_camara,
    popular_banco_carga_inicial,
)


class ParseDateTestCase(TestCase):
    """Testes para a função _parse_date."""

    def test_date_simples(self):
        self.assertEqual(_parse_date("2025-01-31"), datetime.date(2025, 1, 31))

    def test_date_com_datetime(self):
        self.assertEqual(_parse_date("2025-01-31T09:00"), datetime.date(2025, 1, 31))

    def test_date_com_datetime_completo(self):
        self.assertEqual(_parse_date("2025-01-31T09:00:00"), datetime.date(2025, 1, 31))

    def test_date_vazia(self):
        self.assertIsNone(_parse_date(""))

    def test_date_none(self):
        self.assertIsNone(_parse_date(None))

    def test_date_invalida(self):
        self.assertIsNone(_parse_date("invalido"))

    def test_date_formato_errado(self):
        self.assertIsNone(_parse_date("31/01/2025"))


class ParseDatetimeTestCase(TestCase):
    """Testes para a função _parse_datetime."""

    def test_datetime_completo(self):
        result = _parse_datetime("2025-01-31T09:00:00")
        self.assertIsNotNone(result)
        self.assertEqual(result.year, 2025)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 31)
        self.assertFalse(timezone.is_naive(result))

    def test_datetime_sem_hora(self):
        result = _parse_datetime("2025-01-31")
        self.assertIsNotNone(result)
        self.assertEqual(result.year, 2025)
        self.assertFalse(timezone.is_naive(result))

    def test_datetime_vazio(self):
        self.assertIsNone(_parse_datetime(""))

    def test_datetime_none(self):
        self.assertIsNone(_parse_datetime(None))

    def test_datetime_invalido(self):
        self.assertIsNone(_parse_datetime("nao-e-data"))


class CoerceListTestCase(TestCase):
    """Testes para a função _coerce_list."""

    def test_none(self):
        self.assertEqual(_coerce_list(None), [])

    def test_lista(self):
        self.assertEqual(_coerce_list([1, 2, 3]), [1, 2, 3])

    def test_lista_vazia(self):
        self.assertEqual(_coerce_list([]), [])

    def test_valor_unico(self):
        self.assertEqual(_coerce_list("item"), ["item"])

    def test_dict_unico(self):
        d = {"key": "value"}
        self.assertEqual(_coerce_list(d), [d])


class ExtractAnoCamaraTestCase(TestCase):
    """Testes para a função _extract_ano_camara."""

    def test_ano_valido(self):
        self.assertEqual(_extract_ano_camara(2025, None), "2025")

    def test_ano_zero_com_data(self):
        data = datetime.date(2025, 6, 1)
        self.assertEqual(_extract_ano_camara(0, data), "2025")

    def test_ano_none_com_data(self):
        data = datetime.date(2024, 3, 15)
        self.assertEqual(_extract_ano_camara(None, data), "2024")

    def test_ano_zero_sem_data(self):
        self.assertEqual(_extract_ano_camara(0, None), "")

    def test_ano_none_sem_data(self):
        self.assertEqual(_extract_ano_camara(None, None), "")

    def test_ano_como_string(self):
        self.assertEqual(_extract_ano_camara("2025", None), "2025")


class MapearProcessoSenadoTestCase(TestCase):
    """Testes para o mapeamento de processos da nova API do Senado."""

    def test_mapeamento_basico(self):
        proc = {
            'id': 8786001,
            'codigoMateria': 166997,
            'identificacao': 'PL 3/2025',
            'sigla': 'PL',
            'numero': '3',
            'ano': 2025,
            'ementa': 'Disciplina o processo estrutural.',
            'autoria': 'Senador Rodrigo Pacheco (PSD/MG)',
            'situacaoAtual': 'MATÉRIA COM A RELATORIA',
            'tipoConteudo': 'Norma Geral',
            'tipoDocumento': 'Projeto de Lei',
            'tramitando': 'Sim',
            'casaIdentificadora': 'SF',
            'objetivo': 'Iniciadora',
            'dataApresentacao': '2025-01-31',
        }
        resultado = _mapear_processo_senado_da_listagem(proc)

        self.assertEqual(resultado['numero'], '3')
        self.assertEqual(resultado['ano'], '2025')
        self.assertEqual(resultado['ementa'], 'Disciplina o processo estrutural.')
        self.assertEqual(resultado['tipo_proposicao'], 'PL')
        self.assertEqual(resultado['status_atual'], 'MATÉRIA COM A RELATORIA')
        self.assertEqual(resultado['id_processo_senado'], '8786001')
        self.assertEqual(resultado['tipo_conteudo'], 'Norma Geral')
        self.assertEqual(resultado['tipo_documento'], 'Projeto de Lei')
        self.assertTrue(resultado['tramitando'])
        self.assertEqual(resultado['casa_identificadora'], 'SF')
        self.assertEqual(resultado['objetivo'], 'Iniciadora')

    def test_mapeamento_com_apelido(self):
        proc = {
            'id': 123,
            'codigoMateria': 456,
            'identificacao': 'MPV 2172-32/2001',
            'sigla': 'MPV',
            'apelido': 'Nulidade de cláusulas usurárias',
            'tramitando': 'Não',
        }
        resultado = _mapear_processo_senado_da_listagem(proc)
        self.assertEqual(resultado['apelido'], 'Nulidade de cláusulas usurárias')
        self.assertFalse(resultado['tramitando'])

    def test_mapeamento_campos_ausentes(self):
        proc = {'id': 999}
        resultado = _mapear_processo_senado_da_listagem(proc)
        self.assertEqual(resultado['id_processo_senado'], '999')
        self.assertEqual(resultado['ementa'], '')
        self.assertIsNone(resultado['tramitando'])


class AtualizarDetalhesCamaraTestCase(TestCase):
    """Testes para atualizar_detalhes_camara com mocks."""

    def setUp(self):
        self.processo = ProcessoLegislativo.objects.create(
            id_externo='12345',
            origem_camara_ou_senado='CAMARA',
            numero='100',
            ano='2025',
            ementa='Ementa original',
            tipo_proposicao='PL',
            status_atual='Em tramitação',
        )

    @patch('Processos.services.buscar_tramitacoes_camara')
    @patch('Processos.services.buscar_detalhe_camara')
    def test_atualiza_campos_basicos(self, mock_detalhe, mock_tramitacoes):
        mock_detalhe.return_value = {
            'statusProposicao': {
                'descricaoSituacao': 'Aprovada',
                'descricaoTramitacao': 'Tramitação concluída',
                'siglaOrgao': 'PLEN',
                'regime': 'Urgência',
            },
            'ementa': 'Ementa atualizada',
            'siglaTipo': 'PL',
            'numero': 100,
            'ano': 2025,
            'dataApresentacao': '2025-01-15',
        }
        mock_tramitacoes.return_value = [{'id': 1, 'descricao': 'Tramite 1'}]

        result = atualizar_detalhes_camara(self.processo)

        self.assertTrue(result)
        self.processo.refresh_from_db()
        self.assertEqual(self.processo.status_atual, 'Aprovada')
        self.assertEqual(self.processo.ementa, 'Ementa atualizada')
        self.assertEqual(self.processo.orgao_atual, 'PLEN')
        self.assertEqual(self.processo.regime, 'Urgência')
        self.assertIsNotNone(self.processo.detalhes_atualizados_em)

    @patch('Processos.services.buscar_detalhe_camara')
    def test_retorna_false_sem_dados(self, mock_detalhe):
        mock_detalhe.return_value = {}
        result = atualizar_detalhes_camara(self.processo)
        self.assertFalse(result)


class AtualizarDetalhesSenadoTestCase(TestCase):
    """Testes para atualizar_detalhes_senado com a nova API."""

    def setUp(self):
        self.processo = ProcessoLegislativo.objects.create(
            id_externo='166997',
            origem_camara_ou_senado='SENADO',
            numero='3',
            ano='2025',
            ementa='Ementa original',
            tipo_proposicao='PL',
            status_atual='Apresentada',
            id_processo_senado='8786001',
        )

    @patch('Processos.services.buscar_detalhe_senado')
    def test_atualiza_campos_nova_api(self, mock_detalhe):
        mock_detalhe.return_value = {
            'id': 8786001,
            'codigoMateria': 166997,
            'identificacao': 'PL 3/2025',
            'sigla': 'PL',
            'descricaoSigla': 'Projeto de Lei',
            'numero': '3',
            'ano': 2025,
            'objetivo': 'Iniciadora',
            'casaIdentificadora': 'SF',
            'situacaoAtual': 'AGUARDANDO DESPACHO',
            'dataSituacaoAtual': '2025-01-31',
            'tramitando': 'Sim',
            'conteudo': {
                'tipo': 'Norma Geral',
                'ementa': 'Disciplina o processo estrutural.',
            },
            'documento': {
                'dataApresentacao': '2025-01-31',
                'indexacao': 'PROCESSO CIVIL, AÇÃO CIVIL PUBLICA',
                'url': 'https://legis.senado.gov.br/sdleg-getter/documento?dm=9889342',
                'autoria': [
                    {
                        'autor': 'Rodrigo Pacheco',
                        'siglaPartido': 'PSD',
                        'uf': 'MG',
                    }
                ],
            },
        }

        result = atualizar_detalhes_senado(self.processo)

        self.assertTrue(result)
        self.processo.refresh_from_db()
        self.assertEqual(self.processo.status_atual, 'AGUARDANDO DESPACHO')
        self.assertEqual(self.processo.ementa, 'Disciplina o processo estrutural.')
        self.assertEqual(self.processo.tipo_conteudo, 'Norma Geral')
        self.assertEqual(self.processo.casa_identificadora, 'SF')
        self.assertEqual(self.processo.objetivo, 'Iniciadora')
        self.assertTrue(self.processo.tramitando)
        self.assertIn('Rodrigo Pacheco', self.processo.autor)
        self.assertIsNotNone(self.processo.detalhes_atualizados_em)

    @patch('Processos.services.buscar_detalhe_senado')
    def test_retorna_false_sem_dados(self, mock_detalhe):
        mock_detalhe.return_value = {}
        result = atualizar_detalhes_senado(self.processo)
        self.assertFalse(result)

    def test_retorna_false_sem_id_processo(self):
        self.processo.id_processo_senado = None
        self.processo.save()
        result = atualizar_detalhes_senado(self.processo)
        self.assertFalse(result)


class BuscarTodasProposicoesCamaraTestCase(TestCase):
    """Testes para paginação da API da Câmara."""

    @patch('Processos.services._get_json')
    def test_paginacao_simples(self, mock_get_json):
        mock_get_json.side_effect = [
            {
                'dados': [{'id': 1, 'ementa': 'Prop 1'}],
                'links': [{'rel': 'next', 'href': 'https://api/page2'}],
            },
            {
                'dados': [{'id': 2, 'ementa': 'Prop 2'}],
                'links': [{'rel': 'self', 'href': 'https://api/page2'}],
            },
        ]

        result = buscar_todas_proposicoes_camara()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[1]['id'], 2)

    @patch('Processos.services._get_json')
    def test_api_falha(self, mock_get_json):
        mock_get_json.return_value = None
        result = buscar_todas_proposicoes_camara()
        self.assertEqual(result, [])


class PopularBancoCargaInicialTestCase(TestCase):
    """Testes para carga inicial."""

    @patch('Processos.services.buscar_todos_processos_senado')
    @patch('Processos.services.buscar_todas_proposicoes_camara')
    def test_carga_basica(self, mock_camara, mock_senado):
        mock_camara.return_value = [
            {
                'id': 100,
                'numero': 1,
                'ano': 2025,
                'ementa': 'Teste câmara',
                'siglaTipo': 'PL',
                'dataApresentacao': '2025-01-01',
                'uri': 'https://api/100',
            },
        ]
        mock_senado.return_value = [
            {
                'id': 8000001,
                'codigoMateria': 200,
                'identificacao': 'PL 1/2025',
                'sigla': 'PL',
                'numero': '1',
                'ano': 2025,
                'ementa': 'Teste senado',
                'autoria': 'Senador Teste',
                'situacaoAtual': 'Em análise',
                'tramitando': 'Sim',
                'tipoConteudo': 'Norma Geral',
                'tipoDocumento': 'Projeto de Lei',
                'casaIdentificadora': 'SF',
                'dataApresentacao': '2025-02-01',
            },
        ]

        novos = popular_banco_carga_inicial(ano_inicio=2025)
        self.assertEqual(novos, 2)
        self.assertEqual(ProcessoLegislativo.objects.count(), 2)

        # Verifica Câmara
        proc_camara = ProcessoLegislativo.objects.get(id_externo='100', origem_camara_ou_senado='CAMARA')
        self.assertEqual(proc_camara.ementa, 'Teste câmara')

        # Verifica Senado
        proc_senado = ProcessoLegislativo.objects.get(id_externo='200', origem_camara_ou_senado='SENADO')
        self.assertEqual(proc_senado.ementa, 'Teste senado')
        self.assertEqual(proc_senado.id_processo_senado, '8000001')
        self.assertTrue(proc_senado.tramitando)

    @patch('Processos.services.buscar_todos_processos_senado')
    @patch('Processos.services.buscar_todas_proposicoes_camara')
    def test_filtra_por_ano(self, mock_camara, mock_senado):
        mock_camara.return_value = []
        mock_senado.return_value = [
            {
                'id': 1,
                'codigoMateria': 100,
                'identificacao': 'PL 1/2020',
                'sigla': 'PL',
                'ano': 2020,
                'ementa': 'Antigo',
                'tramitando': 'Sim',
            },
            {
                'id': 2,
                'codigoMateria': 200,
                'identificacao': 'PL 1/2025',
                'sigla': 'PL',
                'ano': 2025,
                'ementa': 'Recente',
                'tramitando': 'Sim',
            },
        ]

        novos = popular_banco_carga_inicial(ano_inicio=2024)
        self.assertEqual(novos, 1)
        self.assertTrue(ProcessoLegislativo.objects.filter(id_externo='200').exists())
        self.assertFalse(ProcessoLegislativo.objects.filter(id_externo='100').exists())
