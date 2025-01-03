from duckdb_connection import duckdb_connect
from loguru import logger
from jinja2 import Environment, FileSystemLoader

dkdb_conn = duckdb_connect()

logger.info("Initializing Jinja Environment")
jinja_env = Environment (loader=FileSystemLoader('templates'))
template1 = jinja_env.get_template('duckdb_query_temp.jinja')

def grouping_sets_using_duckdb(filter_column: str = '1', filter_value: str = '1'):

    list1 = [x for x in range (2, 10, 2)]
    logger.info (list1)

    logger.info ("Creating the Sales Table in Duckdb")
    cr_sales_tab = """create or replace table sales (supplier varchar, brand varchar, 
            family varchar, groups varchar,
            category varchar, sales numeric(10,2))"""

    dkdb_conn.sql (cr_sales_tab)
    dkdb_conn.sql ("""insert into sales values 
            ('Abc', 'Apple', 'Touch', '5G', 'Smart Phone', 100), 
            ('Abc', 'Asus', 'Touch', '4G', 'Smart Phone', 150), 
            ('Xyz', 'Samsung', 'Flip', '5G', 'Tablet', 200), 
            ('Xyz', 'Redmi', 'Touch', '4G', 'Smart Phone', 250)""")

    logger.info (dkdb_conn.sql ("select * from sales").show())
    
    cr_table_supplier = """create or replace table supplier (supplier varchar, supplier_goals numeric (10,2))"""
    dkdb_conn.sql (cr_table_supplier)
    insert_into_supplier = """insert into supplier values ('Abc', 44444), ('Xyz', 55555)"""
    dkdb_conn.sql (insert_into_supplier)
    
    logger.info (dkdb_conn.sql ("select * from supplier").show())
    
    cr_table_brand = """create or replace table brand (supplier varchar, brand varchar, brand_goals numeric (10,2))"""
    dkdb_conn.sql (cr_table_brand)
    insert_into_brand = """insert into brand values ('Abc', 'Apple', 77777), ('Xyz', 'Samsung', 55111),
            ('Abc', 'Asus', 22999), ('Xyz', 'Redmi', 11999)"""
    dkdb_conn.sql (insert_into_brand)
    logger.info (dkdb_conn.sql ("select * from brand").show())
    
    cr_table_family = """create or replace table family (supplier varchar, brand varchar, family varchar, family_goals numeric (10,2))"""
    dkdb_conn.sql (cr_table_family)
    insert_into_family = """insert into family values ('Abc', 'Apple', 'Touch', 66666), ('Xyz', 'Samsung', 'Flip', 33333), \
            ('Abc', 'Asus', 'Touch', 22222), ('Xyz', 'Redmi', 'Touch', 11111)"""
    dkdb_conn.sql (insert_into_family)
    logger.info (dkdb_conn.sql ("select * from family").show())
    
    cr_table_groups = """create or replace table groups (groups varchar, group_goals numeric (10,2))"""
    dkdb_conn.sql (cr_table_groups)
    insert_into_groups = """insert into groups values ('4G', 44444), ('5G', 88888)"""
    dkdb_conn.sql (insert_into_groups)
    logger.info (dkdb_conn.sql ("select * from groups").show())
    
    cr_table_category = """create or replace table category (category varchar, cat_goals numeric (10,2))"""
    dkdb_conn.sql (cr_table_category)
    insert_into_category = """insert into category values ('Smart Phone', 99999), ('Tablet', 33777)"""
    dkdb_conn.sql (insert_into_category)
    logger.info (dkdb_conn.sql ("select * from category").show())
    
    cr_table_union = """create or replace table union1 as
            select 0::boolean as union_query_num, supplier, brand, family, groups, category, sales, null supplier_goals,
            null brand_goals, null family_goals, null group_goals, null cat_goals from sales
            union
            select 1, supplier, NULL brand, NULL as family, NULL as groups, NULL as category, NULL as sales, supplier_goals,
            NULL as brand_goals, NULL family_goals, null group_goals, null cat_goals from supplier
            union
            select 1, supplier, brand, NULL as family, NULL as groups, NULL as category, NULL as sales, NULL as supplier_goals,
            brand_goals, NULL family_goals, null group_goals, null cat_goals from brand
            union
            select 1, supplier, brand, family, NULL as groups, NULL as category, NULL as sales, null as supplier_goals,
            NULL as brand_goals, family_goals, null group_goals, null cat_goals from family
            union
            select 1, null as supplier, null as brand, null as family, groups, NULL as category, NULL as sales,
            null as supplier_goals, NULL as brand_goals, null as family_goals, group_goals, null cat_goals from groups
            union
            select 1, null as supplier, null as brand, null as family, NULL as groups, category, NULL as sales,
            null as supplier_goals, NULL as brand_goals, null as family_goals, null as group_goals, cat_goals from category"""
    dkdb_conn.sql (cr_table_union)
    dkdb_conn.sql ("select * from union1").show()
    
    group_by_query = """create or replace table group_query as with group_query as
            (select supplier, brand, family, groups, category, min(union_query_num) leaf_level,
            sum(sales) sales, sum (supplier_goals) supplier_goals, sum (brand_goals) brand_goals,
            sum (family_goals) family_goals, sum (group_goals) group_goals, sum (cat_goals) cat_goals,
            grouping_id (supplier, brand, family, groups, category) level1
            from union1
            group by grouping sets ((supplier, brand, family, groups, category), (supplier, brand, family),
            (supplier, brand), supplier, groups, category, ()))
            select supplier, brand, family, groups, category, sales, supplier_goals, brand_goals, family_goals,
            group_goals, cat_goals, level1
            from group_query where leaf_level = 0
            order by ifnull(supplier, '0000'), ifnull (brand, '0000'), ifnull (family, '0000'),
            ifnull (groups, '0000'), ifnull (category, '0000')"""
    dkdb_conn.sql (group_by_query)
    dkdb_conn.sql ("select * from group_query").show()
    sql_text = """select * from group_query """
    
    logger.info ("Calling jinja render function ")
    output = template1.render(sql_text = sql_text, filter_by_column = filter_column, filter_value = filter_value)
    logger.info(output)
    dkdb_conn.sql(output).show()
    
    return 0


