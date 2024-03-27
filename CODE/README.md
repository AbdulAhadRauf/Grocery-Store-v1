# Grocery Store Application with Flask!

App developed by [Abdul Ahad Rauf](mailto:21f3002590@ds.study.iitm.ac.in) (21f3002590)

Made using HTML, Flask, Bootstrap

---

## Steps to run this app

- Create a Virtual environment in the same directory
  - `python -m venv env` for Windows.
  - `virtualenv env` for Linux or MacOS.
- Activate the Virtual environment
  - `env\Scripts\activate` for Windows.
  - `source env/bin/activate` for Linux or MacOS.
- Install the Requirements
  - `pip install requirements.txt`to install requiremnts.
- Run the app `python app.py`
- Don't forget to deactivate the Virtual environment when you're done exploring
  - `env\Scripts/deactivate` for Windows.
  - `source env/bin/deactivate` for Linux or MacOS.

---

## Folder Structure

- ### /apis

  - (/api/grocery_item) - Contains API calls to get, put, delete an Grocery Item [CRUD operations].
  - (/api/user) - Contains API call for getting users.

- ### /application

  - (app.py) - Main code file, contains routes for all pages.
  - (models.py) - Contains Database schemas.

- ### /routes

  - (/) - Home page / Product page . Also acts like the user dashboard when user signs in.
  - (/user/login) - Validates the id password and lets the user login or redirect back to login page.
  - (/user/signup) - Lets users Signup based on various checks (email, phone must be unqiue), (entiries must not be blank) etc etc.
  - (/admin/dashboard) - Admin can CRUD all Grocery items.
  - (/admin/analysis) - Plots cumulative and total sales line graph. Creates Pie charts based on Category and each item.
  - (/logout) - logs the current user out.

- ### /static

  - (style.css) - Stylesheet.
  - (artbreeder-image.png) - Image for Background.
  - (cumulative_revenue.png) - Image for cumulative_revenue ([Graph] creates new everytime).
  - (daily_sales.png) - Image for daily_sales ([Graph] creates new everytime).
  - (Grocery1.jpg) - Image for home page carousel.
  - (Grocery2.jpg) - Image for home page carousel.
  - (Grocery3.jpg) - Image for home page carousel.
  - (pchart_category.png) - Image for pchart_category (PIE [Chart] creates new everytime).
  - (pchart_items.png) - Image for pchart_items (PIE [Chart] creates new everytime).

- ### /templates

  - (admin_dashboard.html) - admin_dashboard where he can CRUD all Grocery Items, has all validations.
  - (admin_update.html) - admin_update can updated previous items.
  - (analysis.html) - shows the analysis by plotting charts.
  - (base.html) - base template for all the child templates.
  - (cart.html) - User cart that automatically clears once user makes the purchase.
  - (checkout.html) - Final checkout page to make payment and add/change details.
  - (product_page.html) - product_page/ Home page, diplays the data in table form.
  - (user_login.html) - user_login with proper validations.
  - (user_signup.html) - user can signup with proper validations.

- ### (app.py) - Configuration of Application.
- ### (database.sqlite3) - Database.
- ### (CHECKLIST.md) - Checklist for Project Submission.
- ### (README.md)
- ### (Project Report.pdf) - https://drive.google.com/file/d/1lFJWQwPk2q3w65k8GD98EgEF5jraSJzM/view?usp=drive_link
- ### (api.yaml) - YAML file for API description.
- ### (requirements.txt) - Packages required.
- ### (video) - https://drive.google.com/file/d/1k22hdY5as-Mui1NxF9prtbGYy0abYIoy/view?usp=drive_link

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Author

The web application is created by Abdul Ahad Rauf.
