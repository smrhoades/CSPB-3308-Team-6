# ADD CONTACT FEATURE SPECIFICATION (backend)

## Searching for a User

1. User wants to add new contact, so User clicks on "add contact" on nav bar.
1. Client displays '/addcontact' component, which includes an input field.
1. User types search term into input field and clicks 'send'.
1. Client sends URL with the search term to server (endpoint = '/users/search')
1. Server parses URL, validates search term (no empty strings; length limits).
1. Server validates search term and queries database using parameterized queries for usernames that are "like" the search term (just use the SQL "like" function for now; make search case insensitive; use LIMIT clause for performance).
1. If search returns results, Server sends information from search as JSON: 
	- {'status': 'success', 'usernames': [u1, u2, ...], 'total_found': 3}.
1. Otherwise, return error message: 
	- {'status': 'error', 'message': 'no results found'}

## Adding the contact to User's Contacts

1. Given a successful search, User wants to add a User to their contacts, so User clicks on the contact name which is displayed in the results list.
1. Client sends POST request to Server with the contact's username as data (endpoint = '/contacts'; request body: {"user_name": "john_doe"}
1. Server validates request (make sure contact exists, isn't the User themselves, isn't already in the User's contacts).
1. Server updates database, adding contact to User's Contacts.
1. Server sends success message and updated contacts list if successful, otherwise an error message.
	- {"status": "success", "message": "Contact added successfully", "contacts": [...]}
	- {"status": "error", "message": "Contact already exists"}
	- {"status": "error", "message": "User not found"}
	- {"status": "error", "message": "Cannot add yourself as contact"}
