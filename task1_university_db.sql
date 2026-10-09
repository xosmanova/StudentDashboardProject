-- ============================================================================
-- Mini Project: Student Performance Dashboard
-- Task 1: SQL Server Database Creation & Stored Procedure
-- Database: UniversityDB
-- ============================================================================

-- 1. Create Database if it does not exist
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'UniversityDB')
BEGIN
    CREATE DATABASE UniversityDB;
    PRINT 'Database UniversityDB created successfully.';
END
ELSE
BEGIN
    PRINT 'Database UniversityDB already exists.';
END
GO

USE UniversityDB;
GO

-- 2. Create Students Table
IF OBJECT_ID(N'dbo.Students', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Students (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Name NVARCHAR(100) NOT NULL,
        Score FLOAT NOT NULL CHECK (Score >= 0 AND Score <= 100),
        CreatedAt DATETIME DEFAULT GETDATE()
    );
    PRINT 'Table Students created successfully.';
END
ELSE
BEGIN
    PRINT 'Table Students already exists.';
END
GO

-- 3. Insert Initial Sample Students if table is empty
IF NOT EXISTS (SELECT 1 FROM dbo.Students)
BEGIN
    INSERT INTO dbo.Students (Name, Score) VALUES
    (N'Ali', 85),
    (N'Leyla', 72),
    (N'Murad', 48),
    (N'Aysel', 91),
    (N'Kamran', 63);
    PRINT 'Sample student records inserted successfully.';
END
GO

-- 4. Create or Alter Stored Procedure: GetStudentResult
-- This stored procedure allows retrieving student results,
-- either all students or filtered by student name.
IF OBJECT_ID(N'dbo.GetStudentResult', N'P') IS NOT NULL
    DROP PROCEDURE dbo.GetStudentResult;
GO

CREATE PROCEDURE dbo.GetStudentResult
    @StudentName NVARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    IF @StudentName IS NULL OR LTRIM(RTRIM(@StudentName)) = ''
    BEGIN
        SELECT 
            Id,
            Name,
            Score,
            CreatedAt
        FROM dbo.Students
        ORDER BY Score DESC;
    END
    ELSE
    BEGIN
        SELECT 
            Id,
            Name,
            Score,
            CreatedAt
        FROM dbo.Students
        WHERE Name LIKE '%' + LTRIM(RTRIM(@StudentName)) + '%'
        ORDER BY Score DESC;
    END
END
GO

-- 5. Stored Procedure for Adding a Student (Clean Code / DB Layer Best Practice)
IF OBJECT_ID(N'dbo.AddStudent', N'P') IS NOT NULL
    DROP PROCEDURE dbo.AddStudent;
GO

CREATE PROCEDURE dbo.AddStudent
    @Name NVARCHAR(100),
    @Score FLOAT
AS
BEGIN
    SET NOCOUNT ON;

    IF @Name IS NULL OR LTRIM(RTRIM(@Name)) = ''
    BEGIN
        RAISERROR(N'Student name cannot be empty.', 16, 1);
        RETURN;
    END

    IF @Score < 0 OR @Score > 100
    BEGIN
        RAISERROR(N'Student score must be between 0 and 100.', 16, 1);
        RETURN;
    END

    INSERT INTO dbo.Students (Name, Score)
    VALUES (LTRIM(RTRIM(@Name)), @Score);

    SELECT SCOPE_IDENTITY() AS NewStudentId;
END
GO

PRINT 'Task 1 setup completed successfully!';
