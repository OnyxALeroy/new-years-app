#!/usr/bin/env python3
"""
AUTOMATED FIX: Add missing 'dates' field to all events
This script automatically fixes the KeyError: 'dates' issue in your backend
"""

import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone, timedelta

async def fix_events():
    """Automatically fix missing dates field in events"""
    print("🔧 AUTOMATED MongoDB Fix Script")
    print("Fixing KeyError: 'dates' in events collection...")
    print("=" * 50)
    
    client = None
    
    try:
        # Connect to MongoDB (using credentials from docker-compose.yml)
        client = AsyncIOMotorClient("mongodb://root:password@localhost:27017")
        db = client["newyears_db"]
        await db.list_collection_names()  # Test connection
        print("✅ Connected to MongoDB")
        
        events_collection = db["events"]
        
        # Find all events
        all_events = await events_collection.find({}).to_list(length=None)
        print(f"📊 Total events found: {len(all_events)}")
        
        # Find events without dates
        events_without_dates = [event for event in all_events if "dates" not in event]
        
        if not events_without_dates:
            print("✅ All events already have 'dates' field!")
        else:
            print(f"🔧 Found {len(events_without_dates)} events without 'dates' field")
            
            # Create a default date (tomorrow at noon UTC)
            tomorrow = datetime.now(timezone.utc).replace(hour=12, minute=0, second=0, microsecond=0)
            tomorrow = tomorrow + timedelta(days=1)
            default_date = tomorrow.isoformat()
            
            # Update all events without dates
            for event in events_without_dates:
                await events_collection.update_one(
                    {"_id": event["_id"]},
                    {"$set": {"dates": [default_date]}}
                )
                description = event.get('description', 'No description')[:50]
                print(f"  ✅ Fixed: {description}...")
            
            print(f"✅ Fixed {len(events_without_dates)} events with 'dates' field!")
        
        # Verify the fix
        events_with_dates = await events_collection.find({"dates": {"$exists": True}}).to_list(length=None)
        print(f"✅ Verification: {len(events_with_dates)} events now have 'dates' field")
        
        print("\n🎉 SUCCESS: Your backend should now work!")
        print("   The KeyError: 'dates' error should be resolved.")
        print("   Try refreshing your frontend now.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if client:
            client.close()
        print("\n✅ Script completed!")

if __name__ == "__main__":
    asyncio.run(fix_events())