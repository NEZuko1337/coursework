from fastapi import APIRouter, Depends, File, UploadFile, status

from src.algorithm.algorithm import InvestmentOptimizer
from src.backend.db.schemas.investments_results import (
    InvestmentsResultCreateSchema, OptimizationResultSchema)
from src.backend.db.session import session_manager
from src.backend.exceptions import BadRequestError, ServerError
from src.backend.middlewares.auth import auth_user
from src.backend.services.investments_results import InvestmentsResultService

router = APIRouter(dependencies=[Depends(auth_user)])


@router.post(
    "/upload_file/",
    status_code=status.HTTP_200_OK,
    response_model=OptimizationResultSchema
)
async def upload_file(
    excel_file: UploadFile = File(...)
):
    async_session = session_manager.async_session
    """
    Эндпоинт для загрузки Excel файла,
    оптимизации инвестиций и сохранения результатов в БД.
    """
    try:
        file_bytes = await excel_file.read()
    except Exception as e:
        raise BadRequestError(f"Не удалось прочитать файл: {e}")

    try:
        investments, profits = InvestmentOptimizer.load_data_from_excel_bytes(
            file_bytes=file_bytes
        )
    except ValueError as e:
        raise BadRequestError(str(e))

    try:
        max_profit, distribution = InvestmentOptimizer.optimize_investments(
            investments=investments,
            profits=profits
        )
        stats = InvestmentOptimizer.get_investment_stats(
            investments=investments,
            profits=profits,
            distribution=distribution
        )
    except Exception as e:
        raise ServerError(f"Ошибка оптимизации: {e}")

    result = OptimizationResultSchema(
        max_profit=max_profit,
        distribution=distribution,
        statistics=stats
    )

    # Преобразование данных для сохранения в БД
    try:
        # Конвертируем распределение в словарь {предприятие: сумма}
        distribution_dict = {
            str(i+1): amount
            for i, amount in enumerate(result.distribution)
        }

        # Формируем детализацию по предприятиям
        enterprise_details = {
            str(ent.enterprise_id): {
                "investment": ent.investment,
                "profit": ent.profit,
                "roi": ent.roi
            }
            for ent in result.statistics.enterprises
        }

        # Создаем объект для сохранения
        create_data = InvestmentsResultCreateSchema(
            file_name=excel_file.filename,
            max_profit=result.max_profit,
            total_investment=result.statistics.total_investment,
            roi=result.statistics.roi,
            distribution=distribution_dict,
            enterprise_details=enterprise_details
        )

        # Сохраняем в базу данных
        await InvestmentsResultService.create_investment(
            async_session=async_session,
            data=create_data
        )
    except Exception as e:
        raise ServerError(f"Ошибка сохранения результатов: {e}")

    return result


@router.get(
    path='/last_investment/',
    status_code=status.HTTP_200_OK
)
async def get_last_investment():
    async_session = session_manager.async_session
    """
    Эндпоинт для получения последнего сохраненного результата оптимизации.
    """
    try:
        result = await InvestmentsResultService.get_last_investment(
            async_session=async_session
        )
    except Exception as e:
        raise ServerError(f"Ошибка получения последнего результата: {e}")

    return result

@router.get(
    path='/investments/',
    status_code=status.HTTP_200_OK,
)
async def get_all_investments():
    async_session = session_manager.async_session
    """
    Эндпоинт для получения всех сохраненных результатов оптимизации.
    """
    try:
        results = await InvestmentsResultService.get_all_investments(
            async_session=async_session
        )
    except Exception as e:
        raise ServerError(f"Ошибка получения всех результатов: {e}")

    return results