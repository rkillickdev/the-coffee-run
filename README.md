# **The Coffee Run App**

The Coffee Run App has been developed as part of the Code Institute Diploma in Full Stack Software Development (Portfolio Project #3 - Python Essentials).  The app targets people on a busy schedule who want the ability to order their coffee in advance and pick up at a designated time.

<br>

![Deployed Site View](docs/devices/coffee-run-deployed-mockup.png)

<br>

[View the deployed app on Heroku](https://the-coffee-run.herokuapp.com/)

[View the Google Sheets worksheet for the app here](https://docs.google.com/spreadsheets/d/1xP6diVy29WpZ_O2dBV_bloRFv9dYs0kOkFteq5djAqs/edit?usp=sharing)

<br>

## **CONTENTS**

* [User Experience (UX)](#user-experience-ux)
    * [Strategy](#strategy)
        * [Project Goals](#project-goals)
        * [User Stories](#user-stories)
    * [Scope](#scope)
    * [Design](#design)
        * [Python Logic Flow Chart](#python-logic-flow-chart)
        * [App Functionality and Features](#app-functionality-and-features)
        * [Database](#database)
        * [Error Handling](#error-handling)
        * [Typography](#typography)
        * [Imagery](#imagery)
* [Technologies Used](#technologies-used)
    * [Languages Used](#languages-used)
    * [Programs Used](#programs-used)
    * [Frameworks and Libraries used](#frameworks-and-libraries-used)
* [Deployment and Local Development](#deployment-and-local-development)
* [Testing](#testing)
    * [Automated Testing](#automated-testing)
    * [Manual Testing](#manual-testing)
* [Bugs](#bugs)
    * [Known Bugs](#known-bugs)
    * [Solved Bugs](#solved-bugs)
* [Credits](#credits)
    * [Code Used and Referenced](#code-used-and-referenced)
    * [Media](#media)
    * [Acknowledgements](#acknowledgements)


# **User Experience (UX)**

## **STRATEGY**
___

## **Project Goals**

<br>

The client for this project is a fictional coffee shop although this scenario could be applied to many real world examples.  The business is based next door to a train station and therefore a large part of revenue comes from take away orders.  The cafe space itself is relatively small, and the owner has noticed that at peak times of train travel this space becomes quickly overcrowded and cramped with takeaway customers waiting for their order.  This means that prospective customers may not even attempt to purchase a coffee as they are put off by the queue.  It also degrades the customer experience of those who have chosen to sit in and enjoy a more leisurely coffee.  The owner has also observed that many of the takeaway customers are purchasing their coffee with the intention of then jumping on the train as part of their commute to work.  Customers are left unhappy if the amount of time spent waiting for their coffee to be made, results in them missing their train and being late for work.

The aim of the project is to therefore develop an app that can be used by customers to order their takeaway coffee in advance and be provided a specific pickup time.  This should improve the customer experience and remove one element of stress from their daily commute. Another target user for the app will be those doing the office 'coffee run', who normally place quite large orders with various different types of coffee.  The ability to order in advance means there will not be a long wait for the customer when arriving at the cafe as their order will be ready to take away. 

Along with a reduction in overcrowding at peak times, the cafe owner also hopes that the data collected from the app will provide a valuable insight for the business. They hope analysis of this data will help to build a profile of the busiest times of the day and allow them to schedule staffing appropriately so sufficient baristas are on shift to manage the demand.  The app will also provide the business with sales data, which they can use to inform them in stock buying decisions for coffee beans and milk.  

<br>

## **User Stories**

<br>

### Client Goals:

<br>

* As the client, I want to reduce queues building up inside/outside the coffee shop and maximise the number of customers that can get their coffee before catching their train.
* As the client, I want to collect data from orders made via the app to make future business decisions.
* As the client, I want all user input to be validated and errors handled gracefully.
* As the client, I want to ensure a good user experience by making the app easy to use and intuitive. 
* As the client, I want to keep the user informed throughout the ordering process by providing feedback at each stage.

<br>

### User Goals:

<br>

* As the user, I want to view all available coffee & milk options to make my choice.
* As the user, I want to order my coffee quickly and for the experience to be intuitive.
* As the user, I want to be provided clear information about when my order will be ready to pickup.
* As the user, I want to be able to view my order details and pickup time once the order has been placed. 

<br>

## **SCOPE**
___

### **Features**

<br>

In order to satisfy the goals outlined in the project strategy, I will implement the following features:

* Allow user to enter username details so messages can be personalised throughout the order.
* Present the user with a coffee price menu from which they can select their type of coffee.
* Allow the user to select the type of milk.
* Select the quantity they would like of this particular coffee.
* Provide the option for user to add additional items to their order before finalising.
* Allow the user to remove items from their order.
* Allow the user to edit the quantity of an item in the order.
* Log time and date of order to base estimated pick up time on.
* Provide the user with a finalised order summary, with order details, price, estimated pickup time and unique order reference.
* Update the "orders" sheet with order data that can be used by the client to prepare the necessary coffee.
* Update the "sales" sheet with order data that can be used by the client in future business decision making.

<br>

### **Future Implementations**

<br>

Functionality that is not within the scope of this project, but that could be added at a later date to enhance the user experience would be:

* The ability for the user to pay for the order using the app, to make the pickup process even smoother and quicker.
* The ability for users to create an account where they can accrue loyalty points for each coffee order and redeem them when sufficient total reached.
* Admin View can only be accessed with username and password login
* Increase options for the business owner in Admin View to manipulate the data in ways that are most useful to them.  More functions could be written to analyse and display the data as required.

<br>

## **DESIGN**
___

<br>

## **Python Logic Flow Chart**

<br>

![Flow Chart displaying stages and logic of the program](docs/flow-charts/coffee-run-flow-chart-logic.png)

## **App Functionality and Features**

<br>

### **Main Menu**

<br>

![Main Menu](docs/features/coffee-run-main-menu.png)

When loading the app, users land on the main menu page so they can immediately access the service they need.  The large 'Coffee Run' title at the top was created using the Pyfiglet module and lets the user know that they have come to the right place to order coffee.

4 options are provided.  Number 1 allows the user to start the process of ordering their coffee.  I have given this option priority, as this is the main reason why most users will access the app.  Number 2 allows the user to access details of an order that has already been submitted.  Number 3 is an admin view designed for the owner of the coffee shop so they can access information about sales based on the data collected by the app.  Option 4 gives the user an opportunity to quit the app.  I have only made this option available at this level of the program, as this is where users return once an order has been submitted.

Users are prompted to enter a number between 1 and 4 which correspond with the menu options.  User input here must pass validation before progressing to the next step.  If a non valid number or any character is entered by the user, feedback is displayed to the user in the form of the following message:

![Main Menu Validation](docs/features/coffee-run-main-menu-validation.png)

### **Order Coffee**

<br>

When selecting option 1 in the main menu, the user will first be prompted to enter a name:

![User Enter Name](docs/features/coffee-run-enter-name.png)

To pass validation, the name entered must only contain letters.  The following feedback is displayed if this validation test is not passed:

![Name Input Validate Only Letters](docs/features/coffee-run-name-validation-letters.png)

The name provided by the user is limited to 10 characters.  If they input more than this, the following feedback is displayed and they are prompted to try again:

![Name Input Validate Length](docs/features/coffee-run-name-validation-length.png)

Once a valid name has been provided, the user is presented with a personalised message using the name they provided in the previous step.  The coffee types available to order and their prices are displayed in table format - created using the python module tabulate.  Users are encouraged to enter the coffee they want by entering the corresponding code from the table:

![Choose Coffee Type](docs/features/coffee-run-coffee-type.png)

If the code entered by the user does not pass validation, the following feedback is provided:

![Invalid Coffee Type Code](docs/features/coffee-run-validate-type.png)

Once a valid code has been entered for selection of coffee type, the user progresses to the next stage, where they can specify the milk they would prefer:

![Choose Milk Type](docs/features/coffee-run-milk-type.png)

Again, the code entered for milk choice must pass validation before the user can progress.  The following feedback is presented if an invalid code is entered:

![Invalid Milk Type Code](docs/features/coffee-run-validate-milk.png)

The next step in the ordering process is to specify the quantity required of the selected coffee:

![Select Quantity](docs/features/coffee-run-select-quantity.png)

If the user tries to enter a quantity using a non numeric value, they receive the following feedback:

![Quantity Invalid Non Numeric](docs/features/coffee-run-quantity-validate-non-numeric.png)

Users are only allowed to order a maximum of 5 drinks per order.  I mainly chose this number so I was still able to display the largest orders in the terminal display without scrolling.  In reality, this number could be made greater by the coffee shop owner.  If a user tries to order more than 5 drinks, the following feedback is displayed:

![Quanity Invalid Exceeds Item Limit](docs/features/coffee-run-quantity-validate-exceeds-item-total.png)

Once a valid quantity has been input, the user is presented with a summary of their current order in table format:

![Current Order Summary](docs/features/coffee-run-current-order-summary.png)

To view their next options, users are prompted to enter 'm'.  If an invalid character is entered, the following feedback is displayed:

![Return To Menu Code Invalid](docs/features/coffee-run-menu-return-code-invalid.png)

<br>

#### **Order Options**

<br>

The user is presented with 6 options of how they can proceed and are prompted to enter a code corresponding to an action in the table menu:

![Order Options](docs/features/coffee-run-order-options.png)

If the code input by the user does not pass validation, the following feedback is displayed:

![Order Options Code Invalid](docs/features/coffee-run-order-option-invalid.png)

#### **Option 1: Add an item to order**

<br>

If this is selected, the user will cycle back over the 'Order Coffee' steps outlined above.  In total they can enter 5 drinks to their order.  If at any time the quantity they select pushes total drinks over 5, they will be given feedback and prompted to enter a different quantity. If they are unable to add any more drinks to their order because they have reached the maximum of 5, the following will be displayed:

![Max Drinks Total Reached](docs/features/coffee-run-max-drinks-total-reached.png)

#### **Option 2: Remove an item from order**

<br>

If a user chooses to remove an item, they are presented with the following summary of their order and prompted to select the item they wish to remove:

![Remove Item Menu](docs/features/coffee-run-remove-item.png)

If the user inputs an invalid item code to remove, they will be presented with the following feedback:

![Remove Item Invalid Code](docs/features/coffee-run-remove-item-invalid-code.png)

If the user enters a valid code corresponding to an item in their order, this will be removed from the order and an updated order summary displayed along with a prompt to return to the Order Options menu by entering 'm':

![Removed Item Updated Summary](docs/features/coffee-run-remove-item-updated-summary.png)

If the user were to remove all items from the order, on removing the final item, they would be directed back to the Main Menu display.

#### **Option 3: Edit Quantities**

<br>

If the user chooses to edit the quantity of an item in the order, they are presented with the following summary of their order and prompted to select the item they would like to edit:

![Edit Quantities Select Item](docs/features/coffee-run-edit-quantities-select-item.png)

If an invalid item code is input by the user, the following feedback is displayed:

![Edit Quantities Invalid Code](docs/features/coffee-run-edit-quantities-invalid-code.png)

The user is then prompted to enter the quantity that they would like of the item they are editing:

![Edit Enter New Quantity](docs/features/coffee-run-edit-enter-new-quantity.png)

If the user attempts to enter an amended quantity that would take the drinks total of the order over 5, they are presented with the following feedback:

![Quanity Invalid Exceeds Item Limit](docs/features/coffee-run-quantity-validate-exceeds-item-total.png)

Once the user has edited the quantity of the item with a valid value, a summary of the order displaying the amended quantity and amended price is shown, along with a prompt to return to the Order Options menu by entering 'm':

![Edited Item Updated Summary](docs/features/coffee-run-edit-item-updated-summary.png)

#### **Option 4: View Current Order**

<br>

At any point during the order process, the user can choose to view their current order.  I originally had the current order displayed at all stages of the process, but I realised that this would not be possible if I wanted to work within the constraints of the deployed terminal display (24 rows in height) and not require the user to scroll.  Selecting option 4 provides a tabular view of the items currently in their order.  Entering 'm' takes the user back to the Order Options menu:

![View Current Order](docs/features/coffee-run-view-current-order.png)

#### **Option 5: Finalise Order**

<br>

Selecting option 5 takes the user to a page providing them with a personalised message to let them know that their order has been submitted. Key details of the order are also provided including their unique order reference number, the total amount due for the order on pickup, and the estimated pickup time:

![Finalised Order View](docs/features/coffee-run-finalise-order.png)

The user can then either choose to return to the main menu or view a summary of the items in their order.  The code entered by the user is validated here and an invalid entry will provide the following feedback:

![Finalised Order Next Step Invalid](docs/features/coffee-run-finalised-order-invalid-code.png)

Choosing option 1 will direct the user back to the main menu and choosing option 2 will display a summary of items in the submitted order, with an option to then return to the main menu:

![Finalised Order Summary](docs/features/coffee-run-finalised-order-summary.png)

### **View Existing Order**

<br>

Users of the app can view the details and status of an existing order if they have their order reference to hand.  Selecting option 2 on the main menu provides the user with the following prompt:

![Enter Existing Order Reference](docs/features/coffee-run-existing-order-enter-ref.png)

The order reference provided by the user, is checked against the list of order references stored in the "orders" sheet on the google sheets doc the_coffee_run.  If it cannot be matched, the following feedback is displayed:

![Invalid Order Reference](docs/features/cofee-run-invalid-order-ref.png)

If the order reference entered is found on the "orders" sheet, key information about the order is presented to the user:

![Existing Order Pending](docs/features/coffee-run-existing-order-pending.png)

When an existing order is called, the current time is checked against the estimated pickup time.  If current time is found to be greater than pickup time, the order will be shown as 'Ready':

![Existing Order Ready](docs/features/coffee-run-existing-order-ready.png)

### **Admin View**

<br>

This feature of the app is designed for use by the owners of the coffee shop.  As mentioned in the future implementations section, a username and password login stage would be created, so only those with admin credentials could access this option.  But for the purpose of this project, everyone can access to see this part of the app in action.

When selecting this option, the user is presented with some key stats that have been created through analysis of the sales data stored in the "sales" sheet in the google sheets doc. For the purpose of this project, I have chosen to collate the data from coffee sales over the past 10 days and display the total number of coffees sold in this time period, and also a breakdown of coffee types sold in tabular form.  I have also used this data to inform the business owner about which coffee type and milk choice was most popular over the 10 day period.  This is just an illustration of how this feature of the app could work. Moving forward, further functions could be written to manipulate and represent the data in a way that is most useful for the business owner and could help them make decisions about stock purchasing, staffing etc.

![Admin View](docs/features/coffee-run-admin-view.png)

### **Quit App**

<br>

Once the user has done everything they want to do, they can quit the app by selecting option 4, which displays the following message:

![Quit App](docs/features/coffee-run-quit-app.png)

<br>

## **Database**

Data is stored in a google sheets document and accessed by the app using the Google Drive and Google Sheets APIs.  The spreadsheet can be viewed [here](https://docs.google.com/spreadsheets/d/1xP6diVy29WpZ_O2dBV_bloRFv9dYs0kOkFteq5djAqs/edit?usp=sharing).  The spreadsheet consists of the following sheets:

### **Coffee**

<br>

This stores the coffee menu items and associated prices.  The Business owner could update pricing information on the sheet, and these updates would be mirrored on the app:

![Coffee Sheet](docs/features/google-sheets-coffee.png)


### **Milk**

<br>

This stores the milk menu options and associated prices:

![Milk Sheet](docs/features/google-sheets-milk.png)


### **Orders**

<br>

Once an order has been submitted on the app, it is appended as a row on the orders sheet.  It is this information that the coffee shop will use to put the order together:

![Orders Sheet](docs/features/google-sheets-orders.png)

### **Sales**

<br>

As an order is submitted, the elements of the order are broken down into sales data which is then appended as a row in the sales sheet:

![Sales Sheet](docs/features/google-sheets-sales.png)

<br>

## **Error Handling**

<br>

* As outlined in the [App Functionality and Features](#app-functionality-and-features) section, all user inputs are validated and any errors handled in a graceful manner so the user stays informed about the problem and feedback is offered to help the user correct their error.

* I am using an API to communicate with Google Sheets which stores data for the app.  It was therefore necessary to implement error handling for this aspect, so any API calls that fail to execute or return data are handled gracefully and users are notified in an obvious way.  To do this, I included a try/except block in the function access_google_sheet which is responsible for returning data from the worksheet:

```python
try:
    gs_data = SHEET.worksheet(sheet)
    return gs_data

except Exception as error:
    print(f"{colored(f'There was a problem gathering data.','red')}")
    print(f"\n{colored(f'Sorry, please try again later.', 'red')}\n")
    sys.exit()
```

To test whether this was working, I searched for each instance in the code where the access_google_sheet function is called and modified the call to an invalid sheet id.  Below is an example of some modified code where the 'sheet' argument passed to the function ia an invalid sheet name "order": 

```python
def get_orders():
    """
    Pulls data from "orders" sheet and returns the data without the headers
    as orders_list.
    """

    orders = access_google_sheet("order")
    data = orders.get_all_values()
    orders_list = data[1:]
    return orders_list
```

The resulting error message displayed to the user can be seen below:

![api-call-error-handling](docs/features/coffee-run-api-error-handling.png)

I also tested this error handling on the deployed app, by temporarily changing the sheet names in the Google Worksheet, to check that the error would be handled in the expected way.

<br>

## **Typography**

<br>

Consistent colour schemes have been used throughout the app, to provide an intuitive user experience and ensure that key information is highlighted.  Green text informs the user that an input value is required, red text flags user input errors and provides feedback to the user about how they can input a valid value.  Key information such as total price, order reference and pickup time are highlighted with the colour cyan and also made bold.

<br>

## **Imagery**

This project is deployed on Heroku and uses the Code Institute template to run the app in the mock terminal.  I made some amendments to the default html and css files to personalise the app and also help the user understand immediately the purpose of the site:  

![Deployed Site Landing Page](docs/colour-palette/coffee-run-deployed-site.png)

The following background image has been added to the css class 'body' in the layout.html file:

![Deployed Site Background Image](assets/images/coffee-art.webp)

I also centred the 'Run Program' button and changed the colour to fit better with the background image being used.  I uploaded the coffee art background image to the [coolors website](https://coolors.co/) and used the palette generator tool to create a complimentary palette.  I chose #C26F31 'Copper' as the colour for the button:

![Background Image Colour Palette](docs/colour-palette/coffee-run-colour-palette.png)

I also added the following favicon in the head element of the layout.html file, to establish branding for the site:

![Favicon Image](docs/features/plastic-takeaway-coffee-icon.jpg)

<br>

# **Technologies Used**

## **Languages Used**

<br>

Python was used to create this project.

<br>

## **Programs Used**

<br>

* Git -  Version control.
* [GitHub](https://github.com/) - All files for the website stored and saved in a repository.
* Gitpod - IDE used to write the code.
* [LucidChart](https://www.lucidchart.com/pages/) -For creating a flow diagram
* [Heroku](https://dashboard.heroku.com/apps) - For deployment of the project.
* [PEP8](https://pep8ci.herokuapp.com/) CI Python Linter
* [Black](https://www.freecodecamp.org/news/auto-format-your-python-code-with-black/) - Python Auto Formatter
* [TinyPNG](https://tinypng.com/) - For compression of image files to improve website performance.
* [Birme](https://www.birme.net/?target_width=425&target_height=450&auto_focal=false&image_format=jpeg&quality_jpeg=100&quality_webp=100) - For resizing and re-formatting images to make them suitable for use on the website.
* [Favicon.ico & App Icon Generator](https://www.favicon-generator.org/) - for creating the 16x16px ico favicon.
* [Techsini](https://techsini.com/multi-mockup/index.php) - For generating an image of the deployed app on devices 

<br>

## **Frameworks and Libraries used**

<br>

* [gspread](https://docs.gspread.org/en/latest/) - This is a Python API for Google Sheets and is used within the app to access and update data stored in various sheets across the master worksheet "the_coffee_run".

* [google.oauth2.service_account](https://google-auth.readthedocs.io/en/master/reference/google.oauth2.service_account.html) - From this module, the Credentials Class has been imported which then uses the creds.json file.

* [pandas](https://pandas.pydata.org/) - This is a python library that is used to analyse data. I imported the library so I could turn dictionaries into dataframes and then display the data stored in table format for the user.

* [os](https://docs.python.org/3/library/os.html) - This module provides a way of using operating system dependent functionality.  This was imported so I could use the clear terminal command when calling certain functions.  The purpose of this was to allow me to always keep the information displayed to the user within the boundaries of the terminal display, without the need to scroll.

* [sys](https://docs.python.org/3/library/sys.html) - This module was imported to use the exit command sys.exit() to terminate the app when calling the quit_app function.  I have also used this command when handling API errors.

* [tabulate](https://pypi.org/project/tabulate/) - This library provides the ability to 'pretty-print' tabular data in Python.  I imported the tabulate function from this library to display menus and summaries in table format, to ensure that users are presented with information in a clear, easy to understand way and therefore make navigation of the app intuitive.

* [datetime, timedelta & timezone imported from datetime module](https://docs.python.org/3/library/datetime.html) - These were used throughout the app to get current time and date.  It was necessary to use this functionality when calculating order prep time as information on recently placed orders was required.  It was also used to calculate the differences between current time and pickup time when establishing whether an order is ready to pickup.

* [pytz](https://pypi.org/project/pytz/) - This library was used for setting current time to the desired timezone.

* [colored & cprint imported from termcolor module](https://pypi.org/project/termcolor/) - This module was imported to change font colours in the terminal display, as a way of differentiating types of information for the user.

* [figlet imported from pyfiglet module](https://pypi.org/project/pyfiglet/0.7/) - I used this module to display 'Coffee Run' on the title page in a larger more interesting font.

* [OrderedDict imported from the collections module](https://docs.python.org/3/library/collections.html) - I imported the collections module to make use of ordered dictionaries, a dictionary subclass that remembers the order entries were added.

<br>

# **Deployment and Local Development**

<br>

## **Deployment to Heroku**

<br>

Before starting the deployment procedure, I created a list of requirements in gitpod, by entering the following command in the terminal:

```
pip3 freeze > requirements.txt
```

Heroku then uses this requirements.txt file to install the required dependencies.

The following steps were followed to deploy the app to Heroku:

1.  Create an account and login to [Heroku](https://id.heroku.com/login)
2.  In the Heroku dashboard, click the 'New' button at the top right of the screen and then select "Create new app".
3.  I selected the name 'the-coffee-run' ,set my region to Europe and clicked on the 'Create app' button.

![Heroku Acreate App](docs/deployment/heroku-create-app.png)

4.  Click on the settings tab and then click the 'Reveal Config Vars' button.

![Heroku Reveal Config Vars](docs/deployment/heroku-reveal-config-vars.png)

5.  In the field for Key, enter CREDS (All capital letters).

![Heroku Add Config Var](docs/deployment/heroku-add-config-var.png)

6.  From my Gitpod workspace, I went to my creds.json file which has been listed in the .gitignore file, copied the entire contents of this file and pasted it in the config var value field.  Then click 'Add'.
7.  Add another config var, this time with the Key set to PORT and the value 8000.
8.  From the 'Buildpacks' section click on the 'Add buildpack' button.

![Heroku Add Build Packs](docs/deployment/heroku-add-build-packs.png)

9.  Select Python, then click 'save changes' button.
10.  Next add the node.js buildpack and click the 'save changes' button again.  **It is important that the buildpacks are added in this order.  If they have been added in the wrong order, they can be clicked and dragged so Python comes first and node.js is below it.**

11.  Next select the 'Deploy' tab, select GitHub as the deployment method, and click the 'Connect to GitHub' button.
12.  Search for the GitHub repository name in the 'App Connected to GitHub' section and then click the 'connect' button'

![Heroku Deployment Tab](docs/deployment/heroku-deploy-tab.png)

13.  You can now choose to enable automatic deploys or deploy manually.  When the 'automatic deploys' button is clicked and enabled, Heroku will rebuild the app every time a new change is pushed to GitHub.  In the 'Manual deploy' section, the 'Deploy branch' button can be clicked to deploy manually.

![Heroku Deployment Methods](docs/deployment/heroku-deployment-method.png)

14.  I chose to deploy manually. Once the app is built, a link is provided to the [deployed app](https://the-coffee-run.herokuapp.com/).

![Heroku Successful Deployment](docs/deployment/heroku-successful-deployment.png)

<br>

## **Local Development**

<br>

### **How to fork:**

<br>

1. Log in (or sign up) to GitHub.
2. Find the required repository, in this case: rkillickdev/the-coffee-run
3. Click on the "fork" button at the top right of the page.

<br>

### **How to clone:**

<br>

1. Log in (or sign up) to GitHub.
2. Find the required repository, in this case: rkillickdev/the-coffee-run
3. Click on the green code button.  This will give you the choice of cloning the repository using HTTPS, an SSH key or GitHub CLI.  Make your selection and copy the provided URL link.
4. Open Terminal
5. Change the current working directory to the location where you want the cloned directory.
6. Type 'git clone' and then paste the URL you copied earlier.
7. Press enter.

<br>

# **Testing**

<br>

## **Automated Testing**

<br>

### **PEP8 Validation:**

<br>

I passed my run.py file through the [Code Institute Python Linter](https://pep8ci.herokuapp.com/) and no errors are found:

<br>

![CI Python Linter Validation](docs/validation/pep8/coffee-run-ci-python-linter-all-clear.png)

<br>

Towards the end of the project, I installed the tool [Black](https://www.freecodecamp.org/news/auto-format-your-python-code-with-black/) and ran this on my run.py file to make sure everything was formatted correctly and following best practices.

<br>

### **W3C Validator:**

<br>

I used the [W3C](https://validator.w3.org/) Markup Validation Service to validate the layout.html page as I made a few amendments to personalise the deployed app.  This passed with no errors or warnings:

![layout.html validation pass](docs/validation/html/coffee-run-layout-html-validation.png)

<br>

I used the [W3C jigsaw](https://jigsaw.w3.org/css-validator/) CSS Validation Service to validate the css included in the head of the layout.html file as I had made some additions to personalise the deployed app. It passed with no errors:

![layout.html css validation pass](docs/validation/css/coffee-run-layout-css-validation.png)

## **Manual Testing**

<br>

Please follow this link to the [TESTING.md file](https://github.com/rkillickdev/the-coffee-run/blob/main/TESTING.md), for documentation about the manual testing procedure I followed for this project.

<br>

## **Bugs**

<br>

### **Known Bugs:**

<br>

**1.**

I encountered a bug a couple of times while testing the deployed app, that I have not been able to reproduce consistently.  On quitting the app, a quantity input option was displayed:

![Quit App Known Bug](docs/bugs/quit-app-bug-displaying-input-option.png)

I have since added the sys.exit() command at the end of the quit_app function and I have not experienced the bug since doing this.

<br>

### **Solved Bugs:**

<br>

**1.**  Deleting Items Keys Not Updated:

This was a problem when deleting an item from the order. Once an item had been removed, the item numbers shown in the table displaying the order, did not match up to the position of the dictionary in the list.  Therefore if an item was originally number 3 in the list, even when number 2 was deleted, the 2nd item would still be displayed as number 3, and if the user input this number it would throw an error.  I eventually worked out that I could not modify the key in the existing dictionaries, therefore I created new ones and updated user_order.items in the update_order_dict function with the following code:

```python
   for k, item in zip(keys, user_order.items):
        dict_key = list(item.keys())
        value = dict_key[0]
        new_dict = {k: item[value]}
        updated_order_list.append(new_dict)

    user_order.items = updated_order_list
```

**2.**  Order Details Displaying Incorrectly in Spreadsheet:

![Order Details Bug](docs/bugs/order-detail-bug-wrong-quantities.png)

I had an issue where the quantity value displayed in the order details was incorrect.  I realised that it was actually using the value for unit_price which had been added to the item dictionary in the third position, but I had not subsequently updated the items_to_string function with the correct index. When I changed this to index 3 as seen below, the bug was solved:

```python
summary = f"{item[3]} X {item[0]} with {item[1]} milk"
```

**3.**  Quantity Error Handling:

During testing I realised that it was possible to enter the value zero as a quantity.  To fix this, I added the following line of code in the function validate_data:

```python
if user_input.isalpha() or int(user_input) < 1:
```

This means that user input will not be validated if they enter a character or a number that is less than 1.  Users are prevented from entering a quantity over 5 by the validate_drinks function.

**4.**  Main Menu Error Handling:

I noticed during testing that error handling for invalid codes in the main menu was not working as expected.  On investigation, I realised that the validate_function was attempting to compare integers against strings and throwing an error.  I solved this by converting the list of keys to validate against from a list of integers to a list of strings in the function input options:

```python
keys_as_strings = [str(x) for x in keys]
```

**5.**  Edit Quantities Exceeds Max drinks allowed:

I experienced a bug where if there was more than one item in the order and you tried to edit the quantity, it was possible to enter a number that would take the order drinks total over the maximum of 5 allowed.  I used the following code below to check whether user input + user_order.total_drinks exceeded the max allowed.  (Please note, when this snapshot was taken I was still allowing 10 drinks per order before eventually changing to 5 in the final version):

```python
elif step == "edit" and int(user_input) > 10 or int(user_input) + user_order.total_drinks > 10:
```

However, on further testing, I realised that the value for user_order.total_drinks was still taking into account the quantity for the item that the user was trying to edit.  As you can see in the image below, I should have been able to amend the flat white order from 8 to 3:

![Edit Quantities Bug](docs/bugs/edit-quantities-bug.png)

I therefore needed to set the quantity value to zero for the item being edited and then recalculate drinks total by calling get_drinks_total method on the user_order instance of Order.  When the updated quantity is entered by the user, the item being edited has a quantity value of zero rather than its existing quantity.  I achieved this by adding the following code in the input_options function:

```python
elif option == "edit":
item = user_order.items[index]
item[index + 1]['Quantity'] = 0
user_order.get_drinks_total()
updated_quantity = coffee_quantity("edit")
```

**6.**  Current Time 1 Hour behind London time:

As the coffee shop is based in London, I wanted to make sure that order times were based on the correct timezone.  To solve this, I imported the pytz module and passed in ‘Europe/London’ as an argument:

```python
now = datetime.now(pytz.timezone("Europe/London"))
```

**7.**  Duplicate Order Reference:

I realised during testing that if a user submitted an order and then returned to the main menu and created another order, on submitting this, the order reference was the same.  The solution to this was to update the attribute order_ref for the instance of Order (user_order) in the clear_order function.

![Duplicate Order Bug](docs/bugs/cofee-run-bug-duplicate-order-number%20.png)

**8.**  Order Summary Table Incorrect Column Order:

When printing the order summary to the terminal using tabulate, when only 1 item is present in the order, the price column displays before unit price therefore not adhering to the order they appear in the item dictionary (in the screenshot below I have printed the dictionary to the terminal to demonstrate this):

![Tabulate Column Order Incorrect](docs/bugs/view-order-columns-incorrect.png)

However, once a second item is added and the table is updated, the columns now appear in the correct order:

![Tabulate Column Order Correct](docs/bugs/view-order-columns-correct.png)

This bug was solved when I ended up renaming the columns.  For the 1st item, columns were being displayed in alphabetical order.  I actually wanted to label my columns differently and it happened that the new names fell in the correct alphabetical order, but a better solution should be investigated during future development.

**9.**  Pickup Status:

I noticed that if the order time was on one side of midnight and pickup time the other side, the order was  labelled as 'Ready'.  This is because current time is found to be greater than pickup time. I solved this by updating the variables present_datetime and pickup_datetime defined in the function view_completed.  I already had the following code in place to compare these two variables:

```python
if present_datetime < pickup_datetime:
                print(
                    f"Your coffee will be ready to pickup at"
                    f" {colored(order[7],'cyan',attrs=['bold'])}"
                    f" on {colored(order[8],'cyan',attrs=['bold'])}\n"
                )
```

But initially the variables present_datetime and pickup_datetime only stored the time.  When adding date, this functionality  began to work correctly.

In reality there would need to be time boundaries for when the app could be used or perhaps some code written to inform the user that if their order is placed after 6pm, pickup time is 7am the next day.  But for the purpose of this project, I wanted to make ordering available at any time of day so the full functionality of the app can be experienced without limitation.

**10.**  Prep Time Calculation 

During testing I realised that estimated prep time was not being calculated correctly, based on the number of recent orders.  I traced this to the get_recent function and realised when comparing the current and past, only time was being taken into account.  I therefore amended this function to also iterate over order date as shown in the code below:

```python
for order, date, time in zip(drinks, order_dates, order_times):
        max_time = timedelta(minutes=15)
        past_string = date + time
        past = datetime.strptime(past_string, "%d/%m/%Y%H:%M:%S")
        difference = current - past
```

Once fixed, you can see from the screen shot below that pickup times are now calculated correctly.  Order 191 is placed first with no other drinks placed in the past 15 minutes, so 5 drinks is estimated to take 10 minutes to prepare. Order 192 takes into account these other 5 drinks, adding 10 minutes of additional prep time so the total prep time for this 4 drink order is 18 minutes. Order 193 is for 1 drink but there are 9 other drinks placed in the past 15 minutes so prep time is calculated at 12 minutes.  And finally order 194 is only for 1 drink, but because there are 10 other drinks ordered in the past 15 minutes, an additional 15 minutes is added to the prep time which gives a total of 17 minutes.

![Pickup Time Bug Fix](docs/bugs/incorrect-prep-time-bug.png)

**10.**  Existing Order Error

When attempting to view older existing orders, the following error was thrown:

![Old Existing Orders Bug](docs/bugs/existing-order-pickup-time-missing-bug.png)

I realised that the data stored in the "orders" sheet did not have a pickup time value for orders 1 - 50, as this feature had not been implemented when these orders were input.

![Google Sheets pickup time missing](docs/bugs/google-sheets-missing-pickup-times-bug.png)

To fix this, I entered pickup time values for these first 50 orders on the "orders" sheet, and as you can see below, details are now displayed correctly if you attempt to view any of these past orders:

![Old Existing Orders Bug Fixed](docs/bugs/existing-orders-bug-fixed.png)

<br>

# **Credits**

## **Code Used and Referenced**

<br>

* Code for setting up the Google Sheets API so the app could add and manipulate data stored in the google sheets doc, was adapted from the Code Institute [Love Sandwiches](https://github.com/Code-Institute-Solutions/love-sandwiches-p5-sourcecode/tree/master) walk through project.

* Initial Inspiration when planning the project and coming up with an idea, came from the [American Pizza Project](https://github.com/useriasminna/american_pizza_order_system) which was provided as an example project by Code Institute.

* [Clearing the screen in the terminal](https://code-institute-room.slack.com/archives/C027C3S3TEU/p1634300241255100?thread_ts=1634300071.255000&cid=C027C3S3TEU)

* [Using Tabulate in Python](https://www.askpython.com/python-modules/tabulate-tables-in-python)

* [Getting values from dictionaries in Python](https://www.codingem.com/python-dict-get-method-vs-square-brackets/)

* [Adding two lists to a dictionary in Python](https://pythonhow.com/how/convert-two-lists-into-a-dictionary/#:~:text=You%20can%20use%20the%20zip,values%20into%20a%20single%20iterable.)

* [Accessing Dictionary Keys](https://www.learnbyexample.org/python-nested-dictionary/#:~:text='%3A%20''%7D%7D-,Access%20Nested%20Dictionary%20Items,key%20in%20multiple%20square%20brackets.&text=If%20you%20refer%20to%20a,What%20is%20this%3F&text=To%20avoid%20such%20exception%2C%20you,special%20dictionary%20get()%20method)

* [Iterating over multiple lists](https://learnpython.com/blog/loop-over-multiple-lists/#:~:text=Using%20the%20zip%20Function%20to,more%20lists%20side%20by%20side.)

* [Checking if a string only contains letters](https://careerkarma.com/blog/python-isalpha-isnumeric-isalnum/#:~:text=isalnum()%20is%20a%20built,method%20returns%20the%20value%20False%20.)

* [Breaking up long lines of code](https://www.pythonmorsels.com/breaking-long-lines-code-python/)

* [Changing font colour in the terminal](https://towardsdatascience.com/prettify-your-terminal-text-with-termcolor-and-pyfiglet-880de83fda6b)

* [Using sum and zip to get sales totals function](https://sparkbyexamples.com/python/python-add-two-lists/?expand_article=1)

* [Getting past 10 days dates](https://www.pythonprogramming.in/getting-the-date-of-7-days-ago-from-current-date-in-python.html)

* [Converting a list of integers into a list of strings](https://blog.finxter.com/how-to-convert-an-integer-list-to-a-string-list-in-python/)

* [Learning how to use Datetime](https://www.freecodecamp.org/news/how-to-get-the-current-time-in-python-with-datetime/#:~:text=To%20get%20the%20current%20time%20in%20particular%2C%20you%20can%20use,hours%2C%20minutes%2C%20and%20seconds.)

* [Reference list of pytz timezones](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568)

* [Inspiration from Code Institute Home Library Project, for html updates to enhance visual aspect of app](https://github.com/alexkisielewicz/home-library-app)

<br>

## **Media**

<br>

* [Royalty free image used for the coffee cup favicon](https://uxwing.com/)

<br>

## **Acknowledgements**

<br>

* To my family for supporting me through this journey!
* To my Code Institute Mentor Can Sucullu for his help, advice and feedback during our mentoring sessions.