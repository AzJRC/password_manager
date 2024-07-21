from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class Vault(Base):
    __tablename__ = "vaults"

    vault_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    entries = relationship("VaultEntries", back_populates="vault")


class VaultEntries(Base):
    __tablename__ = "vault_entries"

    entry_id = Column(Integer, primary_key=True)
    vault_id = Column(Integer, ForeignKey("vaults.vault_id"))
    service_name = Column(String, nullable=False)
    encrypted_password = Column(String, nullable=False)

    vault = relationship("Vault", back_populates="entries")
