Lab 3 Team Pointing

   * Team Number: Team 6
   * Team Name: Undefined
   * Day/Time of Weekly Team Meeting: Wednesdays 6 pm MDT-USA / 7 pm CDT-USA / 8am CST-China (Thurs)
   * Team Members in meeting:
   *   Sara Rhoades (elected scrum master for the meeting)
   *   Joey Musholt
   *   Joel Henry
   *   Jitesh Mullapudi
   *   Daniel Williams
   * Link to Zoom recording of team activity: 

Planning Poker: 1, 2, 3, 5, 8, 13, 20, ?

For a Moodle-type service:
As a user, I want to upload graphs & images so that I can share them with peers.
As an administrator, I want to introduce an anti-plagiarism tool.
As a user, I want data visualization on Moodle, so I have better understanding of my progress.

For an e-commerce service:
As a user, I want to compare the costs and reviews of products.
As a busy shopper, I want to check out just one item.
As an unsatisfied customer, I want to cancel my order.

```
User Story Card
______________________________________________________________________________
As a 	: As a user,
I want	: I want to upload graphs & images 
So that : so that I can share them with peers.

Effort
Level	: 5

Acceptance Criteria
Given	: 	I am logged and have an image on my computer
When 	: 	I click the upload button
Then 	: 	then the image is stored and shared to others
____________________________________________________________________________

```

```
User Story Card
______________________________________________________________________________
As a 	: As an administrator,
I want	: I want to introduce an anti-plagiarism tool.
So that : So that I can grade them as zero.

Assumptions:
Use built-libraries (NOT from scratch).

Effort
Level	: 5

Acceptance Criteria
Given	: 	Someone submits an assignment
When 	: 	Automatically
Then 	: 	I get a probability of plagarism score
____________________________________________________________________________

```

```
User Story Card
______________________________________________________________________________
As a 	: As a user,
I want	: I want data visualization on Moodle
So that : so I have better understanding of my progress.

Assumptions:
Many types of visualizations possible - have to limit scope
Two visuals:
  our grade in course for each asignment
  checkerboard of completed / uncompleted tasks
Data already exists to full vis

Effort
Level	: 5

Acceptance Criteria
Given	: 	I am enrolled in a class
When 	: 	I view my home page
Then 	: 	I view all visualizations
____________________________________________________________________________

```

```
User Story Card
______________________________________________________________________________
As a 	: As a user,
I want	:I want to compare the costs and reviews of products.
So that : I can choose the one that aligns with my goals

Assumptions:
Comparisons are within the platform (not reaching out to other sites)
Software should not generate the comparison (user selected what to compare)
Assume we have product data / specs in a database

Effort
Level	: 3

Acceptance Criteria
Given	: 	I have selected 2-5 items
When 	: 	I click a button
Then 	: 	The product specs are displayed in a chart
____________________________________________________________________________

```

```
User Story Card
______________________________________________________________________________
As a 	: As a busy shopper,
I want	: I want to check out just one item.
So that : To save time

Assume:
One-click 'Buy Now'-type feature
Already have a 'standard' checkout procedure which prompts for details
Have 'defaults' saved somewhere, else would have to add those details

Effort
Level	: 5

Acceptance Criteria
Given	: 	I am on an item page
When 	: 	I click the 'Buy Now' button
Then 	: 	The product is auto purchased (if all data avaliable),
          Else data is entered and product is purchased
____________________________________________________________________________

```

```
User Story Card
______________________________________________________________________________
As a 	: As an unsatisfied customer,
I want	:  I want to cancel my order.
So that : I get a refund

Assumptions:
If sent, cannot cancel the order
  Order tracking already exists
Need to refund customer (payment already made)
  Refund is a mod on payment system

Effort
Level	: 5

Acceptance Criteria
Given	: 	I have made an order previously and I am on order page
When 	: 	I click 'cancel order button'
Then 	: 	The item is nnot shipped and the money is refunded.
____________________________________________________________________________

```

