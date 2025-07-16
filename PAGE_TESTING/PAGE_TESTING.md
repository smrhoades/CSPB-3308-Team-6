# Page Testing


# 1) Login/Registration Page

### Description:
![Login Page](login-page.png)
![Registration Page](registration-page.png)

### Parameters/Data:
- JSON from Flask notifying the browser if the provided username is available for registration
- JSON from Flask notifying the browser if the provided credentials are valid

### Link Destinations:
- Login Page after successful registration
- Contacts Page upon succesful login

### Tests:
- Confirm that incorrect login credentials are rejected
- Confirm that valid registration credentials can be used to login
- Confirm that correct login credentials result in a redirect to the Contacts page

# 2) Contact List

# 3) Chat

# 4) Profile

# 5) Create Contact
### Page title
Add Contact

### Page description
Page where users can search for a user by username so that they can add them to their contact list.

![add_contact_mockup](add_contact_mockup.png)

### Parameters needed for the page
```search``` is an optional query parameter, which is the username being searched for.

### Data needed to render the page
- List of users that match the search query
- Current user information (to exclude from the results)
- Existing contacts (to show if someone is already a contact)

### Link destinations for the page
- A link to 'add contacts' will appear on every page on the nav bar.
- An icon for adding contacts will appear on the 'contacts' page.

### List of tests verifying the rendering of the page
*Basic page rendering*
- only logged in users can view the page. Anonymous users should be redirected to login page.
- page loads successfully with correct title and main elements
- search form has correct input field and search button
- nav bar displays with "add contact" in bold/highlighted

*Search functionality rendering*
- empty search shows appropriate message (e.g. "search for a user")
- no results found displays helpful message (e.g. ("No users found matching 'xyz'")
- search results display correctly: username and add button if applicable

*UI tests*
- add button disappears after contact has been added
- error messages display properly (e.g. "Failed to add contact - please try again")

*Edge cases*
- long usernames display properly (truncation or wrapping)
- large number of search results doesn't break layout

*Integration with existing data*
- existing contacts indicated (e.g. with color)
- logged-in user is excluded from search results
- contact status updates immediately after adding (no page refresh needed)
