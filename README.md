# Token-based Auth in Flask

## Overview
This project is a full implementation of token-based authentication for Flask--everything but the frontend. Weakly based on Twitter, it shows how to conditionally protect routes based on the following scenarios:
- Creating posts
- Getting a personal "timeline" of posts
- Following other users


## Technical Improvement Ideas
- Database proxy (currently, connection is opened and closed for every query)
- Redesign so that deleting a post puts a marker on it instead of deleting it from the DB
- Find a better way to check for method type when overloaded on a single route (/post)