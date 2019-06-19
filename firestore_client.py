import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class FirestoreClient:
	CREDS = './config/fcm_service_account.json'
	COLLECTION = u'articles'

	def __init__(self):
		cred = credentials.Certificate(CREDS)
		firebase_admin.initialize_app(cred)
		self.db = firestore.client()

	def store_in_collection(document, article):
		doc_ref = db.collection(COLLECTION).document(article.link)		# TODO maybe add a UUID
		doc_ref.set({
		    u'link': article.link,
		    u'address': article.address,
		    u'rent_price': article.prices.rent,
		    u'expenses_price': article.expenses.rent
		})

	def fetch_all_from_collections():
		doc_ref = db.collection(COLLECTION)
		docs = doc_ref.get()

		# TODO add to a collection, instead of printing
		for doc in docs:
		    print(u'{} => {}'.format(doc.id, doc.to_dict()))
