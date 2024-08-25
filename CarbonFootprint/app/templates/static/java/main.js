document.getElementById('login').addEventListener('submit', function(event) {
   event.preventDefault(); // Prevent the default form submission

   // Get form values
   const username = document.getElementById('login-email').value;
   const password = document.getElementById('login-pass').value;

   // Dummy credentials for demonstration
   const validUsername = 'admin@user.com';
   const validPassword = 'msec1234';

   // Validate credentials
   if (username === validUsername && password === validPassword) {
       // Redirect to the next page if credentials are correct
       window.location.href = 'new.html'; // Replace with your URL
   } else {
       // Display an error message if credentials are incorrect
       document.getElementById('error-message').textContent = 'Invalid username or password';
   }
});