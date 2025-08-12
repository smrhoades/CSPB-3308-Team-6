## User Search Test Cases (```/users/search``` GET endpoint)

*Valid Search Cases:*
- Test that searching with a valid term (non-empty string) returns success status and matching usernames √
- Test that search returns case-insensitive matches (searching "john" finds "John", "JOHN", etc.) √
- Test that search uses LIKE functionality (searching "joh" finds "john_doe") √
- Test that search results include total_found count 
- Test that search respects LIMIT clause and doesn't return more than maximum allowed results 

*Invalid Search Cases:*
- Test that empty search term returns error message 
- Test that search term above maximum length returns error message
- Test that search with no matching results returns "no results found" error √

*Edge Cases:*
- Test that search handles special characters safely (doesn't break query) 
- Test that search doesn't return the searching user in results 


## Add Contact Test Cases (```/contacts``` POST endpoint)

*Valid Add Contact Cases:*
- Test that adding a valid, existing username returns success message √
- Test that contact is actually added to user's contact list in database √
- Test that adding contact updates the database correctly √

*Invalid Add Contact Cases:*
- Test that adding non-existent username returns "User not found" error √
- Test that adding yourself as contact returns "Cannot add yourself as contact" error √
- Test that adding existing contact returns "Contact already exists" error √

*Request Validation:*
- Test that missing username in request body returns appropriate error
- Test that empty username in request body returns appropriate error
- Test that malformed JSON request returns appropriate error

*Authentication/Authorization:*
- Test that unauthenticated requests are rejected √

*Security:*
- Test that SQL injection attempts in search terms are prevented

*Integration Tests:*
- Test complete flow: search for user, then add them as contact
- Test that newly added contact appears in GET /contacts response