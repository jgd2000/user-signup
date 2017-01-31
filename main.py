import webapp2
import cgi
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User-Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <div href="/">Signup</div>
    </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""


class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.user-signup.com/
    """

    def get(self):

        username = self.request.get("username")
        username_error = self.request.get("username_error")
        password_error = self.request.get("password_error")
        verify_error = self.request.get("verify_error")
        email = self.request.get("email")
        email_error = self.request.get("email_error")

        # a form for adding new users
        add_form = """
        <form action="/add" method="post">
        <table>
        <tbody>
        <tr>

        <td>
        <label for "username">Username</label>
        </td>

        <td>
        <input name="username" type="text" value ="{0}" required>
        <span class="error">{1}</span>
        </td>
        </tr>

        <tr>
        <td>
        <label for "password">Password</label>
        </td>
        <td>
        <input name="password" type="text" value required>
        <span class="error">{2}</span>
        </td>
        </tr>

        <tr>
        <td>
        <label for "verify">Verify Password</label>
        </td>
        <td>
        <input name="verify" type="text" value required>
        <span class="error">{3}</span>
        </td>
        </tr>

        <tr>
        <td>
        <label for "email">Email (optional)</label>
        </td>
        <td>
        <input name="email" type="text" value="{4}">
        <span class="error">{5}</span>
        </td>
        </tr>

        <tbody>
        </table>
        <input type="submit" value="Submit"/>
        </form>

        """.format(username,username_error,password_error,verify_error,email,email_error)

        # combine all the pieces to build the content of our response
        main_content = add_form
        content = page_header + main_content + page_footer
        self.response.write(content)


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)


class AddUser(webapp2.RequestHandler):
    """ Handles requests coming in to '/add'
        e.g. www.user-signup.com/add
    """

    def post(self):
        # look inside the request to figure out what the user typed
        input_errors = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""

        if not valid_username(username):
            username_error = "That is not a valid username."
            input_errors = True

        if not valid_password(password):
            password_error = "That is not a valid password. ( 3 - 20 chars )"
            input_errors = True

        if password != verify:
            verify_error = "Passwords do not match."
            input_errors = True

        if not valid_email(email):
            email_error = "That is not a valid email."
            input_errors = True

#        main_content = add_form
#        content = page_header + main_content + page_footer
#+        self.response.write(content)
        if input_errors == False:
            self.redirect('/Welcome?username=' + username)
        else:
            self.redirect('/?username=' + username + '&username_error=' + username_error + '&password_error=' + password_error +
        '&verify_error=' + verify_error + '&email=' + email + '&email_error=' + email_error)


class Welcome(webapp2.RequestHandler):
    """ Welcomes new user
    """

    def get(self):
#        username_error="this is a username error"
        username = self.request.get("username")
        content ="<h2>" +"Welcome " + username + "</h2>"
        self.response.write(content)



app = webapp2.WSGIApplication([
    ('/', Index),
    ('/add', AddUser),
    ('/Welcome', Welcome)
], debug=True)
