from ..utils.base_schema import CamelBaseModel


class JWTData(CamelBaseModel):
    id: int
    email: str
    is_admin: bool
    exp: int
