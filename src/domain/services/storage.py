from io import BytesIO

from minio import Minio
from minio.error import S3Error

from config import settings
from domain.enums import StorageSource


class StorageService:
    def __init__(self):
        self.client = Minio(
            endpoint=settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key.get_secret_value(),
            secure=settings.minio_secure,
        )
        self.bucket_name = settings.minio_bucket_name
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    def _build_object_name(self, user_id: int, source: str, filename: str) -> str:
        return f"users/{user_id}/{source}/{filename}"

    async def put_file(
        self, user_id: int, source: str, filename: str, file_data: bytes
    ) -> str:
        object_name = self._build_object_name(user_id, source, filename)
        self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=object_name,
            data=BytesIO(file_data),
            length=len(file_data),
        )
        return object_name

    async def get_file(self, user_id: int, source: str, filename: str) -> bytes:
        object_name = self._build_object_name(user_id, source, filename)
        try:
            response = self.client.get_object(self.bucket_name, object_name)
            return response.read()
        except S3Error as e:
            if e.code == "NoSuchKey":
                from domain.exceptions import NotFoundError

                raise NotFoundError(entity_name="File", entity_id=object_name)
            raise

    async def rename_file(
        self, user_id: int, source: str, old_filename: str, new_filename: str
    ) -> str:
        old_object_name = self._build_object_name(user_id, source, old_filename)
        new_object_name = self._build_object_name(user_id, source, new_filename)

        try:
            self.client.copy_object(
                bucket_name=self.bucket_name,
                object_name=new_object_name,
                source={"Bucket": self.bucket_name, "Key": old_object_name},
            )
            self.client.remove_object(self.bucket_name, old_object_name)
            return new_object_name
        except S3Error as e:
            if e.code == "NoSuchKey":
                from domain.exceptions import NotFoundError

                raise NotFoundError(entity_name="File", entity_id=old_object_name)
            raise

    def list_files(self, user_id: int, source: str | None = None) -> list[str]:
        prefix = f"users/{user_id}/"
        if source:
            prefix += f"{source}/"

        objects = self.client.list_objects(
            bucket_name=self.bucket_name, prefix=prefix, recursive=True
        )
        return [obj.object_name for obj in objects]


storage_service = StorageService()
