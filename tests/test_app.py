from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def restore_activities_state():
    original_activities = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_activities)


def test_unregister_participant_removes_email_from_activity():
    client = TestClient(app)
    activity_name = "Chess Club"
    participant_email = activities[activity_name]["participants"][0]

    response = client.delete(f"/activities/{activity_name}/participants/{participant_email}")

    assert response.status_code == 200
    assert participant_email not in activities[activity_name]["participants"]
    assert response.json() == {
        "message": f"Unregistered {participant_email} from {activity_name}"
    }
