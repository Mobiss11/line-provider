import pytest
import httpx

from tests.mocks import MockRedis
from app.models.events import Event, EventStatus
from app.storage.redis import RedisStorage
from app.services.events import EventService

# URL вашего API
BASE_URL = "http://localhost:8000"

TEST_EVENTS = [
    {
        "event_id": "event1",
        "coefficient": 1.85,
        "deadline": "2024-03-25T12:00:00",
        "status": "new"
    },
    {
        "event_id": "event2",
        "coefficient": 2.10,
        "deadline": "2024-03-26T15:30:00",
        "status": "new"
    },
    {
        "event_id": "event3",
        "coefficient": 1.95,
        "deadline": "2024-03-27T18:45:00",
        "status": "new"
    }
]


@pytest.fixture
async def http_client():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        yield client


@pytest.fixture
def mock_redis():
    return MockRedis()


@pytest.fixture
def storage(mock_redis):
    storage = RedisStorage()
    storage.redis = mock_redis
    return storage


@pytest.fixture
def event_service(storage):
    return EventService(storage)


@pytest.fixture
def sample_event():
    return Event(
        event_id="test_event_1",
        coefficient=1.85,
        deadline="2024-03-25T12:00:00",
        status=EventStatus.NEW
    )


@pytest.fixture
def sample_events():
    return [Event(**event_data) for event_data in TEST_EVENTS]
