"""Модуль отвечает за старт ETL процесса."""

from config.settings import STATE_STORAGE_PARAMS, PROCESS_IS_STARTED_STATE
from services.storages.api import get_backoff_key_value_storage
from services.process.processes import ETLProcess, ETLProcessType, ETLProcessParameters

if __name__ == '__main__':
    state_storage = get_backoff_key_value_storage(STATE_STORAGE_PARAMS)
    etl_params = ETLProcessParameters(
        state_storage=state_storage,
        process_type=ETLProcessType.FILM_WORK,
        loader=None,
        extractor=None,
    )

    state_storage.set_value(PROCESS_IS_STARTED_STATE, 0)

    with ETLProcess(etl_params) as process:
        process.start()
