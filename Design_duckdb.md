# DuckDB - Grouping Sets

## 1. Introduction
Use DuckDB in Python to read the data from Actual Sales data and compare them with the defined measures of Goals against them. Also, provide the rollup of data at various levels of dimensional elements.

## 2. Problem Statement

We have Sales data and Goals for the Business domains. We need to compare data from Sales tables and Goals tables side by side. While we display the Fact Sales records and Goals for the business domains, we should also aggregate (rollup) the data by every domain to give the top to bottom view of the business. 

There will be duplicates of records due to base data and aggregate data. We need to remove the duplicates from the resultset.

Example:

SUPPLIER $~~~~~$ BRAND $~~~~~$ FAMILY $~~~~~$ GROUPS $~~~~~$ CATEGORY $~~~~~$ SALES $~~~~~$ GROUP_GOALS $~~~~~~~~~$ CATEGORY_GOALS

$----~~~~----~~---~~~~~----~~~~----~~~-----~~~~-------~~~~-------$

NULL $~~~~~~~~~$ NULL $~~~~~~~~~$ NULL $~~~~~~~~~~~~$ NULL $~~~~~$ Smart Phone $~$ NULL $~~~~~$ NULL $~~~~~$ 1000

NULL $~~~~~~~~~$ NULL $~~~~~~~~~$ NULL $~~~~~~~~~~~~$ NULL $~~~~~$ Smart Phone $~$ 500 $~~~~~~~$ NULL $~~~~~$ 1000


Here, the data is duplicated at the Category level.

## 3. Requirements

Sales data comprises Dimensions of Suppliers, Brand, Family, Groups and Categories, and fact of Sales Amount.

The Dimesnsions Suppliers, Brand and Family are the hierarchies in the same order of sequence.

The measure Goals are defined at Supplier, Supplier-Brand, Supplier-Brand-Family hierarchy levels.

Also, the measure Goals Groups and Categories are defined independently at the entire dataset level.

We need to produce the Sales output at lowest hierarchy levels, alongside goals shown for Groups and Categories. In addition to that, we need to rollup the summary by every level.

Remove the duplicate data arising due to leaf records and summary records.

We give users the ability to filter the values of entries from the resultant dataset.

## 4. Solution Approach

In Order to combine the Sales Data with Goals Data, we use Pivot concept of augmenting metrics and measures. Using UNION clause of SQL construct for Leaf nodes' Sales data and separate query for each Goals data.

Ex:

SELECT SUPPLIER, BRAND, FAMILY, GROUPS, CATEGORY, SALES, NULL SUPP_GOALS, NULL GROUP_GOALS FROM SALES

UNION

SELECT SUPPLIER, NULL, NULL, NULL, NULL, NULL SALES, SUPP_GOALS, NULL GROUP_GOALS FROM SUPPLIER

UNION

SELECT NULL, NULL, NULL, GROUPS, NULL CATEGORY, NULL, NULL, GROUP_GOALS FROM GROUP_GOALS

We are using DuckDB's in-memory database option to create the query and produce the resultset.

We use DuckDB's built-in functionality GROUPING SET to produce the automatic rollup of measures and metrics data at the specified levels. Here we will use the GROUPING SET at (SUPPLIER, BRAND, FAMILY, GROUPS, CATEGORY) and every other levels in the data.

To remove the duplicate arising due to aggregate functions, we use Binary ENUM (0, 1) values for Sales node queries and Goals queries respectively. This ENUM field is used as numeric value to get Mininum of the grouping set.

Finally, this minimum of ENUM value is equated to zero to remove the duplicated records as the minimum aggregate function eleminates other records with value 1.

## 5. Design

We will be using Python, DuckDB, Loguru and Jinja templates in this platform. The base sales data is at Supplier, Brand, Family, Group and Category level.

The first query selects all attributes from the base sales data, and with an static enum value of 0. 

This query is union-ed with the goals data at all levels. The static enum for these additional queries are maintained as 1. The respective missing dimensions and metrics are made as NULL values in these queries.

SELECT 0 leaf_level, supplier, ...., group, category, sales, null <each goal> FROM SALES
union
SELECT 1, supplier, ...., null group, null category, null sales, supplier_goal FROM SUPPLIER_GOALS

UNION

SELECT 1, supplier, brand, ..., null group, null category, null sales, null supplier_goal, brand_goal FROM BRAND_GOALS

...

UNION

SELECT 1, null supplier, null brand, ...., group, null category, null sales, group_goals FROM GROUP_GOALS

UNION

SELECT 1, null supplier, null brand, ...., null group, category, null sales, category_goals FROM CATEGORY_GOALS

Then, a new query with GROUPING SETS caluse in the GROUP BY is applied at the below levels:

-  Supplier, Brand, Family
-  Supplier, Brand
-  Supplier
-  Group
-  Category

While all the metrics are aplied with SUM aggregate function, the ENUM value is applied with MIN aggregate function. This min aggregate function later is used to remove the duplicates in the final output. 

All these queries are made in the main python pgoram with two arguments, one for the filter column name and the other for the value for the filter column.

These filter conditions will be applied to the final query with the WHERE condition.

The filer condition is applied with Jinja2 Templating library.

The python program is tested using pytest library.

Test program files have the file name starting with test_ and the functions within the file starting with "test_".

We also parameterize the input arguments and expected results to the test function.

pytest command takes all the test_ files and executes actual function in the main python program.

Logging is done using loguru.logger method to capture information at key places.

## 6. Assumptions
The functioni in the main python file accepts two parameters, one for filter column and the other for filter value. We can enhance these parameters that can be applied to the function.

## 7. Conclusion
The queries use GROUPING SETS for rollup functionality. We can customize the GROUPING SETS according to the requirement.

The report combines data present at different levels (hierarchies and across hierarchies).

