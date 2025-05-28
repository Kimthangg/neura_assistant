import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from datetime import datetime, timedelta

import pytest

from bot.agent import extraction_model
from bot.agent_intent import intent_model

# Test cases for intent classification
test_intent_cases = [
    ("Đặt lịch ăn tối với toàn vào tối nay", "create_normal_event"),
    ("Tạo lịch họp team vào lúc 14h chiều mai", "create_normal_event"),
    ("Lịch của tôi ngày mai là gì?", "get_first_calendar"),
    ("Tôi có những lịch hẹn nào vào tuần tới?", "get_first_calendar"),
    ("Xoá lịch họp ngày mai", "delete_event"),
    ("Cập nhật thời gian cuộc họp vào ngày 20/5", "update_event"),
    ("Bạn có thể giúp tôi tìm thời gian trống ngày mai được không?", "get_freetime"),
    ("Chào bạn, thời tiết hôm nay thế nào?", "normal_message"),
]

# Test cases for datetime extraction
test_extraction_cases = [
    ("Đặt lịch ăn tối với toàn vào tối nay", datetime.now().strftime("%Y-%m-%d")),
    (
        "Tạo lịch họp team vào lúc 14h chiều mai",
        (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
    ),
    (
        "Xoá lịch họp ngày mai",
        (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
    ),
    ("Cập nhật thời gian cuộc họp vào ngày 20/5", f"{datetime.now().year}-05-20"),
]


@pytest.mark.parametrize("prompt, expected_intent", test_intent_cases)
def test_intent_classification(prompt, expected_intent):
    """Test if the intent model correctly classifies messages"""
    result = intent_model(prompt)
    assert result is not None, f"Intent model returned None for prompt: {prompt}"
    assert "intent" in result, f"Intent key missing in result for prompt: {prompt}"
    assert (
        result["intent"] == expected_intent
    ), f"Expected intent '{expected_intent}' but got '{result['intent']}' for prompt: {prompt}"


@pytest.mark.parametrize("prompt, expected_date", test_extraction_cases)
def test_datetime_extraction(prompt, expected_date):
    """Test if the extraction model correctly extracts datetime information"""
    result = extraction_model(prompt)
    assert result is not None, f"Extraction model returned None for prompt: {prompt}"
    assert (
        "datetime_ranges" in result
    ), f"datetime_ranges key missing in result for prompt: {prompt}"
    assert (
        len(result["datetime_ranges"]) > 0
    ), f"No datetime ranges found for prompt: {prompt}"

    # Check if the extracted date matches the expected date
    extracted_date = result["datetime_ranges"][0]["start_datetime"].split()[
        0
    ]  # Get just the date part
    assert (
        extracted_date == expected_date
    ), f"Expected date '{expected_date}' but got '{extracted_date}' for prompt: {prompt}"


def test_extraction_structure():
    """Test if the extraction model returns the expected structure"""
    prompt = "Đặt lịch ăn tối với toàn vào tối nay"
    result = extraction_model(prompt)

    # Verify the structure of the returned data
    assert "datetime_ranges" in result, "datetime_ranges missing in result"
    assert isinstance(
        result["datetime_ranges"], list
    ), "datetime_ranges should be a list"

    # For each datetime range, verify required fields
    for dt_range in result["datetime_ranges"]:
        assert "start_datetime" in dt_range, "start_datetime missing in datetime range"
        assert "end_datetime" in dt_range, "end_datetime missing in datetime range"

        # Verify datetime format (YYYY-MM-DD HH:MM:SS)
        start_dt = dt_range["start_datetime"]
        end_dt = dt_range["end_datetime"]

        assert len(start_dt) == 19, f"start_datetime format incorrect: {start_dt}"
        assert len(end_dt) == 19, f"end_datetime format incorrect: {end_dt}"


if __name__ == "__main__":
    # Run a simple test example
    prompt = "Đặt lịch ăn tối với toàn vào tối nay"
    intent_result = intent_model(prompt)
    print(f"Intent classification: {intent_result}")

    extraction_result = extraction_model(prompt)
    print(f"Datetime extraction: {extraction_result['datetime_ranges']}")
