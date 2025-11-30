from google.cloud.firestore_v1 import Client

from app.core.entities.user import User


class AuthRepository:
    COLLECTION_NAME = "users"

    def __init__(self, firestore_client: Client) -> None:
        self.firestore_client = firestore_client

    def find_user_by_email(self, email: str) -> User | None:
        query = (
            self.firestore_client.collection(self.COLLECTION_NAME)
            .where(field_path="email", op_string="==", value=email)
            .limit(1)
        )

        documents = query.stream()

        for document in documents:
            return document
        return None

    def create_user(self, user: User) -> User:
        collection = self.firestore_client.collection(self.COLLECTION_NAME)
        document_reference = collection.document()

        document_reference.set(user.to_firestore())

        return user.model_copy(update={"user_id": document_reference.id})
