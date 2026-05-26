import logging
import sys
from functools import wraps

from flask import jsonify, request

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] in %(module)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app_errors.log'),
    ],
)
logger = logging.getLogger(__name__)


def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)

        except KeyError as e:
            logger.warning(
                f'Erro de validação: Campo {str(e)} ausente em {request.path}'
            )
            return (
                jsonify({'error': f'Campo obrigatório ausente: {str(e)}'}),
                400,
            )

        except ValueError as e:
            logger.warning(f'Valor inválido em {request.path}: {str(e)}')
            return jsonify({'error': str(e)}), 400

        except Exception as e:
            logger.error(
                f'Erro crítico em {request.method} {request.path}: {str(e)}',
                exc_info=True,
            )

            return (
                jsonify(
                    {
                        'error': 'Erro interno no servidor',
                        'message': 'Uma falha inesperada ocorreu.'
                        + ' Por favor, tente novamente mais tarde.',
                    }
                ),
                500,
            )

    return decorated_function
