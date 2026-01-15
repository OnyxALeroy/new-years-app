#!/usr/bin/env python3
"""
Simple MongoDB Fix Script for New Years App
Fixes missing 'dates' field in existing events documents
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone, timedelta

async def main():
    """Main function"""
    print("🔧 MongoDB Fix Script for Missing Dates Field")
    print("=" * 50)
    
    client = None
    
    try:
        # Try connecting without auth first
        print("🔗 Attempting connection...")
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        db = client["newyears_db"]
        
        # Test connection
        await db.list_collection_names()
        print("✅ Connected to MongoDB")
        
        # Get events collection
        events_collection = db["events"]
        
        # Find all events that don't have a 'dates' field
        events_without_dates = await events_collection.find({"dates": {"$exists": False}}).to_list(length=None)
        
        if not events_without_dates:
            print("✅ All events already have 'dates' field!")
        else:
            print(f"📊 Found {len(events_without_dates)} events without dates field")
            
            # Create a default date (tomorrow at noon) for events without dates
            tomorrow = datetime.now(timezone.utc).replace(hour=12, minute=0, second=0, microsecond=0)
            tomorrow = tomorrow + timedelta(days=1)
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
        
        # Count events with dates
        events_with_dates = await events_collection.find({"dates": {"$exists": True}}).to_list(length=None)
        print(f"  Events with dates: {len(events_with_dates)}")
        
        # Show sample of events
        print(f"\n📋 Sample events:")
        for i, event in enumerate(all_events[:3], 1):
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
        print(f"❌ Error during fix: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close connection
        if client:
            client.close()
        print("\n✅ Fix script completed!")

if __name__ == "__main__":
    asyncio.run(main())