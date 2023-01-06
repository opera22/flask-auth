# Token-based Auth in Flask

## Overview
This project is a full implementation of token-based authentication for Flask--everything but the frontend. Weakly based on Twitter, it shows how to conditionally protect routes for the following functions:
- Creating a post
- Getting a personal "timeline" of posts
- Following other users
- Deleting posts

**Note**: While the Auth and App servers are combined here, the two services could exist separately, because JWTs are stateless. (Just make sure you have the secret key on both systems at deployment, as it's *symmetric* encryption.)

## *Auth Flow*
![](images/jwt_flow.png)

*Credit: [Mark Macneil](https://fullstackmark.com/post/19/jwt-authentication-flow-with-refresh-tokens-in-aspnet-core-web-api)*

## *Getting a Token*
The first step, which at this point is completely unprotected, is to create an account at the `/signup` route with the following payload:
```json
{
    "username":"joey2go",
    "password":"bestpass123"
}
```

This step returns nothing to the user except a 200 Successful status. A user is created in the Users table.

Next, the user logs in with those same credentials at the `/login` route:
```json
{
    "username":"joey2go",
    "password":"bestpass123"
}
```

If successful, the server returns the bearer token (to be used with every subsequent request):
```json
{
    "status": 200,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjcsImlhdCI6MTY3Mjk2OTAyNywiZXhwIjoxNjcyOTcyNjI3fQ.OFLKAgJzUQ4_p_HT455TaKLmPXRNU-31R_n2GXjLdNs"
}
```

## Endpoints

*In progress...*

## Technical Improvement Ideas
- Database proxy (currently, connection is opened and closed for every query)
- Redesign so that deleting a post puts a marker on it instead of deleting it from the DB
- More secure way to check auth for *deleting* a post?
- Find a better way to check for method type when overloaded on a single route (`/post`)

## Helpful Resources
- [IBM documentation for JWTs](https://www.ibm.com/docs/en/cics-ts/6.1?topic=cics-json-web-token-jwt)
- [JWT debugger](https://jwt.io)
- [Working with PyJWT](https://pyjwt.readthedocs.io/en/stable/usage.html#encoding-decoding-tokens-with-hs256)
- [Difference between HS256 and RS256](https://auth0.com/blog/rs256-vs-hs256-whats-the-difference/)