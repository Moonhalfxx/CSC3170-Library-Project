# CUHK(SZ) Library Management System

## Overview
A Flask-based library management system supporting 2 roles (Librarians and Students) with 10+ core functions.

## Key Features
### Book Management
- Display tables for physical books, e-resources, users, and borrowing records
- Query/borrow/return/edit physical books
- Add new book entries

### User Management
- Query/edit user information
- User-friendly login/registration interface

### Analytics
- Statistics on borrowing frequency by:
  - Author
  - Title  
  - ISBN
- Tracking popular resources for inventory optimization

## System Requirements
### Student Access
- Search across:
  - Physical collections
  - Digital archives  
  - Online databases

### Librarian Privileges
- Manage book borrowing/returning
- Edit physical/digital resources:
  - Update information
  - Manage inventory
  - Add new resources
- View borrowing records and category statistics

### Interface Requirements
- Intuitive management dashboard
- User-friendly authentication pages

## Technical Credits
- CSS/HTML components adapted from:
  - [Bilibili: Dropdown Menu Tutorial](https://www.bilibili.com)
  - [Bilibili: Login Interface Tutorial](https://www.bilibili.com)  
- Located in:
  - `static/` (CSS files)
  - `templates/` (login/registration UI)

## Quick Start Guide
1. **Database Setup**  
   Pre-configured database included

2. **Launch Application**  
   Run `flaskProject` to start the system

3. **Authentication**  
   - Toggle between Login/Register using the sliding interface
   - Test accounts:
     - Librarian: `moon/123`
     - Student: `mimi111/111`

4. **Navigation**  
   - Hover over navigation bar to access different modules
   - Dropdown menus provide access to all functions

## System Screenshot
![image](https://github.com/user-attachments/assets/e7303ecf-aad2-49de-9ccd-03a4ce076673)
  
*Sliding authentication interface with login/register toggle*
