from app.models import Citation
from sqlalchemy.orm import selectinload
from app.services.database import SessionLocal
from app.models import User
from app.models import Chat
from app.models import Message
from app.models import (Chunk, Source, SourceCredential,CompanyDocument,SyncJob,
SyncJobChange)
from datetime import datetime, timezone, timedelta
from app.constants import ACTIVE_SYNC_STATUSES,TERMINAL_SYNC_STATUSES


def get_user_by_email(email: str):
    with SessionLocal() as db:
        return db.query(User).filter(
            User.email == email
        ).first()


def get_user_by_id(user_id: int):
    with SessionLocal() as db:
        return db.query(User).filter(
            User.id == user_id
        ).first()


def create_user(name: str, email: str, password_hash: str):
    with SessionLocal() as db:

        user = User(
            name=name,
            email=email,
            password_hash=password_hash
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

def load_chats(user_id:int):
    with SessionLocal() as db:
        return db.query(Chat).filter(
            Chat.user_id == user_id
        ).all()



def create_new_chat(user_id: int, title: str):

    title = title.strip()[:60]

    with SessionLocal() as db:

        chat = Chat(
            title=title,
            user_id=user_id
        )

        db.add(chat)
        db.commit()
        db.refresh(chat)

        return chat

def search_chat_id_with_user_id(user_id:int, chat_id:int):
    with SessionLocal() as db:
        return db.query(Chat).filter(
            Chat.id == chat_id,
            Chat.user_id == user_id
        ).first()


def load_messages(chat_id: int):

    with SessionLocal() as db:

        messages = (
            db.query(Message)
            .options(
                selectinload(Message.citations)
            )
            .filter(Message.chat_id == chat_id)
            .order_by(Message.created_at.asc())
            .all()
        )

        return [
            {
                "role": message.role,
                "content": message.content,
                "citations": [
                    {
                        "citationNumber": citation.citation_number,
                        "chunkId": citation.chunk_id
                    }
                    for citation in message.citations
                ]
            }
            for message in messages
        ]


def save_message(chat_id: int,role:str,content:str):

    with SessionLocal() as db:

        message = Message(
            chat_id=chat_id,
            role=role,
            content=content
        )

        db.add(message)
        db.commit()
        db.refresh(message)

        return message



def save_citations(chunk_results, message_id: int):
    try:
        if chunk_results:

            citations = [
                Citation(
                    message_id=message_id,
                    citation_number=int(chunk["citationNumber"]),
                    chunk_id=chunk["id"]
                )
                for chunk in chunk_results
            ]

            with SessionLocal() as db:
                db.add_all(citations)
                db.commit()

    except Exception as error:
        print(error)

from sqlalchemy import select
from sqlalchemy.orm import joinedload

def load_chunk(chunk_id: int):

    with SessionLocal() as db:

        chunk = (
            db.query(Chunk)
            .options(
                joinedload(Chunk.document)
            )
            .filter(
                Chunk.id == chunk_id
            )
            .first()
        )

        if chunk is None:
            return None

        return {
            "id": chunk.id,
            "documentId": chunk.document_id,
            "chunkIndex": chunk.chunk_index,
            "text": chunk.text,
            "pages": chunk.pages,
            "type": chunk.type,
            "sectionHeading": chunk.section_heading,
            "originalFileName": chunk.document.original_file_name,
        }

#source service
def get_source_by_type(source_type: str):
    with SessionLocal() as db:
        return db.query(Source).filter(
            Source.type == source_type
        ).first()


def update_source(source_id: int, status: str, account_email: str):
    with SessionLocal() as db:
        source = db.query(Source).filter(
            Source.id == source_id
        ).first()

        if not source:
            return None

        source.status = status
        source.account_email = account_email

        db.commit()
        db.refresh(source)

        return source


def create_source(source_type:str,name:str,status:str,account_email:str):
     with SessionLocal() as db:

        source = Source(
            type=source_type,
            name=name,
            account_email=account_email,
            status=status
        )

        db.add(source)
        db.commit()
        db.refresh(source)

        return source


def get_source_credentials_by_source_id(source_id: int):
    with SessionLocal() as db:
        return db.query(SourceCredential).filter(
            SourceCredential.source_id == source_id
        ).first()


def update_source_credentials(source_id: int, access_token: str, refresh_token: str,token_expiry:datetime):
    with SessionLocal() as db:
        source_credentials = db.query(SourceCredential).filter(
            SourceCredential.source_id == source_id
        ).first()

        if not source_credentials:
            return None

        source_credentials.access_token = access_token
        source_credentials.refresh_token = refresh_token
        source_credentials.token_expiry = token_expiry

        db.commit()
        db.refresh(source_credentials)

        return source_credentials


def create_source_credentials(source_id: int, access_token: str, refresh_token: str,token_expiry:datetime):
     with SessionLocal() as db:

        source_credentials = SourceCredential(
            source_id=source_id,
            access_token=access_token,
            refresh_token=refresh_token,
            token_expiry=token_expiry
        )

        db.add(source_credentials)
        db.commit()
        db.refresh(source_credentials)

        return source_credentials


def get_sources():
    with SessionLocal() as db:
        return db.query(Source).all()


def delete_source_credentials(source_id: int):
    with SessionLocal() as db:
        source_credentials = db.query(SourceCredential).filter(
            SourceCredential.source_id == source_id
        ).first()

        if not source_credentials:
            return

        db.delete(source_credentials)
        db.commit()


def delete_source(source_id: int):
    with SessionLocal() as db:
        source = db.query(Source).filter(
            Source.id == source_id
        ).first()

        if not source:
            return None

        db.delete(source)
        db.commit()

        return source

def update_source_root_folder(source_id: int, folder_id: str|None, folder_name: str|None):
    with SessionLocal() as db:
        source = db.query(Source).filter(
            Source.id == source_id
        ).first()

        if not source:
            return None

        source.root_folder_id = folder_id
        source.root_folder_name = folder_name

        db.commit()
        db.refresh(source)

        return source

def update_access_token(
    source_id: int,
    access_token: str,
    token_expiry: datetime
):
    with SessionLocal() as db:
        source_credentials = db.query(SourceCredential).filter(
            SourceCredential.source_id == source_id
        ).first()

        if not source_credentials:
            return None

        source_credentials.access_token = access_token
        source_credentials.token_expiry = token_expiry

        db.commit()
        db.refresh(source_credentials)

        return source_credentials

#company document

def get_company_documents_by_source(source_id: int):
    with SessionLocal() as db:
        return (
            db.query(CompanyDocument)
            .filter(CompanyDocument.source_id == source_id)
            .all()
        )

def get_company_document_by_external_file_id(external_file_id: str):
    with SessionLocal() as db:
        return (
            db.query(CompanyDocument)
            .filter(
                CompanyDocument.external_file_id == external_file_id
            )
            .first()
        )


#sync_job

def create_sync_job_with_changes(
    source_id,
    user_id,
    changes
):
    db = SessionLocal()

    try:
        # Create parent job
        sync_job = SyncJob(
            source_id=source_id,
            user_id=user_id,
            status="queued",
            total_files=len(changes),
            completed_files=0,
            failed_files=0
        )

        db.add(sync_job)

        # Generate parent ID without committing
        db.flush()

        # Create child records
        for change in changes:

            job_change = SyncJobChange(
                sync_job_id=sync_job.id,
                external_file_id=change["file"]["id"],
                file_name=change["file"]["name"],
                change_type=change["type"],
                status="queued"
            )

            db.add(job_change)

        # Commit parent and children together
        db.commit()

        return sync_job.id

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def update_sync_job_dispatch_error(sync_job_id, error):

    db = SessionLocal()

    try:
        job = (
            db.query(SyncJob)
            .filter(SyncJob.id == sync_job_id)
            .first()
        )

        if not job:
            raise ValueError(
                f"SyncJob {sync_job_id} not found"
            )

        job.dispatch_error = error

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def mark_sync_job_enqueued(sync_job_id, redis_message_id):

    db = SessionLocal()

    try:
        job = (
            db.query(SyncJob)
            .filter(SyncJob.id == sync_job_id)
            .first()
        )

        if not job:
            raise ValueError(
                f"SyncJob {sync_job_id} not found"
            )

        job.redis_message_id = redis_message_id
        job.enqueued_at = datetime.now(timezone.utc)
        job.dispatch_error = None

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def claim_sync_job(
    sync_job_id,
    worker_id,
    lease_minutes=45
):

    db = SessionLocal()

    terminal_statuses = {
        "completed",
        "completed_with_errors",
        "failed",
        "cancelled"
    }

    try:
        with db.begin():

            job = (
                db.query(SyncJob)
                .filter(SyncJob.id == sync_job_id)
                .with_for_update()
                .first()
            )

            if not job:
                return "not_found"

            if job.status in terminal_statuses:
                return "terminal"

            now = datetime.now(timezone.utc)

            # Another worker still has a valid lease
            if (
                job.status == "processing"
                and job.locked_until is not None
                and job.locked_until > now
            ):
                return "active"

            if job.status not in ("queued", "processing"):
                return "not_claimable"

            # Claim the job
            job.status = "processing"
            job.locked_by = worker_id
            job.locked_until = now + timedelta(
                minutes=lease_minutes
            )

            job.attempts += 1

            if job.started_at is None:
                job.started_at = now

            return "claimed"

    except Exception:
        raise

    finally:
        db.close()


def mark_sync_job_successful_for_testing(sync_job_id):

    db = SessionLocal()

    try:
        with db.begin():

            # 1. Fetch and lock the parent job
            job = (
                db.query(SyncJob)
                .filter(SyncJob.id == sync_job_id)
                .with_for_update()
                .first()
            )

            if not job:
                raise ValueError(
                    f"Sync job {sync_job_id} not found"
                )

            # 2. Fetch and lock all child records
            changes = (
                db.query(SyncJobChange)
                .filter(
                    SyncJobChange.sync_job_id == sync_job_id
                )
                .with_for_update()
                .all()
            )

            # Verify that all expected child records exist
            if len(changes) != job.total_files:
                raise ValueError(
                    f"Expected {job.total_files} changes, "
                    f"but found {len(changes)}"
                )

            now = datetime.now(timezone.utc)

            # 3. Mark every document change as completed
            for change in changes:

                change.status = "completed"
                change.error_message = None

                if change.started_at is None:
                    change.started_at = now

                change.completed_at = now

            # 4. Update parent job progress
            job.completed_files = len(changes)
            job.failed_files = 0

            # 5. Mark parent job as completed
            job.status = "completed"
            job.completed_at = now

            if job.started_at is None:
                job.started_at = now

            job.last_error = None

            # 6. Release processing lock
            job.locked_by = None
            job.locked_until = None

        # Transaction automatically commits here

        return True

    except Exception:
        raise

    finally:
        db.close()


def get_sync_job_status(sync_job_id):

    db = SessionLocal()

    try:
        job = (
            db.query(SyncJob)
            .filter(SyncJob.id == sync_job_id)
            .first()
        )

        return job.status if job else None

    finally:
        db.close()


def get_active_sync_job(source_id):

    db = SessionLocal()

    try:
        return (
            db.query(SyncJob)
            .filter(
                SyncJob.source_id == source_id,
                SyncJob.status.in_(ACTIVE_SYNC_STATUSES)
            )
            .order_by(SyncJob.created_at.desc())
            .first()
        )

    finally:
        db.close()


def get_active_sync_job_details(source_id):

    db = SessionLocal()

    try:
        job = (
            db.query(SyncJob)
            .filter(
                SyncJob.source_id == source_id,
                SyncJob.status.in_(ACTIVE_SYNC_STATUSES)
            )
            .order_by(SyncJob.created_at.desc())
            .first()
        )

        if not job:
            return None

        changes = (
            db.query(SyncJobChange)
            .filter(
                SyncJobChange.sync_job_id == job.id
            )
            .order_by(SyncJobChange.id)
            .all()
        )

        return {
            "sync_job_id": job.id,
            "status": job.status,
            "total_files": job.total_files,
            "completed_files": job.completed_files,
            "failed_files": job.failed_files,
            "created_at": job.created_at.isoformat(),
            "changes": [
                {
                    "id": change.id,
                    "external_file_id": change.external_file_id,
                    "file_name": change.file_name,
                    "change_type": change.change_type,
                    "status": change.status,
                    "error_message": change.error_message
                }
                for change in changes
            ]
        }

    finally:
        db.close()

def get_sync_job_details(sync_job_id, source_id):

    db = SessionLocal()

    try:
        job = (
            db.query(SyncJob)
            .filter(
                SyncJob.id == sync_job_id,
                SyncJob.source_id == source_id
            )
            .first()
        )

        if not job:
            return None

        changes = (
            db.query(SyncJobChange)
            .filter(
                SyncJobChange.sync_job_id == job.id
            )
            .order_by(SyncJobChange.id)
            .all()
        )

        return {
            "sync_job_id": job.id,
            "source_id": job.source_id,
            "status": job.status,
            "total_files": job.total_files,
            "completed_files": job.completed_files,
            "failed_files": job.failed_files,
            "created_at": (
                job.created_at.isoformat()
                if job.created_at else None
            ),
            "started_at": (
                job.started_at.isoformat()
                if job.started_at else None
            ),
            "completed_at": (
                job.completed_at.isoformat()
                if job.completed_at else None
            ),
            "last_error": job.last_error,

            "changes": [
                {
                    "id": change.id,
                    "external_file_id": change.external_file_id,
                    "file_name": change.file_name,
                    "change_type": change.change_type,
                    "status": change.status,
                    "attempts": change.attempts,
                    "error_message": change.error_message,
                    "started_at": (
                        change.started_at.isoformat()
                        if change.started_at else None
                    ),
                    "completed_at": (
                        change.completed_at.isoformat()
                        if change.completed_at else None
                    )
                }
                for change in changes
            ]
        }

    finally:
        db.close()

    
def get_sync_job_for_processing(sync_job_id):

    db = SessionLocal()

    try:
        job = (
            db.query(SyncJob)
            .filter(SyncJob.id == sync_job_id)
            .first()
        )

        if not job:
            return None

        changes = (
            db.query(SyncJobChange)
            .filter(
                SyncJobChange.sync_job_id == job.id
            )
            .order_by(SyncJobChange.id)
            .all()
        )

        return {
            "sync_job_id": job.id,
            "source_id": job.source_id,
            "status": job.status,
            "total_files": job.total_files,

            "changes": [
                {
                    "id": change.id,
                    "external_file_id": change.external_file_id,
                    "file_name": change.file_name,
                    "change_type": change.change_type,
                    "status": change.status,
                    "attempts": change.attempts
                }
                for change in changes
            ]
        }

    finally:
        db.close()