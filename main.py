import atexit
from datetime import datetime, timezone
import json
from cancellation import cancellation
from loop import read
import boto3

STREAM_NAME = 'd-mon-stream-input'


def on_exit_requested():
    cancellation.request_cancellation()


if __name__ == '__main__':
    atexit.register(on_exit_requested)
    kinesis_client=boto3.client("kinesis")
    for db in read():
        records = [{"Data": json.dumps({ 'db': db, 'at': datetime.now(timezone.utc).isoformat() }), "PartitionKey": "primary"}]
        kinesis_client.put_records(StreamName=STREAM_NAME, Records=records)


