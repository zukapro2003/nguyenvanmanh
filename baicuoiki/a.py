import pandas as pd
import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Kết nối tới MySQL
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("Kết nối tới MySQL thành công")
    except Error as e:
        print(f"Lỗi '{e}' xảy ra")
    return connection

# Xóa dữ liệu cũ trong bảng
def delete_old_data(connection, table_name):
    cursor = connection.cursor()
    if table_name == 'benhnhan':
        sql = f"DELETE FROM {table_name}"
        cursor.execute(sql)
        connection.commit()
        print(f"Dữ liệu cũ đã được xóa trong bảng {table_name}")
    else:
        # Xóa dữ liệu trong bảng BenhNhan trước khi xóa Benh
        cursor.execute("DELETE FROM benhnhan")
        connection.commit()
        print("Dữ liệu cũ trong bảng BenhNhan đã được xóa")

        sql = f"DELETE FROM {table_name}"
        cursor.execute(sql)
        connection.commit()
        print(f"Dữ liệu cũ đã được xóa trong bảng {table_name}")

# Chèn dữ liệu vào bảng
def insert_data(connection, table_name, data):
    cursor = connection.cursor()
    for row in data.itertuples(index=False):
        placeholders = ', '.join(['%s'] * len(row))
        sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        cursor.execute(sql, row)
    connection.commit()
    print(f"Dữ liệu đã được chèn vào bảng {table_name}")

# Đọc dữ liệu từ file CSV và chèn vào bảng
def load_data_from_csv(connection):
    # Đọc dữ liệu từ file CSV
    benh_data = pd.read_csv('baicuoiki/benh.csv')
    khoa_data = pd.read_csv('baicuoiki/khoa.csv')
    benh_nhan_data = pd.read_csv('baicuoiki/benh_nhan.csv')

    # Xóa dữ liệu cũ và chèn dữ liệu mới vào từng bảng
    delete_old_data(connection, 'benh')
    insert_data(connection, 'benh', benh_data)

    delete_old_data(connection, 'khoa')
    insert_data(connection, 'khoa', khoa_data)

    delete_old_data(connection, 'benhnhan')
    insert_data(connection, 'benhnhan', benh_nhan_data)

#vẽ biểu đồ về tuổi 
def fetch_and_plot_age_distribution(connection):
    query = """
    SELECT 
        CASE 
            WHEN tuoi < 18 THEN '0-18'
            WHEN tuoi BETWEEN 18 AND 35 THEN '19-35'
            WHEN tuoi BETWEEN 36 AND 50 THEN '36-50'
            WHEN tuoi BETWEEN 51 AND 65 THEN '51-65'
            ELSE '65+' 
        END AS age_group,
        COUNT(*) AS patient_count
    FROM BenhNhan
    GROUP BY age_group;
    """

    # Truy xuất dữ liệu
    data = pd.read_sql(query, connection)

    # Vẽ biểu đồ cột
    plt.bar(data['age_group'], data['patient_count'], color='skyblue')
    plt.xlabel('Nhóm tuổi')
    plt.ylabel('Số lượng bệnh nhân')
    plt.title('Tỷ lệ bệnh nhân theo nhóm tuổi')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Truy xuất dữ liệu và vẽ biểu đồ về tỷ lệ bệnh nhân theo loại bệnh
def fetch_and_plot_disease_distribution(connection):
    query = """
    SELECT 
        b.ten_benh, 
        COUNT(bn.id) AS patient_count
    FROM Benh b
    LEFT JOIN benhnhan bn ON b.id = bn.id_benh
    GROUP BY b.ten_benh;
    """

    # Truy xuất dữ liệu
    data = pd.read_sql(query, connection)

    # Vẽ biểu đồ cột
    plt.figure(figsize=(10, 6))
    plt.bar(data['ten_benh'], data['patient_count'], color='lightcoral')
    plt.xlabel('Loại bệnh')
    plt.ylabel('Số lượng bệnh nhân')
    plt.title('Tỷ lệ bệnh nhân theo loại bệnh')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Truy xuất dữ liệu và vẽ biểu đồ đường về chi phí điều trị theo loại bệnh
def fetch_and_plot_treatment_cost_distribution(connection):
    query = """
    SELECT 
        b.ten_benh,
        AVG(b.chi_phi) AS average_cost
    FROM Benh b
    GROUP BY b.ten_benh
    ORDER BY average_cost;
    """

    # Truy xuất dữ liệu
    data = pd.read_sql(query, connection)

    # Vẽ biểu đồ đường
    plt.figure(figsize=(10, 6))
    plt.plot(data['ten_benh'], data['average_cost'], marker='o', color='blue')
    plt.xlabel('Loại bệnh')
    plt.ylabel('Chi phí điều trị trung bình')
    plt.title('Chi phí điều trị trung bình theo loại bệnh')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid()
    plt.show()

# Truy xuất dữ liệu và vẽ biểu đồ cột về thời gian sử dụng giường bệnh
def fetch_and_plot_bed_usage_time(connection):
    query = """
    SELECT 
        b.ten_benh, 
        AVG(bn.thoi_gian_kéo_dai) AS average_duration
    FROM benh bn
    JOIN Benh b ON bn.id = b.id
    GROUP BY b.ten_benh
    ORDER BY average_duration;
    """

    # Truy xuất dữ liệu
    data = pd.read_sql(query, connection)

    # Vẽ biểu đồ cột
    plt.figure(figsize=(10, 6))
    plt.bar(data['ten_benh'], data['average_duration'], color='lightgreen')
    plt.xlabel('Loại bệnh')
    plt.ylabel('Thời gian sử dụng giường bệnh (ngày)')
    plt.title('Thời gian sử dụng giường bệnh theo loại bệnh')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(axis='y')
    plt.show()

# Truy xuất dữ liệu và vẽ biểu đồ tròn về số lượng bệnh nhân theo từng khoa
def fetch_and_plot_patient_distribution_by_department(connection):
    query = """
    SELECT 
        k.ten_phong_ban, 
        COUNT(bn.id) AS patient_count
    FROM benhnhan bn
    JOIN khoa k ON bn.id_khoa = k.id
    GROUP BY k.ten_phong_ban;
    """

    # Truy xuất dữ liệu
    data = pd.read_sql(query, connection)

    # Vẽ biểu đồ tròn
    plt.figure(figsize=(8, 8))
    plt.pie(data['patient_count'], labels=data['ten_phong_ban'], autopct='%1.1f%%', startangle=140)
    plt.title('Tỷ lệ bệnh nhân theo từng khoa')
    plt.axis('equal')  # Đảm bảo biểu đồ là hình tròn
    plt.show()

if __name__ == "__main__":
    conn = create_connection("localhost",  "root", "Manh@18102003","quanlybenhnhan")
    if conn:
        load_data_from_csv(conn)
        fetch_and_plot_age_distribution(conn)
        fetch_and_plot_disease_distribution(conn)
        fetch_and_plot_treatment_cost_distribution(conn)
        fetch_and_plot_bed_usage_time(conn)
        fetch_and_plot_patient_distribution_by_department(conn)
        conn.close()