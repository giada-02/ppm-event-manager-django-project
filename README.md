# Event Management System

## Django Project Assignment Objectives
Full Website (Model, View, Template): A complete web application must be developed. Take care of the dynamic aspect of a website. Put more attention on the development of the Model and the View.\
Build an event management system where users can create, manage, and attend events. Implement features such as event creation, event registration, and event attendance tracking. The model complexity can involve defining relationships between users, events, and registrations. The templates can focus on displaying event details and attendee information.

## Event Manager Website - Features
Anyone who visits the website can observe a list of events created by users, the event details and the organizer's username and bio. It is also allowed to search events by their title, organizer, and by selecting a date.\ A user can `Sign Up` or `Login` to register or access their account. The registration form requires an adequate username, password and age (>=18).\
Once the user has be authenticated, they can either `Logout` or go to their Profile. `Your Profile` provides the user's details and a series of Actions.\
In regards to the user's account and profile, they can Logout, Delete their account or Edit the profile details through a form. As for handling the events, a user can create a new event through the event creation form providing a title, description, date and location. A user can also view the events they are attending and the ones they are hosting.\
To attend an event hosted by another user, a user can `Join` it, to remove the event from attending list, a user can `Leave` it.\
Tracking event attendance is achieved by the hosting page of the organizer of the event, this user can view how many users joined the event and the attendees details.
The organizer is also allowed to edit and delete the events they are hosting.
