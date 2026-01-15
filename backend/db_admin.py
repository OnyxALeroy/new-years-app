import json
import sys
from pprint import pprint
import pymongo
from bson import ObjectId

# --- CONFIGURATION ---
# Credentials from your docker-compose.yml
MONGO_URI = "mongodb://root:password@localhost:27017/?authSource=admin"
DB_NAME = "newyears_db"


class DBAdmin:
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
            self.client.server_info()  # Trigger connection check
            self.db = self.client[DB_NAME]
            self.current_collection = None
            print(f"✅ Connected to MongoDB: {DB_NAME}")
        except Exception as e:
            print(f"❌ Connection Failed: {e}")
            print("Make sure your Docker container is running.")
            sys.exit(1)

    def select_collection(self):
        """Lists collections and asks user to pick one."""
        collections = self.db.list_collection_names()
        if not collections:
            print("No collections found in database.")
            return False

        print("\n📂 Available Collections:")
        for idx, name in enumerate(collections):
            print(f"  {idx + 1}. {name}")

        choice = input("\nSelect collection # (or 'q' to quit): ")
        if choice.lower() == "q":
            sys.exit(0)

        try:
            selection = int(choice) - 1
            if 0 <= selection < len(collections):
                self.current_collection = self.db[collections[selection]]
                print(f"👉 Selected: {collections[selection]}")
                return True
            else:
                print("❌ Invalid number.")
        except ValueError:
            print("❌ Please enter a number.")
        return False

    def list_documents(self):
        """Lists ID and a summary of documents."""
        if self.current_collection is None:
            print("❌ No collection selected.")
            return
            
        print(f"\n📃 Documents in '{self.current_collection.name}':")
        docs = list(self.current_collection.find().limit(20))

        if not docs:
            print("   (Empty Collection)")
            return

        for doc in docs:
            # Try to find a human-readable field to show alongside ID
            summary = (
                doc.get("description")
                or doc.get("name")
                or doc.get("email")
                or "No description"
            )
            print(f"   🆔 {doc['_id']} | 📝 {str(summary)[:50]}...")

    def get_document_by_id(self):
        """Helper to ask user for ID and fetch doc."""
        if self.current_collection is None:
            print("❌ No collection selected.")
            return None
            
        doc_id = input("\nEnter Document ID to select: ").strip()
        try:
            oid = ObjectId(doc_id)
            doc = self.current_collection.find_one({"_id": oid})
            if doc:
                return doc
            print("❌ Document not found.")
        except Exception:
            print("❌ Invalid Object ID format.")
        return None

    def view_document(self):
        doc = self.get_document_by_id()
        if doc:
            print("\n🔍 Document Content:")
            pprint(doc)

    def delete_document(self):
        doc = self.get_document_by_id()
        if doc:
            print(f"\n⚠️  WARNING: You are about to delete document {doc['_id']}")
            confirm = input("Type 'DELETE' to confirm: ")
            if confirm == "DELETE":
                self.current_collection.delete_one({"_id": doc["_id"]})
                print("✅ Deleted.")
            else:
                print("🚫 Cancelled.")

    def edit_document(self):
        """Edits or Adds a field to a document."""
        doc = self.get_document_by_id()
        if not doc:
            return

        print("\n📋 Current Fields:")
        print(list(doc.keys()))

        key = input(
            "\nEnter field name to edit/add (e.g., 'dates', 'participants'): "
        ).strip()
        raw_value = input(
            f"Enter new value for '{key}' (JSON format supported, e.g., [] or 123): "
        ).strip()

        # Try to parse input as JSON (for lists, dicts, bools, numbers)
        try:
            value = json.loads(raw_value)
            print(f"   📊 Interpreted as type: {type(value).__name__}")
        except json.JSONDecodeError:
            # If valid JSON fails, treat as a plain string
            value = raw_value
            print(f"   📝 Interpreted as String")

        if self.current_collection is not None:
            self.current_collection.update_one({"_id": doc["_id"]}, {"$set": {key: value}})
            print(f"✅ Updated field '{key}' successfully!")
        else:
            print("❌ No collection selected.")

    def menu(self):
        while True:
            if self.current_collection is None:
                if not self.select_collection():
                    continue

            collection_name = self.current_collection.name if self.current_collection is not None else "None"
            print(f"\n--- 🛠️  Managing: {collection_name} ---")
            print("1. [List]   Show all documents")
            print("2. [View]   Inspect a specific document")
            print("3. [Edit]   Edit or Add a field (Fix your data)")
            print("4. [Delete] Remove a document")
            print("5. [Back]   Choose different collection")
            print("6. [Exit]   Quit")

            choice = input("Choice: ")

            if choice == "1":
                self.list_documents()
            elif choice == "2":
                self.view_document()
            elif choice == "3":
                self.edit_document()
            elif choice == "4":
                self.delete_document()
            elif choice == "5":
                self.current_collection = None
            elif choice == "6":
                sys.exit(0)
            else:
                print("Invalid choice.")


if __name__ == "__main__":
    try:
        app = DBAdmin()
        app.menu()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")