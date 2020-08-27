# manage-todos(Mini Project)

Create a simple web-based application to manage Todos. The frontend will be built using React & NextJS, and will contain one page, with functionality similar to this page: http://todomvc.com/examples/vanillajs/ (the UI & styling can be simplified to basic inputs & divs). The frontend will fetch, create, update and delete Todos in JSON format using a REST API served by a Flask webserver. The todos will be stored in a relational database (you can use SQLite, MySQL or Postgres) and the database operations will be done using SQL alchemy.

If you are done with the basic version of the project, try making the following enhancements:

- Use Redux for state management, if you weren’t using it already.
- Give each todo its own URL and perform server-side rendering of the pages using NextJS
- Add a “Delete all Todos” button, clicking on which deletes all todos.
- As there can be hundreds or thousands of todos in the database. The deletion should be done in background using a celery task. Deploy the frontend & backend online.
- Deploy the frontend for free on Vercel and the backend server powering the REST API can be deployed to Heroku.
