<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Secure REST API — Authentication & Authorization Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: auto;
            padding: 20px;
        }
        h1, h2, h3 {
            color: #222;
        }
        code, pre {
            background: #f4f4f4;
            padding: 10px;
            display: block;
            overflow-x: auto;
        }
        .note {
            background: #eef6ff;
            border-left: 4px solid #3b82f6;
            padding: 10px;
            margin: 15px 0;
        }
        .warning {
            background: #fff4e5;
            border-left: 4px solid #f59e0b;
            padding: 10px;
            margin: 15px 0;
        }
    </style>
</head>
<body>

<h1>🔐 Secure REST API (FastAPI)</h1>

<p>
This project is a minimal but security-focused REST API built using <strong>FastAPI</strong>.
It demonstrates how <strong>authentication</strong> and <strong>authorization</strong> should be implemented correctly
in real-world APIs.
</p>

<hr>

<h2>📌 What This API Does</h2>

<ul>
    <li>User registration</li>
    <li>User login with password hashing</li>
    <li>JWT-based authentication</li>
    <li>Post creation tied to a user</li>
    <li>Authorization checks to prevent cross-user access</li>
</ul>

<p>
This is intentionally kept simple — no roles, no admin panels, no overengineering.
</p>

<hr>

<h2>🔑 Authentication Model</h2>

<p>
Authentication answers the question:
</p>

<strong>“Who is the user making this request?”</strong>

<h3>How it works</h3>

<ol>
    <li>User logs in with username & password</li>
    <li>Password is verified using a secure hash</li>
    <li>A JWT access token is issued</li>
    <li>The token is sent in the <code>Authorization</code> header</li>
</ol>

<pre>
Authorization: Bearer &lt;JWT_TOKEN&gt;
</pre>

<p>
Every protected endpoint depends on <code>get_current_user</code>,
which validates the token and resolves the user from the database.
</p>

<div class="note">
<strong>Important:</strong> Authentication alone is not enough.  
An authenticated user can still be malicious.
</div>

<hr>

<h2>🛂 Authorization Model</h2>

<p>
Authorization answers the question:
</p>

<strong>“Is this user allowed to perform this action on this resource?”</strong>

<h3>Ownership Enforcement</h3>

<ul>
    <li>Each post has an <code>owner_id</code></li>
    <li>Update/Delete endpoints verify ownership</li>
    <li>If the user does not own the post → request is rejected</li>
</ul>

<pre>
if post.owner_id != current_user.id:
    raise HTTPException(status_code=403)
</pre>

<div class="warning">
This is where most real-world API breaches happen (IDOR / Broken Object Level Authorization).
</div>

<hr>

<h2>🧠 Threats Considered</h2>

<ul>
    <li>Plaintext password storage ❌</li>
    <li>Unauthenticated access to protected routes ❌</li>
    <li>Cross-user post deletion (IDOR) ❌</li>
    <li>Token tampering ❌</li>
</ul>

<p>
This API explicitly prevents these by design.
</p>

<hr>

<h2>🧪 How to Test (curl Examples)</h2>

<h3>1️⃣ Register a user</h3>

<pre>
curl -X POST http://127.0.0.1:8000/users \
-H "Content-Type: application/json" \
-d '{"username":"alice","password":"Password321"}'
</pre>

<h3>2️⃣ Login</h3>

<pre>
curl -X POST http://127.0.0.1:8000/login \
-H "Content-Type: application/json" \
-d '{"username":"alice","password":"Password321"}'
</pre>

<p>
Copy the <code>access_token</code> from the response.
</p>

<h3>3️⃣ Try creating a post WITHOUT auth (should fail)</h3>

<pre>
curl -X POST "http://127.0.0.1:8000/posts?title=Nope&content=Fail"
</pre>

<h3>4️⃣ Create a post WITH auth</h3>

<pre>
curl -X POST http://127.0.0.1:8000/posts \
-H "Authorization: Bearer &lt;YOUR_TOKEN&gt;" \
-H "Content-Type: application/json" \
-d '{"title":"Bada Bada","content":"Booom"}'
</pre>

<h3>5️⃣ Attempt to delete someone else’s post (should fail)</h3>

<pre>
curl -X DELETE http://127.0.0.1:8000/posts/1 \
-H "Authorization: Bearer &lt;YOUR_TOKEN&gt;"
</pre>

<p>
Expected response:
</p>

<pre>
{"detail":"Not authorized to delete this post"}
</pre>

<hr>

<h2>📍 Where Security Lives in the Code</h2>

<ul>
    <li><strong>Password hashing:</strong> <code>security.py</code></li>
    <li><strong>JWT creation & validation:</strong> <code>security.py</code> + <code>get_current_user</code></li>
    <li><strong>Authentication enforcement:</strong> FastAPI dependencies</li>
    <li><strong>Authorization enforcement:</strong> Post ownership checks</li>
</ul>

<hr>

<h2>🎓 Final Notes</h2>

<p>
This project is intentionally small but realistic.
If you can understand and explain this API, you understand the core of secure backend development.
</p>

<p>
You could confidently teach this to a junior developer — and explain why
<strong>authentication ≠ authorization</strong>.
</p>

</body>
</html>
