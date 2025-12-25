<h1>🔐 Secure REST API with Authentication & Authorization</h1>

<p>
This learning project is a minimal but security-focused REST API built using <strong>FastAPI</strong>.
It demonstrates how <strong>authentication</strong> and <strong>authorization</strong> should be implemented in real-world APIs.
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

<h2>🎓 Final Notes</h2>

<p>
This project is intentionally small but realistic, to understand how APIs and API security operates in real life.
</p>

