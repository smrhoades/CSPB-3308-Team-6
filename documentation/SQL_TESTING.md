# SQL Design

![Database_Model](Database_Model.png)

# 1) Message Data

### Table Name
message_data

### Table Description
This table contains data of messages being sent between individual users. It contains the Ids of the two users, the text of the message, and a timestamp of when the message was sent.

### Table Parameters
id: (table index) auto-incrimenting id of the message
user_from: (foreign key) the id of the user who sent the message
user_to: (foreign key) the id of the user who recieved the message
text: variable length content of the message
created_at: timestamp of when the message was sent

### List of tests for verifying each table
- table can be created
- entry can be added to the table
- entry cannot be added unless all fields have values (non-null)
- entry cannot be added unless both users exist in the user_data table

### Data Access Methods

#### Name
getMessageHistory

#### Description
Get ordered list of messages previously sent between two users

#### Parameters
user1: id of one user
user2: id of a different user

#### return values
textArray: list of messages in order from oldest to newest
timestampArray: list of timestamps cooresponding to the messages

#### List of tests for verifying each access method
- arrays are returned with entries if two users have messages sent between them
- messages are returned for both sides of the conversation (user1->user2 AND user2->user1)
- timestampArray entries are ordered from oldest to newest regardless of message direction
- textArray entries are correctly ordered and coorespond to timestampArray entries
- empty arrays are returned if two users have no messages sent between them
- empty arrays are returned if either of the users does not exist in the user_data table

# 2) User Data

### Table Name
user_data

### Table Description

### Table Parameters

### List of tests for verifying each table

### Data Access Methods

#### Name

#### Description

#### Parameters

#### return values

#### List of tests for verifying each access method


# 3) Contact Data

### Table Name
contact_data

### Table Description

### Table Parameters

### List of tests for verifying each table

### Data Access Methods

#### Name

#### Description

#### Parameters

#### return values

#### List of tests for verifying each access method