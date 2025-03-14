# Event Replay and reprocessing in an even driven system (AWS Kinesis) without relying on Traditional Database

## Overview
This project is about **replaying and recalculating missed or incorrectevents** in an **event-driven system** using AWS Kinesis. This approach does not rely on a traditional database for historical even storage but instead leverages **event streaming, logs and real-time validation**.

## How It Works
- Fetches **historical events** from an AWS **Kinesis stream** using a timestamp-based iterator.
- Processes events in real time , recalculating the necessary values.
- Ensures **data accuracy** by validating or verifying event integrity using **MD5 checksums**
- Handles **Large-scale event replays efficiently**

## Technologies Used
- Code : **Python**
- Event streaming and replay : **AWS Kinesis**
- Libraries : **Boto3**, **Haslib**
- **sha256 Hashing** (for event validation)

## Explanation 
- **Approach**
- Since we cannot rely on a traditional database to store historical event data , here i explored some alternate ways to recover and reprocess the missed or incorrect events. Here's how i would approach the problem
- **Strategy for Recovery & Reprocessing** :
  1. Event Replay from the source (if available) : if events are coming from a system or even streaming services like Kafka, Kinesis or an Event Bus continously , i would attempt to replay the past events from a checkpoint before the failure occured.
Example : As i work with AWS Cloud most of the time, For AWS Kinesis, i would use **GetSharditerator** to read past events within the retention period.
  2. Leveraging Event Logs & Dead Letter Queues (DLQ) : Basically, if messages failed due to processing errors, they might be stored in DLQ in SQS(Simple Queue Service). I would fetch those messages, reprocess them, and emit new correct events back to the event bus.
  3. Reconstructing Events from Downstream Systems : If i have derivative data or logs from previously processed events, i can use them to reverse-engineer the missing inputs.
Example : If system maintains a cache (Redis, DynamoDB Streams, or in-memory store), i can infer the missing values.
Note : I ensure that recalculate results are idempotent to avoid duplicate processing if events are re-emitted. ( By storing unique event ids in a temporary cache to avoid duplicate computation)

**SOLUTION**
Lets assume events are coming from AWS Kinesis, and i need to replay them from a previous timestamp.
Please find attached Python Code to this repository .
  

