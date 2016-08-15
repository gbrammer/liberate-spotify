liberate-spotify
================
Transfer Spotify albums and followed artists from one account to another.  

For example, pull information from an account locked to Facebook and dump it into a new account tied to just an email address.  This is all necessary since Spotify makes it apparently impossible to de-facebookify an account.

Steps:

1) Log into spotify.com with the original account.

2) Generate an API token with access to the scopes `user-follow-read` and `user-library-read` from, e.g., https://developer.spotify.com/web-api/console/put-following/#complete.  Write the token down as `READ_AUTH_TOKEN`.

3) Log out of spotify.com with the old account.

4) Make new account at spotify.com and log in

5) Generate an API token with access to the scopes `user-follow-modify` and `user-library-modify` from, e.g., https://developer.spotify.com/web-api/console/put-following/#complete.  Write the token down as `MODIFY_AUTH_TOKEN`.

6) Clone this repo

```git clone https://github.com/gbrammer/liberate-spotify.git```

7) Put the API tokens you generated in the top few lines of `transfer.py`. 

8) Run it!

```python
>>> import transfer
>>> transfer.run_transfer()
```

  *NB:* The album transfer can take a while because a small pause is inserted before each album import to preserve the "added order" of the album list.
