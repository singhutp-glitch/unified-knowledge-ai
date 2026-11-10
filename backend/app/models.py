from sqlalchemy.dialects.postgresql import TSVECTOR
from datetime import datetime
from sqlalchemy import Computed

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Column,
    CheckConstraint,
    Index,
    func,
    text
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    


    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    chats: Mapped[list["Chat"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    documents: Mapped[list["Document"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="chats",
    )

    documents: Mapped[list["Document"]] = relationship(
        back_populates="chat",
        cascade="all, delete-orphan",
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat",
        cascade="all, delete-orphan",
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    chat: Mapped["Chat"] = relationship(
        back_populates="messages",
    )

    citations: Mapped[list["Citation"]] = relationship(
        back_populates="message",
        cascade="all, delete-orphan",
    )

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    original_file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    stored_file_name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    document_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="user",
        server_default="user",
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    chat_id: Mapped[int | None] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    user: Mapped["User | None"] = relationship(
        back_populates="documents",
    )

    chat: Mapped["Chat | None"] = relationship(
        back_populates="documents",
    )

    chunks: Mapped[list["Chunk"]] = relationship(
    back_populates="document",
    cascade="all, delete-orphan",
    passive_deletes=True,
)

    company_details: Mapped["CompanyDocument | None"] = relationship(
        back_populates="document",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True,
        passive_deletes=True,
    )

    __table_args__ = (
        CheckConstraint(
            """
            (
                document_type = 'user'
                AND user_id IS NOT NULL
                AND chat_id IS NOT NULL
            )
            OR
            (
                document_type = 'company'
                AND user_id IS NULL
                AND chat_id IS NULL
            )
            """,
            name="check_document_ownership",
        ),
    )

    
class CompanyDocument(Base):
    __tablename__ = "company_documents"

    document_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("documents.id", ondelete="CASCADE"),
        primary_key=True,
    )

    source_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sources.id"),
        nullable=False,
        index=True,
    )

    external_file_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    external_modified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    document: Mapped["Document"] = relationship(
        back_populates="company_details",
    )

    source: Mapped["Source"] = relationship()

    __table_args__ = (
        UniqueConstraint(
            "source_id",
            "external_file_id",
            name="uq_company_document_source_file",
        ),
    )


class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    document_id: Mapped[int] = mapped_column(
    ForeignKey("documents.id", ondelete="CASCADE"),
    nullable=False,
    index=True,
)

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    section_heading: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    pages: Mapped[list[int]] = mapped_column(
        ARRAY(Integer),
        nullable=False,
    )

    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(),
        nullable=True,
    )

    search_vector = mapped_column(
    TSVECTOR,
    Computed(
        "to_tsvector('english', coalesce(text, ''))",
        persisted=True
        )
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    document: Mapped["Document"] = relationship(
        back_populates="chunks",
    )

    citations: Mapped[list["Citation"]] = relationship(
    back_populates="chunk",
    passive_deletes=True,
)

    __table_args__ = (
        UniqueConstraint(
            "document_id",
            "chunk_index",
            name="uq_chunks_document_chunk_index",
        ),
    )


class Citation(Base):
    __tablename__ = "citations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    citation_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    message_id: Mapped[int] = mapped_column(
        ForeignKey("messages.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    chunk_id: Mapped[int | None] = mapped_column(
    ForeignKey("chunks.id", ondelete="SET NULL"),
    nullable=True,
)

    message: Mapped["Message"] = relationship(
        back_populates="citations",
    )

    chunk: Mapped["Chunk | None"] = relationship(
    back_populates="citations",
)

    __table_args__ = (
        UniqueConstraint(
            "message_id",
            "citation_number",
            name="uq_citations_message_citation_number",
        ),
    )

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    account_email = Column(String, nullable=True)

    root_folder_id = Column(String, nullable=True)
    root_folder_name = Column(String, nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)




class SourceCredential(Base):
    __tablename__ = "source_credentials"

    id = Column(Integer, primary_key=True)

    source_id = Column(
        Integer,
        ForeignKey("sources.id"),
        nullable=False,
        unique=True
    )

    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    token_expiry = Column(DateTime, nullable=True)



class SyncJob(Base):
    __tablename__ = "sync_jobs"

    id = Column(Integer, primary_key=True, index=True)

    # Job ownership and source
    source_id = Column(
        Integer,
        ForeignKey("sources.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # Overall job status
    status = Column(
        String(30),
        nullable=False,
        default="queued",
        server_default="queued"
    )

    # Progress tracking
    total_files = Column(Integer, nullable=False, default=0)
    completed_files = Column(Integer, nullable=False, default=0)
    failed_files = Column(Integer, nullable=False, default=0)

    # Processing attempts and recovery
    attempts = Column(Integer, nullable=False, default=0)

    locked_by = Column(String(100), nullable=True)
    locked_until = Column(DateTime(timezone=True), nullable=True)

    # Redis dispatch tracking
    redis_message_id = Column(String(100), nullable=True)
    enqueued_at = Column(DateTime(timezone=True), nullable=True)
    dispatch_error = Column(Text, nullable=True)

    # General error tracking
    last_error = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    started_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationships
    changes = relationship(
        "SyncJobChange",
        back_populates="sync_job",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    source = relationship("Source")
    user = relationship("User")

    __table_args__ = (
        CheckConstraint(
            "status IN ('queued', 'processing', 'completed', "
            "'completed_with_errors', 'failed', 'cancelled')",
            name="check_sync_job_status"
        ),

        CheckConstraint(
            "total_files >= 0 AND completed_files >= 0 "
            "AND failed_files >= 0",
            name="check_sync_job_counts"
        ),

        Index(
            "ix_sync_jobs_source_status",
            "source_id",
            "status"
        ),
        Index(
            "uq_sync_jobs_one_active_per_source",
            "source_id",
            unique=True,
            postgresql_where=text(
                "status IN ('queued', 'processing')"
            )
        ),
    )


class SyncJobChange(Base):
    __tablename__ = "sync_job_changes"

    id = Column(Integer, primary_key=True, index=True)

    # Parent job
    sync_job_id = Column(
        Integer,
        ForeignKey("sync_jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Google Drive file information
    external_file_id = Column(
        String(255),
        nullable=False
    )

    file_name = Column(
        String(500),
        nullable=False
    )

    # Operation: added, updated or removed
    change_type = Column(
        String(30),
        nullable=False
    )

    # Individual file processing status
    status = Column(
        String(30),
        nullable=False,
        default="queued",
        server_default="queued"
    )

    # Retry and error information
    attempts = Column(Integer, nullable=False, default=0)

    error_message = Column(Text, nullable=True)

    # Processing timestamps
    started_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationship with parent job
    sync_job = relationship(
        "SyncJob",
        back_populates="changes"
    )

    __table_args__ = (
        CheckConstraint(
            "change_type IN ('added', 'updated', 'removed')",
            name="check_sync_change_type"
        ),

        CheckConstraint(
            "status IN ('queued', 'processing', 'completed', "
            "'failed', 'skipped')",
            name="check_sync_change_status"
        ),

        UniqueConstraint(
            "sync_job_id",
            "external_file_id",
            name="uq_sync_job_external_file"
        ),

        Index(
            "ix_sync_job_changes_status",
            "sync_job_id",
            "status"
        ),
    )