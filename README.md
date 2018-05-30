# message_board
Language and framework - Python/Django
A simple message board designed for discussing games. After registering, users can submit comments for new or existing games, and comments will be displayed on that game's page. This framework could be used to discuss other topics in place of (or in addition to) games by modifying contents in and references to the "games" app.

[Features]
-Basic Login/Reg system for users
-User dashboard that displays names and emails of all users, as well as actions (view for all users, edit/delete/add for admins). Admins can also see user levels at this point.
-Game list home page that displays recent comments, lists of games separated into pages with comments and those without comments, and a form to submit a new comment with a game.
-Game page that displays the game title and comments on the game as well as a form to submit a comment for that game.
-'Like' system for both comments and game pages
-Top bar with buttons for different actions (logout, profile link, games list link, dashboard link)
-Comments display the name of the user that submitted the comment (as a link to that user's profile), and, on the games list page, a link to the game.
-Users can delete their own comments.
-User profiles display user information (name, email, total number of comments, total number of liked games, total number of liked comments), games the user likes, and comments the user has posted.
-User's edit profile page displays first name, last name, and email which can be edited, a comment form, and the user's comments and liked games.

[Priority Items]
Implement comment editing feature (requires validate and submit functions in comments.models as well as a form/page for the user to edit the comment)
Implement additional admin features (admins should be able to delete or edit comments by users with an account level with fewer permissions than their own)
Impplement password change ability for users (currently, admins can edit passwords of accounts with account levels with fewer permissions)

[Nice to Haves/Future iterations]
Expand on Game pages/model (release year, platform(s), genres)
Sort/filter options for games, comments, and likes
Search suggest when adding a comment when not on a specific games page (could involve researching APIs/databases with existing and upcoming game titles)
