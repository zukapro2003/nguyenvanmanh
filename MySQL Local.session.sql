CREATE TABLE Diseases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    disease_name VARCHAR(100) NOT NULL
);

CREATE TABLE Departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);

CREATE TABLE Beds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status ENUM('available', 'occupied') NOT NULL,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES Departments(id)
);

CREATE TABLE Patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    disease_id INT,
    department_id INT,
    treatment_cost DECIMAL(10, 2),
    bed_id INT,
    admission_date DATE NOT NULL,
    discharge_date DATE,
    FOREIGN KEY (disease_id) REFERENCES Diseases(id),
    FOREIGN KEY (department_id) REFERENCES Departments(id),
    FOREIGN KEY (bed_id) REFERENCES Beds(id)
);

CREATE TABLE Treatment_Costs (
    disease_id INT,
    cost DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (disease_id) REFERENCES Diseases(id)
);