#!/usr/bin/env python3
"""
Simple MongoDB Fix Script for New Years App
Fixes missing 'dates' field in existing events documents
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone, timedelta

async def fix_missing_dates():
    """Add missing 'dates' field to all events that don't have it"""
    print("🔧 MongoDB Fix Script for Missing Dates Field")
    print("=" * 50)
    
    client = None
    events_collection = None
    
    # Connect to MongoDB (using Docker container credentials)
    try:
        # Try without auth first, then with auth if needed
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        db = client["newyears_db"]
        
        # Test connection
        await db.list_collection_names()
        print("✅ Connected to MongoDB")
    except Exception as e:
        print(f"❌ Failed to connect without auth, trying with auth: {e}")
        try:
            # Try with admin credentials (from docker-compose)
            client = AsyncIOMotorClient("mongodb://admin:password@localhost:27017")
            db = client["newyears_db"]
            await db.list_collection_names()
            print("✅ Connected to MongoDB with admin credentials")
        except Exception as e2:
            print(f"❌ Failed to connect with auth too: {e2}")
            return
    
    try:
        # Find all events that don't have a 'dates' field
        events_without_dates = await events_collection.find({"dates": {"$exists": False}}).to_list(length=None)
        
        if not events_without_dates:
            print("✅ All events already have 'dates' field!")
        else:
            print(f"📊 Found {len(events_without_dates)} events without dates field")
            
            # Create a default date (tomorrow at noon) for events without dates
            tomorrow = datetime.now(timezone.utc).replace(hour=12, minute=0, second=0, microsecond=0)
            tomorrow += datetime.timedelta(days=1)
            default_date = tomorrow.isoformat()
            
            for event in events_without_dates:
                # Update the event with a dates field containing one default date
                await events_collection.update_one(
                    {"_id": event["_id"]},
                    {"$set": {"dates": [default_date]}}
                )
                description = event.get('description', 'No description')
                print(f"  ✅ Updated: {description[:50]}...")
            
            print(f"✅ Successfully updated {len(events_without_dates)} events")
        
        # Show summary of all events
        all_events = await events_collection.find({}).to_list(length=None)
        print(f"\n📈 Database Summary:")
        print(f"  Total events: {len(all_events)}")
        
        events_with_dates = await events_collection.find({"dates": {"$exists": True}}).to_list(length=None)
        print(f"  Events with dates: {len(events_with_dates)}")
        
        # Show sample of events with dates
        print(f"\n📋 Sample events with dates:")
        for i, event in enumerate(events_with_dates[:3], 1):
            description = event.get('description', 'No description')
            dates = event.get('dates', [])
            print(f"  {i}. {description[:60]}...")
            print(f"     Dates: {len(dates)} date(s)")
            if dates:
                for j, date in enumerate(dates[:2], 1):
                    print(f"       {j}. {date}")
                if len(dates) > 2:
                    print(f"       ...and {len(dates) - 2} more dates")
        
    except Exception as e:
        print(f"❌ Error during update: {e}")
    finally:
        # Close connection
        client.close()
        print("\n✅ Fix script completed!")

async def show_database_info():
    """Show current database structure"""
    print("\n🗄️  Current Database Information:")
    print("=" * 50)
    
    try:
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        db = client["newyears_db"]
        
        # List all collections
        collections = await db.list_collection_names()
        print(f"📋 Collections: {collections}")
        
        # Show stats for each collection
        for collection_name in collections:
            collection = db[collection_name]
            count = await collection.count_documents({})
            print(f"\n📊 {collection_name}:")
            print(f"  Document count: {count}")
            
            if count > 0:
                # Get sample document to show structure
                sample = await collection.find_one({})
                print(f"  Sample fields: {list(sample.keys())}")
                
                # Check for 'dates' field in events collection
                if collection_name == 'events':
                    has_dates = 'dates' in sample
                    print(f"  Has dates field: {'✅' if has_dates else '❌'}")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    """Main function"""
    # Show current state
    await show_database_info()
    
    # Fix missing dates
    await fix_missing_dates()

if __name__ == "__main__":
    asyncio.run(main())