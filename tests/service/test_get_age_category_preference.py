from src.app.service import PurchasesService


def test_age_category_preference(mock_purchases_service: PurchasesService):
    expected_result = {
        30: "Electronics",
        25: "Clothing"
    }
    assert mock_purchases_service.get_age_category_preference() == expected_result


def test_empty_purchases(mock_empty_purchases_service: PurchasesService):
    assert mock_empty_purchases_service.get_age_category_preference() == {}
