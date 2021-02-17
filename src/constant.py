"""Constant variables."""

COLUMNS = [
    "customer_id",
    "customer_firstname",
    "customer_lastname",
    "customer_street_address",
    "customer_state",
    "customer_zip_code",
    "purchase_status",
    "product_id",
    "product_name",
    "purchase_amount",
    "date_time"
]

QUERY = open("query/query.sql").read()

DATABASE = "sampleSQLite.db"

TABLE_NAMES = ["customers", "products"]

UPLOAD_FOLDER = '/uploaded_files'

ALLOWED_EXTENSIONs = {'csv'}
