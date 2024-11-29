from common_utils.logger import ActionLogger
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

from task.infras.db.connection import DBConnectionHandler

action_logger = ActionLogger()
db = DBConnectionHandler()
metrics = GunicornInternalPrometheusMetrics.for_app_factory()
metrics.group_by = "url_rule"
