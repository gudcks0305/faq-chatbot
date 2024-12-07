from datetime import datetime

from pydantic import BaseModel


class Schema(BaseModel):
    class Config:
        # camel case 로 응답 변환
        populate_by_name = True

        # json_loads = loads removed in pydantic V2
        json_encoders = {
            datetime: lambda v: v.isoformat(timespec="milliseconds").replace(
                "+00:00", "Z"
            ),
        }
