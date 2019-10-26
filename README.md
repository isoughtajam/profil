# profil
This is my personal site, currently at https://controls.ee

It features a blog and links to my art and work, along with interesting projects by others I'd like to share.

profil is written in React, with a Flask and postgres backend.

## Usage
Build the frontend:

    /profil/static$ webpack
    ...
                Asset     Size  Chunks                    Chunk Names
    search.bundle.js  1.83 MB       0  [emitted]  [big]  search
    links.bundle.js  1.83 MB       1  [emitted]  [big]  links
    app.bundle.js  1.83 MB       2  [emitted]  [big]  app
    admin.bundle.js  1.03 MB       3  [emitted]  [big]  admin
    landing.bundle.js  1.02 MB       4  [emitted]  [big]  landing
    ...

and start the server:

    profil/server$ source <path to virtualenv>/bin/activate
    (virtualenv) profile/server$ python app.py