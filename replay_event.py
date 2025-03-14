#This is a sample code with sample values
#lets import necessary libraries 
import boto3 #this is a offcial AWS SDK for python used to interact with AWS services (Kinesis)
import json
import hashlib #this is for hashing , used to verify the integrity of events

# lets setup AWS Kinesis
kinesis_client = boto3.client('kinesis', region_name='us-east-1')
stream_name = "stream_name"

# create a function to replay events from a past checkpoint

def replay_events(shard_id, start_timestamp): #start_timestamp is timestamp from which we want to replay events
    # firstly lets get shard iterator from the given timestamp
    response = kinesis_client.get_shard_iterator(
        StreamName=stream_name,
        ShardId=shard_id,
        ShardIteratorType="AT_TIMESTAMP",
        Timestamp=start_timestamp
    )
    shard_iterator = response["ShardIterator"] #this stores the iterator, which is used to read the first batch of events from kinesis
    #fetching events in a loop & processing each event 
    while shard_iterator: #this enusures we continue fetching events until there are none left
        response = kinesis_client.get_records(ShardIterator=shard_iterator, Limit=100) #retrieves up to 100 records from the kinesis stream using shard_iterator
        for record in response["Records"]: #it contains the actual event data from kinesis
            event_data = json.loads(record["Data"]) #converts the event data (which is in JSON format) into a Python dictionary 
            process_event(event_data)  # calls the function to process the event and perform necessary calculations
        
        shard_iterator = response.get("NextShardIterator")  # updating iterator to get the next batch, i.e, fetches the next batch of records for processing

# Function to process and recalculate event
def process_event(event):
    event_id = event.get("event_id")
    user_id = event.get("user_id")
    amount = event.get("amount")
    
    # Verify integrity using checksum 
    #lets generate a hash(checksum) for validation 
    #used sha256 hashing to verify if the received event matches the expected format
    expected_hash = hashlib.sha256(f"{user_id}-{amount}".encode()).hexdigest()
    if event.get("checksum") == expected_hash:
        print(f"Processing event {event_id} successfully.")
    else:
        print(f"Data corruption detected for event {event_id}, skipping.")
#if checksum doesn't match , the event might be corrupted or tampered with, so it is skipped

# lets have a Example 
shard_id = "shardId-000000000000"
replay_events(shard_id, "2025-03-10T12:00:00Z") 
# calls replay_events() to reprocess events from a specific point in time,helping to recover lost or incorrect data. so this replay events from March 10th
