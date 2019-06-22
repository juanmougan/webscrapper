import firebase_admin
import jsons
from firebase_admin import credentials
from firebase_admin import firestore

class FirestoreClient:
	def __init__(self, creds, collection):
		cred = credentials.Certificate(creds)
		firebase_admin.initialize_app(cred)
		self.collection = collection
		self.db = firestore.client()

	def store_in_collection(self, article):
		self.db.collection(self.collection).add(jsons.dump(article))

	def fetch_all_from_collection(self):
		documents = []
		doc_ref = self.db.collection(self.collection)
		docs = doc_ref.get()
		for doc in docs:
		    documents.append(doc.to_dict())
		return documents
