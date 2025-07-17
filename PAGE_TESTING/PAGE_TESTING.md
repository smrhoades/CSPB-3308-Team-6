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
### Page Title
- Contacts

### Description:
- The Contacts page shows your recent conversations at the top (newest first) and then all of your contacts in alphabetical order
- It also includes links to add a contact, view your profile, or log out
![Contacts Page](contacts-page.png)

### Parameters/Data:
- **Parameters needed:** current user ID
- **Data needed to render the page:**
    - `recent_conversations`: an array of `{ contact_id, username, last_message_snippet, timestamp }`
    - `contacts`: an array of `{ contact_id, username }`

### Link Destinations:
- Clicking a recent conversation or contact opens the chat page for that contact
- “Add Contact” goes to the add-contact page
- “Profile” goes to the profile page
- “Logout” ends the session and returns to login

### Tests:
- Page loads and shows the “Recents” section when there are recent messages
- Recents are sorted by timestamp (newest first)
- Page shows “Recent” empty state message if there are no recents
- “All Contacts” section lists every contact alphabetically
- Page shows “No contacts” message if the list is empty
- Clicking a contact or convo navigates to the correct chat URL
- Nav links to add contact, profile, and logout work correctly
- Long usernames or very large lists do not break the layout

# 3) Chat
### Page title
Chat

### Page description
- A chat room between two users. 
- Provides a split screen view of the chat log with one user's messages on one side of the screen and the other user's messages on the other. Each side has an indicator at the top of which user is on which side (user initials). Messages include a time stamp and are ordered.
- Below the chat log are two additional areas: an area to type and send new messages, and a menu bar with buttons to other linked pages.

![image](./Chat_Mockup.png)

### Parameters needed for the page
- userIds of each of the two users in the chat

### Data needed to render the page
- Usernames of the two users (for the split screen indicator)
- Message history between the two users including message content and timestamp of each message (for the chat log)

### Link destinations for the page
- This page is linked to two others: the 'Profile' page and the 'Logout' page.

### List of tests verifying the rendering of the page
*Basic page rendering*
- page loads with empty chat log (no history between users)
- page loads with full chat log (long history between users)

*UI tests*
- new messages can be sent by self-user
- new messages appear in the chat log after self-user sending
- new messages appear in the chat log after other-user sending
- can follow link to profile page
- can follow link to logout page

# 4) Profile
### Page Title
- Profile

### Description:
- The Profile page displays your basic account information (username, email, etc...) and offers buttons to change your password or log out
- It also has links back to Contacts and Add Contact.
![Profile Page](profile-page.png)

### Parameters/Data:
- **Parameters needed:** current user ID
- **Data needed to render the page:**
    - `profile`: `{ username, email, ..., any other profile info}`

### Link Destinations:
- “Back to Contacts” goes to the contacts page
- “Add Contact” goes to the add-contact page
- “Change Password” goes to the password-change page
- “Logout” ends the session and returns to login

### Tests:
- Page loads and shows the correct username, email, and signup date
- Missing profile data shows a placeholder or friendly error
- Change-password button opens the correct page
- Logout button ends the session and redirects to login
- Nav links to Contacts and Add Contact work correctly
- Fields and buttons remain usable on mobile or with long text

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
