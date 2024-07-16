from pydantic import BaseModel


class VaultMetadata(BaseModel):
    owner: str
    

class VaultEntry(BaseModel):
    something: str
