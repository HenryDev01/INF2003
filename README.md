## Objective
Our application is an e-commerce analytics platform that is targeted towards the Brazilian market based on the dataset used. It will help sellers and marketplace administrators to analyze sales trends and product performance using historical data.

## DATASET
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

## Functionalities and Implementation Plan

### Product and Consumer Analysis

- **Top-Selling Product Categories by Geography**  
  Analyze which product categories perform best in different regions.

- **Bestsellers by Quantity or Revenue**  
  Identify the most popular products based on sales volume and revenue.

- **Sales Trend Over Time**  
  Monitor performance trends using monthly, weekly, or daily breakdowns.

- **Demand Forecasting**  
  Predict future product demand using historical trends and time-series analysis.

---

### CRUD Operations

#### Create

- Customer and seller registration  
- Product listing creation  
- Order placement  
- Review and rating submission  

#### Read

- View data analytics and sales trends  
- Customer view of order details and product items  
- Customer order history access  
- Customer and public access to product reviews  

#### Update

- Order status updates (e.g., shipping, delivered)  
- Customer address updates  
- Product detail updates (e.g., name, price, stock)  

#### Delete

- Soft delete implementation for reversible actions  
- Order cancellation by customer  
- Product delisting by seller  
- Customer account deactivation  

---

# SETUP

1) For SQL, we use Maria DB for our application. To ensure that the application can run successfully, please also use Maria DB

2) Configure the database password in .env file to access YOUR Maria DB.

3) You will see SQL_PASSWORD=YOUR_PASSWORD , put your password after the equal sign

4) For NoSQL, please download the MongoDB compass and the Mongo Shell

5) By default, the port is 27017. However if your port is different for MongoDB, then please configure the in .env file under MONGO_PORT=YOUR_PORT
