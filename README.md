# Form-Prober
Crawls a website searching for forms vulnerable to script injection attacks.

1. Clone Repo

2. Navigate to Repo's Root folder

3. Install dependencies with command:
        pip install -r "requirements.txt"

4. Run webCrawler_proxyHunter with command:
        python webCrawler_proxyHunter

5. Run webCrawler_formProber with command:
        python webCrawler_formProber

6. After the script has finished running, you will have an output that gives you a list of forms vulnerable to SQL or XSS script injection attacks.

Example Output:

<!-- URL: http://localhost/#/login
Payload: <script>alert('XSS')</script>
Vulnerable: False
Status: Not Vulnerable
Response Snippet: <html lang="en" data-critters-container="" class="fontawesome-i2svg-active fontawesome-i2svg-complete"><head>
  <meta charset="utf-8">
  <title>OWASP Juice Shop</title>
  <meta name="description" cont
Console Logs: ['http://localhost/rest/user/login - Failed to load resource: the server responded with a status of 500 (Internal Server Error)']
--------------------------------------------------
URL: http://localhost/#/login
Payload: 1' OR '1'='1
Vulnerable: True
Status: Vulnerable
Response Snippet: <html lang="en" data-critters-container="" class="fontawesome-i2svg-active fontawesome-i2svg-complete"><head>
  <meta charset="utf-8">
  <title>OWASP Juice Shop</title>
  <meta name="description" cont
Console Logs: ['http://localhost/rest/user/login - Failed to load resource: the server responded with a status of 401 (Unauthorized)', 'http://localhost/rest/user/login - Failed to load resource: the server responded with a status of 401 (Unauthorized)']
--------------------------------------------------
URL: http://localhost/#/contact
Payload: <script>alert('XSS')</script>
Vulnerable: False
Status: Not Vulnerable
Response Snippet: <html lang="en" data-critters-container="" class="fontawesome-i2svg-active fontawesome-i2svg-complete"><head>
  <meta charset="utf-8">
  <title>OWASP Juice Shop</title>
  <meta name="description" cont
Console Logs: ['https://cdnjs.cloudflare.com/ajax/libs/cookieconsent2/3.1.0/cookieconsent.min.css - Failed to load resource: net::ERR_TIMED_OUT', 'https://cdnjs.cloudflare.com/ajax/libs/cookieconsent2/3.1.0/cookieconsent.min.js - Failed to load resource: net::ERR_TIMED_OUT', 'https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js - Failed to load resource: net::ERR_TIMED_OUT', "http://localhost/ 18:27 Uncaught TypeError: Cannot read properties of undefined (reading 'initialise')"]
--------------------------------------------------
URL: http://localhost/#/contact
Payload: 1' OR '1'='1
Vulnerable: True
Status: Vulnerable
Response Snippet: <html lang="en" data-critters-container="" class="fontawesome-i2svg-active fontawesome-i2svg-complete"><head>
  <meta charset="utf-8">
  <title>OWASP Juice Shop</title>
  <meta name="description" cont
Console Logs: []
--------------------------------------------------
URL: http://localhost/#/about
Payload: <script>alert('XSS')</script>
Vulnerable: False
Status: Not Vulnerable
Response Snippet: <html lang="en" data-critters-container="" class="fontawesome-i2svg-active fontawesome-i2svg-complete"><head>
  <meta charset="utf-8">
  <title>OWASP Juice Shop</title>
  <meta name="description" cont
Console Logs: ['https://cdnjs.cloudflare.com/ajax/libs/cookieconsent2/3.1.0/cookieconsent.min.css - Failed to load resource: net::ERR_TIMED_OUT', 'https://cdnjs.cloudflare.com/ajax/libs/cookieconsent2/3.1.0/cookieconsent.min.js - Failed to load resource: net::ERR_TIMED_OUT', 'https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js - Failed to load resource: net::ERR_TIMED_OUT', "http://localhost/ 18:27 Uncaught TypeError: Cannot read properties of undefined (reading 'initialise')"]
--------------------------------------------------
URL: http://localhost/#/about
Payload: 1' OR '1'='1
Vulnerable: True
Status: Vulnerable
Response Snippet: <html lang="en" data-critters-container="" class="fontawesome-i2svg-active fontawesome-i2svg-complete"><head>
  <meta charset="utf-8">
  <title>OWASP Juice Shop</title>
  <meta name="description" cont
Console Logs: []
--------------------------------------------------
URL: http://localhost/#/photo-wall
Payload: <script>alert('XSS')</script>
Vulnerable: False
Status: Not Vulnerable
Response Snippet: <html lang="en" data-critters-container="" class="fontawesome-i2svg-active fontawesome-i2svg-complete"><head>
  <meta charset="utf-8">
  <title>OWASP Juice Shop</title>
  <meta name="description" cont
Console Logs: ['https://cdnjs.cloudflare.com/ajax/libs/cookieconsent2/3.1.0/cookieconsent.min.css - Failed to load resource: net::ERR_TIMED_OUT', 'https://cdnjs.cloudflare.com/ajax/libs/cookieconsent2/3.1.0/cookieconsent.min.js - Failed to load resource: net::ERR_TIMED_OUT', 'https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js - Failed to load resource: net::ERR_TIMED_OUT', "http://localhost/ 18:27 Uncaught TypeError: Cannot read properties of undefined (reading 'initialise')"]
--------------------------------------------------
URL: http://localhost/#/photo-wall
Payload: 1' OR '1'='1
Vulnerable: True
Status: Vulnerable
Response Snippet: <html lang="en" data-critters-container="" class="fontawesome-i2svg-active fontawesome-i2svg-complete"><head>
  <meta charset="utf-8">
  <title>OWASP Juice Shop</title>
  <meta name="description" cont
Console Logs: []
--------------------------------------------------
URL: http://localhost/redirect?to=https://github.com/juice-shop/juice-shop
Payload: N/A
Vulnerable: False
Status: No Inputs
Response Snippet: 
Console Logs: []
--------------------------------------------------
URL: http://localhost/redirect?to=https://github.com/juice-shop/juice-shop
Payload: N/A
Vulnerable: False
Status: No Inputs
Response Snippet: 
Console Logs: []
--------------------------------------------------
URL: http://localhost/#/forgot-password
Payload: <script>alert('XSS')</script>
Vulnerable: False
Status: Not Vulnerable
Response Snippet: <html lang="en" data-critters-container="" class="fontawesome-i2svg-active fontawesome-i2svg-complete"><head>
  <meta charset="utf-8">
  <title>OWASP Juice Shop</title>
  <meta name="description" cont
Console Logs: ['https://cdnjs.cloudflare.com/ajax/libs/cookieconsent2/3.1.0/cookieconsent.min.css - Failed to load resource: net::ERR_TIMED_OUT', 'https://cdnjs.cloudflare.com/ajax/libs/cookieconsent2/3.1.0/cookieconsent.min.js - Failed to load resource: net::ERR_TIMED_OUT', 'https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js - Failed to load resource: net::ERR_TIMED_OUT', "http://localhost/ 18:27 Uncaught TypeError: Cannot read properties of undefined (reading 'initialise')"]
--------------------------------------------------
URL: http://localhost/#/forgot-password
Payload: 1' OR '1'='1
Vulnerable: True
Status: Vulnerable
Response Snippet: <html lang="en" data-critters-container="" class="fontawesome-i2svg-active fontawesome-i2svg-complete"><head>
  <meta charset="utf-8">
  <title>OWASP Juice Shop</title>
  <meta name="description" cont
Console Logs: []
--------------------------------------------------
URL: http://localhost/#/register
Payload: <script>alert('XSS')</script>
Vulnerable: False
Status: Not Vulnerable
Response Snippet: <html lang="en" data-critters-container="" class="fontawesome-i2svg-active fontawesome-i2svg-complete"><head>
  <meta charset="utf-8">
  <title>OWASP Juice Shop</title>
  <meta name="description" cont
Console Logs: ['https://cdnjs.cloudflare.com/ajax/libs/cookieconsent2/3.1.0/cookieconsent.min.css - Failed to load resource: net::ERR_TIMED_OUT', 'https://cdnjs.cloudflare.com/ajax/libs/cookieconsent2/3.1.0/cookieconsent.min.js - Failed to load resource: net::ERR_TIMED_OUT', 'https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js - Failed to load resource: net::ERR_TIMED_OUT', "http://localhost/ 18:27 Uncaught TypeError: Cannot read properties of undefined (reading 'initialise')"]
--------------------------------------------------
URL: http://localhost/#/register
Payload: 1' OR '1'='1
Vulnerable: True
Status: Vulnerable
Response Snippet: <html lang="en" data-critters-container="" class="fontawesome-i2svg-active fontawesome-i2svg-complete"><head>
  <meta charset="utf-8">
  <title>OWASP Juice Shop</title>
  <meta name="description" cont
Console Logs: [] -->
